from django.urls import reverse
from django.test import TestCase


class LandingPageTest(TestCase):
    def test_can_the_landing_page_uses_expected_template(self):
        response = self.client.get(reverse("pages:home"))
        self.assertTemplateUsed(response, "pages/index.html")
