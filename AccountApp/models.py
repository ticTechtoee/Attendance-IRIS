from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Department, Program, Semester, ApplicationType

class AppUser(AbstractUser):
    custom_unique_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program, null=True, blank=True, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.DO_NOTHING)
    application_type = models.ForeignKey(ApplicationType, null=True, blank=True, on_delete=models.DO_NOTHING)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # New field for teacher status
    is_teacher = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the user has an application type selected
        if self.application_type and self.application_type.type_app == 'OTHER':
            # If the application type is 'OTHER', clear program and semester fields
            self.program = None
            self.semester = None

        super(AppUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

class Attendance(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'date', 'time']

    def __str__(self):
        return f"{self.user} - {self.date} {self.time}"