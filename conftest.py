import base64
import os
import re

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import config
import shared_state
from pages import LoginPage, RegisterPage, unique_email


def save_page_screenshot(drv, path, max_height=1400):
    """Capture the page from the top, beyond the visible window (up to max_height CSS px),
    so messages lower on the page (e.g. the Password error) are not cut off."""
    try:
        size = drv.execute_cdp_cmd("Page.getLayoutMetrics", {})["cssContentSize"]
        clip = {"x": 0, "y": 0, "width": size["width"], "height": min(size["height"], max_height), "scale": 1}
        shot = drv.execute_cdp_cmd("Page.captureScreenshot",
                                   {"format": "png", "captureBeyondViewport": True, "clip": clip})
        with open(path, "wb") as f:
            f.write(base64.b64decode(shot["data"]))
    except Exception:
        drv.save_screenshot(path)  # fallback: visible window only


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + call.when, outcome.get_result())


@pytest.fixture
def driver(request):
    """A fresh Chrome session per scenario; saves an evidence screenshot at the end."""
    opts = webdriver.ChromeOptions()
    opts.add_argument("--window-size=1366,900")
    # The demo site's HTTPS certificate is sometimes rejected (NET::ERR_CERT_AUTHORITY_INVALID).
    # Accept it so the certificate warning page does not block the functional tests.
    opts.accept_insecure_certs = True
    if config.HEADLESS:
        opts.add_argument("--headless=new")
    drv = webdriver.Chrome(options=opts)  # Selenium Manager fetches the driver
    yield drv
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    rep = getattr(request.node, "rep_call", None)
    status = "FAIL" if (rep is None or rep.failed) else "PASS"
    name = re.sub(r"[^A-Za-z0-9_]+", "_", request.node.name)
    save_page_screenshot(drv, os.path.join(config.SCREENSHOT_DIR, f"{name}_{status}.png"))
    drv.quit()


@pytest.fixture
def registered_account(driver):
    """Account created by TC01-S1; if TC01 did not run, register one now (then log out)."""
    if "email" not in shared_state.ACCOUNT:
        email = unique_email()
        page = RegisterPage(driver)
        page.register(email)
        page.wait_for_success()
        shared_state.ACCOUNT.update(email=email, password=config.VALID_PASSWORD)
        driver.get(config.URL_LOGOUT)
    return dict(shared_state.ACCOUNT)


@pytest.fixture
def logged_in(driver, registered_account):
    """Precondition for TC03: the registered user is logged in and on My Account."""
    page = LoginPage(driver)
    for attempt in range(2):
        try:
            page.login(registered_account["email"], registered_account["password"])
            page.wait_for_url("account/account")
            return registered_account
        except TimeoutException:
            # The demo site sometimes jumps to the home page after login.
            # If the user is in fact logged in, the My Account page opens directly.
            driver.get(config.URL_ACCOUNT)
            if "account/account" in driver.current_url:
                return registered_account
            if attempt == 1:
                raise
