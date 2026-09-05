from django.utils.http import urlsafe_base64_decode

from accounts.models import VulnTrackAccounts
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from accounts.tasks import send_password_reset_email

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

def password_reset_confirmation_view(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = VulnTrackAccounts.objects.get(id=user_id)
        if not default_token_generator.check_token(user, token):
            messages.error(request, 'Invalid token')
            return redirect('password-reset')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('password-reset')

    if request.method == 'POST':
        form = SetPasswordForm(user,request.POST)

        if form.is_valid():
            form.save()
            auth.login(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('index')

    else:
        form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})


