from django.test import TestCase
from accounts.models import User, Customer, Employee


class AccountsCustomerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="passwordfortesting"
        )

    def test_can_create_customer(self):
        try:
            customer = Customer(user=self.user, phone="89998884433")
        except:
            self.fail("Can't create Customer")

    def test_can_create_employee(self):
        try:
            employee = Employee(user=self.user, role="COOK")
        except:
            self.fail("Can't create Employee")
