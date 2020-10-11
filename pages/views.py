from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy


@user_passes_test(lambda u: u.is_anonymous, login_url=reverse_lazy("dashboard:home"), redirect_field_name=None)
def home(request):
    return render(request, "pages/index.html")
