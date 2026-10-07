# Playwright + Pytest Test Automation Framework Guide

> **Simple rule:** `pages/` = how to interact, `tests/` = what to verify, `conftest.py` = shared setup/resources, `utils/` = generic reusable code, `data/` = reusable test data.

---

## 1. Recommended starter structure

```text
automation/
│
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── profile_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_dashboard.py
│   └── test_profile.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

Start small. You do not need many folders on day one.

---

# 2. `pages/` — HOW to interact with the application

`pages/` contains Page Object classes.

A Page Object answers:

> **How do I interact with this page?**

For a login page, it can contain:

- Locators
- Open/navigate methods
- Fill/click/select actions
- Upload actions
- Reusable page operations
- Small reusable page-state helpers

Example:

```python
# pages/login_page.py

class LoginPage:

    URL = "https://example.com/login"

    def __init__(self, page):
        self.page = page

        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role(
            "button",
            name="Login"
        )

    def open(self):
        self.page.goto(self.URL)

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def is_login_page(self):
        return "/login" in self.page.url
```

This is a **normal Python class**, so using `__init__` here is correct.

You create it yourself:

```python
login = LoginPage(page)
```

---

# 3. `tests/` — WHAT to verify

`tests/` contains the test scenarios.

A test answers:

> **What behavior am I verifying?**

Example:

```python
# tests/test_login.py

from pages.login_page import LoginPage


def test_valid_login(page):
    login = LoginPage(page)

    login.open()
    login.login("Admin", "admin123")

    page.wait_for_url("**/dashboard/index")

    assert "dashboard" in page.url
```

The test decides what the expected result is.

---

# 4. The key difference

### `pages/login_page.py`

```python
def login(self, username, password):
    self.username.fill(username)
    self.password.fill(password)
    self.login_button.click()
```

This means:

> **HOW do I perform login?**

### `tests/test_login.py`

```python
def test_valid_login(page):
    ...
    assert "dashboard" in page.url
```

This means:

> **WHAT should happen after login?**

---

# 5. Why separate pages and tests?

Without Page Objects, tests repeat locators:

```python
def test_valid_login(page):
    page.goto(...)
    page.get_by_placeholder("Username").fill(...)
    page.get_by_placeholder("Password").fill(...)
    page.get_by_role("button", name="Login").click()


def test_invalid_password(page):
    page.goto(...)
    page.get_by_placeholder("Username").fill(...)
    page.get_by_placeholder("Password").fill(...)
    page.get_by_role("button", name="Login").click()
```

If a locator changes, many tests may need changes.

With a Page Object:

```python
login.login("Admin", "admin123")
```

The UI details stay in one place.

---

# 6. `conftest.py` — SHARED SETUP / RESOURCES

`conftest.py` is a special Pytest file.

It is **not mandatory**.

Use it for shared fixtures.

Example:

```python
# conftest.py

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        yield page

        browser.close()
```

A test can now ask for:

```python
def test_login(page):
    ...
```

Pytest sees `page`, finds the fixture, creates the browser/page, and injects it into the test.

---

# 7. Fixture mental model

```text
test_login(page)
       |
       v
Pytest sees "page"
       |
       v
Finds page fixture
       |
       v
Starts Playwright
       |
       v
Creates browser + page
       |
       v
Gives page to test
       |
       v
Test finishes
       |
       v
Browser closes
```

For a fixture using `yield`:

```python
@pytest.fixture
def page():
    # setup
    ...

    yield page

    # cleanup
    ...
```

Think:

```text
BEFORE yield = setup
yield        = test uses resource
AFTER yield  = cleanup
```

---

# 8. `utils/` — GENERIC reusable code

`utils/` is for code that is reusable but not specific to one page.

Example:

```text
utils/
├── api_helper.py
├── file_helper.py
├── date_helper.py
└── random_data.py
```

Examples:

```python
def generate_random_email():
    ...
```

```python
def read_test_file():
    ...
```

Do not put login-page locators in `utils/`.

Those belong in `pages/login_page.py`.

---

# 9. `data/` — REUSABLE TEST DATA

When test data grows, separate it.

```text
data/
├── login_data.py
└── users.py
```

Example:

```python
# data/login_data.py

VALID_USER = {
    "username": "Admin",
    "password": "admin123"
}
```

Then:

```python
from data.login_data import VALID_USER

def test_valid_login(page):
    ...
    login.login(
        VALID_USER["username"],
        VALID_USER["password"]
    )
```

---

# 21. Recommended bigger framework

As the project grows:

```text
automation/
│
├── pages/
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── profile_page.py
│   └── users_page.py
│
├── tests/
│   ├── smoke/
│   │   └── test_login.py
│   │
│   ├── regression/
│   │   ├── test_users.py
│   │   └── test_profile.py
│   │
│   └── api/
│       └── test_auth_api.py
│
├── data/
│   ├── login_data.py
│   └── users.py
│
├── utils/
│   ├── api_helper.py
│   ├── file_helper.py
│   └── random_data.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

Add folders only when the project needs them.

---

# 22. How to decide where code belongs

Ask these questions.

### "Does this describe how to interact with a page?"

Put it in:

```text
pages/
```

Example:

```python
def login(self, username, password):
    ...
```

### "Does this describe what behavior I want to verify?"

Put it in:

```text
tests/
```

Example:

```python
assert "dashboard" in page.url
```

### "Does this prepare something many tests need?"

Put it in:

```text
conftest.py
```

Example:

```python
@pytest.fixture
def page():
    ...
```

### "Is it generic reusable code?"

Put it in:

```text
utils/
```

### "Is it reusable test data?"

Put it in:

```text
data/
```

---

# 23. Complete architecture flow

```text
                         TEST
                           |
                           v
                   tests/test_login.py
                           |
                           v
                   LoginPage(page)
                           |
                           v
                   pages/login_page.py
                           |
                           v
                       Playwright
                           |
                           v
                        Browser
                           |
                           v
                         Action
                           |
                           v
                        ASSERT
                       /       \
                      v         v
                   PASS       FAIL
```

Fixture flow:

```text
test_login(page)
      |
      v
conftest.py
      |
      v
page fixture
      |
      v
browser + page
```

---

# 24. Avoid putting everything into Page Objects

A Page Object should not become:

```text
LoginPage
├── test_valid_login()
├── test_invalid_login()
├── test_logout()
├── database_check()
├── API_check()
└── ...
```

Tests belong in `tests/`.

Keep responsibilities separate:

```text
Page Object
    -> UI interaction

Test
    -> scenario + verification

Fixture
    -> setup/resources

Utility
    -> generic reusable code

Data
    -> test data
```

---

# 25. Final cheat sheet

```text
pages/
    HOW do I interact?

tests/
    WHAT am I verifying?

conftest.py
    WHAT shared resource/setup do tests need?

utils/
    WHAT generic code can be reused?

data/
    WHAT reusable test data do I need?

pytest.ini
    WHAT Pytest configuration/markers do I want?
```

And:

```text
Pytest
    ↓
discovers tests
    ↓
provides fixtures
    ↓
runs test
    ↓
assertion
    ↓
PASS / FAIL
```

> **The goal of a framework is not to have many folders. The goal is to keep responsibilities separated so the automation remains readable, reusable, and maintainable as the test suite grows.**
