from django.test import TestCase
from django.utils import timezone
from storage.models import Order, OrderItem, Item, Changes
from accounts.models import User, Customer, Employee
from datetime import datetime


class StorageItemCreationTest(TestCase):
    def test_can_create_item(self):
        try:
            item = Item.objects.create(
                name="testitem",
                weight="500",
                description="desc",
                contents="cont",
                price="450.99",
            )
            change = Changes.objects.create(
                item=item, component="NONE", selected="no", price=0.0
            )
        except:
            self.fail("Can't create Item")


class StorageOrderCreationTest(TestCase):
    def setUp(self):
        self.user_c = User.objects.create_user(
            username="testcust", password="passwordforcustomer"
        )
        self.customer = Customer.objects.create(user=self.user_c, phone="89998884433")

        self.user_e = User.objects.create_user(
            username="testempl", password="passwordforemployee"
        )
        self.employee = Employee.objects.create(user=self.user_e, role="COOK")

        self.item = Item.objects.create(
            name="testitem",
            weight="500",
            description="desc",
            contents="cont",
            price="450.99",
        )
        self.change = Changes.objects.create(
            item=self.item, component="NONE", selected="no", price=0.0
        )

    def test_can_create_order(self):
        try:
            order = Order.objects.create(
                customer=self.customer,
                creation_date=datetime.now(tz=timezone.UTC),
                completion_date=datetime.now(tz=timezone.UTC),
                delivery_type="DELIVERY",
                delivery_address="ул. Тестовая 53",
                payment_type="CARD",
                status="PROCESSING",
                employee=self.employee,
            )
            orderitem = OrderItem.objects.create(order=order, amount=1)
            orderitem.changeditem.add(self.change)
        except:
            self.fail("Can't create Order")


class StorageMethodsTest(TestCase):
    def setUp(self):
        self.user_c = User.objects.create_user(
            username="testcust", password="passwordforcustomer"
        )
        self.customer = Customer.objects.create(user=self.user_c, phone="89998884433")

        self.user_e = User.objects.create_user(
            username="testempl", password="passwordforemployee"
        )
        self.employee = Employee.objects.create(user=self.user_e, role="COOK")

        self.item = Item.objects.create(
            name="testitem",
            weight=500,
            description="desc",
            contents="cont",
            price=450,
        )
        self.change = Changes.objects.create(
            item=self.item, component="NONE", selected="no", price=100
        )

        self.order = Order.objects.create(
                customer=self.customer,
                creation_date=datetime.now(tz=timezone.UTC),
                completion_date=datetime.now(tz=timezone.UTC),
                delivery_type="DELIVERY",
                delivery_address="ул. Тестовая 53",
                payment_type="CARD",
                status="PROCESSING",
                employee=self.employee,
            )
        self.orderitem = OrderItem.objects.create(order=self.order, amount=2)
        self.orderitem.changeditem.add(self.change)

    def test_order_get_total(self):
        result = self.order.get_total()
        self.assertEqual(result, 1100)

    def test_changes_get_item(self):
        item = self.change.get_item()
        self.assertEqual(item, self.item)

    def test_orderitem_get_item(self):
        item = self.orderitem.get_item()
        self.assertEqual(item, self.item)

    def test_orderitem_get_changes_price(self):
        price = self.orderitem.get_changes_price()
        self.assertEqual(price, 100)

    def test_orderitem_get_item_price(self):
        price = self.orderitem.get_item_price()
        self.assertEqual(price, 550)

    def test_orderitem_get_price(self):
        price = self.orderitem.get_price()
        self.assertEqual(price, 1100)