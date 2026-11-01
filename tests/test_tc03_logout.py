"""TC03 - F03 User Logout
https://opencart.abstracta.us/index.php?route=account/logout
Precondition: the user is logged in (fixture `logged_in`, depends on TC01/TC02)."""
import pytest

import config
from pages import AccountPage

pytestmark = pytest.mark.tc03
LOGGED_OFF = "You have been logged off your account."


def test_tc03_s1_logout_from_header_menu(driver, logged_in):
    page = AccountPage(driver)
    page.logout_from_header()
    page.wait_for_url("account/logout")
    assert LOGGED_OFF in page.page_text()
    items = page.my_account_menu_items()
    assert "Login" in items and "Logout" not in items


def test_tc03_s2_account_page_blocked_after_logout(driver, logged_in):
    page = AccountPage(driver)
    page.logout_from_header()
    page.wait_for_url("account/logout")
    driver.get(config.URL_ACCOUNT)          # protected page
    page.wait_for_url("account/login")       # redirected to the login page
    assert "Returning Customer" in page.page_text()


def test_tc03_s3_logout_from_right_column_then_continue(driver, logged_in):
    page = AccountPage(driver)
    page.logout_from_right_column()
    page.wait_for_url("account/logout")
    assert LOGGED_OFF in page.page_text()
    page.click_continue()
    page.wait_for_url("common/home")
    assert "Login" in page.my_account_menu_items()
