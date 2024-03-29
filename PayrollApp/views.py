# PayrollApp/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import date, timedelta
from AccountApp.models import AppUser, Attendance
from core.models import ApplicationType, ApplicationName
from decimal import Decimal
from openpyxl.styles import Font

def calculate_salary(record, hourly_rate):
    if record.is_present:

        hours_worked = record.calculate_hours_worked()
        daily_salary = hourly_rate * hours_worked[0]
    else:
        daily_salary = Decimal(0)

    return daily_salary

def PayrollView(request):
    get_user = request.user
    application_type = ApplicationType.objects.first()

    try:
        set_logo = ApplicationName.objects.latest('id')
    except ApplicationName.DoesNotExist:
        set_logo = None
    user = None
    payroll_data = None
    total_salary = None
    error_message = False

    if request.method == 'POST':
        if 'search' in request.POST:
            user_ID = request.POST.get('User_ID')

            try:
                user = AppUser.objects.get(custom_unique_id=user_ID)

                today = date.today()
                first_day = today.replace(day=1)
                last_day = today.replace(day=28) + timedelta(days=4)

                hourly_rate = user.hourly_rate

                attendance_records = Attendance.objects.filter(
                    user=user,
                    date__range=[first_day, last_day]
                ).order_by('date')

                total_salary = Decimal(0)
                payroll_data = []

                for record in attendance_records:
                    daily_salary = calculate_salary(record, hourly_rate)
                    total_salary += daily_salary
                    payroll_data.append({'record': record, 'daily_salary': daily_salary, 'total_salary': total_salary})

            except AppUser.DoesNotExist:
                user = None
                error_message = True

    context = {
        'user': user,
        'payroll_data': payroll_data,
        'total_salary': total_salary,
        'Error_Message': error_message,
        'user_info': get_user, 'Set_Logo': set_logo, 'App_type':application_type
    }

    return render(request, 'PayrollApp/view.html', context)

