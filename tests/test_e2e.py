import pytest
import time
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"

# Generate a unique ID once per test run to prevent database duplicate errors
UNIQUE_ID = int(time.time())
TEST_USER = f"e2e_user_{UNIQUE_ID}"
TEST_EMAIL = f"e2e_{UNIQUE_ID}@test.com"

def test_register_positive(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.fill("id=username", TEST_USER)
    page.fill("id=email", TEST_EMAIL)
    page.fill("id=password", "secure123")
    page.click("id=registerBtn")
    
    # Verify success message appears
    success_msg = page.locator("id=message")
    expect(success_msg).to_have_text("Registration successful! Please login.")

def test_register_negative_short_password(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.fill("id=username", "fail_user")
    page.fill("id=email", "fail@test.com")
    page.fill("id=password", "123") # Too short
    
    page.click("id=registerBtn")
    error_msg = page.locator("id=message")
    expect(error_msg).to_have_text("Password must be at least 6 characters.")

def test_login_positive(page: Page):
    # Uses the exact same unique user we just registered above!
    page.goto(f"{BASE_URL}/login")
    page.fill("id=username", TEST_USER)
    page.fill("id=password", "secure123")
    page.click("id=loginBtn")
    
    # Verify redirect to calculator and element visibility
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("id=logoutBtn")).to_be_visible()

def test_login_negative_wrong_password(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("id=username", TEST_USER)
    page.fill("id=password", "WRONG_PASS")
    page.click("id=loginBtn")
    
    error_msg = page.locator("id=message")
    expect(error_msg).to_have_text("Invalid credentials")