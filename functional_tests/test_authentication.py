from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from accounts.models import Account


class AuthenticationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_can_register_for_an_account(self):
        # Jane wanted to register for an Aeternae account, so she went to the accounts registration page and saw that
        # the page title and header does suggest that this is the registration page
        self.selenium.get(self.live_server_url + "/register/")
        self.assertIn("Register", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Create Account", header_title.title())

        # She is prompted for her name, so she enter her first and last name
        first_name_inputbox = self.selenium.find_element_by_name("first_name")
        first_name_inputbox.send_keys("Jane")
        last_name_inputbox = self.selenium.find_element_by_name("last_name")
        last_name_inputbox.send_keys("Doe")

        # Next up is her email
        email_inputbox = self.selenium.find_element_by_name("email")
        email_inputbox.send_keys("jdoe@example.com")

        # Lastly is her password, inputted twice for confirmation
        password1_inputbox = self.selenium.find_element_by_name("password1")
        password1_inputbox.send_keys("p4ssw0rd!")
        password2_inputbox = self.selenium.find_element_by_name("password2")
        password2_inputbox.send_keys("p4ssw0rd!")

        # She then submitted the registration form
        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        # The page redirects to the dashboard where she saw the page title and header saying so, with a nice and warm
        # message appearing to welcoming her and acknowledging that she had succesfully created an account.
        self.assertEquals(self.selenium.current_url + "/", self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have successfully registered for an account. Enjoy your stay!", body_text)

        # Satisfied, she went to bed.

    def test_can_login_with_an_account(self):
        # Alice had registered for an account yesterday and would like to log back in to the dashboard
        account = Account(first_name="Alice", last_name="Green", email="alice.green@example.com")
        account.set_password("p4ssw0rd!")
        account.save()

        # She goes to the login page...
        self.selenium.get(self.live_server_url + "/login/")
        self.assertIn("Login", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Logins", header_title.title())

        # ...and fills out the form with her credentials
        email_inputbox = self.selenium.find_element_by_name("email")
        email_inputbox.send_keys("alice.green@example.com")
        password_inputbox = self.selenium.find_element_by_name("password")
        password_inputbox.send_keys("p4ssw0rd!")

        # She then submits the login form
        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        # The page redirects to the dashboard where she saw the page title and header saying so, with a nice and warm
        # message appearing to welcoming her and acknowledging that she had succesfully logged in.
        self.assertEquals(self.selenium.current_url + "/", self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("It's great to have you back, Alice!", body_text)
