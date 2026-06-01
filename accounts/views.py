from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from accounts.forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect('index')
    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': register_form})


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        error = "Nieprawidłowa nazwa użytkownika lub hasło."
    return render(request, 'accounts/login.html', {'error': error})
