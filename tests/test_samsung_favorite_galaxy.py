#!/usr/bin/env python3
"""
Unified Cross-Browser Product Favoriting Test with POM

This test uses Selenium WebDriver with Page Object Model (POM) pattern,
supporting both local and BrowserStack execution modes.

Features:
- Automatic execution mode detection (local vs BrowserStack)
- BrowserStack SDK integration for cloud testing
- Local WebDriver management for development
- Cross-browser testing on multiple platforms
- Page Object Model for maintainable test structure
- Single test file for both execution modes

Validates the complete user workflow:
1. Navigate to the demo application
2. Login with configured credentials
3. Filter products by target brand
4. Favorite the target device
5. Verify device appears in favorites page
"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.favorites_page import FavoritesPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.env_loader import config
from utils.logger_config import get_test_logger


def get_execution_mode() -> str:
    """Get execution mode from environment variable or detect from context.

    Returns:
        Execution mode: 'local' or 'browserstack'
    """
    # Check explicit environment variable first
    explicit_mode = os.getenv("EXECUTION_MODE", "").lower()
    if explicit_mode in ["local", "browserstack"]:
        return explicit_mode

    # Auto-detect from BrowserStack environment variables
    if os.getenv("BROWSERSTACK_USERNAME") and os.getenv("BROWSERSTACK_ACCESS_KEY"):
        return "browserstack"

    # Default to local
    return "local"


def create_local_driver(browser: str = "chrome"):
    """Create a local WebDriver instance for development/testing.

    Args:
        browser: Browser name (currently supports 'chrome')

    Returns:
        WebDriver instance for local execution
    """
    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    else:
        raise ValueError(f"Unsupported browser for local execution: {browser}")


def test_favorite_galaxy_local():
    """
    Local test for product favoriting using Chrome.

    This test runs locally for development and debugging purposes.
    Uses Chrome browser on the local machine.
    """
    execution_mode = get_execution_mode()

    # Only run this test in local mode
    if execution_mode != "local":
        pytest.skip("This test is only for local execution")

    # Create local driver
    driver = create_local_driver("chrome")

    try:
        logger = get_test_logger("samsung_favorite_galaxy_local")
        logger.info(
            f"🌐 Starting {config.target_product_name} favoriting test on Local Chrome ({execution_mode} mode)"
        )

        # Run the workflow using Page Object Model
        _run_favorite_workflow_with_pom(driver, logger, "Local Chrome")

        logger.info(
            f"✅ {config.target_product_name} favoriting test completed successfully on Local Chrome!"
        )

    except Exception as e:
        logger.error(
            f"❌ {config.target_product_name} favoriting test failed on Local Chrome: {str(e)}"
        )
        raise
    finally:
        driver.quit()


def test_favorite_galaxy_browserstack(driver):
    """
    BrowserStack test for product favoriting.

    This test runs on BrowserStack using the SDK's automatic platform management.
    The BrowserStack SDK automatically handles the cross-browser testing across
    the platforms defined in browserstack.yml.

    The 'driver' fixture is automatically provided by the BrowserStack SDK.

    Args:
        driver: BrowserStack WebDriver instance automatically managed by SDK
    """
    execution_mode = get_execution_mode()

    # Only run this test in browserstack mode
    if execution_mode != "browserstack":
        pytest.skip("This test is only for BrowserStack execution")

    logger = get_test_logger("samsung_favorite_galaxy_browserstack")
    logger.info(
        f"🌐 Starting {config.target_product_name} favoriting test on BrowserStack ({execution_mode} mode)"
    )

    try:
        # Run the workflow using Page Object Model
        _run_favorite_workflow_with_pom(driver, logger, "BrowserStack")

        logger.info(
            f"✅ {config.target_product_name} favoriting test completed successfully on BrowserStack!"
        )

    except Exception as e:
        logger.error(
            f"❌ {config.target_product_name} favoriting test failed on BrowserStack: {str(e)}"
        )
        raise


def _run_favorite_workflow_with_pom(driver, logger, platform_name: str):
    """
    Execute the complete product favoriting workflow using Page Object Model.

    Args:
        driver: WebDriver instance (local or BrowserStack)
        logger: Logger instance for test output
        platform_name: Platform identifier for logging context
    """
    # Initialize page objects with the provided driver
    login_page = LoginPage._create_with_existing_driver(driver)
    product_page = ProductPage._create_with_existing_driver(driver)
    favorites_page = FavoritesPage._create_with_existing_driver(driver)

    # Step 1: Navigate to login page and login
    logger.info(f"📝 [{platform_name}] Step 1: Navigate to bstackdemo.com and login")
    login_page.login()  # Uses default credentials from config
    logger.info(f"✅ [{platform_name}] Login completed successfully")

    # Step 2: Filter products by Samsung brand
    logger.info(f"🔍 [{platform_name}] Step 2: Apply {config.target_brand} filter")
    product_page.filter_by_samsung()
    product_page.wait_for_filtered_products_to_load()
    logger.info(f"✅ [{platform_name}] Samsung filter applied successfully")

    # Step 3: Verify Galaxy S20+ is visible and favorite it
    logger.info(f"❤️ [{platform_name}] Step 3: Favorite {config.target_product_name}")
    if not product_page.is_galaxy_s20_plus_visible():
        raise AssertionError(
            f"{config.target_product_name} should be visible after Samsung filter on {platform_name}"
        )

    product_page.click_galaxy_s20_plus_favorite()
    logger.info(
        f"✅ [{platform_name}] {config.target_product_name} favorited successfully"
    )

    # Step 4: Navigate to favorites page
    logger.info(f"📄 [{platform_name}] Step 4: Navigate to Favourites page")
    product_page.navigate_to_favorites()
    logger.info(f"✅ [{platform_name}] Navigated to favorites page")

    # Step 5: Verify Galaxy S20+ is visible on favorites page
    logger.info(
        f"✅ [{platform_name}] Step 5: Verify {config.target_product_name} is visible on favorites page"
    )
    if not favorites_page.is_galaxy_s20_plus_on_favorites_page():
        raise AssertionError(
            f"{config.target_product_name} should be visible on favorites page on {platform_name}"
        )

    # Get the actual title for verification
    actual_title = favorites_page.get_galaxy_s20_plus_title_on_favorites_page()
    expected_title = config.target_product_name

    assert (
        actual_title == expected_title
    ), f"Expected '{expected_title}' but found '{actual_title}' on {platform_name}"

    logger.info(
        f"🎉 [{platform_name}] {config.target_product_name} favoriting test completed successfully with POM!"
    )
