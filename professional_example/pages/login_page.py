class LoginPage:

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def __init__(self, page):
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def is_login_page(self):
        return "/auth/login" in self.page.url

    def invalid_credentials_message(self):
        return self.page.get_by_text("Invalid credentials")

    def required_messages(self):
        return self.page.get_by_text("Required")
