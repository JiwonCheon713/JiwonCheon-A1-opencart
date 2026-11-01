"""Shared configuration for TC01-TC03."""
import os

BASE_URL = "https://opencart.abstracta.us/index.php"
URL_HOME = f"{BASE_URL}?route=common/home"
URL_REGISTER = f"{BASE_URL}?route=account/register"
URL_LOGIN = f"{BASE_URL}?route=account/login"
URL_ACCOUNT = f"{BASE_URL}?route=account/account"
URL_LOGOUT = f"{BASE_URL}?route=account/logout"

VALID_PASSWORD = "Test@12345"   # site rule: 4-20 characters
TIMEOUT = 20                    # seconds for explicit waits (the demo site can be slow)
HEADLESS = os.getenv("HEADLESS", "0") == "1"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
