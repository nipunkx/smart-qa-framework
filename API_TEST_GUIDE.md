# 🚀 API Test Execution Guide

Complete guide for running and managing backend API tests in the automation framework.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Debugging](#debugging)
- [Common Issues](#common-issues)
- [Best Practices](#best-practices)

---

## Overview

The backend API test suite validates OpenCart's REST API functionality including:
- Authentication and session management
- Cart operations (add, remove, update)
- Product management
- Order processing

**Current Status**:
- ✅ 11 API tests
- ✅ 100% passing rate
- ✅ Comprehensive coverage

---

## Prerequisites

### 1. Python Environment

```bash
# Verify Python version (3.11+)
python3 --version

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify requests library
python3 -c "import requests; print(f'Requests version: {requests.__version__}')"
```

### 3. OpenCart Instance

Ensure OpenCart is running and accessible:

```bash
# Test connectivity
curl -I http://192.168.50.103:8080

# Expected: HTTP/1.1 200 OK
```

### 4. API Credentials

Verify API user is configured in `config/config.yaml`:

```yaml
api:
  username: "TestAPIUser"
  key: "your_api_key_here"
```

---

## Configuration

### Environment Setup

**File**: `config/config.yaml`

```yaml
application:
  base_url: "http://192.168.50.103:8080"

api:
  username: "TestAPIUser"
  key: "this_is_the_api_key_for_local_opencart_on_the_automation_project"
  endpoints:
    login: "/index.php?route=api/account/login"
    cart: "/index.php?route=api/sale/cart"
    cart_add: "/index.php?route=api/sale/cart.add"
    cart_remove: "/index.php?route=api/sale/cart.remove"
```

### API User Setup

If API user doesn't exist, create in OpenCart admin:

1. **Login to admin**: http://192.168.50.103:8080/myadmin
2. **Navigate**: System → Users → API
3. **Create API user**:
   - Username: `TestAPIUser`
   - Generate API key
   - Status: Enabled
4. **Add IP whitelist**:
   - IP Address: `192.168.50.150` (your machine)
   - Or: `192.168.50.0/24` (entire subnet)

### Verify Configuration

```bash
# Test API connectivity
cd ~/Projects/automation-framework

python3 << EOF
from utils.api.opencart_api_client import OpenCartAPIClient
from utils.config_reader import ConfigReader

config = ConfigReader().config
client = OpenCartAPIClient(
    config['application']['base_url'],
    config['api']['username'],
    config['api']['key']
)

try:
    result = client.login()
    print("✅ API connection successful!")
    print(f"Token: {result.get('api_token', 'N/A')[:10]}...")
except Exception as e:
    print(f"❌ API connection failed: {e}")
EOF
```

---

## Running Tests

### All API Tests

```bash
# Run all backend API tests
pytest tests/backend/api/ -v

# Expected output:
# ✅ 11 passed in ~1.2s
```

### Specific Test File

```bash
# Run cart API tests only
pytest tests/backend/api/test_cart_api.py -v
```

### Individual Test

```bash
# Run single test
pytest tests/backend/api/test_cart_api.py::TestCartAPI::test_add_product_to_cart -v

# With detailed output
pytest tests/backend/api/test_cart_api.py::TestCartAPI::test_add_product_to_cart -v -s
```

### Test Class

```bash
# Run all tests in a class
pytest tests/backend/api/test_cart_api.py::TestCartAPI -v
```

### With Markers

```bash
# Run smoke tests
pytest tests/backend/api/ -m smoke -v

# Run critical tests
pytest tests/backend/api/ -m critical -v
```

### Parallel Execution

```bash
# Run tests in parallel (4 workers)
pytest tests/backend/api/ -n 4 -v

# Note: Session-scoped fixtures work correctly with xdist
```

### Generate Report

```bash
# HTML report
pytest tests/backend/api/ -v --html=reports/api_report.html --self-contained-html

# Open report
open reports/api_report.html  # macOS
xdg-open reports/api_report.html  # Linux
start reports/api_report.html  # Windows
```

---

## Test Coverage

### Test Categories

#### 1. Basic Operations (7 tests)

**test_get_empty_cart**
- Verifies cart retrieval when empty
- Checks response structure
- Validates default values

**test_add_product_to_cart**
- Adds single product
- Verifies success message
- Checks cart contains product

**test_add_multiple_quantities**
- Adds product with quantity > 1
- Validates quantity in cart

**test_add_multiple_products**
- Adds 2 different products
- Checks cart has both items

**test_cart_totals_calculation**
- Adds products with prices
- Verifies totals calculation
- Checks subtotal and total fields

**test_remove_product_from_cart**
- Adds product
- Removes it by cart_id
- Verifies cart is empty

**test_cart_persistence_across_requests**
- Tests session persistence
- Multiple API calls
- Cart state maintained

#### 2. Error Handling (1 test)

**test_invalid_product_id**
- Attempts to add non-existent product
- Expects error response
- Validates error handling

#### 3. Edge Cases (3 tests)

**test_add_zero_quantity**
- Adds product with quantity = 0
- Tests API validation

**test_add_negative_quantity**
- Adds product with quantity = -1
- Tests boundary conditions

**test_shipping_required_flag**
- Checks shipping_required flag
- Validates based on cart contents

### API Endpoints Tested

| Endpoint | Method | Tests |
|----------|--------|-------|
| `/api/account/login` | POST | Implicit (fixture) |
| `/api/sale/cart` | POST | 7 tests |
| `/api/sale/cart.add` | POST | 5 tests |
| `/api/sale/cart.remove` | POST | 2 tests |

---

## Debugging

### Enable Debug Logging

```bash
# Run with debug output
pytest tests/backend/api/test_cart_api.py -v -s --log-cli-level=DEBUG

# Shows:
# - HTTP requests/responses
# - Cookie handling
# - Session management
# - API responses
```

### Debug Single Test

```bash
# Run one test with full output
pytest tests/backend/api/test_cart_api.py::TestCartAPI::test_add_product_to_cart \
    -v -s --log-cli-level=DEBUG --tb=short
```

### Inspect API Responses

```python
# Add to test for debugging
def test_something(clean_cart):
    response = clean_cart.add_to_cart(43, 1)
    
    # Print response
    import json
    print(json.dumps(response, indent=2))
    
    # Breakpoint
    import pdb; pdb.set_trace()
```

### Manual API Testing

```bash
# Login manually
TOKEN=$(curl -s -X POST 'http://192.168.50.103:8080/index.php?route=api/account/login' \
  -d 'username=TestAPIUser&key=your_api_key' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['api_token'])")

echo "Token: $TOKEN"

# Test cart endpoint
curl -X POST "http://192.168.50.103:8080/index.php?route=api/sale/cart" \
  --cookie "OCSESSID=$TOKEN" | python3 -m json.tool
```

---

## Common Issues

### Issue 1: IP Not Allowed

**Error**:
```
AssertionError: Login failed: Warning: Your IP 192.168.50.150 is not allowed to access this API!
```

**Solution**:
```bash
# SSH to Proxmox
ssh root@192.168.50.15
pct enter 103

# Add your IP to whitelist
docker exec opencart-mysql mysql -u opencart -popencart123 opencart \
  -e "INSERT INTO oc_api_ip (api_id, ip) VALUES (2, '192.168.50.150');"

# Verify
docker exec opencart-mysql mysql -u opencart -popencart123 opencart \
  -e "SELECT * FROM oc_api_ip WHERE api_id = 2;"
```

### Issue 2: Empty Response / JSON Decode Error

**Error**:
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Causes**:
- Session cookie not persisting
- Wrong endpoint
- API user disabled

**Debug**:
```bash
# Check API user status
docker exec opencart-mysql mysql -u opencart -popencart123 opencart \
  -e "SELECT username, status FROM oc_api WHERE username = 'TestAPIUser';"

# Status should be 1 (enabled)
# If 0, update:
docker exec opencart-mysql mysql -u opencart -popencart123 opencart \
  -e "UPDATE oc_api SET status = 1 WHERE username = 'TestAPIUser';"
```

### Issue 3: Tests Failing Due to Dirty Cart

**Error**:
```
AssertionError: Cart should be empty
assert 2 == 0
```

**Solution**:
```python
# Use clean_cart fixture
def test_something(clean_cart):  # ← Use this fixture
    # Cart is automatically cleaned before test
    cart = clean_cart.get_cart()
    assert len(cart['products']) == 0
```

### Issue 4: Configuration Not Found

**Error**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'config/config.yaml'
```

**Solution**:
```bash
# Run from project root
cd ~/Projects/automation-framework
pytest tests/backend/api/ -v

# Or set PYTHONPATH
export PYTHONPATH=.
pytest tests/backend/api/ -v
```

---

## Best Practices

### 1. Use Fixtures for Setup

```python
# ✅ Good - uses fixture
def test_add_to_cart(clean_cart):
    clean_cart.add_to_cart(43, 1)
    # Cart is automatically cleaned after

# ❌ Bad - manual setup
def test_add_to_cart(api_client):
    # Manual cleanup needed
    cart = api_client.get_cart()
    for product in cart['products']:
        api_client.remove_from_cart(product['cart_id'])
```

### 2. Test Independence

```python
# ✅ Good - independent
def test_cart_operations(clean_cart):
    # Starts with empty cart
    # Doesn't rely on previous tests
    
# ❌ Bad - dependent
def test_step_2(api_client):
    # Assumes test_step_1 ran first
```

### 3. Clear Assertions

```python
# ✅ Good - specific message
assert len(cart['products']) == 1, \
    f"Expected 1 product, found {len(cart['products'])}"

# ❌ Bad - no context
assert len(cart['products']) == 1
```

### 4. Use API Client Methods

```python
# ✅ Good - uses client
def test_add_item(clean_cart):
    clean_cart.add_to_cart(43, 1)
    
# ❌ Bad - direct requests
def test_add_item(clean_cart):
    requests.post(url, data={...})
```

### 5. Log Important Actions

```python
# Already built into API client
logger.info(f"Adding product {product_id}")
logger.debug(f"Response: {response.json()}")
```

---

## Performance Tips

### 1. Use Session-Scoped Fixtures

```python
# api_client is session-scoped
# Login happens once, not per test
@pytest.fixture(scope="session")
def api_client(api_config):
    client = OpenCartAPIClient(...)
    client.login()  # ← Only once per session
    return client
```

### 2. Parallel Execution

```bash
# Run tests in parallel
pytest tests/backend/api/ -n 4

# Faster overall execution
# Tests must be independent
```

### 3. Skip Slow Tests in Development

```python
@pytest.mark.slow
def test_long_operation(api_client):
    # Time-consuming test
    pass

# Run fast tests only
pytest -m "not slow" -v
```

---

## Reporting

### HTML Report

```bash
pytest tests/backend/api/ \
    -v \
    --html=reports/api_report.html \
    --self-contained-html
```

**Report Contains**:
- ✅ Pass/fail summary
- ✅ Execution time per test
- ✅ Logs and output
- ✅ Full stack traces on failure

### JSON Report

```bash
pytest tests/backend/api/ \
    --json-report \
    --json-report-file=reports/api_report.json
```

### Custom Logging

```python
# In conftest.py or test file
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports/api_tests.log'),
        logging.StreamHandler()
    ]
)
```

---

## Next Steps

### Expand Coverage

1. **Customer API**: Registration, profile updates
2. **Order API**: Create, retrieve, update orders  
3. **Product API**: Search, filter, details
4. **Payment API**: Payment method selection

### Add Advanced Tests

1. **Load Testing**: Multiple concurrent requests
2. **Security Testing**: Auth bypass attempts
3. **Data Validation**: Schema validation
4. **Performance Testing**: Response time checks

### Improve Framework

1. **Response Models**: Pydantic models for type safety
2. **Test Data Factory**: Dynamic test data generation
3. **API Mocking**: Local mock server for offline testing
4. **Contract Testing**: API contract validation

---

## Resources

- **OpenCart API**: http://192.168.50.103:8080/myadmin
- **Requests Docs**: https://requests.readthedocs.io/
- **pytest Docs**: https://docs.pytest.org/
- **REST API Testing**: https://testautomationu.applitools.com/api-testing-python/

---

**Last Updated**: January 27, 2026  
**Maintained By**: Pat Xavier  
**Status**: Active Development ✅
