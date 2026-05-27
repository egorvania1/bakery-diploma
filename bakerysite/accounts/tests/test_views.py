from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate, login
from storage.models import Order, OrderItem, Item, Changes
from accounts.models import User, Customer, Employee
from datetime import datetime


class TestAccountLoginPage(TestCase):
    def setUp(self):
        self.credentials = {"username": "testcust", "password": "passwordforcustomer"}
        self.user_c = User.objects.create_user(**self.credentials)
        self.customer = Customer.objects.create(user=self.user_c, phone="89998884433")

    def test_login_can_login(self):
        response = self.client.post(
            reverse("accounts:login"), self.credentials, follow=True
        )
        self.assertTrue(response.context["user"].is_active)

    def test_login_can_not_login_with_bad_creds(self):
        wrong_credentials = {"username": "nonecust", "password": "passwordforcustomer"}
        response = self.client.post(
            reverse("accounts:login"), wrong_credentials, follow=True
        )
        self.assertFalse(response.context["user"].is_active)

    def test_login_correct_template(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertTemplateUsed(response, "accounts/login.html")


class TestAccountRegisterPage(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testcust",
            "password": "passwordforcustomer",
            "password_conf": "passwordforcustomer",
            "first_name": "Test",
            "phone": "89998884433",
        }

    def test_register_correct_template(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_can_register(self):
        response = self.client.post(
            reverse("accounts:register"), self.credentials, follow=True
        )
        try:
            User.objects.get(username="testcust")
        except:
            self.fail("Customer did not register")

    def test_register_can_not_register_duplicate(self):
        user_c = User.objects.create_user(
            username="testcust", password="passwordforcustomer"
        )
        customer = Customer.objects.create(user=user_c, phone="89998884433")
        response = self.client.post(
            reverse("accounts:register"), self.credentials, follow=True
        )
        user_form = response.context["user_form"]
        profile_form = response.context["profile_form"]
        self.assertFormError(
            user_form, "username", "Пользователь с таким именем уже существует."
        )
        self.assertFormError(
            profile_form,
            "phone",
            "Пользователь с таким номером телефона уже существует.",
        )


class TestAccountProfilePage(TestCase):
    def setUp(self):
        self.user_c = User.objects.create_user(
            username="testcust", password="passwordforcustomer", first_name="testcust"
        )
        self.customer = Customer.objects.create(user=self.user_c, phone="89998884433")
        self.user_c2 = User.objects.create_user(
            username="testcust2",
            password="passwordforcustomer2",
            first_name="testcust2",
        )
        self.customer2 = Customer.objects.create(user=self.user_c2, phone="89998883344")

    def test_profile_correct_template(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        response = self.client.get(reverse("accounts:profile"))
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_profile_redirect_to_login_template(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(response, "/accounts/login?next=/accounts/profile")

    def test_profile_can_change_info(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        data = {
            "password": "newpasswordforcustomer",
            "password_conf": "newpasswordforcustomer",
            "first_name": "Test",
            "username": "testcust",
            "phone": "89998883333",
        }
        response = self.client.post(reverse("accounts:profile"), data, follow=True)
        try:
            User.objects.get(first_name="Test")
            Customer.objects.get(phone="89998883333")
        except:
            self.fail("Customer did not change")

    def test_profile_can_not_change_info_to_duplicate(self):
        self.client.login(username="testcust", password="passwordforcustomer")
        data = {
            "password": "",
            "password_conf": "",
            "first_name": "Test",
            "username": "testcust2",
            "phone": "89998883344",
        }
        response = self.client.post(reverse("accounts:profile"), data, follow=True)
        user_form = response.context["user_form"]
        profile_form = response.context["profile_form"]
        self.assertFormError(
            user_form, "username", "Пользователь с таким именем уже существует."
        )
        self.assertFormError(
            profile_form,
            "phone",
            "Пользователь с таким номером телефона уже существует.",
        )
