from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm
from django.contrib.auth import login, authenticate

def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user=register_form.save()
            login(request,user)
            return redirect('index')

    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': register_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'accounts/login.html')

