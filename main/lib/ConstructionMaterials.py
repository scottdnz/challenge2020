import csv
import os.path

from django.conf import settings

class ConstructionMaterials:
	
	def __init__(self):
		pass

	def get_demo_cm(self):
		# SQL query would be:
		# "SELECT cm.*,
		# ct.Name as ct_Name
		# FROM napier_checklists.construction_materials cm
		# inner join napier_checklists.construction_types ct on cm.Type = ct.ID 
		# and ct.Deleted = 'n'
		# where cm.Deleted = 'n'";

		demo_file = os.path.join(settings.STATICFILES_DIRS[0], 
			'data', 
			'napier_construction_materials_example.csv');

		with open(demo_file, newline='') as csv_file:
		    data = list(csv.DictReader(csv_file))

		rows_by_type = {}
		for row in data:
			cm_type = row["ct_Name"]
			if cm_type not in rows_by_type:
				rows_by_type[cm_type] = []
			rows_by_type[cm_type].append(row)

		return rows_by_type

		