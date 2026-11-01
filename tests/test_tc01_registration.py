"""TC01 - F01 User Registration
https://opencart.abstracta.us/index.php?route=account/register"""
import pytest

import config
import shared_state
from pages import RegisterPage, unique_email

pytestmark = pytest.mark.tc01


def test_tc01_s1_register_with_valid_details(driver):
    email = unique_email()
    page = RegisterPage(driver)
    page.register(email)
    page.wait_for_success()
    assert "Congratulations! Your new account has been successfully created!" in page.page_text()
    assert "Logout" in page.my_account_menu_items()      # user is logged in
    shared_state.ACCOUNT.update(email=email, password=config.VALID_PASSWORD)


def test_tc01_s2_register_with_existing_email(driver, registered_account):
    page = RegisterPage(driver)
    page.register(registered_account["email"])
    assert "Warning: E-Mail Address is already registered!" in page.alert_text()
    assert "account/success" not in driver.current_url


def test_tc01_s3_submit_empty_form(driver):
    page = RegisterPage(driver)
    page.submit_empty_form()  # nothing filled in, Privacy Policy not ticked
    assert "Warning: You must agree to the Privacy Policy!" in page.alert_text()
    errors = page.field_errors()
    for expected in [
        "First Name must be between 1 and 32 characters!",
        "Last Name must be between 1 and 32 characters!",
        "E-Mail Address does not appear to be valid!",
        "Telephone must be between 3 and 32 characters!",
        "Password must be between 4 and 20 characters!",
    ]:
        assert expected in errors
    assert "account/register" in driver.current_url
