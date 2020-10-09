from django.urls import reverse
from django.test import TestCase

from accounts.models import Account


class RegistrationPageTest(TestCase):
    def test_the_registration_page_uses_expected_template(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_account_is_created_when_the_register_endpoint_is_POSTed_to(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jdoe@examle.com",
            "password1": "p4ssw0rd!",
            "password2": "p4ssw0rd!",
        }
        response = self.client.post(reverse("accounts:register"), data=data, follow=True)
        created_account = Account.objects.first()

        self.assertEquals(data["first_name"], created_account.first_name)
        self.assertEquals(data["last_name"], created_account.last_name)
        self.assertEquals(data["email"], created_account.email)

        self.assertEquals(response.context["user"], created_account)
        self.assertRedirects(response, reverse("dashboard:home"))


class AuthenticationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.account = Account(email="test@example.com")
        cls.account.set_password("p4ssw0rd!")
        cls.account.save()

    def test_the_registration_page_uses_expected_template(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_can_login_an_existing_account(self):
        account = Account(first_name="John", last_name="Doe", email="jdoe@example.com")
        account.set_password("p4ssw0rd!")
        account.save()

        credentials = {
            "username": account.email,
            "password": "p4ssw0rd!",
        }
        response = self.client.post(reverse("accounts:login"), data=credentials, follow=True)

        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("dashboard:home"))

    def test_account_can_be_logged_out(self):
        account = Account(first_name="John", last_name="Doe", email="jdoe@example.com")
        account.set_password("p4ssw0rd!")
        account.save()

        login_success = self.client.login(username=account.email, password="p4ssw0rd!")
        self.assertTrue(login_success)

        response = self.client.get(reverse("accounts:logout"), follow=True)

        self.assertFalse(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_login_page_cannot_be_accessed_if_already_logged_in(self):
        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("accounts:login"))
        self.assertRedirects(response, reverse("dashboard:home"))
