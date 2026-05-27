from django.test import TestCase
from storage.models import Order
from accounts.models import User, Customer, Employee
from datetime import datetime


class StorageOrderTest(TestCase):
    def setUp(self):
        self.user_c = User.objects.create_user(
            username="testcust", password="passwordforcustomer"
        )
        self.customer = Customer(user=self.user_c, phone="89998884433")

        self.user_e = User.objects.create_user(
            username="testempl", password="passwordforemployee"
        )
        self.employee = Employee(user=self.user_e, role="COOK")

    def test_can_create_order(self):
        try:
            order = Order(
                customer=self.customer,
                creation_date=datetime.now(),
                completion_date=datetime.now(),
                delivery_type="DELIVERY",
                delivery_address="ул. Тестовая 53",
                payment_type="CARD",
                status="PROCESSING",
                employee=self.employee,
            )
        except:
            self.fail("Can't create Employee")
