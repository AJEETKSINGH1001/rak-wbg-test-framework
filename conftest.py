import pytest
import os
from dotenv import load_dotenv
import allure
from playwright.sync_api import sync_playwright

# ✅ Load environment variables from .env at the very beginning
load_dotenv()


import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")  # ✅ Use module scope
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


'''@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshot = page.screenshot()
            allure.attach(screenshot, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
'''