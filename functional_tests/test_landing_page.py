import time
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class LandingPageTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_landing_page_loads_properly(self):
        # John heard of this new Django template called "Aeternae" that he could use with his next project.
        # He visited its website and saw from the title and site header that this site is, in fact, of the template.
        self.selenium.get(self.live_server_url)
        self.assertIn("Aeternae", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Aeternae", header_title.title())

        # Intrigued by the "Find out More" call-to-action, he clicked it and the page scrolled to the "About" section
        cta_button = self.selenium.find_element_by_link_text(
            "Find Out More".upper())
        cta_button.click()
        # Finding text by viewport isn't available in the Selenium API yet, so let's just check the the current url is
        # still the landing page
        self.assertEquals(self.live_server_url + "/",
                          self.selenium.current_url)

        # Scrolling through the page, he reached the bottom and found a copyright notice.
        # Again, viewport testing isn't available so let's just assert the the footer text is in the page's HTML
        footer_text = self.selenium.find_element_by_tag_name("footer").text
        current_year = datetime.today().year
        self.assertIn(
            footer_text, f"Copyright © {current_year} - hoplite.tech")

        # Satisfied, he went to bed.
