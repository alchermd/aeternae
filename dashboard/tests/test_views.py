from django.urls import reverse
from django.test import TestCase


class DashboardTest(TestCase):
    def test_the_dashboard_home_page_uses_expected_template(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertTemplateUsed(response, "dashboard/home.html")
