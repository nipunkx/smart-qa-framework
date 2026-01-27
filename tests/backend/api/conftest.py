"""
API Test Configuration and Fixtures
"""
import pytest
from utils.api.opencart_api_client import OpenCartAPIClient
from utils.config_reader import ConfigReader


@pytest.fixture(scope="session")
def api_config():
    """Load API configuration"""
    config_reader = ConfigReader()
    return config_reader.config


@pytest.fixture(scope="session")
def api_client(api_config):
    """
    Create authenticated API client for the session
    
    Returns:
        OpenCartAPIClient: Authenticated API client
    """
    base_url = api_config['application']['base_url']
    username = api_config['api']['username']
    api_key = api_config['api']['key']
    
    client = OpenCartAPIClient(base_url, username, api_key)
    
    # Login once for the session
    client.login()
    
    yield client
    
    # Cleanup (if needed)


@pytest.fixture
def clean_cart(api_client):
    """
    Ensure cart is empty before test
    
    Yields:
        OpenCartAPIClient: API client with clean cart
    """
    # Get current cart
    cart = api_client.get_cart()
    
    # Remove all items using cart_id (not 'key')
    if 'products' in cart and cart['products']:
        for product in cart['products']:
            if 'cart_id' in product:
                api_client.remove_from_cart(product['cart_id'])
    
    yield api_client
    
    # Cleanup after test
    cart = api_client.get_cart()
    if 'products' in cart and cart['products']:
        for product in cart['products']:
            if 'cart_id' in product:
                api_client.remove_from_cart(product['cart_id'])
