"""
Login Page - OpenCart Login
"""
import logging
from pages.pw.base_page import BasePage
from locators.login_locators import LoginLocators

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """OpenCart Login Page Object"""
    
    # ============== ACTIONS ==============
    
    def login(self, email: str, password: str) -> None:
        """Perform login with credentials"""
        logger.info(f"Logging in as: {email}")
        self.fill(LoginLocators.EMAIL_INPUT, email)
        self.fill(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)
        self.wait_for_load()
    
    def click_forgotten_password(self) -> None:
        """Click forgotten password link"""
        self.click(LoginLocators.FORGOTTEN_PASSWORD)
    
    def click_register(self) -> None:
        """Click register link"""
        self.click(LoginLocators.REGISTER_LINK)
    
    # ============== VERIFICATIONS ==============
    
    def verify_login_page_loaded(self) -> None:
        """Verify login page is displayed"""
        self.expect_visible(LoginLocators.EMAIL_INPUT)
        self.expect_visible(LoginLocators.PASSWORD_INPUT)
    
    def verify_login_error(self) -> None:
        """Verify login error is displayed"""
        self.expect_visible(LoginLocators.ALERT_DANGER)
    
    def verify_login_successful(self) -> None:
        """Verify successful login (redirected to account)"""
        self.expect_url_contains("account")

    def verify_forgotten_password_visible(self) -> None:
        """Verify forgotten password link is visible"""
        self.expect_visible(LoginLocators.FORGOTTEN_PASSWORD)

    def verify_register_link_visible(self) -> None:
        """Verify register/continue link is visible"""
        self.expect_visible(LoginLocators.REGISTER_LINK)
    
    def get_error_message(self) -> str:
        """Get the error message text"""
        return self.get_text(LoginLocators.ALERT_DANGER)