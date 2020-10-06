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
        response = self.client.post(reverse("accounts:register"), data=data)
        created_account = Account.objects.first()

        self.assertEquals(data["first_name"], created_account.first_name)
        self.assertEquals(data["last_name"], created_account.last_name)
        self.assertEquals(data["email"], created_account.email)

        self.assertRedirects(response, reverse("dashboard:home"))
