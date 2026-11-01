from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import config
from .base_page import BasePage


class AccountPage(BasePage):
    """My Account page and the Account Logout page."""
    url = config.URL_ACCOUNT

    RIGHT_COLUMN_LOGOUT = (By.CSS_SELECTOR, "#column-right a[href*='account/logout']")
    HEADER_LOGOUT = (By.CSS_SELECTOR, "#top-links .dropdown-menu a[href*='account/logout']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "#content .buttons a")

    def logout_from_header(self):
        self.open_my_account_menu()
        self.wait.until(EC.element_to_be_clickable(self.HEADER_LOGOUT)).click()

    def logout_from_right_column(self):
        self.wait.until(EC.element_to_be_clickable(self.RIGHT_COLUMN_LOGOUT)).click()

    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON)).click()
