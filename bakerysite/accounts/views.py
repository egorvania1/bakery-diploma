from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm, ProfileRegisterForm, UserEditForm, ProfileEditForm, PasswordEditForm
from accounts.models import User, Customer

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("menu")

    next_url = request.GET.get("next", "menu")

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
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
    if request.user.is_authenticated:
        return redirect("menu")

    if request.method == "POST":
        user_form = UserRegisterForm(data=request.POST)
        profile_form = ProfileRegisterForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.user_type = "CUSTOMER"
            user.set_password(user.password)

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            user.save()
            # messages.error(request, "Аккаунт создан!")
            return redirect('accounts:login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/register.html", context)

@login_required
def profile_view(request):
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=customer)
        pass_form = PasswordEditForm(request.POST)
        password = request.POST.get('password')

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            profile_form.save()

            if pass_form.is_valid() and password != "":
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)

        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=customer)
        pass_form = PasswordEditForm()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "pass_form": pass_form,
    }
    return render(request, "accounts/profile.html", context)