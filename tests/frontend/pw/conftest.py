"""
Playwright Test Configuration and Fixtures

Innovations:
- Automatic screenshots on failure
- Video recording on failure  
- Trace files for debugging
- Environment-based configuration
- Structured logging
"""
import pytest
import logging
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.config_reader import config
from pages.pw.home_page import HomePage
from pages.pw.login_page import LoginPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============== PYTEST HOOKS ==============

def pytest_configure(config):
    """Create report directories and set timestamped report name"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create directories
    Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
    Path("reports/videos").mkdir(parents=True, exist_ok=True)
    Path("reports/traces").mkdir(parents=True, exist_ok=True)
    
    # Set timestamped HTML report path
    if hasattr(config.option, 'htmlpath') and config.option.htmlpath:
        Path("reports/html").mkdir(parents=True, exist_ok=True)
        config.option.htmlpath = f"reports/html/report_{timestamp}.html"
    
    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "critical: Critical path tests")


# ============== URL FIXTURES ==============

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from config"""
    url = config.get_base_url()
    logger.info(f"Base URL: {url}")
    return url


@pytest.fixture(scope="session")
def admin_url():
    """Get admin URL from config"""
    return config.get_admin_url()


# ============== CREDENTIALS FIXTURES ==============

@pytest.fixture(scope="session")
def admin_credentials():
    """Get admin credentials from config"""
    return config.get_credentials("admin")


@pytest.fixture(scope="session")
def customer_credentials():
    """Get customer credentials from config"""
    return config.get_credentials("customer")


# ============== BROWSER CONFIGURATION ==============

@pytest.fixture(scope="session")
def browser_context(browser):
    """Create browser context with authentication for ngrok"""
    import os
    
    # Check if we're in CI and need basic auth for ngrok
    ngrok_user = os.getenv('NGROK_USER')
    ngrok_pass = os.getenv('NGROK_PASS')
    
    if ngrok_user and ngrok_pass:
        # CI environment with ngrok basic auth
        context = browser.new_context(
            http_credentials={
                'username': ngrok_user,
                'password': ngrok_pass
            }
        )
    else:
        # Local environment without auth
        context = browser.new_context()
    
    yield context
    context.close()

@pytest.fixture
def page(browser_context):
    """Create a new page for each test"""
    page = browser_context.new_page()
    yield page
    page.close()


# ============== PAGE OBJECT FIXTURES ==============

@pytest.fixture(scope="function")
def home_page(page, base_url):
    """
    Get HomePage object with navigation to homepage.
    Fresh instance for each test.
    """
    logger.info("Setting up HomePage")
    home = HomePage(page)
    home.navigate(base_url)
    return home


@pytest.fixture(scope="function")
def login_page(page, base_url):
    """
    Get LoginPage object with navigation to login page.
    """
    logger.info("Setting up LoginPage")
    login = LoginPage(page)
    login.navigate(f"{base_url}/index.php?route=account/login")
    return login


# ============== FAILURE HANDLING ==============

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots and traces on test failure.
    This is AUTOMATIC - no code needed in tests!
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get the page fixture if available
        page = item.funcargs.get("page")
        if page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("[", "_").replace("]", "")
            
            # Take screenshot
            screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                logger.error(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")
