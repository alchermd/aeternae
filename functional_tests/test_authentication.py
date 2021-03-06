from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from accounts.models import Account


class AuthenticationTest(StaticLiveServerTestCase):
    DEFAULT_PASSWORD = "p4ssw0rd!"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login(self, username, password):
        """
        Goes to the login page and enters the given credentials.
        """
        self.selenium.get(self.live_server_url + "/login/")

        email_inputbox = self.selenium.find_element_by_id("email")
        email_inputbox.send_keys(username)
        password_inputbox = self.selenium.find_element_by_id("password")
        password_inputbox.send_keys(password)

        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

    def logout(self):
        """
        Executes the steps to log the user out of the system.
        """
        user_dropdown = self.selenium.find_element_by_id("user-dropdown")
        user_dropdown.click()

        logout_button = self.selenium.find_element_by_link_text("Logout")
        logout_button.click()

    def make_account(self, email, password=DEFAULT_PASSWORD, first_name="", last_name=""):
        """
        Creates a new Account instance with the given parameters
        """
        account = Account(email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.save()

        return account

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
        password1_inputbox.send_keys(self.DEFAULT_PASSWORD)
        password2_inputbox = self.selenium.find_element_by_name("password2")
        password2_inputbox.send_keys(self.DEFAULT_PASSWORD)

        # She then submitted the registration form
        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        # The page redirects to the dashboard where she saw the page title and header saying so, with a nice and warm
        # message appearing to welcoming her and acknowledging that she had succesfully created an account.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have successfully registered for an account. Enjoy your stay!", body_text)

        # Satisfied, she went to bed.

    def test_can_login_with_an_account(self):
        # Alice had registered for an account yesterday and would like to log back in to the dashboard
        account = self.make_account(email="alice.green@example.com", first_name="Alice", last_name="Green")

        # She goes to the login page...
        self.selenium.get(self.live_server_url + "/login/")
        self.assertIn("Login", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Login", header_title.title())

        # ...and fills out the form with her credentials
        email_inputbox = self.selenium.find_element_by_id("email")
        email_inputbox.send_keys(account.email)
        password_inputbox = self.selenium.find_element_by_id("password")
        password_inputbox.send_keys(self.DEFAULT_PASSWORD)

        # She then submits the login form
        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        # The page redirects to the dashboard where she saw the page title and header saying so, with a nice and warm
        # message appearing to welcoming her and acknowledging that she had succesfully logged in.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("It's great to have you back, Alice!", body_text)

        # Satisfied, she went to bed.

    def test_can_logout_when_logged_in(self):
        # Bob logs in to his account and after a while, decided that he's done for the day .
        account = self.make_account(email="bob.smith@example.com", first_name="Bob", last_name="Smith")

        self.login(account.email, self.DEFAULT_PASSWORD)
        self.selenium.get(self.live_server_url + "/dashboard/")
        self.assertIn("Dashboard", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Dashboard", header_title.title())

        # He clicks the user dropdown to show the logout button
        user_dropdown = self.selenium.find_element_by_id("user-dropdown")
        user_dropdown.click()

        # And then clicks the logout button itself
        logout_button = self.selenium.find_element_by_link_text("Logout")
        logout_button.click()

        # He is then redirected to the login page with a message stating that he has been indeed logged out of the system.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/login/")
        self.assertIn("Login", self.selenium.title)
        header_title = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Login", header_title.title())
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have been logged out. See you soon!", body_text)

        # Satisfied, he went to bed.

    def test_cannot_access_the_dashboard_when_not_logged_in(self):
        # Shawn had a long day and would like to check up what's new in the Aeternae dashboard.
        account = self.make_account(email="shawn.smith@example.com", first_name="Shawn", last_name="Smith")

        # He remembered the URL and goes to the dashboard page.
        self.selenium.get(self.live_server_url + "/dashboard/")

        # Weirdly enough, he was redirected to the login page.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/login/?next=/dashboard/")

        # "Ooops!", he uttered, as he remembers that he forgot to login to his account.
        # He typed in his credentials and hit the login button.
        email_inputbox = self.selenium.find_element_by_id("email")
        email_inputbox.send_keys(account.email)
        password_inputbox = self.selenium.find_element_by_id("password")
        password_inputbox.send_keys(self.DEFAULT_PASSWORD)
        submit_button = self.selenium.find_element_by_css_selector("input[type=submit]")
        submit_button.click()

        # The page now redirects to the dashboard home, and he was greeted by the familiar friendly message.
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("It's great to have you back, Shawn!", body_text)

        # Satisfied, he went to bed.

    def test_logged_in_users_cannot_access_the_login_page(self):
        # Lorraine had been working inside the Aeternae dashboard for a while now.
        account = self.make_account(email="lorraine.jones@example.com", first_name="Lorraine", last_name="Jones")
        self.login(username=account.email, password=self.DEFAULT_PASSWORD)

        # After a few hours away from the computer, she went on and try to log in to her account.
        self.selenium.get(self.live_server_url + "/login/")

        # "Huh, that's weird", she thought as the page is redirected to the dashboard.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")

        # "Oh, right! I'm already logged in!", she realized. After a while, she finished her work and logged out.
        self.logout()

        # She's sent off by a message confirming she is indeed logged out of the system.
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have been logged out. See you soon!", body_text)

        # Satisfied, she went to bed.

    def test_logged_in_users_cannot_access_the_registration_page(self):
        # Marshall was checking something in the Aeternae dashboard, and had just went out for lunch.
        account = self.make_account(email="marshall.anthony@example.com", first_name="Marshall", last_name="Anthony")
        self.login(username=account.email, password=self.DEFAULT_PASSWORD)

        # Coming back to his desk, he thought of an idea that requires a new account.
        # He goes to the registration page to create one for himself.
        self.selenium.get(self.live_server_url + "/register/")

        # He's surprised that his browser redirects to the dashboard.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")

        # "Oh, right! I'm already logged in!", he realized. He postponed his idea for tomorrow.
        # After a while, he finished his work and logged out.
        self.logout()

        # He's sent off by a message confirming he is indeed logged out of the system.
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have been logged out. See you soon!", body_text)

        # Satisfied, she went to bed.

    def test_logged_in_users_cannot_access_the_landing_page(self):
        # Natalie was just done working on something in the Aeternae dashboard, so he took a quick coffee break.
        account = self.make_account(email="natalie.davis@example.com", first_name="Natalie", last_name="Davis")
        self.login(username=account.email, password=self.DEFAULT_PASSWORD)

        # Coming back to her station, she keys in the Aeternae root URL on her freshly booted browser
        self.selenium.get(self.live_server_url)

        # What do you know, her browser redirects to the dashboard.
        self.assertEquals(self.selenium.current_url, self.live_server_url + "/dashboard/")

        # It all makes sense because she's already logged in. She logged out at the end of the day.
        self.logout()

        # She's sent off by a message confirming she is indeed logged out of the system.
        body_text = self.selenium.find_element_by_tag_name("body").text
        self.assertIn("You have been logged out. See you soon!", body_text)

        # Satisfied, she went to bed.
