import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from main.lib.TestNumPy import TestNumPy
from main.lib.TestPandas import TestPandas


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


def silly_test(request):
	# Select query
	with connection.cursor() as cursor:
		cursor.execute("SELECT id, name, phone from user")
		# row = cursor.fetchone()
		rows = dictfetchall(cursor)

	testNumPy = TestNumPy()
	numPyresult = []

	numPyresult.append("Result for max in array is: " + testNumPy.try_silly())

	testPandas = TestPandas()
	pandasResults = TestPandas.test_silly() 

	# return JsonResponse({'rows': rows})
	return render(request, 'silly_test.html', 
		{ "users": rows,
			"numpy_data": numPyresult,
			"pandas_data": pandasResults
		}
	)


@csrf_exempt
def silly_receive_json(request):
    # try:
	data = json.loads(request.body)

	# Do a bulk insert into DB - works!
	with connection.cursor() as cursor:
		insertSql = "insert into user (name, phone) values "
		params = []
		placeholders = []

		for user in data["users"]:
			params.extend([user["name"], user["phone"]])
			placeholders.append("(%s, %s)")

		insertSql += ", ".join(placeholders)
		cursor.execute(insertSql, params)


	return HttpResponse("OK")