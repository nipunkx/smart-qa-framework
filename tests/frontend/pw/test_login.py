"""
OpenCart Login Tests

Tests for user authentication functionality.
Run: pytest tests/frontend/pw/test_login.py -v --headed
"""
import pytest
from pages.pw.login_page import LoginPage
from pages.pw.home_page import HomePage


@pytest.mark.smoke
class TestLoginPage:
    """Test login page accessibility"""
    
    def test_login_page_loads(self, login_page: LoginPage):
        """
        GIVEN: User navigates to login page
        WHEN: Page loads completely
        THEN: Login form should be visible
        """
        login_page.verify_login_page_loaded()
    
    def test_can_navigate_to_login_from_homepage(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: User clicks My Account → Login
        THEN: User should see login page
        """
        home_page.click_login()
        
        assert "login" in home_page.get_current_url().lower()


@pytest.mark.smoke
@pytest.mark.regression
class TestLoginFunctionality:
    """Test login functionality"""
    
    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: User enters invalid credentials
        THEN: Error message should be displayed
        """
        login_page.login(
            email="invalid@test.com",
            password="wrongpassword"
        )
        login_page.verify_login_error()
    
    def test_login_with_empty_credentials(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: User clicks login without entering credentials
        THEN: Error message should be displayed
        """
        login_page.login(email="", password="")
        login_page.verify_login_error()
    
    def test_login_with_invalid_email_format(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: User enters invalid email format
        THEN: Error message should be displayed
        """
        login_page.login(
            email="notanemail",
            password="somepassword"
        )
        login_page.verify_login_error()
    
    def test_error_message_text(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: User enters wrong credentials
        THEN: Specific error message should be shown
        """
        login_page.login(
            email="wrong@email.com",
            password="wrongpass"
        )
        error_message = login_page.get_error_message()
        assert "Warning" in error_message or "match" in error_message.lower()


@pytest.mark.regression
class TestLoginNavigation:
    """Test login page navigation elements"""
    
    def test_forgotten_password_link_exists(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: Looking at the login form
        THEN: Forgotten password link should be visible
        """
        login_page.verify_forgotten_password_visible()
    
    def test_register_link_exists(self, login_page: LoginPage):
        """
        GIVEN: User is on login page
        WHEN: Looking at the page
        THEN: Register/Continue button should be visible
        """
        login_page.verify_register_link_visible()


@pytest.mark.critical
class TestValidLogin:
    """Test valid login - requires test account"""
    
    @pytest.mark.skip(reason="Requires valid test account - create account first")
    def test_login_with_valid_credentials(self, login_page: LoginPage, customer_credentials):
        """
        GIVEN: User is on login page
        WHEN: User enters valid credentials
        THEN: User should be logged in and redirected to account page
        """
        login_page.login(
            email=customer_credentials["email"],
            password=customer_credentials["password"]
        )
        login_page.verify_login_successful()