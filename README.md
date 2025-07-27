# BrowserStack Cross-Browser Automation Framework

A comprehensive Selenium test automation framework for cross-browser testing using BrowserStack cloud infrastructure. Features enterprise-grade CI/CD integration, quality gates, and modern SDK-based test execution.

## 🚀 Quick Start

### Prerequisites
- **BrowserStack Account**: [Free trial available](https://www.browserstack.com/)
- **Python 3.10+**: For test execution
- **uv Package Manager**: [Installation guide](https://github.com/astral-sh/uv)

### Setup & Execution
```bash
# 1. Clone and setup
git clone <repository-url>
cd selenium-bstack-ab

# 2. Set BrowserStack credentials
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key

# 3. Install dependencies
uv sync --extra dev

# 4. Run tests
./test-pipeline-local.sh
```

## 🎯 BrowserStack SDK Integration

### **⚡ SDK-Based Testing (Recommended)**

We support **BrowserStack SDK** for enhanced test automation with advanced features:

#### **✅ SDK Benefits:**
- **Automatic WebDriver Management**: No manual driver setup
- **Centralized Configuration**: Platform config in `browserstack.yml`
- **Enhanced Reporting**: Advanced test observability and insights
- **Simplified Parallelization**: Built-in cross-browser execution
- **Better Error Handling**: SDK manages connection issues automatically

#### **🔧 SDK Configuration (`browserstack.yml`):**
```yaml
# Authentication via environment variables
userName: ${BROWSERSTACK_USERNAME}
accessKey: ${BROWSERSTACK_ACCESS_KEY}

# Cross-browser testing platforms
platforms:
  - os: "Windows"
    osVersion: "10"
    browserName: "Chrome"
    browserVersion: "latest"
    
  - os: "OS X" 
    osVersion: "Ventura"
    browserName: "Firefox"
    browserVersion: "latest"
    
  - deviceName: "Samsung Galaxy S22"
    osVersion: "12.0"
    browserName: "Chrome"

# Advanced features
testObservability: true
debug: true
networkLogs: true
```

#### **🧪 Test Execution Options:**

**🖥️ Local Development (Chrome)**
```bash
# Run tests locally for development/debugging
EXECUTION_MODE=local uv run pytest tests/test_samsung_favorite_galaxy.py -v
```

**☁️ BrowserStack Cross-Browser Testing**
```bash
# SDK approach (automatic platform management - RECOMMENDED)
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key
uv run browserstack-sdk pytest tests/test_samsung_favorite_galaxy.py -v
```

### **📊 Unified Test Approach**

| Feature | Unified Approach |
|---------|-----------------|
| **Configuration** | `browserstack.yml` |
| **WebDriver** | Auto-managed by SDK |
| **Parallelization** | Built-in cross-browser testing |
| **Reporting** | Enhanced observability |
| **Maintenance** | Low (SDK handles updates) |
| **Error Handling** | Advanced SDK resilience |

## 🏗️ Project Architecture

```
selenium-bstack-ab/
├── browserstack.yml          # SDK configuration
├── tests/
│   └── test_samsung_favorite_galaxy.py      # Unified test (local + BrowserStack)
├── pages/                    # Page Object Model
├── utils/                    # Configuration & helpers
├── scripts/                  # Quality & utility scripts
├── docs/                     # Evidence & documentation
└── test-reports/            # Generated test reports
```

## 💻 Development Workflow

### **Code Quality Tools**
```bash
# Install dev dependencies
uv sync --extra dev

# Code formatting
uv run black --check --diff .    # Check formatting
uv run black .                   # Apply formatting

# Linting  
uv run ruff check .              # Check linting
uv run ruff check --fix .        # Fix auto-fixable issues

# Type checking
uv run mypy .                    # Static type analysis

# All-in-one quality check
./scripts/quality-check.sh
```

### **Test Execution Options**

#### **1. Interactive Local Testing**
```bash
./test-pipeline-local.sh
```

#### **2. Direct Test Commands**
```bash
# BrowserStack testing (recommended)
export EXECUTION_MODE=browserstack
uv run browserstack-sdk pytest tests/test_samsung_favorite_galaxy.py -v

# Local testing
EXECUTION_MODE=local uv run pytest tests/test_samsung_favorite_galaxy.py -v
```

#### **3. Jenkins CI/CD Pipeline**
- Automatically runs unified tests on BrowserStack
- Generates comprehensive reports
- Archives artifacts: `report.html`

## 🔧 Technical Implementation

### **Core Features**
- **Cross-Browser Testing**: Windows 10 Chrome, macOS Ventura Firefox, Samsung Galaxy S22
- **Page Object Model**: Maintainable test structure with reusable components
- **Configurable Test Data**: Environment-driven test parameters (credentials, target products)
- **Parallel Execution**: Multiple concurrent test sessions for faster results
- **Comprehensive Reporting**: JUnit XML + HTML reports with screenshots

### **BrowserStack Integration**
- **SDK Integration**: Latest BrowserStack SDK (v1.17.0+) for enhanced automation
- **Unified Testing**: Single test file supports both local and BrowserStack execution
- **Status Marking**: Real-time test status updates in BrowserStack dashboard
- **Debug Features**: Network logs, console logs, and video recordings enabled

### **Quality Assurance**
- **Code Formatting**: Black (Python code formatter)
- **Linting**: Ruff (fast Python linter)
- **Type Checking**: MyPy (static type analysis)
- **CI/CD Integration**: Jenkins pipeline with quality gates

### **Security**
- **Environment Variables**: Sensitive data (credentials) externalized
- **No Hardcoded Secrets**: BrowserStack credentials via environment variables
- **Secure CI/CD**: Jenkins credentials management integration

## 📦 Dependencies

### **Core Dependencies**
```toml
selenium>=4.15.0              # WebDriver automation
browserstack-sdk>=1.17.0      # Enhanced BrowserStack integration
pytest>=7.4.0                 # Test framework
pytest-html>=4.0.0            # HTML test reports
pytest-xdist>=3.0.0           # Parallel test execution
python-dotenv>=1.0.0          # Environment variable management
```

### **Development Dependencies**
```toml
black>=23.0.0                 # Code formatting
ruff>=0.1.0                   # Fast linting  
mypy>=1.6.0                   # Static type checking
```

## 🚀 Jenkins Setup

See [jenkins-setup.md](jenkins-setup.md) for complete Jenkins configuration including:
- Pipeline script from SCM setup
- BrowserStack credentials configuration  
- Build triggers and notifications
- Test report integration

## 📸 Evidence & Documentation

Complete evidence documentation available in [`docs/README.md`](docs/README.md) including:
- Jenkins CI/CD pipeline screenshots
- BrowserStack cross-browser execution evidence  
- Test results and reporting examples

## 🎯 Tech Challenge Completion

✅ **All Requirements Met:**
- **✓ Cross-Browser Testing**: Windows 10 Chrome, macOS Ventura Firefox, Samsung Galaxy S22
- **✓ BrowserStack Integration**: Unified SDK-based approach implemented
- **✓ Test Workflow**: Login → Samsung filter → Galaxy S20+ favorite → Verification
- **✓ Parallel Execution**: 3 concurrent browser sessions
- **✓ Security**: No hardcoded credentials, environment variable configuration
- **✓ CI/CD Integration**: Complete Jenkins pipeline with quality gates
- **✓ Evidence**: Comprehensive documentation with screenshots
- **✓ GitHub Repository**: Public repository with complete implementation
