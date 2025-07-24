# selenium-bstack-ab

BrowserStack cross-browser test automation framework

## Setup

1. Ensure Python 3.10+ is installed
2. Install uv package manager
3. Install dependencies:

```bash
uv sync
```

## Project Structure

```
selenium-bstack-ab/
├── tests/          # Test files
├── pages/          # Page Object Model
├── utils/          # Utility functions
├── pyproject.toml  # Project configuration
└── README.md       # This file
```

## Run Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests (when implemented)
pytest tests/
``` 