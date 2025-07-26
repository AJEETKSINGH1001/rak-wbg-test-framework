import pytest

from pages.login_page import LoginPage
from pages.portfolio_page import PortfolioPage
from utils.config import Config


@pytest.mark.smoke
def test_login_success(page):
    """✅ Verify login with valid credentials."""
    login_page = LoginPage(page)
    login_page.visit(Config.BASE_URL)
    login_page.login(Config.TEST_EMAIL, Config.PASSWORD)
    assert login_page.is_login_successful(), "❌ Login failed — dashboard not visible after login."


def test_portfolio_title_visible(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.get_title_text() == "Portfolio Summary"


def test_portfolio_table_headers_present(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    expected_headers = [
        "Facility Type", "Funded", "Non Funded", "Total",
        "Funded", "Non Funded", "Total",
        "Funded", "Non Funded", "Total",
        "Existing/New", "Funded"
    ]
    assert portfolio.get_table_headers() == expected_headers


def test_portfolio_search_found(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.search_facility("RCF")
    assert portfolio.is_facility_displayed("RCF")


def test_portfolio_search_not_found(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.search_facility("Nonexistent Facility")
    assert portfolio.is_no_data_displayed()


def test_portfolio_dropdown_default(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.get_dropdown_value() == "WBG Level"


def test_portfolio_dropdown_change(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.select_dropdown_option("Region Level")
    assert portfolio.get_dropdown_value() == "Region Level"


def test_portfolio_row_totals(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.verify_row_totals()


def test_portfolio_column_totals(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.verify_column_totals()


def test_portfolio_number_formatting(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.validate_number_formatting()


def test_portfolio_back_navigation(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.click_back()
    assert portfolio.is_navigated_back()


def test_portfolio_responsive_mobile(page):
    portfolio = PortfolioPage(page)
    portfolio.set_viewport("mobile")
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.is_layout_responsive()


def test_portfolio_keyboard_accessibility(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.test_keyboard_navigation()


def test_portfolio_aria_labels(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.verify_aria_labels()


def test_portfolio_sql_injection_protection(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.search_facility("' OR '1'='1")
    assert portfolio.is_no_data_displayed()


def test_portfolio_script_injection(page):
    portfolio = PortfolioPage(page)
    portfolio.visit(Config.PORTFOLIO_URL)
    portfolio.search_facility("<script>alert(1)</script>")
    assert portfolio.is_no_data_displayed()


def test_portfolio_unauthorized_access(page):
    portfolio = PortfolioPage(page)
    portfolio.logout()
    portfolio.visit(Config.PORTFOLIO_URL)
    assert portfolio.is_redirected_to_login()
