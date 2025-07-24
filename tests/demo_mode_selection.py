"""Demonstration of unified mode selection strategy.

This script shows how the same code works for both local and BrowserStack execution.
Run with different EXECUTION_MODE environment variable to see both modes.
"""

import os

from pages.base_page import BasePage
from utils.env_loader import config
from utils.logger_config import get_test_logger


def demo_unified_execution(
    execution_mode: str = "local", browser: str = "chrome"
) -> None:
    """Demonstrate unified execution across both modes.

    Args:
        execution_mode: "local" or "browserstack"
        browser: Browser name or capability name
    """
    logger = get_test_logger(f"demo_{execution_mode}")

    logger.info(f"🚀 Starting demo in {execution_mode} mode with {browser}")

    try:
        # The SAME code works for both local and BrowserStack!
        with BasePage(execution_mode=execution_mode, browser=browser) as page:

            # Navigate to test application
            logger.info("📍 Navigating to test application...")
            page.navigate_to(config.base_url)

            # Get page information
            title = page.get_page_title()
            url = page.get_current_url()

            logger.info(f"📄 Page Title: {title}")
            logger.info(f"🔗 Current URL: {url}")

            # Test common functionality
            from selenium.webdriver.common.by import By

            # Check if sign-in link exists
            if page.is_element_present((By.ID, "signin")):
                logger.info("🔍 Sign-in button found")
            else:
                logger.info("ℹ️  Sign-in button not found")

            logger.info(f"✅ Demo completed successfully in {execution_mode} mode!")

    except Exception as e:
        logger.error(f"❌ Demo failed in {execution_mode} mode: {str(e)}")
        raise


def main() -> None:
    """Run mode selection demonstration."""
    logger = get_test_logger("demo_main")

    logger.info("🎯 Mode Selection Strategy Demo")
    logger.info("=" * 50)

    # Demo 1: Local execution
    logger.info("\n📱 Demo 1: LOCAL Execution Mode")
    logger.info("-" * 30)
    demo_unified_execution("local", "chrome")

    # Demo 2: BrowserStack execution (if credentials available)
    if config.validate_browserstack_credentials():
        logger.info("\n☁️  Demo 2: BROWSERSTACK Execution Mode")
        logger.info("-" * 30)
        demo_unified_execution("browserstack", "chrome")
    else:
        logger.info("\n⚠️  Skipping BrowserStack demo - credentials not configured")

    # Demo 3: Environment-based mode selection
    logger.info("\n🔧 Demo 3: ENVIRONMENT-Based Mode Selection")
    logger.info("-" * 30)

    # Temporarily set environment variable
    original_mode = os.environ.get("EXECUTION_MODE")

    try:
        # Test with local mode via environment
        os.environ["EXECUTION_MODE"] = "local"
        with BasePage(browser="firefox") as page:  # No explicit mode, reads from env
            logger.info(f"✅ Environment mode detected: {page.execution_mode}")

    finally:
        # Restore original environment
        if original_mode:
            os.environ["EXECUTION_MODE"] = original_mode
        elif "EXECUTION_MODE" in os.environ:
            del os.environ["EXECUTION_MODE"]

    logger.info("\n🎉 All demos completed!")

    # Show the key insight
    logger.info("\n💡 KEY INSIGHT:")
    logger.info("   The SAME test code works in BOTH modes!")
    logger.info("   Just change the execution_mode parameter or environment variable.")
    logger.info("   Perfect for development (local) vs CI/CD (cloud) workflows!")


if __name__ == "__main__":
    main()
