# PayrollApp/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import date, timedelta
from AccountApp.models import AppUser, Attendance
from decimal import Decimal
import openpyxl
from openpyxl.styles import Font

def calculate_salary(record, hourly_rate):
    if record.is_present:
        hours_worked = Decimal(8)
        daily_salary = hourly_rate * hours_worked
    else:
        daily_salary = Decimal(0)

    return daily_salary

def PayrollView(request):
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

                # Export to Excel if the user clicks the export button
                if 'export_to_excel' in request.POST:
                    return export_to_excel(user, payroll_data, total_salary)

            except AppUser.DoesNotExist:
                user = None
                error_message = True

    context = {
        'user': user,
        'payroll_data': payroll_data,
        'total_salary': total_salary,
        'Error_Message': error_message
    }

    return render(request, 'PayrollApp/view.html', context)

def export_to_excel(user, payroll_data, total_salary):
    # Create a new Workbook
    workbook = openpyxl.Workbook()

    # Create a worksheet
    worksheet = workbook.active
    worksheet.title = "Payroll Report"

    # Write the header row
    headers = ['Date', 'Present', 'Daily Salary']
    for col_num, header in enumerate(headers, start=1):
        worksheet.cell(row=1, column=col_num, value=header).font = Font(bold=True)

    # Write the data rows
    for row_num, data in enumerate(payroll_data, start=2):
        worksheet.cell(row=row_num, column=1, value=data['record'].date)
        worksheet.cell(row=row_num, column=2, value='Yes' if data['record'].is_present else 'No')
        worksheet.cell(row=row_num, column=3, value=float(data['daily_salary']))  # Convert Decimal to float

    # Write the total salary row
    worksheet.cell(row=row_num + 1, column=1, value='Total Salary').font = Font(bold=True)
    worksheet.cell(row=row_num + 1, column=3, value=float(total_salary)).font = Font(bold=True)

    # Create a BytesIO buffer to write the Excel file to
    output = BytesIO()

    # Save the workbook to the BytesIO buffer
    workbook.save(output)

    # Set up response headers for an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={user.custom_unique_id}_payroll.xlsx'

    # Write the Excel file to the response
    output.seek(0)
    response.write(output.getvalue())

    return response
