from django.contrib import admin

from .models import Customer, Employee, Order, Item, Changes, ChangedItem, ItemsInOrder

# Register your models here.

admin.site.register(Customer)
admin.site.register(Employee)

admin.site.register(Item)

admin.site.register(Order)
admin.site.register(Changes)

admin.site.register(ChangedItem)
admin.site.register(ItemsInOrder)