from accounts.models import VulnTrackAccounts
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from kombu import message


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
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = VulnTrackAccounts.objects.get(email=email)
            token = default_token_generator.make_token(user)
            send_password_reset_email.delay(user.id, token)
            messages.success(request, 'Password reset link sent to your email')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/password_reset.html', {'form': form})

