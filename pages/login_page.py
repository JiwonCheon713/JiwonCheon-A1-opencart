import config
from .base_page import BasePage


class LoginPage(BasePage):
    url = config.URL_LOGIN
    form_action = "account/login"

    def login(self, email, password):
        self.open()
        self.type("input-email", email)
        self.type("input-password", password)
        self.submit()
