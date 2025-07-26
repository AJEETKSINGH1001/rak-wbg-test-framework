from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = '#login_email'
    PASSWORD_INPUT = '#login_password'
    LOGIN_BUTTON = 'button[type="submit"]'

    def login(self, username: str, password: str):
        self.page.wait_for_selector(self.USERNAME_INPUT)
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()

    def is_login_successful(self) -> bool:
        try:
            # Adjust this selector to something visible on dashboard after login
            self.page.wait_for_selector("text=Hi! Martin Clarke", timeout=5000)
            return True
        except Exception:
            return False
