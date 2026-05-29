from django.contrib import admin

from .models import Order, Item, Changes, OrderItem


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "weight", "price"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    #fields = ('changeditem', 'amount')
    #readonly_fields = ('changeditem', 'amount')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "creation_date", "status"]
    list_filter = ("customer", "status", "creation_date",)

    inlines = [
        OrderItemInline,
    ]


@admin.register(Changes)
class ChangesAdmin(admin.ModelAdmin):
    list_display = ["item", "component", "selected", "price"]
    list_filter = ("item", "component")

#@admin.register(OrderItem)
#class OrderItemAdmin(admin.ModelAdmin):
#    pass
