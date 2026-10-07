import pytest
from pages.login_page import LoginPage


@pytest.mark.login
def test_valid_login(page):
    login = LoginPage(page)

    login.open()
    login.login("Admin", "admin123")

    page.wait_for_url("**/dashboard/index")

    assert "dashboard" in page.url


@pytest.mark.login
def test_invalid_username(page):
    login = LoginPage(page)

    login.open()
    login.login("WrongUser", "admin123")

    assert login.is_login_page()
    assert login.invalid_credentials_message().is_visible()


@pytest.mark.login
def test_invalid_password(page):
    login = LoginPage(page)

    login.open()
    login.login("Admin", "wrongpass")

    assert login.is_login_page()
    assert login.invalid_credentials_message().is_visible()


@pytest.mark.login
def test_empty_fields(page):
    login = LoginPage(page)

    login.open()
    login.login("", "")

    assert login.required_messages().count() >= 1