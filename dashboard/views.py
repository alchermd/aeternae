import json
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def home(request):
    return render(request, "dashboard/home.html")


@login_required
def sessions(request):
    pwd = os.path.dirname(__file__)
    filepath = os.path.join(pwd, "data.json")
    with open(filepath, "r") as f:
        return JsonResponse(json.load(f)["sessions"])
