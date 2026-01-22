# Cloud-Based Automation Testing Framework

A professional test automation framework built with Playwright, Python, and Proxmox infrastructure.

## Architecture
```
├── locators/          # Shared locators (Playwright & Selenium)
├── pages/pw/          # Playwright Page Objects
├── tests/frontend/pw/ # Playwright UI Tests
├── config/            # Configuration files
└── reports/           # Test reports, screenshots, videos
```

## Tech Stack

- **Python 3.11** - Programming language
- **Playwright** - Modern browser automation
- **pytest** - Test framework
- **Page Object Model** - Design pattern
- **Proxmox** - Infrastructure (OpenCart deployed)
- **Docker** - Containerization

## Features

- ✅ 3-layer architecture (locators → pages → tests)
- ✅ Shared locators for multi-framework support
- ✅ Auto-screenshots on failure
- ✅ Video recording
- ✅ Timestamped HTML reports
- ✅ Parallel test execution ready
- ✅ CI/CD ready (Jenkins integration planned)

## Prerequisites

- Python 3.11+
- Node.js (for Playwright browsers)

## Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/automation-framework.git
cd automation-framework

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## 🧪 Running Tests
```bash
# Run all tests (headless)
pytest tests/frontend/pw/ -v

# Run with browser visible
pytest tests/frontend/pw/ -v --headed

# Run smoke tests only
pytest tests/frontend/pw/ -v -m smoke

# Run with HTML report
pytest tests/frontend/pw/ -v --html=reports/report.html
```

## 📊 Test Reports

Reports are generated in `reports/html/` with timestamps.

## Test Coverage

| Module | Tests | Status |
|--------|-------|--------|
| Homepage | 7 | ✅ |
| Login | 9 | ✅ |
| **Total** | **16** | ✅ |

## Roadmap

- [ ] Selenium integration
- [ ] API tests
- [ ] Jenkins CI/CD pipeline
- [ ] AI-powered failure analysis
- [ ] Visual regression testing

## 👤 Author

**Nipun Xavier**  
Senior QA Automation Engineer | 17+ Years Experience

## 📄 License

MIT License