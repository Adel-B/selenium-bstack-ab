#!/bin/bash

# Code Quality Check Script
# Runs Black, Ruff, and MyPy in sequence

set -e

echo "🔍 Running Code Quality Checks"
echo "=============================="

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv package manager is not installed"
    echo "   Install it from: https://github.com/astral-sh/uv"
    exit 1
fi

# Install dev dependencies if needed
echo "📦 Ensuring dev dependencies are installed..."
uv sync --extra dev

echo ""
echo "📝 1. Code Formatting with Black..."
echo "-----------------------------------"
uv run black --check --diff .
if [ $? -eq 0 ]; then
    echo "✅ Black formatting check passed"
else
    echo "❌ Black formatting issues found. Run 'uv run black .' to fix"
    exit 1
fi

echo ""
echo "🔍 2. Linting with Ruff..."
echo "-------------------------"
uv run ruff check .
if [ $? -eq 0 ]; then
    echo "✅ Ruff linting passed"
else
    echo "❌ Ruff linting issues found. Run 'uv run ruff check --fix .' to auto-fix"
    exit 1
fi

echo ""
echo "🔎 3. Type Checking with MyPy..."
echo "-------------------------------"
uv run mypy .
if [ $? -eq 0 ]; then
    echo "✅ MyPy type checking passed"
else
    echo "❌ MyPy type checking issues found"
    exit 1
fi

echo ""
echo "🎉 All code quality checks passed!"
echo "Ready to commit your changes." 