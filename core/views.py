from django.shortcuts import render, redirect
from core.models import *
from users.models import *
from django.conf import settings 
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .forms import *
import os
from django.contrib import messages
from .recognizer import Recognizer
from datetime import date
from .filters import AttendenceFilter
Machine_ROOT = os.path.join(settings.BASE_DIR, 'machine')

def welcome(request):
    return render(request, 'core/welcome.html')

def login_form(request):
    userName = request.POST.get("username")
    userPassword = request.POST.get("password")
    
    if request.POST.get('radAdmin') == '1':
        user = authenticate(username=userName, password=userPassword)
        if user is not None:
            login(request,user)
            return render(request,"core/index.html")
    elif request.POST.get('radTech') == '0':
        getTeacher =  Teacher_Reg.objects.filter(teacher_email=userName)
        if getTeacher.exists():
            getTeacher =  Teacher_Reg.objects.get(teacher_email=userName)
            if getTeacher is not None:
                if getTeacher.teacher_email == userName and getTeacher.teacher_password == userPassword:
                    return render(request,'core/teacher_panel.html')
        else:
            messages.error(request, "Please Provide Email For Teacher...!")
            return render(request,'core/login_form.html')
    return render(request,'core/login_form.html')

def index(request):
    return render(request, 'core/index.html')


from io import BytesIO
from PIL import Image
import re
import base64

def student(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        program = request.POST.get('program')
        semester = request.POST.get('semester')
        image_data = request.POST.get('image_data')
        if User.objects.filter(username=student_id).exists():
            return render(request,'core/student.html',{'useriderror': 'This User id already exists'})

        image_width = 200
        image_height = 300
        image_data = re.sub("^data:image/png;base64,", "", image_data)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        img = Image.open(image_data)
        img = img.convert('RGB')
        globvar = get_random_string(9)

        user = User.objects.create(
            username = student_id,
            first_name = fname,
            password = make_password("School123")
        )
        student = StudentModel(
            user = user,
            department = department,
            program = program,
            profile_picture = f'/images/Student_Images/{department}/{semester}/{program}/{user.username}.jpg',
            semester = semester
        )
        student.save()
        try:
            os.makedirs(settings.MEDIA_ROOT+f"\\images\\Student_Images\\{department}\\{semester}\\{program}")
            img.save(settings.MEDIA_ROOT+f'\\images\\Student_Images\\{department}\\{semester}\\{program}\\{user.username}.jpg')
        except FileExistsError:
            pass
        img.save(settings.MEDIA_ROOT+f'\\images\\Student_Images\\{department}\\{semester}\\{program}\\{user.username}.jpg')
        return redirect('index')

    return render(request,'core/student.html')


def updateStudentDetails(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        department = request.POST.get('department')
        program = request.POST.get('program')
        semester = request.POST.get('semester')

        if not fname == user.first_name:
            user.first_name = fname
            user.save()

        if 'image_data' in request.POST:

            image_data = request.POST.get('image_data')
            if image_data:
                image_width = 200
                image_height = 300
                image_data = re.sub("^data:image/png;base64,", "", image_data)
                image_data = base64.b64decode(image_data)
                image_data = BytesIO(image_data)
                img = Image.open(image_data)
                img = img.convert('RGB')
                globvar = get_random_string(9)
                try:
                    os.makedirs(settings.MEDIA_ROOT+f"\\images\\Student_Images\\{department}\\{semester}\\{program}")
                except FileExistsError:
                    pass
                img.save(settings.MEDIA_ROOT+f'\\images\\Student_Images\\{department}\\{semester}\\{program}\\{user.username}.jpg')
                
                StudentModel.objects.filter(user=user).update(
                    department = department,
                    program = program,
                    profile_picture = f'/images/Student_Images/{department}/{semester}/{program}/{user.username}.jpg',
                    semester = semester
                )
        else:
            StudentModel.objects.filter(user=user).update(
                department = department,
                program = program,
                semester = semester
            )
        return render(request, 'core/index.html')
        
    context ={
        
        'user': user
    }
    return render(request,'core/update_record.html',context)

def updateStudentDetailsfromteacher(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        department = request.POST.get('department')
        program = request.POST.get('program')
        semester = request.POST.get('semester')

        if not fname == user.first_name:
            user.first_name = fname
            user.save()

        if 'image_data' in request.POST:

            image_data = request.POST.get('image_data')
            if image_data:
                image_width = 200
                image_height = 300
                image_data = re.sub("^data:image/png;base64,", "", image_data)
                image_data = base64.b64decode(image_data)
                image_data = BytesIO(image_data)
                img = Image.open(image_data)
                img = img.convert('RGB')
                globvar = get_random_string(9)
                try:
                    os.makedirs(settings.MEDIA_ROOT+f"\\images\\Student_Images\\{department}\\{semester}\\{program}")
                except FileExistsError:
                    pass
                img.save(settings.MEDIA_ROOT+f'\\images\\Student_Images\\{department}\\{semester}\\{program}\\{user.username}.jpg')
                
                StudentModel.objects.filter(user=user).update(
                    department = department,
                    program = program,
                    profile_picture = f'/images/Student_Images/{department}/{semester}/{program}/{user.username}.jpg',
                    semester = semester
                )
        else:
            StudentModel.objects.filter(user=user).update(
                department = department,
                program = program,
                semester = semester
            )
        return redirect('teacher_panel')
        
    context ={
        
        'user': user
    }
    return render(request,'core/teacher_update_record.html',context)

def update_record(request):

    return render(request,'core/update_record.html')



def mark_attendance(request):
    return render(request,'core/mark_attendance.html')
def search_record(request):
    students = StudentModel.objects.all()
    if request.method == 'POST':
        if 'department' in request.POST:
            students = StudentModel.objects.filter(department=request.POST['department'])
        elif 'program' in request.POST:
            students = StudentModel.objects.filter(program=request.POST['program'])
        elif 'semester' in request.POST:
            students = StudentModel.objects.filter(semester=request.POST['semester'])
        elif 'search' in request.POST:
            students = StudentModel.objects.filter(user__first_name__istartswith=request.POST['search'])
    context = {
        'students' : students
    }
    return render(request,'core/search_record.html', context)


import cv2
from django.http import StreamingHttpResponse


from imutils.video import VideoStream
import imutils
import urllib.request
import numpy as np


from django.shortcuts import  get_object_or_404
def changeadminpassword(request):
    print('yessssssssssss')
    context = {}
    print(request.user.username)
    obj = get_object_or_404(User, username=request.user.username)

    form = updatePasswordForm(request.POST or None, instance=obj)
    context['form'] = form
    context['users'] = obj.username
    context['name'] = str(obj.first_name)
    if form.is_valid():
        obj= form.save()
        context['passwordchanged']= True
    return render(request,'core/adminchangepassword.html',context)



def teacher(request):
    techName = request.POST.get('teacher_name')
    techEmail = request.POST.get('teacher_email')
    techPass = request.POST.get('teacher_password')
    if request.POST.get('teacher_name') and request.POST.get('teacher_email') and request.POST.get('teacher_password') is not None:
        teachers = Teacher_Reg(teacher_name = techName, teacher_email = techEmail, teacher_password = techPass)
        teachers.save()
    return render(request,'core/teacher.html')

def teacher_update(request):
    
    return render(request, 'core/teacher_update.index')

def teacher_panel(request):
    return render(request,'core/teacher_panel.html')

def teacher_update_record(request):
    return render(request, 'core/teacher_update_record')
def teacher_search_record(request):
    students = StudentModel.objects.all()
    if request.method == 'POST':
        if 'department' in request.POST:
            students = StudentModel.objects.filter(department=request.POST['department'])
        elif 'program' in request.POST:
            students = StudentModel.objects.filter(program=request.POST['program'])
        elif 'semester' in request.POST:
            students = StudentModel.objects.filter(semester=request.POST['semester'])
        elif 'search' in request.POST:
            students = StudentModel.objects.filter(user__first_name__istartswith=request.POST['search'])
    context = {
        'students' : students
    }
    return render(request, 'core/teacher_search_record.html', context)



from core import faceRecognition as fr







def take_attendance(request):
           

    if request.method == 'POST':
        details = {
            'department':request.POST['department'],
            'semester': request.POST['semester'],
            'program':request.POST['program'],
            'period':request.POST['period'],
            # 'faculty':request.user.faculty
            }
        if Attendence.objects.filter(date = str(date.today()),department = details['department'], semester = details['semester'], program = details['program'],period = details['period']).count() != 0 :
            messages.error(request, "Attendence already recorded.")
            return redirect('teacher_panel')
        else:
            students = StudentModel.objects.filter(department = details['department'], semester = details['semester'], program = details['program'])
            names = Recognizer(details)

            for student in students:
                
                if str(student.user.username) in names:
                    attendence = Attendence(
                        Faculty_Name = 'faculty', 
                        Student_ID = str(student.user.username), 
                        period = details['period'], 
                        department = details['department'], 
                        semester = details['semester'], 
                        program = details['program'],
                        status = 'Present'
                    )
                    attendence.save()
                else:
                    attendence = Attendence(
                        Faculty_Name = 'faculty', 
                        Student_ID = str(student.user.username), 
                        period = details['period'],
                        department = details['department'], 
                        semester = details['semester'], 
                        program = details['program']
                    )
                    attendence.save()
            attendences = Attendence.objects.filter(date = str(date.today()),department = details['department'], semester = details['semester'], program = details['program'],period = details['period'])
            context = {"attendences":attendences, "ta":True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'core/attendence.html', context)        
    context = {}
    return render(request,'core/take_attendance.html')


def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter':myFilter, 'attendences': attendences, 'ta':False}
    return render(request, 'core/attendence.html', context)


def teacher_faqs(request):
    return render(request, 'core/teacher_faqs.html')

def admin_faqs(request):
    return render(request, 'core/admin_faqs.html')

def search_attendance(request):
    return render(request, 'core/search_attendance.html')