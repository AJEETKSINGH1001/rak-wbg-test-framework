import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.config import Config


def run_test_with_browser(test_func):
    """Helper to isolate browser session per test."""
    def wrapper():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            test_func(page)
            browser.close()
    return wrapper


@pytest.mark.smoke
@run_test_with_browser
def test_login_success(page):
    """✅ Verify login with valid credentials."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, Config.PASSWORD)
    assert login_page.is_login_successful(), "❌ Login failed — dashboard not visible after login."


@run_test_with_browser
def test_login_invalid_password(page):
    """❌ Login attempt with valid username and wrong password should fail."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, "wrongpassword123")
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with invalid password."


@run_test_with_browser
def test_login_invalid_username(page):
    """❌ Login attempt with invalid username and valid password should fail."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login("invalid_user", Config.PASSWORD)
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with invalid username."


@run_test_with_browser
def test_login_empty_username(page):
    """❌ Login with empty username should fail."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login("", Config.PASSWORD)
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with empty username."


@run_test_with_browser
def test_login_empty_password(page):
    """❌ Login with empty password should fail."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, "")
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with empty password."


@run_test_with_browser
def test_login_empty_credentials(page):
    """❌ Login with empty credentials should fail."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login("", "")
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with empty credentials."


@run_test_with_browser
def test_login_case_sensitivity(page):
    """❌ Verify if username/password is case sensitive."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL.upper(), Config.PASSWORD.upper())
    assert not login_page.is_login_successful(), "⚠️ Login succeeded with uppercase credentials."


@run_test_with_browser
def test_login_sql_injection_attempt(page):
    """❌ Attempt SQL injection via login fields."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login("' OR '1'='1", "' OR '1'='1")
    assert not login_page.is_login_successful(), "⚠️ SQL injection attempt succeeded."

# Optional:
# @run_test_with_browser
# def test_login_locked_account(page):
#     login_page = LoginPage(page)
#     login_page.visit(Config.BASE_URL)
#     login_page.login("locked_user", "somepassword")
#     assert not login_page.is_login_successful(), "⚠️ Login succeeded with a locked account."
