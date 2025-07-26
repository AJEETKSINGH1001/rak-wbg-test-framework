import pytest
from pages.TaskBoard_page import TaskBoardPage
from pages.login_page import LoginPage
from utils.config import Config

@pytest.mark.smoke
def test_login_success(page):
    """✅ Verify login with valid credentials."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, Config.PASSWORD)
    assert login_page.is_login_successful(), "❌ Login failed — dashboard not visible after login."


def test_taskboard_title_visible(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    assert taskboard.get_title_text() == "Task Board", "❌ Task Board title is not visible."


def test_add_new_task(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    task_title = "Test Task"
    taskboard.add_task_to_column(0, task_title)  # Index 0 = TO-DO
    assert taskboard.is_task_present(task_title), "❌ Task not added to To-Do column."


def test_move_task_between_columns(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    task_title = "Test Task"
    taskboard.move_task_card(task_title, "In Progress")
    assert taskboard.is_task_present(task_title), "❌ Task not moved to In Progress column."


def test_column_task_count(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    count = taskboard.get_column_task_count("To-Do")
    assert isinstance(count, int) and count >= 0, "❌ Invalid task count for To-Do column."


def test_task_due_date_displayed(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    due_date = taskboard.get_task_date("TASK 1")
    assert due_date == "Jul 23", "❌ Incorrect or missing due date for TASK 1."


def test_task_assignees_displayed(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    assignees = taskboard.get_task_assignees("First Task")
    assert "RA" in assignees and "MC" in assignees, "❌ Missing assignees on task card."


def test_task_card_edit_functionality(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    original_title = "EditMe"
    updated_title = "EditedTask"
    taskboard.add_task_to_column(0, original_title)
    taskboard.edit_task_card(original_title, updated_title)
    assert taskboard.is_task_present(updated_title), "❌ Task not updated after edit."


def test_task_card_delete(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    task_title = "DeleteMe"
    taskboard.add_task_to_column(0, task_title)
    taskboard.delete_task_card(task_title)
    assert not taskboard.is_task_present(task_title), "❌ Task not deleted successfully."


def test_goto_mir_navigation(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    taskboard.click_goto_mir()
    assert "mir" in page.url, "❌ Goto MIR button did not redirect correctly."


def test_goto_past_dues_navigation(page):
    taskboard = TaskBoardPage(page)
    taskboard.visit(Config.TASKBOARD_URL)
    taskboard.click_goto_past_dues()
    assert "pastdues" in page.url, "❌ Goto Past Dues button did not redirect correctly."
