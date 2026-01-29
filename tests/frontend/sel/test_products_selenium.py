"""
Selenium Product Tests - Running on Selenoid
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestProductsSelenium:
    """Product interaction tests using Selenium + Selenoid"""
    
    @pytest.mark.browser("chrome")
    def test_product_page_loads(self, driver, base_url):
        """Test individual product page loads"""
        # Navigate to MacBook product
        driver.get(f"{base_url}/index.php?route=product/product&product_id=43")
        
        # Wait for product title
        product_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        
        assert "MacBook" in product_title.text
        
        # Verify add to cart button exists
        add_to_cart = driver.find_element(By.ID, "button-cart")
        assert add_to_cart.is_displayed()
    
    @pytest.mark.browser("firefox")
    def test_add_to_cart(self, driver, base_url):
        """Test adding product to cart"""
        # Navigate to product page
        driver.get(f"{base_url}/index.php?route=product/product&product_id=43")
        
        # Wait for add to cart button
        add_to_cart = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-cart"))
        )
        
        # Click add to cart
        add_to_cart.click()
        
        # Wait for success message
        success_alert = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        
        assert success_alert.is_displayed()
        assert "Success" in success_alert.text
    
    @pytest.mark.browser("chrome")  
    def test_product_image_displayed(self, driver, base_url):
        """Test product image is displayed"""
        driver.get(f"{base_url}/index.php?route=product/product&product_id=43")
        
        # Wait for product image
        product_image = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-image img, .image img, img[title*='MacBook']"))
        )
        
        assert product_image.is_displayed()
        assert product_image.get_attribute("src") != ""
