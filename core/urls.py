from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "core"

urlpatterns = [
    path('', views.SetProjectNameView, name = "ViewWelcomePage"),
    path('index/', views.IndexPageView, name="index"),
    path('capture_image/', views.capture_image, name="ViewCaptureImage"),
    path('model_training/', views.TrainOnDataView, name="ViewTrainData"),
    path('detect_person/', views.DetectPersonView, name="ViewDetectPerson"),
    path('search_attendence/', views.AttendenceSearchView, name="ViewAttendenceSearch"),
    path('update_record/<int:pk>/', views.UpdateRecordView, name="ViewUpdateRecord"),
    path('delete_record/<int:pk>/', views.DeleteRecordView, name="ViewDeleteRecord"),
    path('person_attendence_record/<str:pk>/', views.AttendenceRecordView, name="ViewAttendenceRecord"),

    path('stop_user/', views.ViewStopMessage, name="StopMessageView"),
    path('attendance_success/', views.AttendanceSuccessView, name="ViewAttendanceSuccess"),
    path('attendance_fail/', views.AttendanceFailedView, name="ViewAttendanceFailed"),



    path('hours_per_month/', views.calculate_hours_per_month, name='ViewHoursPerMonth'),
    path('admin_hours_per_month/', views.AdminAverageCalView, name='ViewAdminAverageCal'),

]
