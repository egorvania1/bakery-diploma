from django.contrib import admin

from .models import Order, Item, Changes, OrderItem


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "weight", "price"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    #def view_item(self, obj):
    #    result = obj.get_item().name
    #    return result

    @admin.display(description="Изменения")
    def view_changes(self, obj):
        result = ""
        for change in obj.changeditem.all():
            result += f"{change.get_component_display()} {change.selected} {change.price}\n"
        return result

    @admin.display(description="Цена")
    def view_item_price(self, obj):
        return f"{obj.get_item_price()} руб."

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    exclude= ('changeditem', )
    readonly_fields = ('view_changes', 'amount', 'view_item_price')
    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    @admin.display(description="Стоимость")
    def view_total_price(self, obj):
        return f"{obj.get_total()} руб."

    list_display = ["customer", "creation_date", "status", "view_total_price"]
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
