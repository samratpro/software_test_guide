import pytest


URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


@pytest.mark.login
@pytest.mark.smoke
def test_valid_login(page):
    page.goto(URL)

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/dashboard/index")

    assert "dashboard" in page.url


@pytest.mark.login
def test_invalid_username(page):
    page.goto(URL)

    page.get_by_placeholder("Username").fill("WrongUser")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    assert "/auth/login" in page.url
    assert page.get_by_text("Invalid credentials").is_visible()


@pytest.mark.login
def test_invalid_password(page):
    page.goto(URL)

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("wrongpass")
    page.get_by_role("button", name="Login").click()

    assert "/auth/login" in page.url
    assert page.get_by_text("Invalid credentials").is_visible()


@pytest.mark.login
def test_empty_fields(page):
    page.goto(URL)

    page.get_by_role("button", name="Login").click()

    assert page.get_by_text("Required").count() >= 1
