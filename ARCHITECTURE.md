# 🏗️ Architecture Documentation

## Table of Contents

- [Overview](#overview)
- [Design Principles](#design-principles)
- [System Architecture](#system-architecture)
- [Component Details](#component-details)
- [Design Decisions](#design-decisions)
- [Infrastructure Setup](#infrastructure-setup)
- [Testing Strategy](#testing-strategy)
- [Future Enhancements](#future-enhancements)

---

## Overview

This document describes the architectural decisions, design patterns, and infrastructure setup for the test automation framework.

### Goals

1. **Scalability**: Framework can grow with project needs
2. **Maintainability**: Easy to update and extend
3. **Reliability**: Consistent, repeatable test execution
4. **Independence**: Self-hosted, no external dependencies
5. **Professional Quality**: Production-ready code standards

---

## Design Principles

### 1. Separation of Concerns

Each component has a single, well-defined responsibility:

- **Locators**: Element identification only
- **Page Objects**: Page interactions and business logic
- **Tests**: Test scenarios and assertions
- **Fixtures**: Test setup, teardown, and data
- **Configuration**: Environment-specific settings

**Benefits**:
- Easy to modify without breaking other parts
- Clear ownership of functionality
- Reduced code duplication

### 2. DRY (Don't Repeat Yourself)

Shared functionality is extracted and reused:

- **Base Page**: Common page operations
- **Shared Locators**: Single source of truth for selectors
- **API Client**: Reusable HTTP methods
- **Fixtures**: Common test setup

**Benefits**:
- Single point of modification
- Consistent behavior across tests
- Reduced maintenance burden

### 3. Explicit Over Implicit

Code clarity prioritized over brevity:

- Type hints for all function parameters
- Descriptive variable and function names
- Comprehensive docstrings
- Clear error messages

**Benefits**:
- Better IDE support (autocomplete, type checking)
- Easier onboarding for new developers
- Self-documenting code

### 4. Fail-Fast Philosophy

Issues caught early with clear feedback:

- Input validation at method entry
- Immediate assertion failures
- Comprehensive logging
- Detailed error messages

**Benefits**:
- Faster debugging
- Clearer root cause identification
- Reduced wasted test execution time

---

## System Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    TEST LAYER                            │
│  - Test scenarios                                        │
│  - Assertions                                            │
│  - Test data                                             │
│  Files: test_*.py                                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  ABSTRACTION LAYER                       │
│  - Page Objects (UI)                                     │
│  - API Clients (Backend)                                 │
│  - Fixtures                                              │
│  - Utilities                                             │
│  Files: pages/, utils/, conftest.py                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   DATA LAYER                             │
│  - Locators                                              │
│  - Configuration                                         │
│  - Test data                                             │
│  Files: locators/, config/                               │
└──────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**Test Layer**:
- Implements test scenarios
- Defines expected outcomes
- Uses page objects and API clients
- Independent of implementation details

**Abstraction Layer**:
- Provides high-level interfaces
- Handles interaction logic
- Manages state and sessions
- Translates test intent to actions

**Data Layer**:
- Stores element selectors
- Holds configuration
- Provides test data
- Centralized data management

---

## Component Details

### Frontend Testing (Playwright)

#### Base Page (`pages/pw/base_page.py`)

**Purpose**: Foundation for all page objects with common operations.

**Responsibilities**:
- Navigation and page loading
- Element interactions (click, type, select)
- Waits and synchronization
- Assertions and verifications
- Screenshot and debugging utilities

**Key Methods**:
```python
- navigate(path): Navigate to URL
- click(locator): Click element with wait
- fill(locator, text): Enter text in input
- expect_visible(locator): Assert element visible
- get_text(locator): Extract element text
- wait_for_load(): Wait for page ready
```

**Design Decisions**:
- **Safe Configuration**: Uses `.get()` with defaults to prevent KeyError
- **Comprehensive Logging**: All actions logged for debugging
- **Flexible Waits**: Multiple wait strategies for different scenarios
- **Error Handling**: Clear error messages with context

#### Page Objects (`pages/pw/*.py`)

**Purpose**: Represent individual pages with their specific operations.

**Pattern**: Each page object:
1. Inherits from BasePage
2. Uses shared locators
3. Implements page-specific actions
4. Provides verification methods

**Example Structure**:
```python
class HomePage(BasePage):
    # Actions
    def search_product(self, name): ...
    def add_to_cart(self): ...
    
    # Verifications
    def verify_page_loaded(self): ...
    def verify_search_results(self): ...
```

**Benefits**:
- Tests read like user stories
- Changes isolated to page objects
- Reusable across multiple tests

#### Shared Locators (`locators/*.py`)

**Purpose**: Single source of truth for element selectors.

**Structure**:
```python
class HomeLocators:
    SEARCH_INPUT = "#search > input"
    SEARCH_BUTTON = "#search > button"
    CART_BUTTON = "#cart > button"
```

**Benefits**:
- One place to update selectors
- Shared between frameworks (Playwright/Selenium)
- Easy to find and modify
- Type-safe (class constants)

### Backend Testing (REST API)

#### API Client (`utils/api/opencart_api_client.py`)

**Purpose**: Abstraction for OpenCart REST API interactions.

**Responsibilities**:
- Authentication and session management
- HTTP request methods (GET, POST, DELETE)
- Response parsing and validation
- Error handling and logging

**Key Features**:

1. **Session Management**:
```python
def login(self):
    # Authenticates and stores session token
    # Sets cookie for subsequent requests
```

2. **Cookie Handling**:
```python
# Explicit domain for cookie persistence
self.session.cookies.set(
    'OCSESSID', 
    token,
    domain='192.168.50.103',
    path='/'
)
```

3. **Request Wrapping**:
```python
def post(self, route, data):
    # Ensures authentication
    # Logs request/response
    # Returns parsed response
```

**Design Decisions**:
- **Session-Based Auth**: Matches OpenCart's authentication model
- **Explicit Cookie Domain**: Ensures cookie persistence
- **Comprehensive Logging**: Full request/response visibility
- **Helper Methods**: High-level operations (add_to_cart, etc.)

#### API Fixtures (`tests/backend/api/conftest.py`)

**Purpose**: Setup and teardown for API tests.

**Key Fixtures**:

1. **api_config**: Loads configuration
2. **api_client**: Authenticated session (session-scoped)
3. **clean_cart**: Empty cart before/after test

**Design Pattern**:
```python
@pytest.fixture
def clean_cart(api_client):
    # Setup: Clear cart
    cart = api_client.get_cart()
    for product in cart['products']:
        api_client.remove_from_cart(product['cart_id'])
    
    yield api_client
    
    # Teardown: Clear cart again
    cart = api_client.get_cart()
    for product in cart['products']:
        api_client.remove_from_cart(product['cart_id'])
```

**Benefits**:
- Test isolation
- Consistent starting state
- Automatic cleanup
- Reusable setup logic

---

## Design Decisions

### 1. Why Self-Hosted Infrastructure?

**Decision**: Deploy test application in Proxmox LXC containers.

**Rationale**:
- **Control**: Complete control over environment
- **Consistency**: Same setup every time
- **No External Dependencies**: Works offline
- **Cost**: No cloud service fees
- **Learning**: Demonstrates DevOps skills

**Trade-offs**:
- Setup complexity (one-time)
- Maintenance responsibility
- Hardware requirements

**Verdict**: ✅ Worth it for portfolio demonstration and skill showcase

### 2. Why Playwright Over Selenium?

**Decision**: Use Playwright as primary UI testing tool.

**Rationale**:
- **Modern API**: Clean, intuitive syntax
- **Built-in Waits**: Auto-wait reduces flakiness
- **Performance**: Faster execution
- **Rich Features**: Video, screenshots, tracing built-in
- **Active Development**: Regular updates

**Trade-offs**:
- Smaller community (vs Selenium)
- Newer tool (less established)

**Verdict**: ✅ Best choice for new projects, demonstrates cutting-edge skills

### 3. Why Shared Locators?

**Decision**: Extract locators to separate files shared between frameworks.

**Rationale**:
- **DRY**: Single source of truth
- **Flexibility**: Easy to switch frameworks
- **Maintenance**: Update once, affects all
- **Clarity**: Clear naming conventions

**Trade-offs**:
- Extra files to manage
- Learning curve for new developers

**Verdict**: ✅ Worth it for maintainability and flexibility

### 4. Why Session-Scoped API Client?

**Decision**: Create one authenticated session for all API tests.

**Rationale**:
- **Performance**: Login once, not per test
- **Resource Efficiency**: Fewer connections
- **Realistic**: Matches real user behavior

**Trade-offs**:
- Shared state between tests
- Need for proper cleanup

**Verdict**: ✅ With proper `clean_cart` fixture, benefits outweigh risks

### 5. Why YAML for Configuration?

**Decision**: Use YAML for config files.

**Rationale**:
- **Human-Readable**: Easy to edit
- **Hierarchical**: Natural structure for nested config
- **Comments**: Can add explanations
- **Standard**: Widely used in DevOps

**Trade-offs**:
- Requires PyYAML dependency
- Can be error-prone with indentation

**Verdict**: ✅ Industry standard, worth learning

---

## Infrastructure Setup

### Proxmox Architecture

```
┌──────────────────────────────────────────────────┐
│              Proxmox Host (192.168.50.15)         │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │  LXC Container 103 (OpenCart Test Env)     │  │
│  │  IP: 192.168.50.103                        │  │
│  │                                             │  │
│  │  ┌─────────────────────────────────────┐   │  │
│  │  │   Docker Compose Environment        │   │  │
│  │  │                                     │   │  │
│  │  │  ┌──────────────┐  ┌────────────┐  │   │  │
│  │  │  │  OpenCart    │  │   MySQL    │  │   │  │
│  │  │  │  Container   │  │  Container │  │   │  │
│  │  │  │              │  │            │  │   │  │
│  │  │  │  PHP 8.1     │  │  MySQL 8.0 │  │   │  │
│  │  │  │  Apache      │  │            │  │   │  │
│  │  │  │  Port 8080   │  │  Port 3306 │  │   │  │
│  │  │  └──────────────┘  └────────────┘  │   │  │
│  │  └─────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
         │
         │ Network: 192.168.50.0/24
         │
         ▼
┌──────────────────────────────────────────────────┐
│     Development Machine (192.168.50.150)         │
│     - Runs test automation framework             │
│     - Accesses OpenCart at 192.168.50.103:8080   │
└──────────────────────────────────────────────────┘
```

### Network Configuration

- **Proxmox Host**: 192.168.50.15
- **LXC Container**: 192.168.50.103
- **Development Machine**: 192.168.50.150
- **Network**: 192.168.50.0/24

### Container Resources

- **RAM**: 2GB (expandable to 26GB available)
- **CPU**: 2 cores (16 available)
- **Storage**: 20GB (1.8TB available)

---

## Testing Strategy

### Test Pyramid

```
        ┌─────────────┐
        │     E2E     │  ← Few, critical flows
        │   (UI)      │
        ├─────────────┤
        │             │
        │ Integration │  ← API tests, component tests
        │   (API)     │
        │             │
        ├─────────────┤
        │             │
        │             │
        │    Unit     │  ← Many, fast, focused
        │             │
        │             │
        └─────────────┘
```

**Current Implementation**:
- **UI Tests (15)**: Critical user journeys
- **API Tests (11)**: Backend operations
- **Unit Tests**: (Planned)

### Test Organization

Tests organized by:
1. **Layer**: Frontend vs Backend
2. **Feature**: Homepage, Login, Cart, etc.
3. **Priority**: Smoke, Regression, Critical

### Test Independence

Each test:
- ✅ Runs independently
- ✅ Has own setup/teardown
- ✅ Doesn't rely on other tests
- ✅ Can run in any order
- ✅ Can run in parallel

---

## Future Enhancements

### Phase 1: Infrastructure (Planned)
- [ ] Jenkins CI/CD server
- [ ] Selenoid for parallel browser execution
- [ ] Allure reporting
- [ ] Test data management

### Phase 2: Coverage Expansion
- [ ] Additional API endpoints
- [ ] Checkout flow tests
- [ ] User registration tests
- [ ] Admin panel tests

### Phase 3: Advanced Features
- [ ] Visual regression testing
- [ ] Performance testing
- [ ] Accessibility testing
- [ ] Mobile testing

### Phase 4: AI Integration
- [ ] AI-powered test generation
- [ ] Self-healing locators
- [ ] Intelligent failure analysis
- [ ] Auto-report generation

---

## Lessons Learned

### What Worked Well

1. **Page Object Model**: Clean separation, easy maintenance
2. **Shared Locators**: Single source of truth
3. **Self-Hosted**: Complete control, reliable
4. **Comprehensive Logging**: Easy debugging
5. **Clean Architecture**: Easy to extend

### Challenges Overcome

1. **OpenCart API Discovery**: No official docs, had to explore source
2. **Session Cookie Handling**: Required explicit domain setting
3. **Test Isolation**: Needed proper cleanup fixtures
4. **Import Path Issues**: Solved with pytest.ini pythonpath
5. **ngrok Limitations**: Chose self-hosted over external services

### Key Takeaways

1. **Plan Infrastructure Early**: Validate API availability before building
2. **Test Fixtures Carefully**: Proper cleanup prevents mysterious failures
3. **Log Everything**: Debugging is 10x easier with good logs
4. **Documentation Matters**: Future you will thank present you
5. **Self-Hosting**: More work upfront, but worth it for control

---

## References

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [OpenCart Developer Guide](https://docs.opencart.com/)
- [Page Object Model Pattern](https://martinfowler.com/bliki/PageObject.html)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

---

**Last Updated**: January 27, 2026  
**Version**: 1.0  
**Status**: Active Development
