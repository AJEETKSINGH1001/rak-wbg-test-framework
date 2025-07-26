from typing import re

from pages.base_page import BasePage

class PortfolioPage(BasePage):
    PAGE_TITLE = "text=Portfolio Summary"
    SEARCH_INPUT = "input[placeholder='Search by Facility Type']"
    DROPDOWN_DEFAULT = "text=WBG Level"
    DROPDOWN_TRIGGER = "div[role='combobox']"
    DROPDOWN_OPTIONS = "div[role='option']"
    TABLE_ROWS = "table tbody tr"
    TOTAL_ROW = "table tbody tr:last-child"
    BACK_BUTTON = "text=Back"
    TABLE_CELL = lambda self, row, col: f"table tbody tr:nth-child({row}) td:nth-child({col})"

    def is_title_displayed(self) -> bool:
        return self.page.is_visible(self.PAGE_TITLE)

    def get_title_text(self) -> str:
        """Returns the visible title text of the Portfolio page."""
        return self.page.locator(self.PAGE_TITLE).text_content().strip()

    def get_table_headers(self) -> list:
        headers = self.page.locator("table thead tr th")
        return [headers.nth(i).text_content().strip() for i in range(headers.count())]

    def search_facility(self, text: str):
        self.page.fill(self.SEARCH_INPUT, text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(1000)

    def is_no_data_displayed(self) -> bool:
        """Checks if 'No data' message or empty table is shown when no search results found."""
        try:
            # Adjust selector if your UI shows a specific 'no results' message.
            empty_row_selector = "table tr:has(td:has-text('No data'))"
            return self.page.is_visible(empty_row_selector)
        except:
            # Fallback: check if there are zero data rows
            rows = self.page.locator("table tbody tr")
            return rows.count() == 0

    def is_facility_displayed(self, name: str) -> bool:
        selector = f"table tr:has(td:has-text('{name}'))"
        return self.page.is_visible(selector)

    def no_facility_result_displayed(self) -> bool:
        return self.page.locator("table tr:has(td:has-text('No data'))").is_visible()

    def get_dropdown_value(self) -> str:
        return self.page.locator(self.DROPDOWN_TRIGGER).text_content().strip()

    def select_dropdown_option(self, option_text: str):
        self.page.locator(self.DROPDOWN_TRIGGER).click()
        self.page.locator(f"{self.DROPDOWN_OPTIONS} >> text={option_text}").click()
        self.page.wait_for_timeout(500)

    def get_cell_value(self, row: int, col: int) -> int:
        text = self.page.locator(self.TABLE_CELL(row, col)).text_content().replace(",", "").strip()
        return int(text) if text and text != "-" else 0

    def verify_row_total(self, row_index: int, funded_col: int, non_funded_col: int, total_col: int) -> bool:
        funded = self.get_cell_value(row_index, funded_col)
        non_funded = self.get_cell_value(row_index, non_funded_col)
        total = self.get_cell_value(row_index, total_col)
        return funded + non_funded == total

    def verify_table_row_totals(self) -> bool:
        rows = self.page.locator(self.TABLE_ROWS)
        for i in range(rows.count() - 1):  # skip total row
            if not self.verify_row_total(i + 1, 2, 3, 4):  # Adjust column index if layout changes
                return False
        return True

    def verify_row_totals(self) -> bool:
        """Checks that each table row's total = funded + non-funded amounts."""
        rows = self.page.locator(self.TABLE_ROWS)
        row_count = rows.count()

        for i in range(row_count - 1):  # Exclude total row
            try:
                funded_text = self.page.locator(self.TABLE_CELL(i + 1, 2)).text_content().replace(",", "").strip()
                non_funded_text = self.page.locator(self.TABLE_CELL(i + 1, 3)).text_content().replace(",", "").strip()
                total_text = self.page.locator(self.TABLE_CELL(i + 1, 4)).text_content().replace(",", "").strip()

                funded = float(funded_text or "0")
                non_funded = float(non_funded_text or "0")
                total = float(total_text or "0")

                if not (funded + non_funded == total):
                    return False
            except Exception:
                return False
        return True

    def verify_column_totals(self) -> bool:
        """Verify that the sum of column values matches the total row values."""
        column_indexes = [2, 3, 4]  # Funded, Non-Funded, Total columns
        rows = self.page.locator(self.TABLE_ROWS)
        row_count = rows.count()

        for col_index in column_indexes:
            try:
                total_cell_selector = self.TABLE_CELL(row_count, col_index)
                total_text = self.page.locator(total_cell_selector).text_content().replace(",", "").strip()
                expected_total = float(total_text or "0")

                actual_sum = 0.0
                for row in range(1, row_count):  # Exclude total row
                    cell_selector = self.TABLE_CELL(row, col_index)
                    cell_text = self.page.locator(cell_selector).text_content().replace(",", "").strip()
                    actual_sum += float(cell_text or "0")

                if round(actual_sum, 2) != round(expected_total, 2):
                    return False
            except Exception:
                return False

        return True

    import re

    def validate_number_formatting(self) -> bool:
        """
        Validates that all numeric cells in the portfolio table follow correct formatting:
        - Commas for thousands (e.g., 1,000 or 100,000)
        - Optional decimal places
        """
        number_format_pattern = re.compile(r"^\d{1,3}(,\d{3})*(\.\d{1,2})?$")

        rows = self.page.locator(self.TABLE_ROWS)
        row_count = rows.count()

        for row_index in range(1, row_count + 1):  # Including total row
            for col_index in range(2, 5):  # Columns: Funded, Non-Funded, Total
                cell_selector = self.TABLE_CELL(row_index, col_index)
                cell_text = self.page.locator(cell_selector).text_content().strip()

                # Skip empty or non-numeric cells if needed
                if not cell_text or not cell_text[0].isdigit():
                    continue

                # Remove currency symbols if applicable (e.g., $)
                clean_text = re.sub(r"[^\d.,]", "", cell_text)

                if not number_format_pattern.match(clean_text):
                    return False

        return True

    def is_number_formatting_correct(self) -> bool:
        import re
        rows = self.page.locator(self.TABLE_ROWS)
        for i in range(rows.count()):
            cols = rows.nth(i).locator("td")
            for j in range(cols.count()):
                text = cols.nth(j).text_content().strip()
                if text and text != "-" and not re.match(r'^(\d{1,3}(,\d{3})*|\d+)$', text):
                    return False
        return True

    def click_back(self):
        self.page.click(self.BACK_BUTTON)
        self.page.wait_for_timeout(1000)

    def is_navigated_back(self) -> bool:
        return "dashboard" in self.page.url or "home" in self.page.url

    def set_viewport(self, mode: str = "mobile"):
        sizes = {
            "mobile": (375, 667),
            "tablet": (768, 1024),
            "desktop": (1440, 900)
        }
        width, height = sizes.get(mode, sizes["mobile"])
        self.page.context.set_viewport_size({"width": width, "height": height})

    def is_layout_responsive(self) -> bool:
        self.set_viewport("mobile")
        return self.page.is_visible("table")  # fallback check for visible table

    def test_keyboard_navigation(self) -> bool:
        self.page.keyboard.press("Tab")
        return self.page.evaluate("document.activeElement !== document.body")

    def verify_aria_labels(self) -> bool:
        elements = self.page.locator("[aria-label]")
        return elements.count() > 0

    def check_sql_injection_result(self, query: str) -> bool:
        self.search_facility(query)
        return self.no_facility_result_displayed()

    def handle_invalid_dropdown_input(self) -> bool:
        try:
            self.select_dropdown_option("Invalid Option Text")
            return True  # It didn't break
        except:
            return False

    def logout(self):
        """Logs out the user by clicking the logout button (adjust selector as needed)."""
        self.page.click("text=Logout")  # Update selector if different
        self.page.wait_for_load_state("networkidle")  # Wait for the page to settle

    def is_redirected_to_login(self) -> bool:
        """Checks if the current page is the login page based on URL or login form."""
        return "login" in self.page.url or self.page.is_visible("input#login_email")


