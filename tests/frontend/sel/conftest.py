"""
Selenium Test Configuration with Selenoid Integration
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def config():
    """Load configuration"""
    config_reader = ConfigReader()
    return config_reader.config


@pytest.fixture(scope="session")
def selenoid_config(config):
    """Get Selenoid configuration"""
    return config.get('selenoid', {})


@pytest.fixture(scope="function")
def driver(config, selenoid_config, request):
    """
    Creates a remote WebDriver connected to Selenoid.
    Browser can be specified with pytest marker: @pytest.mark.browser("chrome")
    Defaults to Chrome if not specified.
    
    Yields:
        WebDriver: Selenium WebDriver instance connected to Selenoid
    """
    # Get browser from marker or default to chrome
    browser_marker = request.node.get_closest_marker("browser")
    browser_name = browser_marker.args[0] if browser_marker else "chrome"
    
    # Get Selenoid hub URL
    hub_url = selenoid_config.get('hub_url', 'http://192.168.50.106:4444/wd/hub')
    
    # Get browser config
    browser_config = selenoid_config.get('browsers', {}).get(browser_name, {})
    browser_version = browser_config.get('version', 'latest')
    selenoid_options = browser_config.get('options', {})
    
    # Configure browser options
    if browser_name == "chrome":
        options = ChromeOptions()
        options.set_capability('browserName', 'chrome')
        options.set_capability('browserVersion', browser_version)
        
        # Selenoid-specific options
        options.set_capability('selenoid:options', selenoid_options)
        
        # Additional Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_capability('browserName', 'firefox')
        options.set_capability('browserVersion', browser_version)
        
        # Selenoid-specific options
        options.set_capability('selenoid:options', selenoid_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Create remote WebDriver
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options
    )
    
    # Configure driver
    driver.maximize_window()
    driver.implicitly_wait(config.get('timeouts', {}).get('default', 30))
    
    yield driver
    
    # Teardown
    driver.quit()


@pytest.fixture(scope="session") 
def base_url(config):
    """Get application base URL"""
    return config['application']['base_url']
