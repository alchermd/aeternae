from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered for an account. Enjoy your stay!')
            return redirect(reverse("dashboard:home"))
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {"form": form})
