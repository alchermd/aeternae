from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


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
        self.selenium.get(self.live_server_url + "/accounts/register/")
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
        # message appearing to welcoming her and acknowledging that she had succesfully logged in.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have successfully registered for an account. Enjoy your stay!", body_text)

        # Satisfied, he went to bed.
