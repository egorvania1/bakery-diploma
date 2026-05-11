from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from storage.models import Item

from .forms import ChangesForm

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

def item_info(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ChangesForm(request.POST, item=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = ChangesForm(item=item)

    context = {
        'item': item,
        'form': form
    }

    return render(request, 'item_info.html', context)