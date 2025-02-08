from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import LoginForm, RegistrationForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse('main:student_rating'))
            else:
                form.add_error(None, 'Неправильное имя пользователя или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('main:student_rating'))
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

def user_logout(request):
    auth.logout(request)
    return redirect(reverse('main:student_rating'))