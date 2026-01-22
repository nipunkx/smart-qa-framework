"""
Home Page Locators
Shared between Playwright & Selenium - Only CSS/XPath strings
"""


class HomeLocators:
    """OpenCart Homepage Locators"""
    
    # Header
    LOGO = "#logo"
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "#search button"
    CART_BUTTON = "#header-cart"
    CART_TOTAL = "#header-cart .btn-inverse"
    
    # Navigation
    NAVBAR = ".navbar"
    NAV_CURRENCY = "#form-currency"
    NAV_MY_ACCOUNT = "a[title='My Account']"
    NAV_WISHLIST = "#wishlist-total"
    
    # Main Content
    FEATURED_PRODUCTS = "#content .product-thumb"
    PRODUCT_NAME = ".product-thumb .description h4 a"
    PRODUCT_PRICE = ".product-thumb .price"
    ADD_TO_CART_BUTTON = "button[title='Add to Cart']"
    
    # Footer
    FOOTER = "footer"
    FOOTER_LINKS = "footer a"

    # My Account Dropdown
    MY_ACCOUNT_DROPDOWN = "a.dropdown-toggle:has-text('My Account')"
    LOGIN_LINK = "a.dropdown-item:has-text('Login')"
    REGISTER_LINK = "a.dropdown-item:has-text('Register')"
    LOGOUT_LINK = "a.dropdown-item:has-text('Logout')"