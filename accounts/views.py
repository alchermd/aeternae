from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            account = form.save()
            auth_login(request, account)
            messages.success(request, 'You have successfully registered for an account. Enjoy your stay!')
            return redirect(reverse("dashboard:home"))
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            account = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            auth_login(request, account)
            messages.success(request, f"It's great to have you back, {account.first_name.title()}!")
            return redirect(reverse("dashboard:home"))
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {"form": form})
