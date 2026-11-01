from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import config
from .base_page import BasePage


class RegisterPage(BasePage):
    url = config.URL_REGISTER
    form_action = "account/register"

    def fill(self, first="Test", last="User", email="", phone="0412345678",
             password=config.VALID_PASSWORD, confirm=None):
        self.type("input-firstname", first)
        self.type("input-lastname", last)
        self.type("input-email", email)
        self.type("input-telephone", phone)
        self.type("input-password", password)
        self.type("input-confirm", password if confirm is None else confirm)

    def agree_privacy(self, agree=True):
        box = self.wait.until(EC.element_to_be_clickable((By.NAME, "agree")))  # no id on this site
        if box.is_selected() != agree:
            box.click()

    def register(self, email, **kwargs):
        # The demo site sometimes jumps to the home page right after the first page load,
        # so the form disappears while it is being filled. Retry the whole form once.
        for attempt in range(2):
            try:
                self.open()
                self.fill(email=email, **kwargs)
                self.agree_privacy(True)
                self.submit()
                return
            except TimeoutException:
                if attempt == 1:
                    raise

    def submit_empty_form(self):
        for attempt in range(2):
            try:
                self.open()
                self.submit()
                return
            except TimeoutException:
                if attempt == 1:
                    raise

    def wait_for_success(self):
        self.wait_for_url("account/success")
