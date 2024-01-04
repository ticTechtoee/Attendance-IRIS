from django.contrib import admin
from .models import ApplicationName, ApplicationType,Department,Program,Semester

admin.site.register(ApplicationName)
admin.site.register(ApplicationType)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Semester)
