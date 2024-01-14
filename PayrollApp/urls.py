from django.urls import path
from . import views

app_name = 'PayrollApp'

urlpatterns = [
    path('salary_report/<str:custom_unique_id>/', views.PayrollView, name='ViewPayroll'),
    
]