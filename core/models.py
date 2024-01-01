from django.db import models

class ApplicationName(models.Model):
    application_title = models.TextField()
    logo_of_project = models.ImageField(default='images/default.jpg', upload_to='images/logo')

    class Meta:
        verbose_name_plural = "Application Name"
    def __str__(self):
        return self.application_title