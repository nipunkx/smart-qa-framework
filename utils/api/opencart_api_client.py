"""
OpenCart API Client - Handles authentication and API requests

Uses session-based authentication with OCSESSID cookie
"""
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class OpenCartAPIClient:
    """
    OpenCart API client with session-based authentication
    
    Usage:
        client = OpenCartAPIClient(base_url, username, api_key)
        client.login()
        response = client.get_cart()
    """
    
    def __init__(self, base_url: str, username: str, api_key: str):
        """
        Initialize OpenCart API client
        
        Args:
            base_url: Base URL (e.g., http://192.168.50.103:8080)
            username: API username
            api_key: API key
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_key = api_key
        self.session = requests.Session()
        self.api_token = None
        
        logger.debug(f"Initialized OpenCart API client for: {base_url}")
    
    def login(self) -> Dict[str, Any]:
        """
        Login to API and get session token
        
        Returns:
            Login response JSON
            
        Raises:
            AssertionError: If login fails
        """
        url = f"{self.base_url}/index.php?route=api/account/login"
        
        logger.info(f"Logging in as: {self.username}")
        
        response = self.session.post(
            url,
            data={
                'username': self.username,
                'key': self.api_key
            }
        )
        
        response_json = response.json()
        logger.debug(f"Login response: {response_json}")
        
        # Check for errors
        if 'error' in response_json:
            raise AssertionError(f"Login failed: {response_json['error']}")
        
        # Extract and store token
        if 'api_token' in response_json:
            self.api_token = response_json['api_token']
            # Set session cookie with domain
            self.session.cookies.set(
                'OCSESSID', 
                self.api_token,
                domain='192.168.50.103',
                path='/'
            )
            logger.info(f"Login successful, token: {self.api_token[:10]}...")
            logger.debug(f"Session cookies: {self.session.cookies}")
        else:
            raise AssertionError("No api_token in response")
        
        return response_json
    
    def _build_url(self, route: str) -> str:
        """
        Build full URL from route
        
        Args:
            route: API route (e.g., api/sale/cart)
            
        Returns:
            Full URL
        """
        if route.startswith('/'):
            route = route.lstrip('/')
        
        if route.startswith('index.php'):
            return f"{self.base_url}/{route}"
        
        return f"{self.base_url}/index.php?route={route}"
    
    def _ensure_authenticated(self):
        """Ensure we have a valid session token"""
        if not self.api_token:
            raise AssertionError("Not authenticated. Call login() first.")
    
    def get(self, route: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Send GET request to API
        
        Args:
            route: API route
            params: Query parameters
            
        Returns:
            Response object
        """
        self._ensure_authenticated()
        url = self._build_url(route)
        
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params)
        logger.debug(f"Response [{response.status_code}]: {response.text[:200]}")
        
        return response
    
    def post(self, route: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> requests.Response:
        """
        Send POST request to API
        
        Args:
            route: API route
            data: Form data
            json: JSON data
            
        Returns:
            Response object
        """
        self._ensure_authenticated()
        url = self._build_url(route)
        
        logger.info(f"POST {url}")
        if data:
            logger.debug(f"Data: {data}")
        if json:
            logger.debug(f"JSON: {json}")
        
        response = self.session.post(url, data=data, json=json)
        logger.debug(f"Response [{response.status_code}]: {response.text[:200]}")
        
        return response
    
    def delete(self, route: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Send DELETE request (via POST with data)
        
        Args:
            route: API route
            data: Form data
            
        Returns:
            Response object
        """
        # OpenCart often uses POST for delete operations
        return self.post(route, data=data)
    
    # ============== CART API ==============
    
    def get_cart(self) -> Dict[str, Any]:
        """
        Get cart contents
        
        Returns:
            Cart data
        """
        # OpenCart cart.index() method responds to GET requests
        response = self.get('api/sale/cart')
        
        # Debug: log response
        logger.debug(f"Cart response status: {response.status_code}")
        logger.debug(f"Cart response text: {response.text[:500]}")
        
        # Check if response has content
        if not response.text or response.text.strip() == '':
            logger.error("Empty response from cart API")
            return {"products": [], "totals": [], "vouchers": [], "shipping_required": False}
        
        try:
            return response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON: {response.text}")
            raise AssertionError(f"Invalid JSON response: {response.text[:200]}") from e
    
    def add_to_cart(self, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        """
        Add product to cart
        
        Args:
            product_id: Product ID
            quantity: Quantity to add
            
        Returns:
            Response JSON
        """
        logger.info(f"Adding product {product_id} (qty: {quantity}) to cart")
        response = self.post(
            'api/sale/cart.add',
            data={
                'product_id': product_id,
                'quantity': quantity
            }
        )
        return response.json()
    
    def remove_from_cart(self, cart_id: int) -> Dict[str, Any]:
        """
        Remove item from cart
        
        Args:
            cart_id: Cart item ID (called 'key' in OpenCart, but it's the cart_id from products)
            
        Returns:
            Response JSON
        """
        logger.info(f"Removing cart item: {cart_id}")
        response = self.post(
            'api/sale/cart.remove',
            data={'key': cart_id}
        )
        return response.json()
    
    # ============== CUSTOMER API ==============
    
    def set_customer(self, customer_data: Dict) -> Dict[str, Any]:
        """
        Set customer information
        
        Args:
            customer_data: Customer details
            
        Returns:
            Response JSON
        """
        logger.info("Setting customer information")
        response = self.post('api/sale/customer', data=customer_data)
        return response.json()
    
    # ============== ORDER API ==============
    
    def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Get order details
        
        Args:
            order_id: Order ID
            
        Returns:
            Order data
        """
        logger.info(f"Getting order: {order_id}")
        response = self.post(
            'api/sale/order.load',
            data={'order_id': order_id}
        )
        return response.json()
    
    # ============== HELPERS ==============
    
    def assert_success(self, response_json: Dict) -> None:
        """
        Assert API response is successful
        
        Args:
            response_json: Response JSON
            
        Raises:
            AssertionError: If response contains error
        """
        if 'error' in response_json:
            raise AssertionError(f"API error: {response_json['error']}")
    
    def assert_has_key(self, response_json: Dict, key: str) -> None:
        """
        Assert response has required key
        
        Args:
            response_json: Response JSON
            key: Required key
            
        Raises:
            AssertionError: If key missing
        """
        assert key in response_json, f"Response missing key: {key}"
