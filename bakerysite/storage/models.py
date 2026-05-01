from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    delivery_type = models.CharField(max_length=10)
    delivery_address = models.CharField(max_length=30)
    payment_type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Item(models.Model):
    name = models.CharField(max_length=30)
    weight = models.IntegerField()
    description = models.CharField(max_length=300)
    contents = models.CharField(max_length=100)
    price = models.IntegerField()

class Changes(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    component = models.CharField(max_length=30)
    selected = models.CharField(max_length=30)
    price = models.IntegerField()
    
class ItemsInOrder(models.Model):
    pk = models.CompositePrimaryKey("order_id", "changeditem_id", "changes_id")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    changeditem_id = models.PositiveIntegerField()
    changes = models.ForeignKey(Changes, on_delete=models.CASCADE)


