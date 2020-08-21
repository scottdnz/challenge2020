import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# from main.lib.TestNumPy import TestNumPy
# from main.lib.TestPandas import TestPandas
from main.lib.ConstructionMaterials import ConstructionMaterials
from main.lib.VettingQuestions import VettingQuestions


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

# Create your views here.

def index(request):
    # return HttpResponse("Hello, world. You're at the main index.")
    return render(request, 'index.html')


def vetting_hard_coded_example(request):
	return render(request, 'hardcoded_example.html')


def vetting_example(request):
	return render(request, 'vetting_example1.html', 
		{'job_id': request.GET.get('jid', None)}
	)


def get_construction_materials(request):
	cm = ConstructionMaterials()
	rows = cm.get_demo_cm()
	return JsonResponse({'construction_materials': rows})


def get_vetting_questions(request):
	job_id = request.GET.get('jid', None)

	vet_q = VettingQuestions()
	rows = vet_q.get_demo_vetq(job_id)
	return JsonResponse({'vetting_questions': rows}, safe=False)


@csrf_exempt
def handle_construction_material_inputs(request):
	ids = request.POST.get('cm_ids[]', None)

	cm_ids = []

	if ids is not None and len(ids) > 0:
		for id in ids:
			cm_ids.append(id)

	# Get predicted question IDs here
	qids = [53199, 53201];

	return JsonResponse({"question_ids": qids})


def train_results1(request):
	return render(request, 'train_results1.html')



# def silly_test(request):
# 	# Select query
# 	with connection.cursor() as cursor:
# 		cursor.execute("SELECT id, name, phone from user")
# 		# row = cursor.fetchone()
# 		rows = dictfetchall(cursor)

# 	testNumPy = TestNumPy()
# 	numPyresult = []

# 	numPyresult.append("Result for max in array is: " + testNumPy.try_silly())

# 	testPandas = TestPandas()
# 	pandasResults = TestPandas.test_silly() 

# 	# return JsonResponse({'rows': rows})
# 	return render(request, 'silly_test.html', 
# 		{ "users": rows,
# 			"numpy_data": numPyresult,
# 			"pandas_data": pandasResults
# 		}
# 	)


# @csrf_exempt
# def silly_receive_json(request):
#     # try:
# 	data = json.loads(request.body)

# 	# Do a bulk insert into DB - works!
# 	with connection.cursor() as cursor:
# 		insertSql = "insert into user (name, phone) values "
# 		params = []
# 		placeholders = []

# 		for user in data["users"]:
# 			params.extend([user["name"], user["phone"]])
# 			placeholders.append("(%s, %s)")

# 		insertSql += ", ".join(placeholders)
# 		cursor.execute(insertSql, params)


# 	return HttpResponse("OK")