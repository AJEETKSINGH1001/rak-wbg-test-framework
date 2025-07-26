import pytest
from pages.DashboardPage import DashboardPage
from utils.config import Config

@pytest.mark.smoke
@pytest.mark.usefixtures("page")
def test_dashboard_logo_visible(page):
    dashboard = DashboardPage(page)
    dashboard.visit(Config.BASE_URL)
    dashboard.login(Config.TEST_EMAIL, Config.PASSWORD)
    assert dashboard.is_logo_visible(), "RAKtrack logo not visible."


def test_sidebar_menu_items(page):
    dashboard = DashboardPage(page)
    assert dashboard.verify_sidebar_items(["Dashboard", "ARM", "Pipeline", "Portfolio", "Task Board", "Account Planning", "Companies", "Threads"]), "Sidebar items missing or incorrect."


def test_welcome_message(page):
    dashboard = DashboardPage(page)
    assert dashboard.is_welcome_message_present(), "Welcome message with username not found."


def test_dashboard_cards_present(page):
    dashboard = DashboardPage(page)
    cards = ["Past Dues", "DBR", "Balance Sheet", "MIR", "Pipeline Snapshot", "Portfolio Summary", "Profitability", "Liquidity", "Receivables", "Payables", "Escrow", "Corporate Cards"]
    assert dashboard.verify_dashboard_cards(cards), "One or more dashboard cards are missing."


def test_view_details_navigation(page):
    dashboard = DashboardPage(page)
    assert dashboard.click_view_details("Past Dues"), "Failed to navigate from 'View Details' of Past Dues."


def test_sidebar_navigation_to_arm(page):
    dashboard = DashboardPage(page)
    assert dashboard.navigate_to_sidebar_item("ARM"), "Sidebar navigation to ARM failed."


def test_pipeline_snapshot_totals(page):
    dashboard = DashboardPage(page)
    funded, non_funded, total = dashboard.get_pipeline_totals()
    assert funded + non_funded == total, "Pipeline Snapshot totals mismatch."


def test_currency_format_in_balance_sheet(page):
    dashboard = DashboardPage(page)
    assert dashboard.validate_currency_format("Profitability"), "Currency format in Profitability card is incorrect."


def test_card_data_display(page):
    dashboard = DashboardPage(page)
    assert dashboard.validate_card_data("Receivables", {"Total Receivables (AED)": 1500, "Total Transactions": 2}), "Receivables card data incorrect."


def test_trends_button_functionality(page):
    dashboard = DashboardPage(page)
    assert dashboard.click_show_trends("Liquidity"), "Show Trends button on Liquidity card failed."


def test_dashboard_access_control(page):
    dashboard = DashboardPage(page)
    dashboard.logout()
    dashboard.visit(Config.BASE_URL + "/dashboard")
    assert dashboard.is_redirected_to_login(), "Unauthenticated user accessed dashboard."


def test_no_data_card_handling(page):
    dashboard = DashboardPage(page)
    assert dashboard.handle_empty_state("Assets Value"), "Empty state not handled for zero data scenario."
