import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def unique_email(prefix="tc01tester"):
    """A never-registered e-mail for every run (millisecond timestamp)."""
    return f"{prefix}+{int(time.time() * 1000)}@example.com"


class BasePage:
    url = ""
    form_action = ""  # part of <form action> that identifies this page's form

    MY_ACCOUNT_TOGGLE = (By.CSS_SELECTOR, '#top-links a[title="My Account"]')
    TOP_DROPDOWN_LINKS = (By.CSS_SELECTOR, "#top-links .dropdown-menu a")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.TIMEOUT)

    def open(self):
        """Load the page; retry once if the site redirects elsewhere or loads slowly."""
        route = self.url.split("route=")[-1]
        for attempt in range(2):
            self.driver.get(self.url)
            try:
                WebDriverWait(self.driver, 8).until(EC.url_contains(route))
                self.wait.until(EC.presence_of_element_located((By.ID, "content")))
                return self
            except TimeoutException:
                if attempt == 1:
                    raise
        return self

    def type(self, element_id, value):
        field = self.wait.until(EC.visibility_of_element_located((By.ID, element_id)))
        field.clear()
        field.send_keys(value)

    def submit(self):
        xpath = f"//form[contains(@action,'{self.form_action}')]//input[@type='submit']"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # ---- header "My Account" dropdown ------------------------------------
    def open_my_account_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.MY_ACCOUNT_TOGGLE)).click()
        self.wait.until(EC.visibility_of_any_elements_located(self.TOP_DROPDOWN_LINKS))

    def my_account_menu_items(self):
        self.open_my_account_menu()
        return [a.text.strip() for a in self.driver.find_elements(*self.TOP_DROPDOWN_LINKS) if a.text.strip()]

    # ---- result helpers ---------------------------------------------------
    def page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def alert_text(self, css=".alert-danger"):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css))).text

    def field_errors(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-danger")))
        return [e.text.strip() for e in self.driver.find_elements(By.CSS_SELECTOR, ".text-danger") if e.text.strip()]

    def wait_for_url(self, fragment):
        self.wait.until(EC.url_contains(fragment))
