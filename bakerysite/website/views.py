from django.http import HttpResponse
from django.shortcuts import render

from storage.models import Item

def menu(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }

    return render(request, 'menu.html', context)

def about(request):
    return render(request, 'about.html')

def orders(request):
    return render(request, 'orders.html')

def cart(request):
    return render(request, 'cart.html')