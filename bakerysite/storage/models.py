from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    class Meta:
        unique_together = ('user', 'phone',)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    class Meta:
        unique_together = ('user', 'role',)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    delivery_type = models.CharField(max_length=10)
    delivery_address = models.CharField(max_length=30)
    payment_type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('customer', 'creation_date',)

class Item(models.Model):
    name = models.CharField(max_length=30)
    weight = models.IntegerField()
    description = models.CharField(max_length=300)
    contents = models.CharField(max_length=100)
    price = models.IntegerField()

    image = models.ImageField(upload_to="uploads/")

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

    class Meta:
        unique_together = ('item', 'component', 'selected',)
    
class ChangedItem(models.Model):
    changes = models.ManyToManyField(Changes)

class ItemsInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    changeditem = models.ForeignKey(ChangedItem, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        unique_together = ('order', 'changeditem',)

