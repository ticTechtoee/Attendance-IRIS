from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
APP_NAME = 'core'

urlpatterns = [

    path('', views.welcome, name='welcome'),
    path('index/', views.index, name='index'),
    #path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('login_form/', views.login_form, name='login_form'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('search_record/', views.search_record, name='search_record'),
    path('student/', views.student, name='student'),
    path('updateStudentDetails/<int:id>', views.updateStudentDetails, name='updateStudentDetails'),
    
    path('updateStudentDetailsfromteacher/<int:id>', views.updateStudentDetailsfromteacher, name='updateStudentDetailsfromteacher'),

    path('teacher_panel/', views.teacher_panel, name='teacher_panel'),
    path('teacher_search_record/', views.teacher_search_record, name='teacher_search_record'),
    path('teacher_update_record/', views.teacher_update_record, name='teacher_update_record'),
    path('update_record/', views.update_record, name='update_record'),
    path('teacher/', views.teacher, name='teacher'),
    path('teacher_update/', views.teacher_update, name='teacher_update'),
    path('teacher_faqs/', views.teacher_faqs, name='teacher_faqs'),
    path('admin_faqs/', views.admin_faqs, name='admin_faqs'),
    path('search_attendance/', views.search_attendance, name='search_attendance'),
    path('changeadminpassword/', views.changeadminpassword, name='changeadminpassword'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    path('take_attendance', views.take_attendance, name='take_attendance'),

    path('searchAttendence/', views.searchAttendence, name='searchAttendence'),
]