from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Department, Program, Semester, ApplicationType

class AppUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program, null=True, blank=True, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.DO_NOTHING)

    # Additional field for storing the application type
    application_type = models.ForeignKey(ApplicationType, null=True, blank=True, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        # Check if the user has an application type selected
        if self.application_type and self.application_type.type_app == 'OTHER':
            # If the application type is 'OTHER', clear program and semester fields
            self.program = None
            self.semester = None

        super(WebUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
