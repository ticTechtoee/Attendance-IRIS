from django.urls import path
from . import views

app_name = 'PayrollApp'

urlpatterns = [
    path('salary_report/', views.PayrollView, name='ViewPayroll'),

]