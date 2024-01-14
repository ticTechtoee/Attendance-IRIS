# PayrollApp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, timedelta
from AccountApp.models import AppUser, Attendance
# PayrollApp/calculate_salary.py
from decimal import Decimal


def calculate_salary(record, hourly_rate):
    # Check if the user was present on the given date
    if record.is_present:
        # Assuming 8 hours per day, adjust this based on your needs
        hours_worked = Decimal(8)
        daily_salary = hourly_rate * hours_worked
    else:
        # Deduct salary for absent days
        daily_salary = Decimal(0)

    return daily_salary

def PayrollView(request, custom_unique_id):
    user = AppUser.objects.get(custom_unique_id=custom_unique_id)

    # Get the first and last day of the current month
    today = date.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=28) + timedelta(days=4)

    # Get hourly rate from user
    hourly_rate = user.hourly_rate

    # Get attendance records for the current month
    attendance_records = Attendance.objects.filter(
        user=user,
        date__range=[first_day, last_day]
    ).order_by('date')

    # Calculate total salary for the month
    total_salary = Decimal(0)

    # Prepare a list of dictionaries with record, daily_salary, and total_salary
    payroll_data = []
    for record in attendance_records:
        daily_salary = calculate_salary(record, hourly_rate)
        total_salary += daily_salary
        payroll_data.append({'record': record, 'daily_salary': daily_salary, 'total_salary': total_salary})

    context = {
        'user': user,
        'payroll_data': payroll_data,
        'total_salary': total_salary
    }

    return render(request, 'PayrollApp/view.html', context)