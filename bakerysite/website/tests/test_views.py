from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login
from storage.models import Order, OrderItem, Item, Changes
from accounts.models import User, Customer, Employee
from datetime import datetime

class TestPageMenu(TestCase):
    def setUp(self):
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

    def test_menu_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "menu.html")

    def test_menu_context(self):
        item = Item.objects.create(
            name="NewIten",
            weight=500,
            description="desc",
            contents="cont",
            price=450,
        )
        change = Changes.objects.create(
            item=item, component="NONE", selected="no", price=0
        )
        response = self.client.get("/")
        self.assertEqual(len(response.context['items']), 2)
        self.assertContains(response, "testitem")

class TestPageCart(TestCase):
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
            delivery_type="DELIVERY",
            delivery_address="ул. Тестовая 53",
            payment_type="CARD",
        )
        self.orderitem = OrderItem.objects.create(order=self.order, amount=2)
        self.orderitem.changeditem.add(self.change)

    def test_cart_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("cart"))
        self.assertTemplateUsed(response, "cart.html")

    def test_cart_redirect_to_login_template(self):
        response = self.client.get(reverse("cart"))
        self.assertRedirects(response, "/accounts/login?next=/cart")

    def test_cart_context(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("cart"))
        self.assertEqual(len(response.context['items']), 1)
        self.assertContains(response, "testitem")

    def test_cart_can_order(self):
        data = {
            "delivery_type": "DELIVERY",
            "delivery_address": "ул. Тестовая 53",
            "payment_type": "CARD",
        }
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.post(reverse("cart"), data, follow=True)
        cart = Order.objects.filter(creation_date=None).count()
        self.assertEqual(cart, 0)

class TestPageOrders(TestCase):
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

    def test_orders_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("orders"))
        self.assertTemplateUsed(response, "orders.html")

    def test_orders_redirect_to_login_template(self):
        response = self.client.get(reverse("orders"))
        self.assertRedirects(response, "/accounts/login?next=/orders")

    def test_orders_context(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("orders"))
        self.assertEqual(len(response.context['items']), 1)
        self.assertContains(response, "testitem")

class TestPageAbout(TestCase):
    def test_about_correct_template(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")