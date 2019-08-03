from .models import Institute, Departments, Departmentfloormap
from rest_framework import serializers


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ['pkid', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['pkid', 'name', 'institute_id']

