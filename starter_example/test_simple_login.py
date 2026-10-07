def test_login(page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")

    page.get_by_role("button", name="Login").click()

    page.wait_for_url("**/dashboard/index")

    assert "dashboard" in page.url