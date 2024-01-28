from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Department, Program, Semester, ApplicationType
from django.utils import timezone

class AppUser(AbstractUser):
    custom_unique_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program, null=True, blank=True, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.DO_NOTHING)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        # Check if the user has an application type selected
        application_type = ApplicationType.objects.first()
        if application_type and application_type.type_app == 'OTHER':
            # If the application type is 'OTHER', clear program and semester fields
            self.program = None
            self.semester = None

        super(AppUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Attendance(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateField()
    entry_time = models.TimeField(null=True, blank=True)
    exit_time = models.TimeField(null=True, blank=True)
    is_present = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user} - {self.date} Entry: {self.entry_time} Exit: {self.exit_time}"

    def calculate_hours_worked(self):
        if self.entry_time and self.exit_time:
            entry_datetime = timezone.datetime.combine(self.date, self.entry_time)
            exit_datetime = timezone.datetime.combine(self.date, self.exit_time)
            duration = exit_datetime - entry_datetime

            # Calculate hours, minutes, and seconds
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)

            return int(hours), int(minutes), int(seconds)
        else:
            return 0, 0, 0