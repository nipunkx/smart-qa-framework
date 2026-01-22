"""
Login Page Locators
Shared between Playwright & Selenium
"""


class LoginLocators:
    """OpenCart Login Page Locators"""
    
    # Login Form
    EMAIL_INPUT = "#input-email"
    PASSWORD_INPUT = "#input-password"
    LOGIN_BUTTON = "button[type='submit']"
    FORGOTTEN_PASSWORD = "a:has-text('Forgotten Password'):not(.list-group-item)"
    
    # Registration
    REGISTER_LINK = "#column-right a.list-group-item:has-text('Register')"
    CONTINUE_BUTTON = "#content a.btn-primary:has-text('Continue')"
    
    # Error Messages
    ALERT_DANGER = ".alert-danger"
    
    # Account Page (after login)
    ACCOUNT_HEADER = "#content h2"
    LOGOUT_LINK = "a:has-text('Logout')"