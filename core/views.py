import base64
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ApplicationName

def SetProjectNameView(request):
    set_name =  ApplicationName.objects.latest('id')
    context = {'Name_of_Project': set_name}
    return render(request, 'core/welcome.html', context)


def IndexPageView(request):
    set_logo = ApplicationName.objects.latest('id')
    print("Logo URL:", set_logo.logo_of_project.url)
    context = {'Set_Logo': set_logo}
    return render(request, 'core/index.html', context)

def RegisterStudentView(request):
    context = {}
    return render(request, "core/student.html", context)

def add_padding(data):
    # Ensure that the Base64 data has proper padding
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return data

def capture_image(request):
    if request.method == 'POST':
        # Get the image data from the request
        image_data = request.POST.get('image_data')

        # Add padding to the Base64 data
        padded_image_data = add_padding(image_data)

        # Decode the Base64-encoded image data
        try:
            image_data_decoded = base64.b64decode(padded_image_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error decoding image: {str(e)}'})

        # Save the image to the media folder
        image_path = 'captured_images/image.png'
        image_full_path = default_storage.path(image_path)

        with open(image_full_path, 'wb') as image_file:
            image_file.write(image_data_decoded)

        # Respond with success or additional data
        return JsonResponse({'status': 'success', 'image_path': image_path})

    return render(request, 'core/student.html')