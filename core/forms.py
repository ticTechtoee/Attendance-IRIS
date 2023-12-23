from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from .models import *


class updatePasswordForm(UserCreationForm):
# class updatePassword(forms.ModelForm):
    class Meta:
        model = User
        fields=['password1','password2']
    def __init__(self, *args, **kwargs):
        super(updatePasswordForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control input'
        self.fields['password2'].widget.attrs['class'] = 'form-control input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter New Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Enter New Password'

class updateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['first_name']

    def __init__(self, *args, **kwargs):
        super(updateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control input'


class updateStudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(updateStudentForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control input'


