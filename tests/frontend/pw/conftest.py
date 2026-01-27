"""
Pytest configuration and fixtures for Playwright tests
"""
import os
import sys
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from pages.pw.home_page import HomePage
from pages.pw.login_page import LoginPage
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def config():
    """Load configuration for tests"""
    config_reader = ConfigReader()
    return config_reader.config


@pytest.fixture(scope="session")
def playwright_instance():
    """Create Playwright instance for the session"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch browser for the session"""
    browser = playwright_instance.chromium.launch(
        headless=False,
        slow_mo=500
    )
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser, config) -> BrowserContext:
    """Create browser context with standard configuration"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        record_video_dir='./videos/',
        record_video_size={'width': 1920, 'height': 1080}
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Create new page for each test"""
    page = context.new_page()
    
    # Take screenshot on test failure
    yield page
    
    # Cleanup
    page.close()


@pytest.fixture
def home_page(page: Page, config) -> HomePage:
    """Initialize HomePage with navigation"""
    home = HomePage(page, config)
    home.navigate()
    return home


@pytest.fixture
def login_page(page: Page, config) -> LoginPage:
    """Initialize LoginPage with navigation"""
    login = LoginPage(page, config)
    login.navigate()
    return login


def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure
    """
    if call.when == "call" and call.excinfo is not None:
        # Test failed, capture screenshot
        try:
            page = item.funcargs.get('page')
            if page:
                screenshot_dir = "reports/screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = f"{screenshot_dir}/{item.name}_failure.png"
                page.screenshot(path=screenshot_path)
                print(f"\n📸 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"\n⚠️ Could not capture screenshot: {e}")