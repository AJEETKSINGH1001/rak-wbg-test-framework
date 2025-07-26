# pages/dashboard_page.py

from pages.base_page import BasePage
from playwright.sync_api import expect

class DashboardPage(BasePage):
    LOGO_SELECTOR = "img[alt='logo']"
    SIDEBAR_SELECTOR = "ul.ant-menu li.ant-menu-item a >> text={}"
    WELCOME_SELECTOR = "text=Hi! Martin Clarke"
    CARD_TITLES_SELECTOR = "div.card-header >> text={}"
    VIEW_DETAILS_BUTTON_SELECTOR = "div.card-header:has-text('{}') >> text=View Details"
    SHOW_TRENDS_BUTTON_SELECTOR = "div.card:has-text('{}') >> text=Show Trends"
    CURRENCY_CARD_SELECTOR = "div.card:has-text('{}')"
    DATA_LABEL_SELECTOR = "div.card:has-text('{}') >> text={}"
    LOGOUT_BUTTON_SELECTOR = "button:has-text('Logout')"
    LOGIN_PAGE_INDICATOR = "#login_email"

    def login(self, username: str, password: str):
        self.page.fill("#login_email", username)
        self.page.fill("#login_password", password)
        self.page.click("button[type='submit']")
        self.page.wait_for_selector(self.WELCOME_SELECTOR)

    def is_logo_visible(self) -> bool:
        return self.page.is_visible(self.LOGO_SELECTOR)

    def verify_sidebar_items(self, expected_items: list) -> bool:
        sidebar_text = self.page.locator("nav").all_text_contents()
        return all(any(item in line for line in sidebar_text) for item in expected_items)

    def is_welcome_message_present(self) -> bool:
        return self.page.is_visible(self.WELCOME_SELECTOR)

    def verify_dashboard_cards(self, cards: list) -> bool:
        for card in cards:
            if not self.page.is_visible(f"text={card}"):
                return False
        return True

    def click_view_details(self, card_title: str) -> bool:
        try:
            self.page.click(self.VIEW_DETAILS_BUTTON_SELECTOR.format(card_title))
            self.page.wait_for_load_state("networkidle")
            return True
        except:
            return False

    def navigate_to_sidebar_item(self, item: str) -> bool:
        try:
            self.page.click(self.SIDEBAR_SELECTOR.format(item))
            self.page.wait_for_load_state("networkidle")
            return True
        except:
            return False

    def get_pipeline_totals(self):
        try:
            funded = int(self.page.locator("text=Pipeline").locator("xpath=..").locator("text=Funded").nth(0).evaluate("e => e.nextSibling.textContent"))
            non_funded = int(self.page.locator("text=Pipeline").locator("xpath=..").locator("text=Non-Funded").nth(0).evaluate("e => e.nextSibling.textContent"))
            total = int(self.page.locator("text=Pipeline").locator("xpath=..").locator("text=Total").nth(0).evaluate("e => e.nextSibling.textContent"))
            return funded, non_funded, total
        except:
            return 0, 0, 0

    def validate_currency_format(self, card_title: str) -> bool:
        amounts = self.page.locator(self.CURRENCY_CARD_SELECTOR.format(card_title)).locator("text=AED").all_inner_texts()
        return all(amount.strip().startswith("AED") for amount in amounts)

    def validate_card_data(self, card_title: str, expected_data: dict) -> bool:
        card = self.page.locator(self.CURRENCY_CARD_SELECTOR.format(card_title))
        for label, value in expected_data.items():
            if not card.locator(f"text={label}").is_visible():
                return False
            actual_text = card.locator(f"text={label}").evaluate("e => e.nextSibling?.textContent || ''").strip()
            if str(value) not in actual_text:
                return False
        return True

    def click_show_trends(self, card_title: str) -> bool:
        try:
            self.page.click(self.SHOW_TRENDS_BUTTON_SELECTOR.format(card_title))
            self.page.wait_for_timeout(1000)
            return True
        except:
            return False

    def logout(self):
        if self.page.is_visible(self.LOGOUT_BUTTON_SELECTOR):
            self.page.click(self.LOGOUT_BUTTON_SELECTOR)
            self.page.wait_for_selector(self.LOGIN_PAGE_INDICATOR)

    def is_redirected_to_login(self) -> bool:
        return self.page.url.endswith("/login")

    def handle_empty_state(self, label_text: str) -> bool:
        try:
            label = self.page.locator(f"text={label_text}")
            value = label.evaluate("e => e.nextSibling?.textContent || ''").strip()
            return value in ["AED 0", "0"]
        except:
            return False
