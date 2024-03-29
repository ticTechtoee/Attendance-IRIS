from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from core.models import ApplicationName,ApplicationType,Department, Semester, Program
from django.contrib.auth.decorators import user_passes_test, login_required

import os
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError

AppUser = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# @user_passes_test(is_admin, login_url="AccountApp:custom_login")

def RegisterPersonView(request):
    current_user = request.user
    get_user = request.user
    try:
        set_logo = ApplicationName.objects.latest('id')
    except ApplicationName.DoesNotExist:
        set_logo = None

    get_dept_name = Department.objects.all()
    get_student_program = Program.objects.all()
    get_student_semester = Semester.objects.all()

    try:
        get_application_type = ApplicationType.objects.get()
    except ApplicationType.DoesNotExist:
        get_application_type = None

    error_messages = []

    if request.method == 'POST':
        u_id = request.POST.get('Unique_ID')
        user_name = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        deptt = request.POST.get('department')
        user_role = request.POST.get('role')

        try:
            # Ensure passwords match
            if password != confirm_password:
                error_messages.append('Passwords do not match')
                raise ValidationError('Passwords do not match')  # Raise an exception to stop further execution

            # Validate the password
            validate_password(password)

            # Validate the email format
            validate_email(email)

            # Hash the password
            hashed_password = make_password(password)

            # Get the department
            get_deptt = Department.objects.get(id=deptt)

            if get_application_type.type_app == "OTHER":
                user = AppUser(custom_unique_id=u_id, username=user_name, first_name=first_name, last_name=last_name,
                            email=email, department=get_deptt, password=hashed_password)
            elif get_application_type.type_app == "EDU":
                program_id = request.POST.get('program')
                program_instance = Program.objects.get(id=program_id)
                semester_id = request.POST.get('semester')
                semester_instance = Semester.objects.get(id=semester_id)
                user = AppUser(custom_unique_id=u_id, username=user_name, first_name=first_name, last_name=last_name,
                            email=email, department=get_deptt, password=hashed_password,
                            program=program_instance, semester=semester_instance)

            if user_role == 'teacher':
                user.is_teacher = True
            elif user_role == 'superuser':
                user.is_superuser = True

            user.save()

            if user:
                folder_name = f"{u_id}_{first_name}_{last_name}"
                media_folder_path = os.path.join("media/dataset/", folder_name)

                if not os.path.exists(media_folder_path):
                    os.makedirs(media_folder_path)

            return redirect('core:ViewCaptureImage')

        except ValidationError as e:
            error_messages.extend(e.messages)
        except IntegrityError:
            error_messages.append('User with this email already exists')

    if current_user.is_superuser:
        user_role = "superuser"
    elif current_user.is_teacher:
        user_role = "teacher"
    else:
        user_role = None

    context = {'dept_names': get_dept_name, 'app_type': get_application_type,
               'Student_Program': get_student_program, 'Student_Semester': get_student_semester,
               'user_role': user_role, 'error_messages': error_messages, 'user_info': get_user, 'Set_Logo': set_logo}

    return render(request, "core/student.html", context)



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Manually authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the authenticated user
            login(request, user)

            # Set user role in the session for access in the template
            request.session['user_role'] = 'superuser' if user.is_superuser else ('teacher' if user.is_teacher else 'student')

            if user.is_superuser or user.is_teacher:
                return redirect('core:index')
            else:
                return redirect('core:ViewDetectPerson')
        else:
            # Handle authentication failure, e.g., show an error message
            return render(request, 'AccountApp/login_form.html', {'error_message': 'Invalid credentials'})

    return render(request, 'AccountApp/login_form.html', {'user_role': request.session.get('user_role', 'student')})


def logoutView(request):
    logout(request)
    return redirect('AccountApp:custom_login')