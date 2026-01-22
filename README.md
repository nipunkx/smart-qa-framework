# 🚀 Smart QA Framework

> **Cloud-Native Test Automation Framework** built with Playwright, Python, and self-hosted Proxmox infrastructure

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Overview

Professional-grade test automation framework demonstrating modern QA engineering practices with **cloud-based infrastructure deployment**. Built on enterprise-grade Proxmox virtualization platform, this framework showcases end-to-end automation capabilities suitable for European tech companies requiring robust, scalable testing solutions.

**Key Differentiators:**
- 🏗️ **Self-Hosted Infrastructure** - Complete Proxmox-based cloud environment
- 🎯 **Production-Ready Architecture** - 3-layer design pattern with separation of concerns
- 🔄 **Multi-Framework Support** - Shared locators for Playwright & Selenium integration
- 📊 **Enterprise Reporting** - Timestamped HTML reports with screenshots and video
- 🌍 **GDPR-Compliant** - Data remains in European infrastructure
- ⚡ **CI/CD Ready** - Designed for Jenkins integration and parallel execution

---

## 🏛️ Architecture

```
smart-qa-framework/
│
├── config/                 # Environment and test configuration
│   └── config.yaml        # Centralized config management
│
├── locators/              # Shared locators (framework-agnostic)
│   └── opencart_locators.py
│
├── pages/                 # Page Object Model
│   └── pw/               # Playwright-specific implementations
│       ├── base_page.py
│       ├── home_page.py
│       └── login_page.py
│
├── tests/                 # Test suites
│   └── frontend/
│       └── playwright/   # Playwright UI tests
│           ├── test_homepage.py
│           └── test_login.py
│
├── utils/                 # Helper utilities
│   ├── config_loader.py
│   └── logger.py
│
└── reports/              # Test artifacts
    ├── html/            # HTML reports
    ├── screenshots/     # Failure screenshots
    └── videos/          # Test execution recordings
```

### **Design Patterns Implemented**
- ✅ **Page Object Model (POM)** - Maintainable, reusable page interactions
- ✅ **Dependency Injection** - Loose coupling via fixtures
- ✅ **Factory Pattern** - Browser instance management
- ✅ **Singleton Pattern** - Configuration management
- ✅ **Strategy Pattern** - Multi-framework selector strategy

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.11 | Modern async/await support |
| **Automation** | Playwright | Fast, reliable browser automation |
| **Test Framework** | pytest | Powerful fixtures and parametrization |
| **Infrastructure** | Proxmox VE | Enterprise virtualization platform |
| **Target App** | OpenCart | E-commerce test environment |
| **Containerization** | Docker & LXC | Lightweight, scalable deployments |
| **CI/CD** | Jenkins *(planned)* | Automated test execution |

---

## 🌐 Infrastructure

### **Proxmox Self-Hosted Cloud**
```
Proxmox Server (192.168.50.15)
├── LXC 103: OpenCart (192.168.50.103)
│   ├── Docker: Web Server
│   ├── Docker: MySQL Database
│   └── Auto-start: Enabled
│
└── VM/LXC: Jenkins CI/CD (planned)
    └── Automated test triggers
```

**Infrastructure Highlights:**
- 🖥️ **Resources:** 31GB RAM, 16 CPU cores, 2.27TB storage
- 🔒 **Network Isolation:** Separate test environment
- 🔄 **Auto-Recovery:** Containers auto-start after host reboot
- 📦 **Container-Based:** Fast provisioning and tear-down

---

## ⚡ Quick Start

### **Prerequisites**
```bash
Python 3.11+
Node.js 18+ (for Playwright)
Git
```

### **Installation**

```bash
# Clone the repository
git clone https://github.com/nipunkx/smart-qa-framework.git
cd smart-qa-framework

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium firefox webkit
```

### **Configuration**

Update `config/config.yaml` with your test environment:

```yaml
opencart:
  base_url: "http://your-opencart-url"
  admin_url: "http://your-opencart-url/admin"
```

---

## 🧪 Running Tests

### **Basic Execution**

```bash
# Run all tests (headless mode)
pytest tests/frontend/playwright/ -v

# Run with browser visible (headed mode)
pytest tests/frontend/playwright/ -v --headed

# Run specific test file
pytest tests/frontend/playwright/test_login.py -v
```

### **Advanced Options**

```bash
# Run smoke tests only
pytest tests/frontend/playwright/ -v -m smoke

# Run with specific browser
pytest tests/frontend/playwright/ -v --browser firefox

# Parallel execution (requires pytest-xdist)
pytest tests/frontend/playwright/ -v -n 4

# Generate HTML report
pytest tests/frontend/playwright/ -v --html=reports/report_$(date +%Y%m%d_%H%M%S).html
```

### **Test Markers**

```python
@pytest.mark.smoke     # Critical path tests
@pytest.mark.regression  # Full test suite
@pytest.mark.slow      # Long-running tests
```

---

## 📊 Test Reports & Artifacts

### **Generated Artifacts**
- 📄 **HTML Reports** - `reports/html/report_YYYYMMDD_HHMMSS.html`
- 📸 **Screenshots** - Auto-captured on test failure
- 🎥 **Videos** - Full test execution recording
- 📝 **Logs** - Detailed execution logs

### **Report Features**
- Timestamped execution history
- Failure screenshot embedding
- Video playback integration
- Test duration metrics
- Environment details

---

## 🎯 Test Coverage

| **Module** | **Test Cases** | **Status** | **Coverage** |
|------------|----------------|------------|--------------|
| Homepage | 7 | ✅ Passing | Navigation, Search, Links |
| User Login | 9 | ✅ Passing | Valid/Invalid credentials, Validation |
| **Total** | **16** | ✅ **100%** | **Core Flows** |

### **Upcoming Test Modules**
- [ ] Product Catalog (Browse, Filter, Sort)
- [ ] Shopping Cart (Add, Update, Remove)
- [ ] Checkout Flow (Guest, Registered User)
- [ ] API Testing (REST endpoints)
- [ ] Performance Testing (Load, Stress)

---

## 🚀 Roadmap

### **Phase 1: Foundation** ✅ *Completed*
- [x] Proxmox infrastructure setup
- [x] OpenCart deployment in Docker
- [x] Playwright framework implementation
- [x] Page Object Model architecture
- [x] Shared locators design
- [x] HTML reporting with screenshots/videos

### **Phase 2: Expansion** 🚧 *In Progress*
- [ ] Selenium integration (cross-browser support)
- [ ] REST API testing suite
- [ ] Test data management (fixtures, factories)
- [ ] GitHub Actions CI/CD pipeline

### **Phase 3: Advanced Features** 📅 *Planned*
- [ ] Jenkins integration on Proxmox
- [ ] Selenoid Grid for parallel execution
- [ ] AI-powered failure analysis (Claude API)
- [ ] Visual regression testing
- [ ] Self-healing locators with AI
- [ ] Performance testing integration

---

## 🏢 Enterprise Features

### **German Market Considerations**
- ✅ **GDPR Compliance** - Self-hosted infrastructure, data sovereignty
- ✅ **European Deployment** - Can be deployed on German/EU cloud providers
- ✅ **Multilingual Support Ready** - Framework structure supports i18n testing
- ✅ **Enterprise Scalability** - Proxmox clustering support for growth

### **DevOps Best Practices**
- Infrastructure as Code (IaC) ready
- Container orchestration capabilities
- Automated environment provisioning
- Blue-green deployment testing support

---

## 🔒 Security & Compliance

- **Credentials:** Stored in `config.yaml` (git-ignored)
- **Secrets Management:** Environment variables for CI/CD
- **Network Isolation:** Proxmox VLAN segmentation
- **Access Control:** Role-based test environment access

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| **Avg Test Duration** | 2-5 seconds |
| **Parallel Execution** | Ready (pytest-xdist) |
| **Browser Startup** | < 1 second |
| **Report Generation** | < 2 seconds |

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Contact & Professional Profile

**Nipun Xavier**  
*Senior QA Automation Engineer | 17+ Years Experience*

- 📧 Email: nipunkx@gmail.com
- 💼 LinkedIn: [linkedin.com/in/nipun-xavier](https://linkedin.com/in/nipun-xavier)
- 🐙 GitHub: [@nipunkx](https://github.com/nipunkx)
- 🌍 Location: Pursuing opportunities in US/Canada/Germany/Australia

**Areas of Expertise:**
- Test Automation Architecture
- CI/CD Pipeline Design
- Cloud Infrastructure (Proxmox, AWS, Azure)
- DevOps Practices
- Agile/Scrum Methodologies

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenCart team for the excellent e-commerce platform
- Playwright team for the modern automation framework
- Proxmox community for the powerful virtualization platform
- Python testing community for pytest excellence

---

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
- [Proxmox VE Documentation](https://pve.proxmox.com/wiki/Main_Page)

---

**⭐ If you find this project helpful, please consider giving it a star!**

*Built with ❤️ for the German Tech Community*
