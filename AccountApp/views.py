from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # Redirect to a success page or homepage
            return redirect('core:ViewDetectPerson')
    else:
        form = AuthenticationForm(request)

    return render(request, 'AccountApp/login_form.html', {'form': form})