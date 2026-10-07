# Run the OrangeHRM examples

Open a terminal in the project root.

## 1. Install

```bash
pip install -r requirements.txt
playwright install
```

## 2. Run every test

```bash
pytest
```

## 3. Run function-based tests

```bash
pytest tests/test_login_function.py
```

## 4. Run class-based tests

```bash
pytest tests/test_login_class.py
```

## 5. Run one function test

```bash
pytest tests/test_login_function.py::test_valid_login
```

## 6. Run the whole class

```bash
pytest tests/test_login_class.py::TestLogin
```

## 7. Run one class method

```bash
pytest tests/test_login_class.py::TestLogin::test_valid_login
```

## 8. Run all login-marked tests

```bash
pytest -m login
```

## 9. Run smoke tests

```bash
pytest -m smoke
```

## 10. Run by keyword

```bash
pytest -k invalid
```

## 11. Run and stop at the first failure

```bash
pytest -x
```

## 12. Do NOT use the normal VS Code "Run Python File" button for these tests

Do this:

```bash
pytest
```

instead of:

```bash
python tests/test_login_function.py
```

The Python command only loads/defines the functions. Pytest discovers and executes the test functions.

## Expected basic output

You should see something similar to:

```text
================ test session starts ================
collected ... items

tests/test_login_function.py::test_valid_login PASSED
tests/test_login_function.py::test_invalid_username PASSED
...
================ ... passed ================
```
