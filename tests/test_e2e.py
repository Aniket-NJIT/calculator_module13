import pytest
from playwright.sync_api import Page, expect

# Change URL if your test server runs on a different port
BASE_URL = "http://localhost:8000" #"http://127.0.0.1:8000/"

def test_register_positive(page: Page):
    page.goto(f"{BASE_URL}/register")
    page.fill("id=username", "e2e_user")
    page.fill("id=email", "e2e@test.com")
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
    
    # HTML5 validation should prevent submission, or JS intercepts it
    page.click("id=registerBtn")
    error_msg = page.locator("id=message")
    expect(error_msg).to_have_text("Password must be at least 6 characters.")

def test_login_positive(page: Page):
    # Ensure user exists first (depends on test execution order, or use a setup fixture)
    page.goto(f"{BASE_URL}/login")
    page.fill("id=username", "e2e_user")
    page.fill("id=password", "secure123")
    page.click("id=loginBtn")
    
    # Verify redirect to calculator and element visibility
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("id=logoutBtn")).to_be_visible()

def test_login_negative_wrong_password(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill("id=username", "e2e_user")
    page.fill("id=password", "WRONG_PASS")
    page.click("id=loginBtn")
    
    error_msg = page.locator("id=message")
    expect(error_msg).to_have_text("Invalid credentials")