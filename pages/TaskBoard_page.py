from pages.base_page import BasePage
from playwright.sync_api import TimeoutError

class TaskBoardPage(BasePage):
    PAGE_TITLE = "text=Task Board"
    LOGIN_EMAIL = "input[placeholder='* Email or User ID']"
    LOGIN_PASSWORD = "input[placeholder='* Password']"
    LOGIN_BUTTON = "button:has-text('Login')"
    ADD_BUTTONS = "button:has-text('plus')"
    SAVE_BUTTON = "button:has-text('Save')"
    CARD_TITLE_INPUT = "input[placeholder='* Title']"
    TASK_BOARD_LINK = "role=link[name='Task Board']"
    GOTO_MIR_BUTTON = "role=button[name='Goto Mir']"
    GOTO_PAST_DUES_BUTTON = "role=button[name='Goto Past Dues']"
    SUCCESS_TOAST = "text=Successfully created task"
    CLOSE_BUTTON = "role=button[name='Close']"

    def get_title_text(self) -> str:
        return self.page.locator(self.PAGE_TITLE).text_content().strip()

    def login(self, email: str, password: str):
        self.page.fill(self.LOGIN_EMAIL, email)
        self.page.fill(self.LOGIN_PASSWORD, password)
        self.page.click(self.LOGIN_BUTTON)

    def visit_taskboard(self):
        self.page.click("role=link[name='Task Board']")
        self.page.wait_for_selector(self.PAGE_TITLE)

    def add_task_to_column(self, column_index: int, task_title: str):
        self.page.get_by_role("button", name="plus", exact=True).nth(column_index).click()
        self.page.wait_for_selector(self.CARD_TITLE_INPUT)
        self.page.fill(self.CARD_TITLE_INPUT, task_title)
        self.page.click(self.SAVE_BUTTON)
        self.page.wait_for_selector(self.SUCCESS_TOAST)

    def is_task_present(self, title: str) -> bool:
        try:
            return self.page.locator(f"text={title}").is_visible()
        except TimeoutError:
            return False

    def move_task_card(self, task_title: str, target_column: str):
        source = self.page.locator(f".task-card:has-text('{task_title}')")
        target = self.page.locator(f"text={target_column}").first()
        source.drag_to(target)
        self.page.wait_for_timeout(1000)

    def get_column_task_count(self, column_title: str) -> int:
        badge_locator = self.page.locator(f"text={column_title} >> xpath=../..//span[contains(@class, 'badge')]")
        badge_text = badge_locator.inner_text().strip()
        return int(badge_text) if badge_text.isdigit() else 0

    def get_task_date(self, task_title: str) -> str:
        return self.page.locator(f".task-card:has-text('{task_title}') .date-label").inner_text().strip()

    def get_task_assignees(self, task_title: str) -> list:
        tags = self.page.locator(f".task-card:has-text('{task_title}') .user-tag")
        return [tags.nth(i).inner_text().strip() for i in range(tags.count())]

    def edit_task_card(self, old_title: str, new_title: str):
        self.page.locator(f".task-card:has-text('{old_title}') button[aria-label='more']").click()
        self.page.click("text=Edit")
        self.page.fill(self.CARD_TITLE_INPUT, new_title)
        self.page.click(self.SAVE_BUTTON)
        self.page.wait_for_selector(f"text={new_title}")

    def delete_task_card(self, title: str):
        self.page.locator(f".task-card:has-text('{title}') button[aria-label='more']").click()
        self.page.click("text=Delete")
        self.page.wait_for_timeout(500)

    def view_task_card(self, task_name: str):
        self.page.get_by_role("button", name=task_name).click()
        self.page.get_by_text("View card").click()
        self.page.get_by_label(task_name).click()
        self.page.locator(self.CLOSE_BUTTON).click()

    def click_goto_mir(self):
        self.page.get_by_role("button", name="Goto Mir").click()

    def click_goto_past_dues(self):
        self.page.get_by_role("button", name="Goto Past Dues").click()

    def go_back(self):
        self.page.get_by_text("Back").click()
