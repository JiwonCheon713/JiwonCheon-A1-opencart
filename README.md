# EST Assignment 3 – System Testing (Student 1: TC01–TC03)

Automated system tests for the OpenCart demo store **https://opencart.abstracta.us/**, written in **Python + Selenium WebDriver + pytest**.

| Test case | Function | Scenarios | Test file |
|---|---|---|---|
| TC01 | F1 User Registration | valid registration · existing e-mail rejected · empty form validation | `tests/test_tc01_registration.py` |
| TC02 | F2 User Login | valid login · wrong password · unregistered e-mail | `tests/test_tc02_login.py` |
| TC03 | F3 User Logout | logout from header menu · My Account blocked after logout · logout from right column + Continue | `tests/test_tc03_logout.py` |

Result of the final run: **9 passed, 0 failed, 0 errors** (evidence in `screenshots/`).

## Environment
- macOS (Apple silicon, Arm64), Google Chrome 156
- Python 3.13.7, Selenium 4.51.0, pytest 9.2.0
- VS Code with the Python extension

## Project structure
```
config.py          URLs, timeouts, test password
conftest.py        Chrome driver fixture (fresh session per scenario), full-page screenshot,
                   shared registered-account and logged-in fixtures
shared_state.py    account created in TC01, reused by TC02 / TC03
pages/             page objects (BasePage, RegisterPage, LoginPage, AccountPage) – all locators live here
tests/             one file per test case (pytest markers tc01, tc02, tc03)
screenshots/       PASS/FAIL screenshot saved automatically for every scenario
```

## Setup and run
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # ChromeDriver is downloaded automatically by Selenium Manager

pytest -v                          # all 9 scenarios (TC01 -> TC02 -> TC03)
pytest -v -m tc01                  # one test case
HEADLESS=1 pytest -v               # without opening a browser window
```

## Notes
- Every run registers a **new account** with a timestamped e-mail (`tc01tester+<timestamp>@example.com`); TC01-S2, TC02 and TC03 reuse it, or register one themselves when run alone.
- The demo site is occasionally unstable (certificate warning `NET::ERR_CERT_AUTHORITY_INVALID`, unexpected redirects to the home page). Chrome is therefore started with `acceptInsecureCerts`, and page loads, form submission and login are retried once.
