import json
import os

from django.urls import reverse
from django.test import TestCase

from accounts.models import Account


class DashboardTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.account = Account(email="test@example.com")
        cls.account.set_password("p4ssw0rd!")
        cls.account.save()

    def test_the_dashboard_home_page_uses_expected_template(self):
        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("dashboard:home"))
        self.assertTemplateUsed(response, "dashboard/home.html")

    def test_the_dashboard_home_page_cannot_be_access_unless_logged_in(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=/dashboard/")

        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("dashboard:home"))
        self.assertEquals(200, response.status_code)

    def test_can_fetch_sample_sessions_data(self):
        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("dashboard:sessions"))

        pwd = os.path.dirname(__file__)
        filepath = os.path.join(pwd, "../data.json")
        with open(filepath, "r") as f:
            self.assertEquals(json.load(f)["sessions"], json.loads(response.content.decode("utf-8")))

    def test_can_fetch_sample_revenue_data(self):
        self.client.login(username=self.account.email, password="p4ssw0rd!")
        response = self.client.get(reverse("dashboard:revenue"))

        pwd = os.path.dirname(__file__)
        filepath = os.path.join(pwd, "../data.json")
        with open(filepath, "r") as f:
            self.assertEquals(json.load(f)["revenue"], json.loads(response.content.decode("utf-8")))
