from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from core.models import ApplicationName,ApplicationType,Department
from django.contrib.auth.decorators import user_passes_test, login_required
import os

AppUser = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_superuser

# @user_passes_test(is_admin, login_url="AccountApp:custom_login")
def RegisterPersonView(request):
    get_dept_name = Department.objects.all()
    try:
        # Assuming there's only one record in the ApplicationType model
        get_application_type = ApplicationType.objects.get()
    except ApplicationType.DoesNotExist:
        # Handle the case where no record is found
        get_application_type = None

    # Retrieve the role of the logged-in user from the session
    user_role = request.session.get('user_role', 'student')

    if request.method == 'POST':
        u_id = request.POST.get('Unique_ID')
        user_name = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        deptt = request.POST.get('department')

        # Ensure passwords match
        if password != confirm_password:
            # Handle the case where passwords do not match
            return render(request, "core/student.html", {'dept_names': get_dept_name, 'app_type': get_application_type, 'user_role': user_role, 'error_message': 'Passwords do not match'})

        # Hash the password
        hashed_password = make_password(password)

        # Get the department
        get_deptt = Department.objects.get(id=deptt)

        # Create the user with the appropriate role
        user = AppUser(custom_unique_id=u_id, username=user_name, first_name=first_name, last_name=last_name,
                       email=email, department=get_deptt, password=hashed_password)

        if user_role == 'teacher':
            user.is_teacher = True
        elif user_role == 'superuser':
            user.is_superuser = True

        user.save()

        if user:
            # Create a folder in the media directory using the unique ID, first name, and last name
            folder_name = f"{u_id}_{first_name}_{last_name}"
            media_folder_path = os.path.join("media/dataset/", folder_name)

            # Check if the folder already exists, and create it if not
            if not os.path.exists(media_folder_path):
                os.makedirs(media_folder_path)

        return redirect('core:ViewCaptureImage')

    context = {'dept_names': get_dept_name, 'app_type': get_application_type, 'user_role': user_role}
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

            if user.is_superuser:
                return redirect('core:ViewIndexAdmin')
            else:
                return redirect('core:ViewDetectPerson')
        else:
            # Handle authentication failure, e.g., show an error message
            return render(request, 'AccountApp/login_form.html', {'error_message': 'Invalid credentials'})

    return render(request, 'AccountApp/login_form.html', {'user_role': request.session.get('user_role', 'student')})


def logoutView(request):
    logout(request)
    return redirect('core:Home')