from django.db import models

# from django.contrib.auth.models import User
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer, Employee


class Order(models.Model):
    DELIVERY = {
        "SELF": "Самовывоз",
        "DELIVERY": "Доставка",
    }

    PAYMENT = {
        "ON_RECEIVE": "При получении",
        "CARD": "По карте",
    }

    STATUS = {
        "PROCESSING": "Обрабатывается",
        "IN_BUILDING": "В готовке",
        "IN_DELIVERY": "В доставке",
        "RECEIVED": "Получен",
        "CANCELLED": "Отменен",
    }
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата оформления")
    completion_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата завершения")
    delivery_type = models.CharField(max_length=10, null=True, choices=DELIVERY, verbose_name="Тип доставки")
    delivery_address = models.CharField(max_length=30, null=True, verbose_name="Адрес доставки")
    payment_type = models.CharField(max_length=10, null=True, choices=PAYMENT, verbose_name="Тип оплаты")
    status = models.CharField(max_length=11, null=True, choices=STATUS, verbose_name="Статус")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name="Сотрудник")

    class Meta:
        unique_together = (
            "customer",
            "creation_date",
        )

        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_total(self):
        order_items = OrderItem.objects.filter(order=self)
        total = sum([order_item.get_price() for order_item in order_items])
        return total

    def __str__(self):
        return f"{self.customer} {self.creation_date}"


class Item(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    weight = models.PositiveIntegerField(verbose_name="Вес")
    description = models.CharField(max_length=300, verbose_name="Описание")
    contents = models.CharField(max_length=100, verbose_name="Состав")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")

    image = models.ImageField(upload_to="static/uploads/", verbose_name="Изображение")

    class Meta:
        unique_together = (
            "name",
            "weight",
        )

        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Changes(models.Model):
    COMPONENTS = {
        "NONE": "Нету",
        "CREAM": "Крем",
        "KORZH": "Корж",
        "GLAZE": "Глазурь",
        "DECOR": "Украшение",
    }
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Товар")
    component = models.CharField(max_length=30, choices=COMPONENTS, verbose_name="Компонент")
    selected = models.CharField(max_length=30, verbose_name="Выбранный")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")

    class Meta:
        unique_together = (
            "item",
            "component",
            "selected",
        )

        verbose_name = "Изменение"
        verbose_name_plural = "Изменения"

    def get_item(self):
        return self.item

    def __str__(self):
        return f"{self.selected} {self.price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    # changeditem = models.ForeignKey(ChangedItem, on_delete=models.CASCADE)
    changeditem = models.ManyToManyField(Changes, verbose_name="Изменения")
    amount = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def get_item(self):
        return self.changeditem.first().item

    def get_changes_price(self):
        sum = 0
        for change in self.changeditem.all():
            sum += change.price
        return sum

    def get_item_price(self):
        return self.get_changes_price() + self.get_item().price

    def get_price(self):
        return self.get_item_price() * self.amount

    def __str__(self):
        return self.get_item().name
    # class Meta:
    #    unique_together = ('order', 'changeditem',)
