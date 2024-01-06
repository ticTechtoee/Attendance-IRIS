import base64
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import ApplicationName
import os
import logging  # Import the logging module for error logging
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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
@csrf_exempt
def capture_image(request):
    if request.method == 'POST' and 'image_data' in request.POST:
        image_data = request.POST['image_data'].split(',')[1]
        image_content = ContentFile(base64.b64decode(image_data), name='captured_image.png')

            # Save the image to the /captured_images/ folder in the media directory
        image_path = 'captured_images/captured_image.png'
        with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb') as img_file:
            img_file.write(image_content.read())
            return JsonResponse({'message': 'Image captured and saved successfully!'})
    else:
        return render(request, 'core/student.html')
    