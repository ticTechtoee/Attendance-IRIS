from django.db import models
from django.forms import CharField
# from django.contrib.auth.models import User
# Create your models here.
from users.models import *

class Teacher_Reg(models.Model):
    teacher_name=models.CharField(max_length=50)
    teacher_email=models.EmailField(max_length=30)
    teacher_password=models.CharField(max_length=30)

    class Meta:
        db_table="teacher_reg"

def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.registration_id
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch,instance.year,instance.section,filename)

    
class StudentModel(models.Model):
    user = models.OneToOneField(
        User, related_name='student', on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=50)
    program =  models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="admissionDocuments/")
    semester = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user) + str(self.user.username)


class Attendence(models.Model):
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    department = models.CharField(max_length=200, null = True)
    semester = models.CharField(max_length=200, null = True)
    program = models.CharField(max_length=200, null = True)
    period = models.CharField(max_length=200, null = True)
    status = models.CharField(max_length=200, null = True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date)+ "_" + str(self.period))