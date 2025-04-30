from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import login
from . import forms
from .forms import CustomLoginForm


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomLoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
