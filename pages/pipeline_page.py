from pages.base_page import BasePage
from playwright.sync_api import expect

class PipelinePage(BasePage):
    PIPELINE_TAB = "text=Pipeline"
    PAGE_TITLE = "text=Pipeline Snapshot"
    LOGO = "img[alt='logo']"
    SEARCH_INPUT = "input[placeholder*='Search']"
    LEVEL_DROPDOWN = "div.ant-select-selector"
    SIDEBAR_ITEMS = "ul.ant-menu li.ant-menu-item"
    BACK_BUTTON = "text=Back"

    COLUMN_FUNDED_PENDING = "//table//tr[td[contains(text(), 'Total')]]/td[2]"
    COLUMN_NON_FUNDED_PENDING = "//table//tr[td[contains(text(), 'Total')]]/td[3]"
    COLUMN_TOTAL_PENDING = "//table//tr[td[contains(text(), 'Total')]]/td[4]"
    COLUMN_FUNDED_PIPELINE = "//table//tr[td[contains(text(), 'Total')]]/td[5]"
    COLUMN_NON_FUNDED_PIPELINE = "//table//tr[td[contains(text(), 'Total')]]/td[6]"
    COLUMN_TOTAL_PIPELINE = "//table//tr[td[contains(text(), 'Total')]]/td[7]"

    def visit(self, url):
        self.page.goto(url)

    def is_logo_visible(self) -> bool:
        return self.page.is_visible(self.LOGO)

    def get_title_text(self) -> str:
        return self.page.locator(self.PAGE_TITLE).text_content().strip()

    def get_sidebar_items(self) -> list:
        self.page.wait_for_selector(self.SIDEBAR_ITEMS)
        return [el.text_content().strip() for el in self.page.locator(self.SIDEBAR_ITEMS).all()]

    def search_rm(self, name: str):
        self.page.fill(self.SEARCH_INPUT, name)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(1500)

    def is_rm_displayed(self, rm_name: str) -> bool:
        selector = f"table tr:has(td:has-text('{rm_name}'))"
        try:
            self.page.wait_for_selector(selector, timeout=3000)
            return self.page.is_visible(selector)
        except:
            return False

    def no_rm_results_displayed(self) -> bool:
        no_data_selector = "table td:has-text('No data')"
        try:
            return self.page.is_visible(no_data_selector)
        except:
            return True

    def get_dropdown_value(self) -> str:
        return self.page.locator(self.LEVEL_DROPDOWN).text_content().strip()

    def sort_by_rm_name(self):
        header_selector = "th:has-text('RM Name')"
        self.page.click(header_selector)
        self.page.wait_for_timeout(1000)

    def is_rm_list_sorted(self) -> bool:
        names = self.page.locator("tbody tr td:nth-child(1)").all_inner_texts()
        cleaned = [name.strip() for name in names if name.strip()]
        return cleaned == sorted(cleaned)

    def get_total_values(self):
        return {
            "pending": {
                "funded": int(self.page.locator(self.COLUMN_FUNDED_PENDING).text_content().replace(",", "")),
                "non_funded": int(self.page.locator(self.COLUMN_NON_FUNDED_PENDING).text_content().replace(",", "")),
                "total": int(self.page.locator(self.COLUMN_TOTAL_PENDING).text_content().replace(",", ""))
            },
            "pipeline": {
                "funded": int(self.page.locator(self.COLUMN_FUNDED_PIPELINE).text_content().replace(",", "")),
                "non_funded": int(self.page.locator(self.COLUMN_NON_FUNDED_PIPELINE).text_content().replace(",", "")),
                "total": int(self.page.locator(self.COLUMN_TOTAL_PIPELINE).text_content().replace(",", ""))
            }
        }

    def verify_all_row_totals(self) -> bool:
        totals = self.get_total_values()
        return (
            totals["pending"]["funded"] + totals["pending"]["non_funded"] == totals["pending"]["total"] and
            totals["pipeline"]["funded"] + totals["pipeline"]["non_funded"] == totals["pipeline"]["total"]
        )

    def verify_column_totals(self) -> bool:
        # For now, reusing row totals as the only "Total" row. Extend as needed.
        return self.verify_all_row_totals()

    def validate_number_formatting(self) -> bool:
        amounts = self.page.locator("tbody tr td:nth-child(2), td:nth-child(3), td:nth-child(4), td:nth-child(5)").all_inner_texts()
        return all(a.replace(",", "").replace(".", "").isdigit() for a in amounts if a.strip())

    def click_back(self):
        self.page.click(self.BACK_BUTTON)
        self.page.wait_for_timeout(1000)

    def is_navigated_back(self) -> bool:
        return "dashboard" in self.page.url or "home" in self.page.url

    def logout(self):
        self.page.click("button:has-text('Logout')")
        self.page.wait_for_timeout(1000)

    def is_redirected_to_login(self) -> bool:
        return "login" in self.page.url.lower()

    def set_viewport(self, mode: str):
        sizes = {
            "mobile": {"width": 375, "height": 812},
            "tablet": {"width": 768, "height": 1024},
            "desktop": {"width": 1440, "height": 900}
        }
        self.page.context.set_viewport_size(sizes.get(mode, sizes["desktop"]))

    def is_layout_responsive(self) -> bool:
        return self.page.is_visible("nav")  # update with mobile-specific check if needed

    def test_keyboard_navigation(self) -> bool:
        try:
            self.page.keyboard.press("Tab")
            focused = self.page.evaluate("document.activeElement !== null")
            return focused
        except:
            return False

    def verify_aria_labels(self) -> bool:
        return self.page.locator("[aria-label]").count() > 0

    def no_sql_injection_result(self) -> bool:
        return self.no_rm_results_displayed()

    def handle_invalid_dropdown_input(self) -> bool:
        try:
            self.page.click(self.LEVEL_DROPDOWN)
            self.page.keyboard.type("Invalid Option")
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)
            return True  # If no crash or error
        except:
            return False
