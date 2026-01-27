# 🚀 Test Automation Framework

A comprehensive, production-ready test automation framework demonstrating full-stack QA capabilities for e-commerce applications. Built with modern best practices and designed for scalability.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Test Execution](#test-execution)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This framework demonstrates enterprise-level test automation skills through:

- **Full-Stack Testing**: Frontend (UI) + Backend (API) test coverage
- **Production Architecture**: Page Object Model, fixtures, clean separation of concerns
- **Self-Hosted Infrastructure**: No external dependencies, complete control
- **Real Application Testing**: OpenCart e-commerce platform
- **Professional Practices**: Git workflow, documentation, maintainable code

**Current Test Coverage:**
- ✅ **26 automated tests** (15 UI + 11 API)
- ✅ **100% passing** rate
- ✅ **Comprehensive reporting** with screenshots and videos

---

## 🏗️ Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     Test Automation Framework                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  Frontend Tests  │              │  Backend Tests   │        │
│  │   (Playwright)   │              │   (REST API)     │        │
│  │                  │              │                  │        │
│  │  • Page Objects  │              │  • API Client    │        │
│  │  • Locators      │              │  • Fixtures      │        │
│  │  • 15 UI Tests   │              │  • 11 API Tests  │        │
│  └────────┬─────────┘              └─────────┬────────┘        │
│           │                                  │                  │
│           └──────────────┬───────────────────┘                  │
│                          │                                      │
│                   ┌──────▼──────┐                              │
│                   │   Fixtures   │                              │
│                   │   & Config   │                              │
│                   └──────┬───────┘                              │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────────┐
            │  Application Under Test      │
            │  (OpenCart 4.0.2.3)          │
            │                              │
            │  • Docker Containers         │
            │  • Proxmox LXC 103          │
            │  • Self-Hosted              │
            └──────────────────────────────┘
```

### Infrastructure

**Deployment Environment:**
- **Proxmox VE**: Virtualization platform
- **LXC Container**: Isolated test environment
- **Docker Compose**: Application orchestration
  - OpenCart (PHP 8.1 + Apache)
  - MySQL 8.0

**Benefits:**
- ✅ Complete control over test environment
- ✅ Consistent, reproducible setup
- ✅ No external dependencies
- ✅ Easy scaling and maintenance

---

## ✨ Features

### Frontend Testing (Playwright)
- **Page Object Model** architecture
- **Shared locators** between frameworks
- **Comprehensive coverage**:
  - Homepage navigation and search
  - Product catalog interactions
  - Shopping cart functionality
  - User authentication flows
- **Rich reporting**: HTML reports with screenshots and video recordings
- **Cross-browser support**: Chromium, Firefox, WebKit

### Backend Testing (REST API)
- **Session-based authentication**
- **OpenCart API integration**:
  - Cart operations (add, remove, update)
  - Product management
  - Order processing
- **Comprehensive test coverage**:
  - Happy paths
  - Edge cases
  - Error handling
- **Reusable API client** with logging and assertions

### Quality Practices
- ✅ **Clean Architecture**: Separation of concerns, DRY principles
- ✅ **Type Hints**: Enhanced IDE support and code clarity
- ✅ **Logging**: Comprehensive debug and info logging
- ✅ **Error Handling**: Graceful failures with clear messages
- ✅ **Documentation**: Inline comments and comprehensive README

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|-----------|---------|
| **Language** | Python | 3.11+ |
| **UI Testing** | Playwright | 1.57+ |
| **API Testing** | Requests | 2.32+ |
| **Test Framework** | pytest | 9.0+ |
| **Reporting** | pytest-html | 4.2+ |
| **Config Management** | PyYAML | 6.0+ |
| **Application** | OpenCart | 4.0.2.3 |
| **Database** | MySQL | 8.0 |
| **Container** | Docker | Latest |
| **Virtualization** | Proxmox VE | Latest |

---

## 📁 Project Structure

```
automation-framework/
├── config/                    # Configuration files
│   └── config.yaml           # Application settings
├── locators/                  # Shared element locators
│   ├── __init__.py
│   ├── home_locators.py
│   └── login_locators.py
├── pages/                     # Page Object classes
│   ├── __init__.py
│   └── pw/                   # Playwright pages
│       ├── __init__.py
│       ├── base_page.py      # Base page with common methods
│       ├── home_page.py
│       └── login_page.py
├── tests/                     # Test suites
│   ├── backend/              # API tests
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── conftest.py   # API fixtures
│   │       └── test_cart_api.py
│   └── frontend/             # UI tests
│       ├── __init__.py
│       └── pw/               # Playwright tests
│           ├── __init__.py
│           ├── conftest.py   # UI fixtures
│           ├── test_homepage.py
│           └── test_login.py
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── opencart_api_client.py  # API client
│   └── config_reader.py      # Config loader
├── reports/                   # Test reports (generated)
│   └── screenshots/          # Failure screenshots
├── .gitignore                # Git ignore rules
├── pytest.ini                # pytest configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── ARCHITECTURE.md           # Detailed architecture docs
└── LICENSE                   # MIT License
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv)

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/automation-framework.git
cd automation-framework

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Configuration

Update `config/config.yaml` with your environment details:

```yaml
application:
  base_url: "http://your-opencart-url:8080"
  
timeouts:
  default: 30
  
api:
  username: "your_api_username"
  key: "your_api_key"
```

---

## 🧪 Test Execution

### Run All Tests

```bash
# All tests
pytest -v

# Frontend tests only
pytest tests/frontend/pw/ -v

# Backend tests only
pytest tests/backend/api/ -v
```

### Run Specific Test Files

```bash
# Homepage tests
pytest tests/frontend/pw/test_homepage.py -v

# Cart API tests
pytest tests/backend/api/test_cart_api.py -v
```

### Run with Markers

```bash
# Smoke tests only
pytest -m smoke -v

# Critical path tests
pytest -m critical -v
```

### Generate HTML Report

```bash
pytest -v --html=reports/report.html --self-contained-html
```

### Parallel Execution

```bash
# Run tests in parallel (4 workers)
pytest -n 4 -v
```

### Debug Mode

```bash
# Run with live logs
pytest -v -s --log-cli-level=DEBUG

# Run single test with full output
pytest tests/frontend/pw/test_homepage.py::TestHomepage::test_homepage_loads -v -s
```

---

## 📊 Test Reports

### HTML Reports

After test execution, open `reports/report.html` in a browser to see:
- ✅ Test results summary
- ✅ Pass/fail status
- ✅ Execution time
- ✅ Screenshots (on failure)
- ✅ Video recordings

### Screenshots

Failure screenshots are automatically saved to `reports/screenshots/`:
- Named by test: `test_name_failure.png`
- Captured at moment of failure
- Included in HTML report

### Videos

Playwright videos saved to `reports/videos/`:
- Full test execution recording
- Only for failed tests (configurable)

---

## 🔄 CI/CD Integration

### Future: GitHub Actions (Planned)

```yaml
# .github/workflows/tests.yml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: pytest -v
```

### Current: Self-Hosted Infrastructure

Tests run against self-hosted OpenCart instance:
- No external service dependencies
- Complete environment control
- Consistent test data

---

## 🎓 Key Learning Demonstrations

This framework showcases:

1. **Full-Stack Testing**
   - Frontend: UI interactions, navigation, form submissions
   - Backend: API authentication, CRUD operations, data validation

2. **Clean Architecture**
   - Page Object Model for UI
   - API client abstraction
   - Shared components and DRY principles

3. **Professional Development Practices**
   - Version control (Git)
   - Virtual environments
   - Dependency management
   - Comprehensive documentation

4. **Test Design Patterns**
   - Fixtures for test setup/teardown
   - Parameterized tests
   - Test markers for organization
   - Independent test isolation

5. **DevOps Knowledge**
   - Docker containerization
   - Proxmox virtualization
   - Self-hosted infrastructure
   - Environment configuration

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Update documentation
6. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Pat Xavier** - Senior QA Automation Engineer

- **Experience**: 17+ years in software testing and automation
- **Expertise**: Full-stack test automation, DevOps, CI/CD
- **Focus**: German tech market positioning

---

## 📞 Contact & Links

- **GitHub**: [Your GitHub Profile]
- **LinkedIn**: [Your LinkedIn Profile]
- **Email**: your.email@example.com

---

## 🎯 Project Goals

This framework was built to demonstrate:

✅ **Enterprise-level automation skills** for senior QA roles  
✅ **Full-stack testing capabilities** (UI + API)  
✅ **Clean, maintainable code** following best practices  
✅ **Self-hosted infrastructure** knowledge  
✅ **Professional documentation** and communication

**Target Audience**: German tech companies seeking senior test automation engineers with comprehensive skill sets.

---

**Last Updated**: January 27, 2026  
**Status**: Active Development ✅  
**Test Coverage**: 26 tests, 100% passing 🎉
