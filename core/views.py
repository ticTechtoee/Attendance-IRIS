import face_recognition
import os
import base64
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ApplicationName,ApplicationType,Department
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

from AccountApp.models import AppUser, Attendance
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pickle

def is_admin(user):
    return user.is_authenticated and user.is_superuser



def SetProjectNameView(request):
    set_name =  ApplicationName.objects.latest('id')
    context = {'Name_of_Project': set_name}
    return render(request, 'core/welcome.html', context)

@login_required(login_url="AccountApp:custom_login")
def IndexPageView(request):
    set_logo = ApplicationName.objects.latest('id')
    context = {'Set_Logo': set_logo}
    return render(request, 'core/index.html', context)

@user_passes_test(is_admin, login_url="AccountApp:custom_login")
def RegisterPersonView(request):
    get_dept_name = Department.objects.all()
    try:
        # Assuming there's only one record in the ApplicationType model
        get_application_type = ApplicationType.objects.get()
    except ApplicationType.DoesNotExist:
        # Handle the case where no record is found
        get_application_type = None

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
            return render(request, "core/student.html", {'dept_names': get_dept_name, 'app_type': get_application_type, 'error_message': 'Passwords do not match'})

        # Hash the password
        hashed_password = make_password(password)

        # Get the department
        get_deptt = Department.objects.get(id=deptt)

        # Create the user
        user = AppUser(custom_unique_id=u_id, username=user_name, first_name=first_name, last_name=last_name,
                       email=email, department=get_deptt, password=hashed_password)
        user.save()

        if user:
            # Create a folder in the media directory using the unique ID, first name, and last name
            folder_name = f"{u_id}_{first_name}_{last_name}"
            media_folder_path = os.path.join("media/dataset/", folder_name)

            # Check if the folder already exists, and create it if not
            if not os.path.exists(media_folder_path):
                os.makedirs(media_folder_path)

        return redirect('core:ViewCaptureImage')

    context = {'dept_names': get_dept_name, 'app_type': get_application_type}
    return render(request, "core/student.html", context)


def add_padding(data):
    # Ensure that the Base64 data has proper padding
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return data

@csrf_exempt
@user_passes_test(is_admin, login_url="AccountApp:custom_login")
def capture_image(request):
    if request.method == 'POST' and 'image_data' in request.POST:
        get_id = request.POST.get('user_id')
        try:
            # Retrieve the AppUser based on the custom unique ID
            user_data = AppUser.objects.get(custom_unique_id=get_id)
            

            # Get the media root from Django settings
            media_root = settings.MEDIA_ROOT
        
            # Generate a timestamp for the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            folder_name = f"{get_id}_{user_data.first_name}_{user_data.last_name}"
            
            # Create the folder path using the custom unique ID and names
            folder_path = os.path.join(media_root + "/dataset", folder_name)

            # Create the file name with the timestamp
            file_name = f"{user_data.first_name}_{user_data.last_name}_{timestamp}.png"
                       
            try:
                # Check if the folder already exists, and create it if not
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"Folder '{folder_name}' created successfully at '{folder_path}'.")
                else:
                    print(f"Folder '{folder_name}' already exists at '{folder_path}'.")
            except Exception as e:
                print(f"Error creating folder: {e}")
            
            # Process the captured image data
            image_data = request.POST['image_data'].split(',')[1]
            image_content = ContentFile(base64.b64decode(image_data), name=file_name)        
            
            # Create the full image path
            image_path = os.path.join(folder_path, file_name)

            # Save the image file to the specified path
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as img_file:
                img_file.write(image_content.read())

            # Update the image path in the AppUser model
            #user_data.image_path = image_path
            user_data.save()

            return JsonResponse({'message': 'Image captured and saved successfully!'})
        
        except AppUser.DoesNotExist:
            # Handle the case where the user with the given custom unique ID does not exist
            return JsonResponse({'error': 'User not found'}, status=404)
    
    else:
        get_data = AppUser.objects.filter(is_superuser=False)
        context = {'user_data': get_data}
        return render(request, 'core/capture_image.html', context)

def train_system(dataset_path):
    known_face_encodings = []
    known_face_names = []

    for person_folder in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_folder)
        if os.path.isdir(person_path):

            folder_parts = person_folder.split('_')
            if len(folder_parts) == 3:
                person_id, first_name, last_name = folder_parts[0], folder_parts[1], folder_parts[2]
                
                person_name = f"{first_name} {last_name}"

            for image_file in os.listdir(person_path):
                image_path = os.path.join(person_path, image_file)
                print(person_path)
                print("")
                print(image_file)

                # Load the image
                image = face_recognition.load_image_file(image_path)

                # Get the face encoding
                face_encoding = face_recognition.face_encodings(image)
                
                if len(face_encoding) > 0:
                    # Store the face encoding and the corresponding person's name
                    known_face_encodings.append(face_encoding[0])
                    known_face_names.append({'id': person_id, 'name': person_name})

    trained_data_folder_name = "trained_data"
    dat_file_folder = os.path.join(settings.BASE_DIR, trained_data_folder_name)

    if not os.path.exists(dat_file_folder):
        os.makedirs(dat_file_folder)

    print(dat_file_folder)
    # Save the trained data
    with open(os.path.join(dat_file_folder, 'trained_data.dat'), 'wb') as file:
        data = {'encodings': known_face_encodings, 'names': known_face_names}
        pickle.dump(data, file)

@user_passes_test(is_admin, login_url="AccountApp:custom_login")
def TrainOnDataView(request):
    context = {}
    if request.method == 'POST':
        datasetfolder_name = "dataset"
        dataset_path = os.path.join(settings.MEDIA_ROOT, datasetfolder_name)
        train_system(dataset_path)
        context = {'Message':'Training completed on the active Dataset'}
        return render(request, 'core/train_data.html', context)
    return render(request, 'core/train_data.html', context)
   

@csrf_exempt
@login_required(login_url="AccountApp:custom_login")
def DetectPersonView(request):
    if request.method == 'POST' and 'image_data' in request.POST:
            try:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                
                capture_image_folder = "detect_image"
                image_recognize_path = os.path.join(settings.BASE_DIR, capture_image_folder)
                if not os.path.exists(image_recognize_path):
                    os.makedirs(image_recognize_path)
                
                # Create the file name with the timestamp
                file_name = f"_{timestamp}.png"

                # Process the captured image data
                image_data = request.POST['image_data'].split(',')[1]
                image_content = ContentFile(base64.b64decode(image_data), name=file_name)        
                
                # Create the full image path
                image_path = os.path.join(image_recognize_path, file_name)

                # Save the image file to the specified path
                print(image_path)
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_content.read())

                print("Recognizing")

                recognize_faces(image_path)

                # Delete Image after recognition
                os.remove(image_path)
            
            except Exception as e:
                print(e)
            
    context = {}
    return render(request, 'core/detect_person.html', context)

def recognize_faces(image_path):
    get_trained_data_file = os.path.join(settings.BASE_DIR,"trained_data")
    complete_path = os.path.join(get_trained_data_file,"trained_data.dat")
    print(complete_path)

    # Load the trained data
    with open(complete_path, 'rb') as file:
        data = pickle.load(file)
        known_face_encodings = data['encodings']
        known_face_names = data['names']

    # Load the image
    unknown_image = face_recognition.load_image_file(image_path)

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        person_info = {'id': "Unknown", 'name': "Unknown"}

        if True in matches:
            first_match_index = matches.index(True)
            person_info = known_face_names[first_match_index]

        person_id = person_info['id']
        person_name = person_info['name']

        print(f"Person ID: {person_id}, Person Name: {person_name}, Location: {top},{right},{bottom},{left}")
        Mark_Attendance(person_id)
        
def Mark_Attendance(unique_ID):
    # Retrieve the user
    user = AppUser.objects.get(custom_unique_id=unique_ID)

    # Get the current date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Create or update the attendance record
    attendance, created = Attendance.objects.get_or_create(user=user, date=current_date, time=current_time)
    attendance.is_present = True
    attendance.save()

    return HttpResponse("Attendance Marked")

@login_required(login_url="AccountApp:custom_login")
def AttendenceSearchView(request):
    get_deptt_name = Department.objects.all()
    users_in_department = None  # Initialize the variable

    if request.method == 'POST':
        select_deptt_name = request.POST.get('search_field')
        get_deptt_object = Department.objects.get(id=select_deptt_name)
        users_in_department = AppUser.objects.filter(department=get_deptt_object)
    
    context = {'Department_Names': get_deptt_name, 'Users_Info': users_in_department}
    return render(request, 'core/attendence_search.html', context)

@login_required(login_url="AccountApp:custom_login")
def AttendenceRecordView(request, pk):
    get_user = get_object_or_404(AppUser, custom_unique_id=pk)
    get_attendance_record = Attendance.objects.filter(user=get_user)

    # Check if export button is clicked
    if 'export' in request.GET:
        # Create a workbook and add a worksheet
        wb = Workbook()
        ws = wb.active

        # Define header row
        header = ['Unique ID', 'User Name', 'Date', 'Time', 'Present']
        for col_num, header_text in enumerate(header, 1):
            col_letter = get_column_letter(col_num)
            ws[f'{col_letter}1'] = header_text
            ws[f'{col_letter}1'].font = Font(bold=True)

        # Populate data rows
        for row_num, attendance in enumerate(get_attendance_record, 2):
            ws.cell(row=row_num, column=1, value=get_user.custom_unique_id)
            ws.cell(row=row_num, column=2, value=get_user.username)
            ws.cell(row=row_num, column=3, value=attendance.date)
            ws.cell(row=row_num, column=4, value=attendance.time)
            ws.cell(row=row_num, column=5, value=attendance.is_present)

        # Create a response object with the appropriate headers
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={get_user.custom_unique_id}_attendance_record.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response

    context = {'Attendance_Record': get_attendance_record, 'User': get_user}
    return render(request, 'core/person_record.html', context)