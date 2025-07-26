import pytest

from pages.login_page import LoginPage
from pages.pipeline_page import PipelinePage
from utils.config import Config

@pytest.mark.smoke

def test_login_success(page):
    """✅ Verify login with valid credentials."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, Config.PASSWORD)
    assert login_page.is_login_successful(), "❌ Login failed — dashboard not visible after login."


def test_logo_visibility(page):
    pipeline = PipelinePage(page)
    pipeline.visit(Config.PIPELINE_URL)
    assert pipeline.is_logo_visible(), "Logo not visible on pipeline page."


def test_pipeline_title_present(page):
    pipeline = PipelinePage(page)
    pipeline.visit(Config.PIPELINE_URL)
    assert pipeline.get_title_text() == "Pipeline Snapshot", "Incorrect or missing title."


def test_sidebar_menu_items(page):
    pipeline = PipelinePage(page)
    expected_items = ["Dashboard", "ARM", "Pipeline", "Portfolio", "Task Board", "Account Planning", "Companies", "Threads"]
    assert pipeline.get_sidebar_items() == expected_items, "Sidebar items incorrect or missing."


def test_search_rm_found(page):
    pipeline = PipelinePage(page)
    pipeline.search_rm("Martin")
    assert pipeline.is_rm_displayed("Martin Clarke"), "RM not found after search."


def test_search_rm_not_found(page):
    pipeline = PipelinePage(page)
    pipeline.search_rm("Nonexistent RM")
    assert pipeline.no_rm_results_displayed(), "Unexpected results for nonexistent RM."


def test_dropdown_default_value(page):
    pipeline = PipelinePage(page)
    assert pipeline.get_dropdown_value() == "WBG Level", "Dropdown default value incorrect."


def test_sorting_rm_name(page):
    pipeline = PipelinePage(page)
    pipeline.sort_by_rm_name()
    assert pipeline.is_rm_list_sorted(), "RM names are not sorted correctly."


def test_table_totals_calculation(page):
    pipeline = PipelinePage(page)
    assert pipeline.verify_all_row_totals(), "Row totals do not match funded + non-funded."
    assert pipeline.verify_column_totals(), "Column totals do not match sum of entries."


def test_number_formatting(page):
    pipeline = PipelinePage(page)
    assert pipeline.validate_number_formatting(), "Number formatting is incorrect."


def test_back_button_navigation(page):
    pipeline = PipelinePage(page)
    pipeline.click_back()
    assert pipeline.is_navigated_back(), "Back button did not navigate correctly."


def test_unauthorized_access_redirect(page):
    pipeline = PipelinePage(page)
    pipeline.logout()
    pipeline.visit(Config.PIPELINE_URL)
    assert pipeline.is_redirected_to_login(), "Unauthorized access not redirected to login."


def test_responsive_layout(page):
    pipeline = PipelinePage(page)
    pipeline.set_viewport("mobile")
    assert pipeline.is_layout_responsive(), "Pipeline page is not responsive on mobile view."


def test_keyboard_accessibility(page):
    pipeline = PipelinePage(page)
    assert pipeline.test_keyboard_navigation(), "Page not fully accessible via keyboard."


def test_aria_labels_present(page):
    pipeline = PipelinePage(page)
    assert pipeline.verify_aria_labels(), "ARIA labels missing for accessibility."


def test_pipeline_sql_injection_protection(page):
    pipeline = PipelinePage(page)
    pipeline.search_rm("' OR '1'='1")
    assert pipeline.no_sql_injection_result(), "SQL injection was successful, which should not happen."


def test_pipeline_dropdown_invalid_option(page):
    pipeline = PipelinePage(page)
    assert pipeline.handle_invalid_dropdown_input(), "Dropdown failed to handle invalid value."

# This assumes a PipelinePage class with helper methods for UI interaction and assertions
