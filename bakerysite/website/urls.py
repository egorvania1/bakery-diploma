"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    
    path('admin/', admin.site.urls),

    #Главные страницы
    path('', views.menu, name="menu"),
    path('about', views.about, name="about"),

    #Товар
    path('item/<int:pk>', views.item_info, name="item_info"),

    #Заказы
    path('orders', views.orders, name="orders"),

    #Корзина
    path('cart', views.cart, name="cart"),
    path('cart/delete/<int:pk>', views.remove_item, name='remove_item'),
    path('cart/increase/<int:pk>', views.increase_amount, name='increase_amount'),
    path('cart/decrease/<int:pk>', views.decrease_amount, name='decrease_amount'),

    #Аккаунты
    path('accounts/', include('accounts.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
