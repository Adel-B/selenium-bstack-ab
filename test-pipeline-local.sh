#!/bin/bash

# Simple test script to validate BrowserStack tests work locally

set -e

echo "🧪 Testing BrowserStack Galaxy S20+ Tests"
echo "========================================="

# Check BrowserStack credentials
if [ -z "$BROWSERSTACK_USERNAME" ] || [ -z "$BROWSERSTACK_ACCESS_KEY" ]; then
    echo "❌ Please set your BrowserStack credentials:"
    echo "   export BROWSERSTACK_USERNAME=your_username"
    echo "   export BROWSERSTACK_ACCESS_KEY=your_access_key"
    exit 1
fi

echo "✅ BrowserStack credentials found"
echo "Username: ${BROWSERSTACK_USERNAME:0:3}***"

# Install dependencies (including dev tools)
echo "📦 Installing dependencies..."
uv sync --extra dev

# Run code quality checks
echo "🔍 Running code quality checks..."
echo "📝 Formatting check with Black..."
uv run black --check --diff .

echo "🔍 Linting with Ruff..."
uv run ruff check .

echo "🔎 Type checking with MyPy..."
uv run mypy .

echo "✅ Code quality checks passed!"

# Create reports directory
mkdir -p test-reports

echo ""
echo "🚀 Running BrowserStack tests..."
echo ""

echo "☁️ Running BrowserStack tests (3 platforms automatically)..."
export EXECUTION_MODE=browserstack
uv run browserstack-sdk pytest tests/test_samsung_favorite_galaxy.py::test_favorite_galaxy_browserstack \
    -v \
    --junit-xml=test-reports/results.xml \
    --html=test-reports/report.html \
    --self-contained-html

echo "✅ Tests completed! Check test-reports/ for results" 