"""TC02 - F02 User Login
https://opencart.abstracta.us/index.php?route=account/login
Precondition: an account registered in TC01 (fixture `registered_account`)."""
import pytest

import config
from pages import LoginPage, unique_email

pytestmark = pytest.mark.tc02
NO_MATCH = "Warning: No match for E-Mail Address and/or Password."


def test_tc02_s1_login_with_valid_credentials(driver, registered_account):
    page = LoginPage(driver)
    page.login(registered_account["email"], registered_account["password"])
    page.wait_for_url("account/account")
    assert "My Account" in page.page_text()
    assert "Logout" in page.my_account_menu_items()


def test_tc02_s2_login_with_wrong_password(driver, registered_account):
    page = LoginPage(driver)
    page.login(registered_account["email"], "WrongPass#999")
    assert NO_MATCH in page.alert_text()
    assert "account/login" in driver.current_url


def test_tc02_s3_login_with_unregistered_email(driver):
    page = LoginPage(driver)
    page.login(unique_email("nobody"), config.VALID_PASSWORD)
    assert NO_MATCH in page.alert_text()
    assert "account/login" in driver.current_url
