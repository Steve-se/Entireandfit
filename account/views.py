from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User
from django.db import IntegrityError
from .utils import check_username_exists
# Create your views here.


def user_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            error = "Please enter a valid username"
        elif password == '':
            error = "Please enter password"

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # check if user is active
            if user.is_active:
                login(request, user)
                return redirect(reverse('blog:homepage'))
            else:
                error = "This account has been disabled"
        else:
            error = "Invalid username and password"

    return render(request, 'account/login.html', {"error": error})


def register(request):
    error = ''
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('passwordConf')

        if check_username_exists(username):
            error = "This username already exists"
        elif password != confirm_password:
            error = "passwords didn't match"

        else:
            try:
                new_user = User(username=username,
                                password=password, email=email)
                new_user.set_password(password)

                new_user.save()
                return redirect('account:login')
            except IntegrityError as e:
                error = "Email already exists"

    return render(request, 'account/register.html', {"error": error})


def logout_user(request):
    logout(request)
    return redirect(reverse('blog:homepage'))
