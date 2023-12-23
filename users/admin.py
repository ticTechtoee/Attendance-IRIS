from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    class Media:
        js = (
            'js/admin.js',  # inside app static folder
        )
    list_display = ['username',]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'user_role',
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)