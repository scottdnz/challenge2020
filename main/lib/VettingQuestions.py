import csv
import os.path

from django.conf import settings

class VettingQuestions:
	
	def __init__(self):
		pass


	def get_demo_vetq(self, job_id):
		# sql query would be:
		# "select napier_checklists.jobs.VettingId,
		# 	q.ID as qID, q.QCode, q.Question,
		# 	pc.ID      as pcID,
		# 	cl.Public  as clPublic,
		# 	cl.Private as clPrivate,
		# 	cl.ID as criteriaLId,
		# 	jobs.Id as jobsID
		# 	from napier_checklists.jobs
		# 	inner join jobs_buildings jb on jb.JID = jobs.ID and jb.Active = 'y' AND jb.Deleted = 'n'
		# 	inner join checklists on checklists.ID = jb.BuildingType and checklists.Complexity like 'C%'
		# 	inner join public_criteria pc on pc.ID = jobs.VettingID
		# 	inner join criteria_links cl on cl.Public = pc.ID
		# 	inner join questions q on q.ID = cl.Private
		# 	-- where 
		# 	-- jobs.ID = 182462
		# 	limit 200;"

		demo_file = os.path.join(settings.STATICFILES_DIRS[0], 
			'data', 
			'napier_vet_questions_example.csv');

		with open(demo_file, newline='') as csv_file:
		    data = list(csv.DictReader(csv_file))

		rows_by_job = {}

		if job_id:
			for row in data:
				jid = row["jobsID"]
				if job_id == jid:
					if jid not in rows_by_job:
						rows_by_job[jid] = []
					# ugly hack
					if (row["Question"].find("/img") != -1):
						row["Question"] = row["Question"].replace("/img", "/static/img")

					rows_by_job[jid].append(row)
		else:
			for row in data:
				jid = row["jobsID"]
				if jid not in rows_by_job:
					rows_by_job[jid] = []
				rows_by_job[jid].append(row)

		return rows_by_job
		