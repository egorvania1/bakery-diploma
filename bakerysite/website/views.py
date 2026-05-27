from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

from storage.models import Item, Order, OrderItem
from accounts.models import Customer

from .forms import ChangesForm, CartForm

def customer_check(user):
    return user.is_staff == False
   #return user.user_type == "CUSTOMER"

@user_passes_test(customer_check)
def about(request):
    return render(request, 'about.html')

@user_passes_test(customer_check)
def menu(request):
    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'menu.html', context)

@login_required
@user_passes_test(customer_check)
def item_info(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ChangesForm(request.POST, item=item)
        if form.is_valid():

            #Добавляем товар в корзину (и создаем её при необходимости)
            customer = Customer.objects.get(user=request.user)
            try:
                order = Order.objects.get(customer=customer, creation_date=None)
            except:
                order = Order.objects.create(customer=customer)

            #Собираем выбранные пользователем изменения
            orderitem = OrderItem.objects.create(order=order)
            for field in form.cleaned_data:
                orderitem.changeditem.add(form.cleaned_data[field])
            orderitem.save()
            
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


@login_required
@user_passes_test(customer_check)
def orders(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.exclude(creation_date=None).filter(customer=customer)

    items = OrderItem.objects.filter(order__in=orders)

    context = {
        'items': items
    }

    return render(request, 'orders.html', context)

@login_required
@user_passes_test(customer_check)
def cart(request):
    customer = Customer.objects.get(user=request.user)
    try:
        order = Order.objects.get(customer=customer, creation_date=None)
    except:
        order = Order.objects.create(customer=customer)

    items = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        form = CartForm(request.POST, instance=order)
        if items.count() <= 0:
            messages.error(request, 'Отсутствуют товары в корзине')
        elif form.is_valid():
            instance = form.save(commit=False)
            instance.creation_date = datetime.now(tz=timezone.UTC)
            instance.status = "PROCESSING"
            instance.is_ordered = True
            instance.save()
            return redirect('orders')
    else:
        form = CartForm(instance=order)

    context = {
        'form': form,
        'items': items,
        'order': order,
    }

    return render(request, 'cart.html', context)

@user_passes_test(customer_check)
def remove_item(request, pk=None):
    item = get_object_or_404(OrderItem, pk=pk)
    item.delete()
    return redirect('cart')

@user_passes_test(customer_check)
def increase_amount(request, pk=None):
    item = get_object_or_404(OrderItem, pk=pk)
    item.amount += 1
    item.save()
    return redirect('cart')

@user_passes_test(customer_check)
def decrease_amount(request, pk=None):
    item = get_object_or_404(OrderItem, pk=pk)
    if item.amount > 1:
        item.amount -= 1
        item.save()
    return redirect('cart')