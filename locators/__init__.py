"""
Locators Package - Shared between Playwright & Selenium
"""
from locators.home_locators import HomeLocators
from locators.login_locators import LoginLocators

__all__ = ["HomeLocators", "LoginLocators"]