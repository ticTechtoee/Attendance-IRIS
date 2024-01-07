import base64
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ApplicationName,ApplicationType
import os
from .models import Department
from AccountApp.models import AppUser
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import face_recognition
import pickle

def SetProjectNameView(request):
    set_name =  ApplicationName.objects.latest('id')
    context = {'Name_of_Project': set_name}
    return render(request, 'core/welcome.html', context)


def IndexPageView(request):
    set_logo = ApplicationName.objects.latest('id')
    print("Logo URL:", set_logo.logo_of_project.url)
    context = {'Set_Logo': set_logo}
    return render(request, 'core/index.html', context)

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
        deptt = request.POST.get('department')
        
        get_deptt = Department.objects.get(id = deptt)

        AppUser(custom_unique_id=u_id, username=user_name, first_name = first_name, last_name = last_name, email= email, department=get_deptt).save()

        if AppUser.save:
            # Create a folder in the media directory using the unique ID, first name, and last name
            folder_name = f"{u_id}_{first_name}_{last_name}"
            media_folder_path = os.path.join("media/dataset/", folder_name)

            # Check if the folder already exists, and create it if not
            if not os.path.exists(media_folder_path):
                os.makedirs(media_folder_path)
        return redirect('core:ViewCaptureImage')
    
    context = {'dept_names':get_dept_name, 'app_type':get_application_type}
    return render(request, "core/student.html", context)



def add_padding(data):
    # Ensure that the Base64 data has proper padding
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return data

@csrf_exempt
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
            user_data.image_path = image_path
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
    known_persons_data = []  # List to store data for each person

    for person_folder in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_folder)
        if os.path.isdir(person_path):
            # Extracting ID, first name, and last name from folder name
            folder_parts = person_folder.split('_')
            if len(folder_parts) == 3:
                person_id, first_name, last_name = folder_parts
                person_name = f"{first_name} {last_name}"
                print(f"Person ID: {person_id}, Name: {person_name}")
            else:
                print(f"Skipping folder {person_folder} due to incorrect naming format.")
                continue

            # Dictionary to store data for the current person
            person_data = {'id': person_id, 'name': person_name, 'encodings': []}

            for image_file in os.listdir(person_path):
                image_path = os.path.join(person_path, image_file)

                # Load the image
                image = face_recognition.load_image_file(image_path)

                # Get the face encoding
                face_encoding = face_recognition.face_encodings(image)

                if len(face_encoding) > 0:
                    # Store the face encoding
                    person_data['encodings'].append(face_encoding[0])

            # Append the person's data to the list
            known_persons_data.append(person_data)

    trained_data_folder_name = "trained_data"
    dat_file_folder = os.path.join(settings.BASE_DIR, trained_data_folder_name)

    if not os.path.exists(dat_file_folder):
        os.makedirs(dat_file_folder)

    # Save the trained data
    with open(os.path.join(dat_file_folder, 'trained_data.dat'), 'wb') as file:
        pickle.dump(known_persons_data, file)

def TrainOnDataView(request):
    context = {}
    if request.method == 'POST':
        datasetfolder_name = "dataset"
        dataset_path = os.path.join(settings.MEDIA_ROOT, datasetfolder_name)
        train_system(dataset_path)
        context = {'Message':'Training completed on the active Dataset'}
        return render(request, 'core/train_data.html', context)
    return render(request, 'core/train_data.html', context)
   

def recognize_faces(image_path):
    # Load the trained data
    get_trained_data_path = os.path.join(settings.BASE_DIR, "trained_data")
    print(get_trained_data_path)
    with open(get_trained_data_path + '\\trained_data.dat', 'rb') as file:
        data = pickle.load(file)
        known_persons_data = data  # Assume 'known_data' contains a list of dictionaries

    # Load the image
    unknown_image = face_recognition.load_image_file(image_path)

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known face
        matches = face_recognition.compare_faces(
            [person['encodings'] for person in known_persons_data],
            face_encoding,
            tolerance=0.5
        )

        name = "Unknown"
        person_id = None

        if True in matches:
            first_match_index = matches.index(True)
            name = known_persons_data[first_match_index]['name']
            person_id = known_persons_data[first_match_index]['id']

        print(f"Person: {name}, ID: {person_id}, Location: {top},{right},{bottom},{left}")

@csrf_exempt
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
                with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as img_file:
                    img_file.write(image_content.read())

                #recognize_faces(image_path)

                print("Recognizing")
            
            except Exception as e:
                print("Error:" + e)
            
    context = {}
    return render(request, 'core/detect_person.html', context)
