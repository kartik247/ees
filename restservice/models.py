from django.db import models

# Create your models here.


class Institute(models.Model):
    pkid = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)

    def __int__(self):
        return self.pkid

    @property
    def institute_id(self):
        return self.pkid


class Departments(models.Model):
    pkid = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    institute_id = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institute_department')

    def __int__(self):
        return self.pkid

    @property
    def department_id(self):
        return self.pkid


class Departmentfloormap(models.Model):
    pkid = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='department_floor')
    floor_number = models.IntegerField()
    num_of_users = models.IntegerField()

    def __int__(self):
        return self.pkid

