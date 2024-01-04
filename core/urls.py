from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "core"

urlpatterns = [
    path('welcome', views.SetProjectNameView, name = "ViewWelcomePage"),
    path('index', views.IndexPageView, name="index"),
    path('regstudent', views.RegisterStudentView, name="ViewRegisterStudent"),
    path('capture_image/', views.capture_image, name="ViewCaptureImage"),
]
