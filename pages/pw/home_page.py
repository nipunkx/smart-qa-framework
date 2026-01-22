"""
Home Page - OpenCart Homepage
Uses shared locators + Playwright-specific actions
"""
import logging
from pages.pw.base_page import BasePage
from locators.home_locators import HomeLocators

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    OpenCart Homepage Page Object
    Inherits common methods from BasePage
    """
    
    # ============== ACTIONS ==============
    
    def search_product(self, product_name: str) -> None:
        """Search for a product by name"""
        logger.info(f"Searching for product: {product_name}")
        self.fill(HomeLocators.SEARCH_INPUT, product_name)
        self.click(HomeLocators.SEARCH_BUTTON)
        self.wait_for_load()
    
    def open_cart(self) -> None:
        """Open the shopping cart dropdown"""
        logger.info("Opening cart")
        self.click(HomeLocators.CART_BUTTON)
    
    def get_cart_total(self) -> str:
        """Get the cart total text"""
        return self.get_text(HomeLocators.CART_TOTAL)
    
    def get_featured_products_count(self) -> int:
        """Get count of featured products on homepage"""
        return self.get_element_count(HomeLocators.FEATURED_PRODUCTS)
    
    def get_product_names(self) -> list[str]:
        """Get all featured product names"""
        products = self.page.locator(HomeLocators.PRODUCT_NAME).all()
        return [p.inner_text() for p in products]
    
    def click_product(self, product_name: str) -> None:
        """Click on a product by name"""
        logger.info(f"Clicking product: {product_name}")
        self.page.locator(HomeLocators.PRODUCT_NAME, has_text=product_name).click()
    
    def add_first_product_to_cart(self) -> None:
        """Add the first featured product to cart"""
        logger.info("Adding first product to cart")
        self.page.locator(HomeLocators.ADD_TO_CART_BUTTON).first.click()
    
    # ============== NAVIGATION ==============
    
    def go_to_my_account(self) -> None:
        """Click on My Account link"""
        self.click(HomeLocators.NAV_MY_ACCOUNT)
    
    # ============== VERIFICATIONS ==============
    
    def verify_page_loaded(self) -> None:
        """Verify homepage is loaded correctly"""
        logger.info("Verifying homepage loaded")
        self.expect_title("Your Store")
        self.expect_visible(HomeLocators.LOGO)
    
    def verify_search_box_visible(self) -> None:
        """Verify search box is visible"""
        self.expect_visible(HomeLocators.SEARCH_INPUT)
        self.expect_visible(HomeLocators.SEARCH_BUTTON)
    
    def verify_cart_visible(self) -> None:
        """Verify cart button is visible"""
        self.expect_visible(HomeLocators.CART_BUTTON)
    
    def verify_on_search_results(self) -> None:
        """Verify navigation to search results page"""
        self.expect_url_contains("search")
    
    def verify_products_displayed(self, minimum: int = 1) -> None:
        """Verify at least minimum products are displayed"""
        count = self.get_featured_products_count()
        assert count >= minimum, f"Expected at least {minimum} products, found {count}"

    def click_login(self) -> None:
        """Click My Account → Login"""
        logger.info("Navigating to Login page")
        self.click(HomeLocators.MY_ACCOUNT_DROPDOWN)
        self.click(HomeLocators.LOGIN_LINK)
        self.wait_for_load()

    def click_register(self) -> None:
        """Click My Account → Register"""
        logger.info("Navigating to Register page")
        self.click(HomeLocators.MY_ACCOUNT_DROPDOWN)
        self.click(HomeLocators.REGISTER_LINK)
        self.wait_for_load()