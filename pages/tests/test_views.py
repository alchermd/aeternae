from django.urls import reverse
from django.test import TestCase

from accounts.models import Account


class LandingPageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.account = Account(email="test@example.com")
        cls.account.set_password("p4ssw0rd!")
        cls.account.save()

    def test_the_landing_page_uses_expected_template(self):
        response = self.client.get(reverse("pages:home"))
        self.assertTemplateUsed(response, "pages/index.html")

    def test_login_page_cannot_be_accessed_if_already_logged_in(self):
        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("pages:home"))
        self.assertRedirects(response, reverse("dashboard:home"))
