from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Manually authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the authenticated user
            login(request, user)

            # Redirect to a success page or homepage
            return redirect('core:ViewDetectPerson')
        else:
            # Handle authentication failure, e.g., show an error message
            return render(request, 'AccountApp/login_form.html', {'error_message': 'Invalid credentials'})

    return render(request, 'AccountApp/login_form.html')