from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from storage.models import Item, ChangedItem, Order, OrderItem
from accounts.models import Customer

from .forms import ChangesForm, CartForm



def menu(request):
    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'menu.html', context)

def about(request):
    return render(request, 'about.html')

@login_required
def orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer, is_ordered=True)

    return render(request, 'orders.html')

@login_required
def cart(request):
    customer = Customer.objects.get(user=request.user)
    try:
        order = Order.objects.get(customer=customer, is_ordered=False)
    except:
        order = Order.objects.create(customer=customer)

    items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        form = CartForm(request.POST, instance=order)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creation_date = datetime.now()
            instance.status = "PROCESSING"
            instance.is_ordered = True
            instance.save()
            return redirect('orders')
    else:
        form = CartForm(instance=order)

    context = {
        'form': form,
        'items': items,
    }

    return render(request, 'cart.html', context)

@login_required
def item_info(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ChangesForm(request.POST, item=item)
        if form.is_valid():

            #Собираем выбранные пользователем изменения
            changesinitem = ChangedItem()
            changesinitem.save()
            for field in form.cleaned_data:
                changesinitem.changes.add(form.cleaned_data[field])
            changesinitem.save()

            #Добавляем товар в корзину (и создаем её при необходимости)
            customer = Customer.objects.get(user=request.user)
            try:
                order = Order.objects.get(customer=customer, is_ordered=False)
            except:
                order = Order.objects.create(customer=customer)
            orderitem = OrderItem.objects.create(order=order, changeditem=changesinitem)
            
            return HttpResponseRedirect("/")
        else:
            print(form.errors.as_data())
    else:
        form = ChangesForm(item=item)

    context = {
        'item': item,
        'form': form
    }

    return render(request, 'item_info.html', context)