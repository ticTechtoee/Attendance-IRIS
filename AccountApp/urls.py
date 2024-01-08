from django.urls import path
from . import views

app_name = 'AccountApp'

urlpatterns = [
    path('login/', views.user_login, name='custom_login'),
    #path('password/reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),
    
]