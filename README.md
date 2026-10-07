# Pytest + Playwright + OrangeHRM — Super Guide

A beginner-to-intermediate tutorial for learning Pytest clearly before building a large automation framework.

Target site:

https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Demo credentials supplied for this tutorial:

- Username: `Admin`
- Password: `admin123`

---

# 1. What are we learning?

This project demonstrates:

- How Pytest discovers tests
- File and function naming rules
- Function-based tests
- Class-based tests
- How Pytest creates test class instances
- Why Pytest test classes should not use a custom `__init__`
- Fixtures
- `conftest.py`
- Fixture arguments / dependency injection
- Markers
- Class-level and test-level markers
- Assertions
- Four login test cases
- Playwright browser/page fixture
- Optional Page Object Model (OOP)
- Running all, selected, class, function, keyword, and marked tests

The goal is to understand the **ideas**, not just copy a framework.

---

# 2. Project structure

```text
pytest_orangehrm_super_guide/
│
├── README.md
├── RUNNING.md
├── requirements.txt
├── pytest.ini
│
├── conftest.py
│
├── pages/
│   └── login_page.py
│
└── tests/
    ├── test_login_function.py
    └── test_login_class.py
```

## What each file does

### `conftest.py`
Shared Pytest fixtures.

### `pytest.ini`
Only used here to register custom markers and set a small default option.

### `test_login_function.py`
Function-based tests.

### `test_login_class.py`
Class-based Pytest tests.

### `pages/login_page.py`
Optional OOP Page Object. This is a normal Python class and can use `__init__`.

---

# 3. The most important Pytest mental model

```text
pytest
  |
  +--> discover test files
  |
  +--> discover test functions/classes
  |
  +--> create/use fixtures
  |
  +--> run test
  |
  +--> execute assert
  |
  +--> report PASSED / FAILED
```

Playwright is different:

```text
Playwright
   |
   +--> open browser
   +--> create page
   +--> goto
   +--> fill
   +--> click
```

So:

> Pytest manages the tests. Playwright controls the browser.

---

# 4. Pytest installation

```bash
pip install pytest playwright
playwright install
```

Check:

```bash
pytest --version
```

---

# 5. Test discovery rules

Pytest must first identify what is a test.

## 5.1 Test file names

By default, common test file patterns are:

```text
test_*.py
*_test.py
```

Examples:

```text
test_login.py        ✅
test_payment.py      ✅
login_test.py        ✅
payment_test.py      ✅
login.py             ❌ normally not discovered
```

The exact discovery rules can be changed with configuration, but beginners should remember the default patterns.

---

# 6. Do folders need a special name?

No.

This is conventional:

```text
tests/
```

but it is not a Python or Pytest requirement.

You can also have:

```text
testing/
automation/
qa/
```

What matters is whether Pytest can find the test files.

For a normal project, use:

```text
tests/
```

because it is clear and conventional.

---

# 7. Test function naming

By default, Pytest looks for functions whose names start with:

```text
test_
```

Example:

```python
def test_login():
    assert True
```

Collected as a test:

```text
test_login
```

This is not normally collected as a test:

```python
def login():
    assert True
```

Another important detail:

```python
def login_test():
```

is not the normal default function pattern because it does not start with `test_`.

---

# 8. Test classes

A Pytest test class normally starts with:

```text
Test
```

Example:

```python
class TestLogin:

    def test_valid_login(self):
        assert True
```

Pytest sees:

```text
TestLogin
   |
   +--> test_valid_login
```

The methods still start with:

```text
test_
```

---

# 9. Function-based vs class-based tests

Both are valid.

## Function-based

```python
def test_valid_login(page):
    ...
```

This is simple and usually the best starting point.

## Class-based

```python
class TestLogin:

    def test_valid_login(self, page):
        ...
```

The main benefit of the test class is **organization/grouping**.

For example:

```text
TestLogin
   |
   +-- test_valid_login
   +-- test_invalid_username
   +-- test_invalid_password
   +-- test_empty_fields
```

This does not mean Pytest test classes are normal business/domain classes.

They are mainly containers for related tests.

---

# 10. What is `self`?

Normal Python:

```python
class Login:
    def hello(self):
        print("hello")
```

`self` represents the current object instance.

Pytest class:

```python
class TestLogin:

    def test_valid_login(self, page):
        ...
```

There are two parameters here:

```text
self
page
```

`self` = normal Python class instance.

`page` = Pytest fixture.

Important:

```python
def test_valid_login(page):
```

for a function test.

```python
def test_valid_login(self, page):
```

for a class method.

---

# 11. How is the class instance created if we do not use `__init__`?

This is the confusing part for many Python developers.

Normally, Python object creation can look like:

```python
class Login:

    def __init__(self, username):
        self.username = username

login = Login("Admin")
```

But for a Pytest test class, you normally do NOT create the object yourself.

You write:

```python
class TestLogin:

    def test_valid_login(self):
        assert True
```

Pytest collects the class and creates the test instance internally.

Conceptually, think of it like:

```python
test_object = TestLogin()
test_object.test_valid_login()
```

That is a simplified mental model.

You should NOT write the object creation yourself.

---

# 12. Why should we avoid `__init__` in a Pytest test class?

Do not do this:

```python
class TestLogin:

    def __init__(self):
        self.username = "Admin"
```

Pytest does not want a custom constructor on its collected test classes.

Instead, use a fixture:

```python
import pytest

@pytest.fixture
def credentials():
    return {
        "username": "Admin",
        "password": "admin123"
    }
```

Then:

```python
class TestLogin:

    def test_valid_login(self, credentials):
        assert credentials["username"] == "Admin"
```

This is **fixture injection**.

---

# 13. What is a fixture?

A fixture prepares something that a test needs.

Example:

```python
import pytest

@pytest.fixture
def username():
    return "Admin"
```

Test:

```python
def test_username(username):
    assert username == "Admin"
```

The test does not call:

```python
username()
```

Pytest sees the parameter:

```python
username
```

and finds the fixture with the same name.

Conceptually:

```text
test_username(username)
             |
             +--> Pytest finds username fixture
                         |
                         +--> returns "Admin"
```

---

# 14. Why do we use `conftest.py`?

`conftest.py` is a special Pytest file for shared fixtures/configuration.

It is NOT mandatory.

Without it:

```text
tests/
└── test_login.py
```

can work.

When multiple tests need the same fixture, `conftest.py` becomes convenient.

Example:

```text
conftest.py
     |
     +--> page fixture
     |
     +--> credentials fixture

tests/
   |
   +--> test_login.py
   +--> test_profile.py
   +--> test_dashboard.py
```

Tests below that `conftest.py` can use those fixtures without manually importing the fixture.

---

# 15. Browser/page fixture

Our `conftest.py` contains:

```python
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

Understand `yield` as:

```text
setup
  |
  +--> start Playwright
  +--> launch browser
  +--> create page
  |
 yield page
  |
  +--> test runs here
  |
cleanup
  |
  +--> browser.close()
```

---

# 16. Passing data to a test with fixtures

You asked an important question:

> "How do I pass arguments if I cannot use `__init__`?"

Use fixtures.

`conftest.py`:

```python
@pytest.fixture
def credentials():
    return {
        "username": "Admin",
        "password": "admin123"
    }
```

Then a function:

```python
def test_login(page, credentials):
    ...
```

or a class method:

```python
class TestLogin:

    def test_login(self, page, credentials):
        ...
```

Pytest injects both.

```text
page
  --> page fixture

credentials
  --> credentials fixture
```

You can have many fixture arguments.

---

# 17. Four login test cases

A good beginner login suite should not only test the happy path.

We will use four cases:

| Test | Username | Password | Expected |
|---|---|---|---|
| Valid credentials | Admin | admin123 | Dashboard |
| Invalid username | WrongUser | admin123 | Error / stay on login |
| Invalid password | Admin | wrongpass | Error / stay on login |
| Empty fields | empty | empty | Required validation / stay on login |

The point is **test design**, not just automation.

---

# 18. Functional-style test example

`tests/test_login_function.py`

```python
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
```

This is called **function-based testing** because every test is a separate function.

---

# 19. Class-based test example

`tests/test_login_class.py`

```python
import pytest


URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


@pytest.mark.login
class TestLogin:

    @pytest.mark.smoke
    def test_valid_login(self, page):
        page.goto(URL)

        page.get_by_placeholder("Username").fill("Admin")
        page.get_by_placeholder("Password").fill("admin123")
        page.get_by_role("button", name="Login").click()

        page.wait_for_url("**/dashboard/index")

        assert "dashboard" in page.url

    def test_invalid_username(self, page):
        page.goto(URL)

        page.get_by_placeholder("Username").fill("WrongUser")
        page.get_by_placeholder("Password").fill("admin123")
        page.get_by_role("button", name="Login").click()

        assert "/auth/login" in page.url
        assert page.get_by_text("Invalid credentials").is_visible()

    def test_invalid_password(self, page):
        page.goto(URL)

        page.get_by_placeholder("Username").fill("Admin")
        page.get_by_placeholder("Password").fill("wrongpass")
        page.get_by_role("button", name="Login").click()

        assert "/auth/login" in page.url
        assert page.get_by_text("Invalid credentials").is_visible()

    def test_empty_fields(self, page):
        page.goto(URL)

        page.get_by_role("button", name="Login").click()

        assert page.get_by_text("Required").count() >= 1
```

Notice:

```python
class TestLogin:
```

does not have:

```python
def __init__(...):
```

The class is created and managed by Pytest.

---

# 20. Functional vs class-based — what changed?

Compare the first test.

Function:

```python
def test_valid_login(page):
```

Class:

```python
class TestLogin:

    def test_valid_login(self, page):
```

The actual browser test is almost the same.

Why use the class?

Mainly organization:

```text
TestLogin
    |
    +-- valid
    +-- invalid username
    +-- invalid password
    +-- empty fields
```

And you can run that entire class:

```bash
pytest tests/test_login_class.py::TestLogin
```

So your instinct was correct:

> For small suites, function-based tests can feel simpler.

Use classes when grouping related tests adds clarity.

---

# 21. Markers — the simple explanation

A marker is a label attached to a test.

Example:

```python
@pytest.mark.login
def test_valid_login(page):
    ...
```

Think:

```text
test_valid_login
       |
       +--> label: login
```

Run:

```bash
pytest -m login
```

Pytest runs tests carrying that marker.

---

# 22. Marker on an individual test

```python
@pytest.mark.smoke
def test_valid_login(page):
    ...
```

Only this test receives `smoke`.

---

# 23. Marker on a class

```python
@pytest.mark.login
class TestLogin:
    ...
```

The marker applies to the tests inside that class.

So:

```text
TestLogin
   |
   +-- test_valid_login    login
   +-- test_invalid_user   login
   +-- test_invalid_pass   login
   +-- test_empty_fields   login
```

Then:

```bash
pytest -m login
```

runs them.

---

# 24. Multiple markers

You can put several markers on one test:

```python
@pytest.mark.login
@pytest.mark.smoke
def test_valid_login(page):
    ...
```

This test has:

```text
login
smoke
```

So:

```bash
pytest -m login
```

finds it.

and:

```bash
pytest -m smoke
```

also finds it.

---

# 25. Why do we need `pytest.ini` for markers?

Custom markers should be registered to avoid Pytest warnings and to document the available marker names.

This project has:

```ini
[pytest]
markers =
    login: Login related tests
    smoke: Smoke tests
```

Important:

`pytest.ini` is **not needed just to run Pytest**.

It is being used here because we intentionally created custom markers.

---

# 26. Marker examples

All login tests:

```bash
pytest -m login
```

All smoke tests:

```bash
pytest -m smoke
```

Login but not smoke:

```bash
pytest -m "login and not smoke"
```

Login OR smoke:

```bash
pytest -m "login or smoke"
```

These become useful when a real project has hundreds of tests.

---

# 27. Running tests

From the project root:

## All tests

```bash
pytest
```

## Verbose

```bash
pytest -v
```

## Function file

```bash
pytest tests/test_login_function.py -v
```

## Class file

```bash
pytest tests/test_login_class.py -v
```

## One function

```bash
pytest tests/test_login_function.py::test_valid_login -v
```

## One class

```bash
pytest tests/test_login_class.py::TestLogin -v
```

## One class method

```bash
pytest tests/test_login_class.py::TestLogin::test_valid_login -v
```

## By keyword

```bash
pytest -k login
```

## By marker

```bash
pytest -m login
```

---

# 28. Assertions

An assertion checks an expected result.

Simple Python:

```python
assert 2 + 2 == 4
```

Playwright:

```python
assert "dashboard" in page.url
```

Another:

```python
assert page.get_by_role("button", name="Login").is_visible()
```

The important idea:

```text
Action
  |
  +--> click
  |
  +--> fill
  |
  +--> goto
  |
  ↓
Assertion
  |
  +--> did the expected thing happen?
```

---

# 29. The OOP Page Object Model

Now this is where normal OOP becomes genuinely useful.

A Pytest test class is mainly for grouping tests.

A Page Object is a normal Python class for reusable application behavior.

`pages/login_page.py`:

```python
class LoginPage:

    def __init__(self, page):
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def open(self):
        self.page.goto(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
```

Notice:

```python
def __init__(self, page):
```

is completely OK here.

Why?

Because this is a **normal Python class**, not a Pytest test class.

---

# 30. Using the Page Object in a test

```python
from pages.login_page import LoginPage


def test_valid_login(page):
    login = LoginPage(page)

    login.open()
    login.login("Admin", "admin123")

    page.wait_for_url("**/dashboard/index")

    assert "dashboard" in page.url
```

Now we get real OOP benefits.

Instead of repeating:

```python
page.get_by_placeholder("Username").fill(...)
page.get_by_placeholder("Password").fill(...)
page.get_by_role("button", name="Login").click()
```

we can simply use:

```python
login.login("Admin", "admin123")
```

---

# 31. This is the important OOP distinction

## Pytest test class

```python
class TestLogin:
    def test_valid_login(self, page):
        ...
```

Purpose:

```text
Organize/group tests
```

## Page Object class

```python
class LoginPage:
    def __init__(self, page):
        ...
```

Purpose:

```text
Encapsulate/reuse application actions
```

This is why OOP is still valuable in automation even though Pytest test classes don't use custom constructors.

---

# 32. Better architecture

As the project grows:

```text
tests/
   |
   +--> test_login.py
   +--> test_dashboard.py
   +--> test_profile.py

pages/
   |
   +--> login_page.py
   +--> dashboard_page.py
   +--> profile_page.py

conftest.py
   |
   +--> shared fixtures
```

Then:

```text
Pytest
   |
   +--> tests
   |
   +--> fixtures
   |
   +--> markers

Playwright
   |
   +--> browser
   +--> page

OOP Page Objects
   |
   +--> reusable UI actions
```

---

# 33. When should I use function tests?

Use functions when:

- The test is simple.
- Tests are mostly independent.
- Grouping adds little value.
- You want the easiest code to read.

Example:

```python
def test_search(page):
    ...

def test_logout(page):
    ...
```

---

# 34. When should I use Pytest test classes?

Use a class when:

- Many tests belong to one feature.
- You want logical grouping.
- You want class-level markers.
- Running a whole feature group is useful.

Example:

```python
@pytest.mark.login
class TestLogin:
    ...
```

---

# 35. When should I use a normal OOP Page Object?

Use a normal class when:

- UI actions are repeated.
- Locators should be centralized.
- Several tests need the same page behavior.
- You want maintainable automation.

Example:

```python
class LoginPage:
    ...
```

---

# 36. Final mental model

```text
                         PYTEST
                           |
          +----------------+----------------+
          |                |                |
          ↓                ↓                ↓
       discover          fixtures         markers
          |                |                |
          ↓                ↓                ↓
   test functions      page/data        labels
   test classes
          |
          ↓
      PLAYWRIGHT
          |
          ↓
       Browser
          |
          ↓
       Actions
          |
          ↓
       ASSERT
          |
      +---+---+
      ↓       ↓
    PASS     FAIL
```

And the OOP layer:

```text
                 Test
                  |
                  ↓
            LoginPage(page)
                  |
                  ↓
         reusable UI behavior
```

---

# 37. Naming cheat sheet

| Item | Default / recommended rule |
|---|---|
| Project folder | Any valid name |
| Test folder | Usually `tests/` |
| Test file | `test_*.py` or `*_test.py` |
| Test function | `test_*` |
| Test class | `Test*` |
| Test method | `test_*` |
| Fixture file | `conftest.py` |
| Fixture function | Any valid name |
| Marker | Any registered marker name |
| Page Object | Any normal class name, e.g. `LoginPage` |

The important distinction is:

```text
Naming rules
     ↓
Tell Pytest what to DISCOVER.

Fixtures
     ↓
Tell Pytest what to PROVIDE.

Markers
     ↓
Tell Pytest how to LABEL/GROUP.

Page Objects
     ↓
Give you normal OOP REUSE.

Assertions
     ↓
Tell Pytest whether the TEST PASSED or FAILED.
```

---

# 38. Practical exercise for the student

After understanding the four login tests, ask the student to add:

```text
test_valid_login
test_invalid_username
test_invalid_password
test_empty_fields
test_logout
```

Then ask them to:

```text
1. Run everything
2. Run only login tests
3. Run only smoke tests
4. Run one test
5. Run the whole TestLogin class
6. Move repeated login actions into LoginPage
```

If they can do all six without help, they understand the foundation of Pytest + Playwright.
