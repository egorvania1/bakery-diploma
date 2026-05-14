from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import UserLoginForm, UserRegisterForm, ProfileRegisterForm


# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("menu")
            else:
                messages.error(request, "Неверное имя пользователя или пароль")
                # return redirect('accounts:login')
    else:
        form = UserLoginForm()

    context = {
        "form_login": form,
    }

    return render(request, "accounts/login.html", context)


def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(data=request.POST)
        profile_form = ProfileRegisterForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save()
            profile.user = user

            profile.save()
            user.save()
            messages.error(request, "Аккаунт создан!")
            # return redirect('accounts:login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/register.html", context)


# def logout(request):
#    logout(request)
