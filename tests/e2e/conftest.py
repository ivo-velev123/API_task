import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:5001"

@pytest.fixture
def anonymous(page: Page):
    page.goto(BASE_URL)
    return page

@pytest.fixture
def user(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name='username']", "user")
    page.fill("input[name='password']", "userpass")
    page.click("button[type='submit']")
    return page

@pytest.fixture
def admin(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "adminpass")
    page.click("button[type='submit']")
    return page
