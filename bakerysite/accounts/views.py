from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import UserLoginForm

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            if 'login' in request.POST:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('menu')
                else:
                    messages.error(request,'Неверное имя пользователя или пароль')
                    #return redirect('accounts:login')
                login(request, user)
                return redirect('menu')

            elif 'register' in request.POST:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.error(request, 'Аккаунт создан!')
                #return redirect('accounts:login')
            else:
                messages.error(request, 'Неизвестная ошибка')
                return redirect('accounts:login')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, "accounts/login.html", context)

#def logout(request):
#    logout(request)