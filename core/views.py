from django.shortcuts import render
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