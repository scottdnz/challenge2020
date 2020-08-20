import csv
from MySQLdb import _mysql

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def add_app_details(db, results):
	for job in results:
		jid = int(job.get("ID"))

		db.query("""SELECT * FROM jobs_app WHERE JID = '%d' AND Active='y' AND Deleted='n'""" % jid)
		r=db.store_result()
		a = r.fetch_row(maxrows=1, how=1)
		for row in a:
			app_type = row.get("ApplicationType").decode("utf-8")
			classified_use = int(row.get("ClassifiedUse"))
			building_use = int(row.get("BuildingUse"))
			if (app_type == '2'):
				job['app_type_bc'] = 1.0
			else:
				job['app_type_bc'] = 0.0

			value = row.get("EstimatedValue")
			area = row.get("NewArea")
			life = row.get("IntendedLife")
			if value == b'':
				value = 0
			if area == b'':
				area = 0
			if life == b'':
				life = 0

			job['estimated_value'] = safe_cast(value, float, 0.0) / 1000000.0
			job['new_area'] = safe_cast(area, float, 0.0) / 1000.0
			job['life'] = safe_cast(life, float, 0.0) / 50.0

			for i in range(0, 14):
				if (classified_use == i):
					job['classified_use_'+str(i)] = 1.0
				else:
					job['classified_use_'+str(i)] = 0.0

			for i in range(0, 22):
				if (building_use == i):
					job['building_use_'+str(i)] = 1.0
				else:
					job['building_use_'+str(i)] = 0.0


def add_cm_details(db, results):
	for job in results:
		jid = int(job.get("ID"))

		materials = {}
		db.query("""SELECT * FROM construction_materials""")
		r=db.store_result()
		a = r.fetch_row(maxrows=0, how=1)
		for row in a:
			materials[int(row.get("ID"))] = row.get("Name").decode("utf-8")

		db.query("""SELECT * FROM jobs_app_cm WHERE JID = '%d' AND Active='y'""" % jid)
		r=db.store_result()
		a = r.fetch_row(maxrows=1, how=1)
		for row in a:
			selections = row.get("Selections").decode("utf-8").split("|")
			selections = [int(i) for i in selections if i] 
			for m in materials:
				if m in selections:
					job[materials[m]] = 1.0
				else:
					job[materials[m]] = 0.0


def add_vetting_results(db, results, qcode):
	qcodes = [
		#'0402249f-3830-11e6-8be5-000c292dee42'
		qcode
	]
	qcode_data = {}

	for q in qcodes:
		db.query("""SELECT * FROM questions WHERE QCode = '%s' AND Deleted =  'n'""" % q)
		r=db.store_result()
		a = r.fetch_row(maxrows=0, how=1)
		group_qids = []
		title = ''
		for row in a:
			group_qids.append(int(row.get("ID")));
			title = row.get("Title").decode("utf-8")

		qcode_data[q] = {"title": title, "qids": group_qids}

	print(qcode_data)


	for job in results:
		jid = int(job.get("ID"))
		for q in qcode_data:
			qid_parts = map(str, qcode_data[q]['qids'])
			qid_str = ",".join(qid_parts)
		

			db.query("""SELECT * FROM jobs_data WHERE JID = '%d' AND Active='y' AND QID IN (%s)""" % (jid, qid_str))
			r=db.store_result()
			a = r.fetch_row(maxrows=0, how=1)
			for row in a:
				qid = row.get("QID")
				ans = row.get("Choice")
				key = 'question_'+q
				if (ans == b'Y'):
					job[key+'_pass'] = 1.0
					job[key+'_fail'] = 0.0
					job[key+'_na'] = 0.0
				elif (ans == b'N/A'):
					job[key+'_pass'] = 0.0
					job[key+'_fail'] = 0.0
					job[key+'_na'] = 1.0
				else:
					job[key+'_pass'] = 0.0
					job[key+'_fail'] = 1.0
					job[key+'_na'] = 0.0

def extract_from_db(dbs, qcode):
	results = []

	for db_name in dbs:
		print("reading "+db_name)
		db=_mysql.connect(host="localhost",user="alpha",
						passwd="1q2w3e4r5t",db=db_name)
		

		db.query("""SELECT * FROM jobs WHERE ID > 100000 AND Deleted='n'""")
		r=db.store_result()
		a = r.fetch_row(maxrows=0, how=1)
		for row in a:
			jid = row.get("ID").decode("utf-8")
			results.append({"DB": db_name, "ID": jid})

		add_app_details(db, results)
		add_cm_details(db, results)
		add_vetting_results(db, results, qcode)

	# filter results with missing data
	results = [i for i in results if ('question_'+qcode+'_pass' in i and 'Concrete' in i)]

	keys = results[0].keys()
	with open('all_results.csv', 'w', newline='')  as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(results)


def main():
	extract_from_db(['napier_checklists', 'pncc_checklists', 'sdc_checklists'], '0ecb7114-1144-11e4-9030-000c29d69785')


if __name__ == "__main__":
	main()
