from django.contrib import admin

from .models import AppUser, Attendance

admin.site.register(AppUser)
admin.site.register(Attendance)
