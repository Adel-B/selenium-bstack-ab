# BrowserStack Selenium Test Automation Framework

 Cross-browser test automation framework for product favoriting functionality across multiple platforms using BrowserStack. Demonstrates industry best practices for CI/CD integration, Page Object Model, and comprehensive test reporting.

## ✅ Implementation Overview

**Test Scenario**: Samsung Galaxy S20+ favoriting workflow
- Login to `www.bstackdemo.com`
- Filter products by Samsung brand
- Favorite Galaxy S20+ device
- Verify product appears on favorites page

**Cross-Platform Execution**: Parallel testing across Windows Chrome, macOS Firefox, and Samsung Galaxy S22

## 🚀 Quick Start

### Prerequisites
- Python 3.10+, [uv package manager](https://github.com/astral-sh/uv), BrowserStack account

### Setup
```bash
git clone <repository-url> && cd selenium-bstack-ab
uv sync  # Auto-creates virtual environment and installs dependencies

# Configure BrowserStack credentials
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key
```

### Run Tests
```bash
./test-pipeline-local.sh                    # Full pipeline with quality checks
uv run pytest tests/test_samsung_favorite_galaxy.py -n 3 -v  # Direct execution
```

## 🏗️ Architecture

```
selenium-bstack-ab/
├── tests/                      # Test implementation
├── pages/                      # Page Object Model
├── utils/                      # Configuration & utilities
├── scripts/                    # Development automation
├── Jenkinsfile                 # CI/CD pipeline
└── pyproject.toml             # Dependencies & tool config
```

**Design Patterns**: Page Object Model, environment-based configuration, BrowserStack SDK integration

## 🔧 Jenkins CI/CD

### Pipeline Features
- **Quality Gates**: Black formatting, Ruff linting, MyPy type checking
- **Parallel Execution**: 3 browsers simultaneously via pytest-xdist
- **Comprehensive Reporting**: JUnit XML + HTML reports + BrowserStack recordings
- **Credential Management**: Secure BrowserStack authentication

### Setup
```bash
# Quick Docker setup
docker run -p 8080:8080 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Pipeline: "Pipeline script from SCM" → Git → `Jenkinsfile`
# Credentials: Add `browserstack-creds` (username/password)
```

## 🛠️ Development

### Code Quality
```bash
./scripts/quality-check.sh      # All checks (Black, Ruff, MyPy)
uv run black .                  # Code formatting
uv run ruff check --fix .       # Linting with auto-fix
uv run mypy .                   # Type checking
```

### Virtual Environment
```bash
uv sync                         # Auto-managed (recommended)
source .venv/bin/activate       # Manual activation (optional)
```

### Test Execution
```bash
uv run pytest tests/ -v                               # All tests
uv run pytest tests/test_samsung_favorite_galaxy.py   # Specific test
uv run pytest --html=reports/report.html --self-contained-html  # Custom report
```

## 📊 Test Reports

- **JUnit XML**: Jenkins integration (`test-reports/results.xml`)
- **HTML Report**: Detailed view (`test-reports/report.html`)
- **BrowserStack Dashboard**: Live sessions and recordings
- **Console Logs**: Real-time execution feedback

## 🔧 Tech Stack

**Core**: Python 3.10, Selenium WebDriver, pytest, BrowserStack SDK  
**Quality**: Black, Ruff, MyPy with strict type checking  
**CI/CD**: Jenkins pipeline with parallel execution  
**Reports**: pytest-html, JUnit XML, BrowserStack recordings  

## 📋 Configuration

All sensitive data externalized via environment variables:
```bash
BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY    # Required
TEST_USERNAME, TEST_PASSWORD                      # Optional (defaults provided)
TARGET_BRAND, TARGET_PRODUCT_NAME                 # Optional (defaults provided)
```

## 🎯 Results

Production-ready test automation demonstrating:
- **Cross-browser compatibility** testing at scale
- **Enterprise CI/CD** integration with quality gates
- **Maintainable architecture** using industry patterns
- **Comprehensive reporting** for stakeholders and debugging

Perfect for validating web applications across multiple browsers with enterprise-level reliability.
