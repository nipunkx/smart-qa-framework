"""
OpenCart Homepage Tests

Clean tests using Page Object Model.
Tests are readable, maintainable, and follow best practices.

Run: pytest tests/frontend/playwright/test_homepage.py -v --headed
"""
import pytest
from pages.pw.home_page import HomePage


@pytest.mark.smoke
class TestHomepage:
    """Test OpenCart homepage functionality"""
    
    def test_homepage_loads(self, home_page: HomePage):
        """
        GIVEN: User navigates to OpenCart homepage
        WHEN: Page loads completely
        THEN: Page title and logo should be visible
        """
        home_page.verify_page_loaded()
    
    def test_search_box_is_visible(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: Looking at the header
        THEN: Search box should be visible and functional
        """
        home_page.verify_search_box_visible()
    
    def test_cart_is_visible(self, home_page: HomePage):
        """
        GIVEN: User is on homepage  
        WHEN: Looking at the header
        THEN: Shopping cart button should be visible
        """
        home_page.verify_cart_visible()


@pytest.mark.smoke
@pytest.mark.regression
class TestProductSearch:
    """Test product search functionality"""
    
    def test_search_for_product(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: User searches for 'mac'
        THEN: User should be redirected to search results page
        """
        home_page.search_product("mac")
        home_page.verify_on_search_results()
    
    def test_search_for_nonexistent_product(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: User searches for a product that doesn't exist
        THEN: User should see search results (possibly empty)
        """
        home_page.search_product("xyznonexistent123")
        home_page.verify_on_search_results()


@pytest.mark.regression
class TestFeaturedProducts:
    """Test featured products section"""
    
    def test_featured_products_displayed(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: Looking at featured products section
        THEN: At least one product should be displayed
        """
        home_page.verify_products_displayed(minimum=1)
    
    def test_can_get_product_names(self, home_page: HomePage):
        """
        GIVEN: User is on homepage
        WHEN: Getting featured product names
        THEN: Product names should be non-empty strings
        """
        product_names = home_page.get_product_names()
        assert len(product_names) > 0, "No products found"
        assert all(name.strip() for name in product_names), "Empty product name found"