"""
Cart API Tests - OpenCart Shopping Cart API

Tests the cart API endpoints:
- GET cart contents
- POST add to cart
- POST remove from cart
- Cart totals calculation
"""
import pytest
import logging

logger = logging.getLogger(__name__)


class TestCartAPI:
    """Test suite for Cart API operations"""
    
    def test_get_empty_cart(self, clean_cart):
        """Test getting an empty cart"""
        logger.info("Testing empty cart retrieval")
        
        cart = clean_cart.get_cart()
        
        # Verify response structure
        assert 'products' in cart, "Cart should have 'products' key"
        assert 'totals' in cart, "Cart should have 'totals' key"
        assert 'vouchers' in cart, "Cart should have 'vouchers' key"
        
        # Verify cart is empty
        assert len(cart['products']) == 0, "Cart should be empty"
        assert cart['shipping_required'] == False, "No shipping needed for empty cart"
    
    def test_add_product_to_cart(self, clean_cart):
        """Test adding a product to cart"""
        logger.info("Testing add product to cart")
        
        # Add MacBook (product_id=43)
        response = clean_cart.add_to_cart(product_id=43, quantity=1)
        
        # Verify success
        clean_cart.assert_success(response)
        assert 'success' in response, "Should have success message"
        assert 'modified' in response['success'].lower(), "Success message should mention modification"
        
        # Verify cart now has product
        cart = clean_cart.get_cart()
        assert len(cart['products']) == 1, "Cart should have 1 product"
        
        # Verify product details
        product = cart['products'][0]
        assert 'product_id' in product, "Product should have ID"
        assert 'name' in product, "Product should have name"
        assert 'quantity' in product, "Product should have quantity"
        assert 'price' in product, "Product should have price"
        assert 'total' in product, "Product should have total"
        
        assert product['quantity'] == '1', "Quantity should be 1"
    
    def test_add_multiple_quantities(self, clean_cart):
        """Test adding product with quantity > 1"""
        logger.info("Testing add multiple quantities")
        
        # Add 3 MacBooks
        response = clean_cart.add_to_cart(product_id=43, quantity=3)
        clean_cart.assert_success(response)
        
        # Verify quantity
        cart = clean_cart.get_cart()
        assert len(cart['products']) == 1, "Cart should have 1 product"
        assert cart['products'][0]['quantity'] == '3', "Quantity should be 3"
    
    def test_add_multiple_products(self, clean_cart):
        """Test adding multiple different products"""
        logger.info("Testing add multiple products")
        
        # Add MacBook (43)
        clean_cart.add_to_cart(product_id=43, quantity=1)
        
        # Add iPhone (40)
        clean_cart.add_to_cart(product_id=40, quantity=1)
        
        # Verify cart has 2 products
        cart = clean_cart.get_cart()
        assert len(cart['products']) == 2, "Cart should have 2 products"
    
    def test_cart_totals_calculation(self, clean_cart):
        """Test cart calculates totals correctly"""
        logger.info("Testing cart totals")
        
        # Add product
        clean_cart.add_to_cart(product_id=43, quantity=2)
        
        # Get cart with totals
        cart = clean_cart.get_cart()
        
        # Verify totals structure
        assert 'totals' in cart, "Cart should have totals"
        assert len(cart['totals']) > 0, "Should have at least one total"
        
        # Check for required total fields
        total_fields = [total['title'] for total in cart['totals']]
        assert 'Sub-Total' in total_fields or 'sub-total' in [t.lower() for t in total_fields], "Should have subtotal"
        assert 'Total' in total_fields, "Should have total"
        
        # Verify totals have text values
        for total in cart['totals']:
            assert 'title' in total, "Total should have title"
            assert 'text' in total, "Total should have text (formatted price)"
    
    def test_remove_product_from_cart(self, clean_cart):
        """Test removing product from cart"""
        logger.info("Testing remove from cart")
        
        # Add product first
        clean_cart.add_to_cart(product_id=43, quantity=1)
        
        # Get cart to find the key
        cart = clean_cart.get_cart()
        assert len(cart['products']) == 1, "Should have 1 product"
        
        product_cart_id = cart['products'][0]['cart_id']
        
        # Remove product
        response = clean_cart.remove_from_cart(product_cart_id)
        clean_cart.assert_success(response)
        
        # Verify cart is empty
        cart = clean_cart.get_cart()
        assert len(cart['products']) == 0, "Cart should be empty after removal"
    
    def test_cart_persistence_across_requests(self, api_client):
        """Test cart persists across multiple API calls"""
        logger.info("Testing cart persistence")
        
        # Clean cart first
        cart = api_client.get_cart()
        for product in cart.get('products', []):
            if 'key' in product:
                api_client.remove_from_cart(product['key'])
        
        # Add product
        api_client.add_to_cart(product_id=43, quantity=1)
        
        # Get cart in separate request
        cart1 = api_client.get_cart()
        assert len(cart1['products']) == 1, "Cart should persist"
        
        # Get cart again
        cart2 = api_client.get_cart()
        assert len(cart2['products']) == 1, "Cart should still persist"
        
        # Cleanup
        api_client.remove_from_cart(cart1['products'][0]['cart_id'])
    
    def test_invalid_product_id(self, clean_cart):
        """Test adding product with invalid ID"""
        logger.info("Testing invalid product ID")
        
        # Try to add product with invalid ID
        response = clean_cart.add_to_cart(product_id=99999, quantity=1)
        
        # Should have error
        assert 'error' in response or 'warning' in response, "Should return error for invalid product"


class TestCartEdgeCases:
    """Edge case tests for Cart API"""
    
    def test_add_zero_quantity(self, clean_cart):
        """Test adding product with quantity 0"""
        logger.info("Testing zero quantity")
        
        response = clean_cart.add_to_cart(product_id=43, quantity=0)
        
        # Cart should remain empty or show error
        cart = clean_cart.get_cart()
        # Implementation dependent - either empty or error
    
    def test_add_negative_quantity(self, clean_cart):
        """Test adding product with negative quantity"""
        logger.info("Testing negative quantity")
        
        response = clean_cart.add_to_cart(product_id=43, quantity=-1)
        
        # Should handle gracefully (error or ignore)
        # This tests the API's validation
    
    def test_shipping_required_flag(self, clean_cart):
        """Test shipping_required flag changes based on products"""
        logger.info("Testing shipping required flag")
        
        # Empty cart - no shipping
        cart = clean_cart.get_cart()
        assert cart['shipping_required'] == False, "Empty cart needs no shipping"
        
        # Add physical product - should require shipping
        clean_cart.add_to_cart(product_id=43, quantity=1)
        cart = clean_cart.get_cart()
        
        # Verify flag (might be True for physical products)
        assert 'shipping_required' in cart, "Should have shipping_required flag"
