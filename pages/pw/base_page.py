"""
Base Page - Foundation for all Playwright page objects

Innovations:
- Built-in wait strategies
- Screenshot & video helpers
- Logging integration
- Common actions abstracted
"""
import logging
from typing import Optional
from playwright.sync_api import Page, expect, Locator

# Configure logging
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all Playwright page objects.
    Contains common methods and utilities.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000  # 10 seconds default timeout
    
    # ============== NAVIGATION ==============
    
    def navigate(self, url: str) -> None:
        """Navigate to a URL and wait for load"""
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="networkidle")
    
    def refresh(self) -> None:
        """Refresh current page"""
        logger.info("Refreshing page")
        self.page.reload(wait_until="networkidle")
    
    def go_back(self) -> None:
        """Navigate back"""
        self.page.go_back()
    
    # ============== ELEMENT INTERACTIONS ==============
    
    def click(self, selector: str) -> None:
        """Click an element with auto-wait"""
        logger.debug(f"Clicking: {selector}")
        self.page.click(selector, timeout=self.timeout)
    
    def fill(self, selector: str, text: str) -> None:
        """Fill input field - clears existing text first"""
        logger.debug(f"Filling '{selector}' with '{text}'")
        self.page.fill(selector, text, timeout=self.timeout)
    
    def type_text(self, selector: str, text: str, delay: int = 50) -> None:
        """Type text character by character (useful for autocomplete)"""
        logger.debug(f"Typing '{text}' into '{selector}'")
        self.page.type(selector, text, delay=delay)
    
    def clear(self, selector: str) -> None:
        """Clear an input field"""
        self.page.fill(selector, "")
    
    def select_option(self, selector: str, value: str) -> None:
        """Select dropdown option by value"""
        logger.debug(f"Selecting '{value}' from '{selector}'")
        self.page.select_option(selector, value)
    
    def check(self, selector: str) -> None:
        """Check a checkbox"""
        self.page.check(selector)
    
    def uncheck(self, selector: str) -> None:
        """Uncheck a checkbox"""
        self.page.uncheck(selector)
    
    # ============== ELEMENT STATE ==============
    
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(selector).is_visible()
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        return self.page.locator(selector).is_enabled()
    
    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked"""
        return self.page.locator(selector).is_checked()
    
    def get_text(self, selector: str) -> str:
        """Get element's text content"""
        return self.page.locator(selector).inner_text()
    
    def get_value(self, selector: str) -> str:
        """Get input element's value"""
        return self.page.locator(selector).input_value()
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element's attribute value"""
        return self.page.locator(selector).get_attribute(attribute)
    
    def get_element_count(self, selector: str) -> int:
        """Get count of matching elements"""
        return self.page.locator(selector).count()
    
    # ============== WAITS ==============
    
    def wait_for_element(self, selector: str, state: str = "visible") -> Locator:
        """
        Wait for element with specific state.
        States: 'attached', 'detached', 'visible', 'hidden'
        """
        logger.debug(f"Waiting for '{selector}' to be {state}")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=self.timeout)
        return locator
    
    def wait_for_url(self, url_pattern: str) -> None:
        """Wait for URL to match pattern"""
        self.page.wait_for_url(url_pattern, timeout=self.timeout)
    
    def wait_for_load(self) -> None:
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle")
    
    # ============== PAGE INFO ==============
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def get_url(self) -> str:
        """Get current URL"""
        return self.page.url
    
    # ============== ASSERTIONS (using Playwright expect) ==============
    
    def expect_visible(self, selector: str) -> None:
        """Assert element is visible"""
        expect(self.page.locator(selector)).to_be_visible()
    
    def expect_hidden(self, selector: str) -> None:
        """Assert element is hidden"""
        expect(self.page.locator(selector)).to_be_hidden()
    
    def expect_text(self, selector: str, text: str) -> None:
        """Assert element contains text"""
        expect(self.page.locator(selector)).to_contain_text(text)
    
    def expect_value(self, selector: str, value: str) -> None:
        """Assert input has value"""
        expect(self.page.locator(selector)).to_have_value(value)
    
    def expect_title(self, title: str) -> None:
        """Assert page title"""
        expect(self.page).to_have_title(title)
    
    def expect_url_contains(self, text: str) -> None:
        """Assert URL contains text"""
        assert text in self.page.url, f"Expected '{text}' in URL, got: {self.page.url}"
    
    # ============== SCREENSHOTS & DEBUGGING ==============
    
    def take_screenshot(self, name: str) -> str:
        """Take a screenshot and return path"""
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot saved: {path}")
        return path
    
    def highlight_element(self, selector: str) -> None:
        """Highlight element for debugging (adds red border)"""
        self.page.eval_on_selector(
            selector,
            "el => el.style.border = '3px solid red'"
        )