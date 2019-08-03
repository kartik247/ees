from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Institute, Departments, Departmentfloormap
from .serializers import InstituteSerializer, DepartmentSerializer


@csrf_exempt
def institute_list(request):
    """
    List all institutes, or create a new institute.
    """
    if request.method == 'GET':
        institute = Institute.objects.all()
        return JsonResponse({}, safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            #print(data['departments'])
            institute_name = data.get('instituteName')
            institute_id = Institute.objects.create(name=institute_name)
            #print('institute_id', institute_id.pkid)

            for eachdep in data['departments']:
                departmentName = eachdep.get('departmentName')
                dep_id = Departments.objects.create(name=departmentName, institute_id=institute_id)
                for eachfloor in eachdep['floorDetails']:
                    floorNumber = eachfloor.get('floorNumber')
                    numberOfUsers = eachfloor.get('numberOfUsers')
                    dfm = Departmentfloormap(department_id=dep_id, floor_number=floorNumber, num_of_users=numberOfUsers)
                    dfm.save()
            responseMsg = {"message": "Your institute ID is " + str(institute_id.pkid) + ". Please call the below URL to generate configurations for your institute",
                       "url": "http://<IPaddress>:<Port>/api/v1/generateConfig/" + str(institute_id.pkid) + "/"}
            return JsonResponse(responseMsg, safe=False, status=201)
        except:
            return JsonResponse({"ERROR: incorrect data provided"}, safe=False, status=400)


@csrf_exempt
def institute_detail(request, pkid):
    """
    Retrieve config or delete an institute.
    """
    try:
        institute = Institute.objects.get(pkid=pkid)
    except Institute.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = InstituteSerializer(institute)
        response = serializer.data
        #response.update({"ab":"cdef"})

        ### Core Switch Config ###


        department = Departments.objects.filter(institute_id=institute)
        print(department)
        for eachdep in department:
            departmentName = eachdep.name
            floor_details = Departmentfloormap.objects.filter(department_id=eachdep)
            for eachfloor in floor_details:
                floor_number = eachfloor.floor_number
                num_of_users = eachfloor.num_of_users

            #dep_serializer = DepartmentSerializer(eachdep)
            #print(dep_serializer)
        return JsonResponse(response)
        #return Departments.objects.filter(institute_id=institute)

    elif request.method == 'DELETE':
        institute.delete()
        return HttpResponse(status=204)

