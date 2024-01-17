from django.urls import path
from . import views

app_name = 'AccountApp'

urlpatterns = [
    path('person_registration/', views.RegisterPersonView, name="ViewRegisterPerson"),
    path('login/', views.user_login, name='custom_login'),
    path('logout/', views.user_login, name='ViewLogout'),
    #path('password/reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),

]