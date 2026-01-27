"""
Base Page - Foundation for all Playwright page objects

Features:
- Built-in wait strategies
- Screenshot & video helpers
- Logging integration
- Common actions abstracted
- Safe config handling
- Extensible for future needs
"""
import logging
from typing import Optional, List
from playwright.sync_api import Page, expect, Locator

# Configure logging
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all Playwright page objects
    Provides common functionality and best practices
    """
    
    def __init__(self, page: Page, config: dict):
        """
        Initialize base page
        
        Args:
            page: Playwright Page object
            config: Configuration dictionary
        """
        self.page = page
        self.config = config
        self.base_url = config['application']['base_url']
        
        # Handle timeout - use default if not in config
        default_timeout = config.get('timeouts', {}).get('default', 30)
        self.timeout = default_timeout * 1000  # Convert to ms
        
        # Set default timeout for all actions
        page.set_default_timeout(self.timeout)
        
        logger.debug(f"Initialized {self.__class__.__name__}")
    
    # ============== NAVIGATION ==============
    
    def navigate(self, path: str = "") -> None:
        """
        Navigate to a URL
        
        Args:
            path: Optional path to append to base URL
        """
        url = f"{self.base_url}{path}"
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')
    
    def wait_for_load(self) -> None:
        """Wait for page to finish loading"""
        logger.debug("Waiting for page to load")
        self.page.wait_for_load_state('networkidle')
    
    def reload(self) -> None:
        """Reload the current page"""
        logger.debug("Reloading page")
        self.page.reload()
        self.wait_for_load()
    
    def go_back(self) -> None:
        """Navigate back in browser history"""
        logger.debug("Navigating back")
        self.page.go_back()
        self.wait_for_load()
    
    def go_forward(self) -> None:
        """Navigate forward in browser history"""
        logger.debug("Navigating forward")
        self.page.go_forward()
        self.wait_for_load()
    
    # ============== INTERACTIONS ==============
    
    def click(self, locator: str) -> None:
        """
        Click an element with explicit wait
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Clicking element: {locator}")
        self.page.click(locator)
    
    def double_click(self, locator: str) -> None:
        """
        Double-click an element
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Double-clicking element: {locator}")
        self.page.dblclick(locator)
    
    def fill(self, locator: str, text: str) -> None:
        """
        Fill input field with text
        
        Args:
            locator: CSS selector for the input
            text: Text to enter
        """
        logger.debug(f"Filling {locator} with: {text}")
        self.page.fill(locator, text)
    
    def clear_and_fill(self, locator: str, text: str) -> None:
        """
        Clear field and fill with new text
        
        Args:
            locator: CSS selector for the input
            text: Text to enter
        """
        logger.debug(f"Clearing and filling {locator}")
        self.page.fill(locator, "")  # Clear first
        self.page.fill(locator, text)
    
    def press_key(self, locator: str, key: str) -> None:
        """
        Press a key in an element
        
        Args:
            locator: CSS selector for the element
            key: Key to press (e.g., 'Enter', 'Escape')
        """
        logger.debug(f"Pressing {key} in {locator}")
        self.page.press(locator, key)
    
    def hover(self, locator: str) -> None:
        """
        Hover over an element
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Hovering over: {locator}")
        self.page.hover(locator)
    
    def select_option(self, locator: str, value: str) -> None:
        """
        Select option from dropdown
        
        Args:
            locator: CSS selector for the select element
            value: Value to select
        """
        logger.debug(f"Selecting {value} in {locator}")
        self.page.select_option(locator, value)
    
    def check(self, locator: str) -> None:
        """
        Check a checkbox
        
        Args:
            locator: CSS selector for the checkbox
        """
        logger.debug(f"Checking: {locator}")
        self.page.check(locator)
    
    def uncheck(self, locator: str) -> None:
        """
        Uncheck a checkbox
        
        Args:
            locator: CSS selector for the checkbox
        """
        logger.debug(f"Unchecking: {locator}")
        self.page.uncheck(locator)
    
    # ============== GETTERS ==============
    
    def get_text(self, locator: str) -> str:
        """
        Get text content of an element
        
        Args:
            locator: CSS selector for the element
            
        Returns:
            Text content of the element
        """
        logger.debug(f"Getting text from: {locator}")
        return self.page.text_content(locator) or ""
    
    def get_attribute(self, locator: str, attribute: str) -> Optional[str]:
        """
        Get attribute value of an element
        
        Args:
            locator: CSS selector for the element
            attribute: Attribute name
            
        Returns:
            Attribute value or None
        """
        logger.debug(f"Getting {attribute} from: {locator}")
        return self.page.get_attribute(locator, attribute)
    
    def get_element_count(self, locator: str) -> int:
        """
        Get count of elements matching locator
        
        Args:
            locator: CSS selector for the elements
            
        Returns:
            Number of matching elements
        """
        logger.debug(f"Counting elements: {locator}")
        return self.page.locator(locator).count()
    
    def get_all_texts(self, locator: str) -> List[str]:
        """
        Get text content of all matching elements
        
        Args:
            locator: CSS selector for the elements
            
        Returns:
            List of text contents
        """
        logger.debug(f"Getting all texts from: {locator}")
        elements = self.page.locator(locator).all()
        return [el.text_content() or "" for el in elements]
    
    def get_current_url(self) -> str:
        """
        Get current page URL
        
        Returns:
            Current URL
        """
        return self.page.url
    
    def get_title(self) -> str:
        """
        Get page title
        
        Returns:
            Page title
        """
        return self.page.title()
    
    # ============== CHECKS ==============
    
    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: CSS selector for the element
            timeout: Maximum wait time in milliseconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            return self.page.is_visible(locator, timeout=timeout)
        except Exception:
            return False
    
    def is_enabled(self, locator: str) -> bool:
        """
        Check if element is enabled
        
        Args:
            locator: CSS selector for the element
            
        Returns:
            True if element is enabled, False otherwise
        """
        try:
            return self.page.is_enabled(locator)
        except Exception:
            return False
    
    def is_checked(self, locator: str) -> bool:
        """
        Check if checkbox is checked
        
        Args:
            locator: CSS selector for the checkbox
            
        Returns:
            True if checked, False otherwise
        """
        try:
            return self.page.is_checked(locator)
        except Exception:
            return False
    
    # ============== WAITS ==============
    
    def wait_for_selector(self, locator: str, state: str = "visible", timeout: Optional[int] = None) -> Locator:
        """
        Wait for selector to reach specified state
        
        Args:
            locator: CSS selector for the element
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Optional timeout in milliseconds
            
        Returns:
            Locator object
        """
        logger.debug(f"Waiting for {locator} to be {state}")
        if timeout:
            return self.page.wait_for_selector(locator, state=state, timeout=timeout)
        return self.page.wait_for_selector(locator, state=state)
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern
        
        Args:
            url_pattern: URL pattern to match
            timeout: Optional timeout in milliseconds
        """
        logger.debug(f"Waiting for URL: {url_pattern}")
        if timeout:
            self.page.wait_for_url(url_pattern, timeout=timeout)
        else:
            self.page.wait_for_url(url_pattern)
    
    def wait_for_timeout(self, milliseconds: int) -> None:
        """
        Wait for specified time (use sparingly, prefer other waits)
        
        Args:
            milliseconds: Time to wait in milliseconds
        """
        logger.debug(f"Waiting for {milliseconds}ms")
        self.page.wait_for_timeout(milliseconds)
    
    # ============== ASSERTIONS ==============
    
    def expect_visible(self, locator: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element is visible
        
        Args:
            locator: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        logger.debug(f"Expecting {locator} to be visible")
        if timeout:
            expect(self.page.locator(locator)).to_be_visible(timeout=timeout)
        else:
            expect(self.page.locator(locator)).to_be_visible()
    
    def expect_hidden(self, locator: str, timeout: Optional[int] = None) -> None:
        """
        Assert that element is hidden
        
        Args:
            locator: CSS selector for the element
            timeout: Optional timeout in milliseconds
        """
        logger.debug(f"Expecting {locator} to be hidden")
        if timeout:
            expect(self.page.locator(locator)).to_be_hidden(timeout=timeout)
        else:
            expect(self.page.locator(locator)).to_be_hidden()
    
    def expect_text(self, locator: str, text: str) -> None:
        """
        Assert that element contains specific text
        
        Args:
            locator: CSS selector for the element
            text: Expected text content
        """
        logger.debug(f"Expecting {locator} to contain: {text}")
        expect(self.page.locator(locator)).to_contain_text(text)
    
    def expect_value(self, locator: str, value: str) -> None:
        """
        Assert that input has specific value
        
        Args:
            locator: CSS selector for the input
            value: Expected value
        """
        logger.debug(f"Expecting {locator} to have value: {value}")
        expect(self.page.locator(locator)).to_have_value(value)
    
    def expect_url(self, url_pattern: str) -> None:
        """
        Assert that current URL matches pattern (exact match)
        
        Args:
            url_pattern: Expected URL pattern
        """
        logger.debug(f"Expecting URL to match: {url_pattern}")
        expect(self.page).to_have_url(url_pattern)
    
    def expect_url_contains(self, substring: str) -> None:
        """
        Assert that current URL contains substring
        
        Args:
            substring: Expected substring in URL
        """
        logger.debug(f"Expecting URL to contain: {substring}")
        current_url = self.page.url
        assert substring in current_url, f"Expected URL to contain '{substring}', but got: {current_url}"
    
    def expect_title(self, title: str) -> None:
        """
        Assert that page has specific title
        
        Args:
            title: Expected page title
        """
        logger.debug(f"Expecting title: {title}")
        expect(self.page).to_have_title(title)
    
    def expect_title_contains(self, substring: str) -> None:
        """
        Assert that page title contains substring
        
        Args:
            substring: Expected substring in title
        """
        logger.debug(f"Expecting title to contain: {substring}")
        current_title = self.page.title()
        assert substring in current_title, f"Expected title to contain '{substring}', but got: {current_title}"
    
    def expect_enabled(self, locator: str) -> None:
        """
        Assert that element is enabled
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Expecting {locator} to be enabled")
        expect(self.page.locator(locator)).to_be_enabled()
    
    def expect_disabled(self, locator: str) -> None:
        """
        Assert that element is disabled
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Expecting {locator} to be disabled")
        expect(self.page.locator(locator)).to_be_disabled()
    
    def expect_checked(self, locator: str) -> None:
        """
        Assert that checkbox is checked
        
        Args:
            locator: CSS selector for the checkbox
        """
        logger.debug(f"Expecting {locator} to be checked")
        expect(self.page.locator(locator)).to_be_checked()
    
    def expect_count(self, locator: str, count: int) -> None:
        """
        Assert that exact number of elements match locator
        
        Args:
            locator: CSS selector for the elements
            count: Expected count
        """
        logger.debug(f"Expecting {count} elements matching: {locator}")
        expect(self.page.locator(locator)).to_have_count(count)
    
    # ============== UTILITIES ==============
    
    def screenshot(self, filename: str) -> str:
        """
        Take screenshot of current page
        
        Args:
            filename: Name for the screenshot file
            
        Returns:
            Path to the screenshot file
        """
        path = f"screenshots/{filename}"
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path)
        return path
    
    def screenshot_element(self, locator: str, filename: str) -> str:
        """
        Take screenshot of specific element
        
        Args:
            locator: CSS selector for the element
            filename: Name for the screenshot file
            
        Returns:
            Path to the screenshot file
        """
        path = f"screenshots/{filename}"
        logger.info(f"Taking element screenshot: {path}")
        self.page.locator(locator).screenshot(path=path)
        return path
    
    def scroll_to_element(self, locator: str) -> None:
        """
        Scroll element into view
        
        Args:
            locator: CSS selector for the element
        """
        logger.debug(f"Scrolling to: {locator}")
        self.page.locator(locator).scroll_into_view_if_needed()
    
    def execute_script(self, script: str) -> any:
        """
        Execute JavaScript on the page
        
        Args:
            script: JavaScript code to execute
            
        Returns:
            Result of the script execution
        """
        logger.debug(f"Executing script: {script[:50]}...")
        return self.page.evaluate(script)
    
    def get_locator(self, selector: str) -> Locator:
        """
        Get Playwright Locator object for advanced operations
        
        Args:
            selector: CSS selector
            
        Returns:
            Locator object
        """
        return self.page.locator(selector)