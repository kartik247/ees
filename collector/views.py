from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.


def display(request):
    return render(request, "departments.html", {})


def departments(request):
    return render(request, "departments.html", {})


def buildings(request):
    return render(request, "buildings.html", {})


@csrf_exempt
def savebuildingdata(request):
    bgljson = request.POST.get('bgljson')
    print(bgljson)
    data = {}
    return HttpResponse(json.dumps(data), content_type="application/json")
