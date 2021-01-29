from django.conf import settings
from functools import wraps
from django.shortcuts import redirect
import requests

base_url = "http://localhost:8000"


def verify(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        try:
            verify_url = base_url + "/auth/verify"
            cookie = request.COOKIES.get('Authorization') 
            bearer, token = cookie.split()
            response = requests.post(verify_url, json={"token": token})
            if "token" not in response.json():
                raise Exception
        except:
            return redirect('login')
        response = func(request, token, *args, **kwargs)
        return response
    return decorator
