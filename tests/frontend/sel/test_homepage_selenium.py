"""
Selenium Homepage Tests - Running on Selenoid
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TestHomepageSelenium:
    """Homepage tests using Selenium + Selenoid"""
    
    @pytest.mark.browser("chrome")
    def test_homepage_loads_chrome(self, driver, base_url):
        """Test homepage loads successfully in Chrome"""
        driver.get(base_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Verify title
        assert "Your Store" in driver.title
        
        # Verify logo is visible
        logo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#logo img"))
        )
        assert logo.is_displayed()
    
    @pytest.mark.browser("firefox")
    def test_homepage_loads_firefox(self, driver, base_url):
        """Test homepage loads successfully in Firefox"""
        driver.get(base_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Verify title
        assert "Your Store" in driver.title
        
        # Verify logo is visible
        logo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#logo img"))
        )
        assert logo.is_displayed()
    
    @pytest.mark.browser("chrome")
    def test_search_functionality(self, driver, base_url):
        """Test search functionality works"""
        driver.get(base_url)
        
        # Find search input
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        
        # Enter search term
        search_input.send_keys("MacBook")
        search_input.send_keys(Keys.RETURN)
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".product-thumb"))
        )
        
        # Verify we're on search results page
        assert "search=MacBook" in driver.current_url
        
        # Verify results contain MacBook
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "MacBook" in page_text
    
    @pytest.mark.browser("chrome")
    def test_cart_icon_visible(self, driver, base_url):
        """Test shopping cart icon is visible"""
        driver.get(base_url)
        
        # Wait for cart button
        cart_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#header-cart button, #cart button, button[title*='cart' i]"))
        )
        
        assert cart_button.is_displayed()
        
        # Verify cart shows empty or has item count
        cart_text = cart_button.text
        assert "Cart" in cart_text or "item" in cart_text.lower()
    
    @pytest.mark.browser("firefox")
    def test_navigation_menu_present(self, driver, base_url):
        """Test navigation menu is present and has items"""
        driver.get(base_url)
        
        # Wait for navigation menu
        nav_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#menu"))
        )
        
        assert nav_menu.is_displayed()
        
        # Verify menu has items
        menu_items = nav_menu.find_elements(By.TAG_NAME, "a")
        assert len(menu_items) > 0, "Navigation menu should have items"
