from django.contrib import admin

from .models import Order, Item, Changes, OrderItem

# Register your models here.
admin.site.register(Item)

admin.site.register(Order)
admin.site.register(Changes)

admin.site.register(OrderItem)