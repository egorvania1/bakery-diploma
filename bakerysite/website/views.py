from django.http import HttpResponse
from django.shortcuts import render

def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')

def orders(request):
    return render(request, 'orders.html')

def cart(request):
    return render(request, 'cart.html')