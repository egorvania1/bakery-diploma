from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login
from storage.models import Order, OrderItem, Item, Changes
from accounts.models import User, Customer, Employee
from datetime import datetime


class TestPagesOpen(TestCase):
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

    def test_menu_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "menu.html")

    def test_about_correct_template(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")

    def test_cart_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("cart"))
        self.assertTemplateUsed(response, "cart.html")

    def test_orders_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("orders"))
        self.assertTemplateUsed(response, "orders.html")

    def test_profile_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("accounts:profile"))
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_redirect_to_login_template(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(response, "/accounts/login?next=/accounts/profile")