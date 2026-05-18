from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer, Employee

class Order(models.Model):
    DELIVERY = {
        "S": "Самовывоз",
        "D": "Доставка",
    }

    PAYMENT = {
        "R": "При получении",
        "C": "По карте",
    }

    STATUS = {
        "PROCESSING": "Обрабатывается",
        "IN_BUILDING": "В готовке",
        "IN_DELIVERY": "В доставке",
        "RECEIVED": "Получен",
        "CANCELLED": "Отменен",
    }
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    delivery_type = models.CharField(max_length=10, null=True, choices=DELIVERY)
    delivery_address = models.CharField(max_length=30, null=True)
    payment_type = models.CharField(max_length=10, null=True, choices=PAYMENT)
    status = models.CharField(max_length=11, null=True, choices=STATUS)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('customer', 'creation_date',)

    def __str__(self):
        return f'{self.customer} + {self.creation_date}'

class Item(models.Model):
    name = models.CharField(max_length=30)
    weight = models.IntegerField()
    description = models.CharField(max_length=300)
    contents = models.CharField(max_length=100)
    price = models.IntegerField()

    image = models.ImageField(upload_to="static/uploads/")

    class Meta:
        unique_together = ('name', 'weight',)

    def __str__(self):
        return self.name

class Changes(models.Model):
    COMPONENTS = {
        "NO": "Нету",
        "CR": "Крем",
        "KO": "Корж",
        "GL": "Глазурь",
        "DE": "Украшение",
    }
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    component = models.CharField(max_length=30, choices=COMPONENTS)
    selected = models.CharField(max_length=30)
    price = models.IntegerField()

    def get_item(self):
        return self.item

    class Meta:
        unique_together = ('item', 'component', 'selected',)

    def __str__(self):
        return f'{self.selected} {self.price}'
    
class ChangedItem(models.Model):
    changes = models.ManyToManyField(Changes)

    def get_item(self):
        return self.changes.first().item

    def get_changes_price(self):
        sum = 0
        for change in self.changes.all():
            sum += change.price
        return sum

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    changeditem = models.ForeignKey(ChangedItem, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def get_item(self):
        return self.changeditem.get_item()

    def get_price(self):
        return (self.changeditem.get_changes_price() + self.changeditem.get_item().price) * self.amount

    class Meta:
        unique_together = ('order', 'changeditem',)

