from django.db import models

class ApplicationName(models.Model):
    application_title = models.TextField()
    logo_of_project = models.ImageField(default='images/default.jpg', upload_to='images/logo')
    application_type = models.ForeignKey('ApplicationType', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Application Names"

    def __str__(self):
        return self.application_title

class ApplicationType(models.Model):
    TYPE_CHOICES = [
        ("EDU", "Education"),
        ("OTHER", "Other")
    ]
    
    type_app = models.CharField(max_length=10, choices=TYPE_CHOICES, default="EDU", unique=True)

    def save(self, *args, **kwargs):
        # Ensure only one object exists by deleting others
        ApplicationType.objects.exclude(pk=self.pk).delete()
        super(ApplicationType, self).save(*args, **kwargs)
        

class Department(models.Model):
    department_name = models.TextField()

    class Meta:
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.department_name

class Program(models.Model):
    program_name = models.TextField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

class Semester(models.Model):
    semester_name = models.TextField()
