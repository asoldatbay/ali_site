from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SignInForm
from utils import token
import requests


base_url = "http://localhost:8000"


def landing(request):
    return render(request, "landing.html")


def login(request):
    try:
        if request.method == 'POST':
            login_url = base_url + "/auth/login"
            form = SignInForm(request.POST)
            if form.is_valid():
                response = requests.post(login_url, json={"username": form.cleaned_data["username"],
                                                          "password": form.cleaned_data["password"]})
                print(response.json())
                token = response.json()["token"]
                response = redirect('me')
                response.set_cookie("Authorization", "Bearer " + token,
                                    max_age=settings.JWT_EXPIRATION_MILIS // 1000)
                return response
            else:
                form = SignInForm()
    except:
        pass
    return render(request, 'login.html', {'form': form})


@token.verify
def me(request, token):
    profile_url = base_url + "/auth/profile"
    try:
        response = requests.post(profile_url, json={"token": token})
        data = response.json()
        return render(request, 'me.html', data)
    except:
        return redirect('login')
