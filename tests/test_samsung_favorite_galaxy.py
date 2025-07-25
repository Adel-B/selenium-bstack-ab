#!/usr/bin/env python3
"""
Cross-Browser Product Favoriting Test

Test suite for validating product favoriting functionality across multiple
browsers and platforms using BrowserStack. Test data is configurable via
environment variables.

Supported platforms:
- Windows 10 Chrome
- macOS Safari
- macOS Monterey Firefox
- Samsung Galaxy S22 Chrome

Features BrowserStack SDK integration for enhanced test reporting.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.env_loader import config
from utils.logger_config import get_test_logger


class TestSamsungFavoriteGalaxy:
    """Cross-browser product favoriting test suite with configurable test data."""

    def setup_method(self):
        """Setup for each test method"""
        self.logger = get_test_logger("samsung_favorite_galaxy")

    @pytest.mark.parametrize(
        "capability_name",
        [
            "Windows_10_Chrome",
            "macOS_Ventura_Firefox",
            "Samsung_Galaxy_S22_Chrome",
        ],
    )
    def test_favorite_galaxy_cross_browser(self, capability_name):
        """
        Test product favoriting across multiple browser platforms.

        Validates the complete user workflow:
        1. Navigate to the demo application
        2. Login with configured credentials
        3. Filter products by target brand
        4. Favorite the target device
        5. Verify device appears in favorites page

        Args:
            capability_name: BrowserStack capability configuration name
        """
        self.logger.info(
            f"🌐 Starting {config.target_product_name} favoriting test on {capability_name}"
        )

        # Initialize BrowserStack browser with SDK integration
        base_page = BasePage(
            execution_mode="browserstack", capability_name=capability_name
        )
        driver = base_page.driver
        wait = WebDriverWait(driver, 20)

        try:
            # Mark test as started
            self._mark_test_status(
                driver, "started", f"Starting {capability_name} test"
            )

            # Run the workflow
            self._run_favorite_workflow(driver, wait, capability_name)

            # Mark test as passed
            self._mark_test_status(
                driver, "passed", f"{capability_name} test completed successfully"
            )

        except Exception as e:
            self.logger.error(
                f"❌ {config.target_product_name} favoriting test failed on {capability_name}: {str(e)}"
            )

            # Mark test as failed
            self._mark_test_status(
                driver, "failed", f"{capability_name} test failed: {str(e)}"
            )
            raise
        finally:
            base_page.close()

    def _mark_test_status(self, driver, status, reason):
        """
        Update test execution status in BrowserStack dashboard.

        Uses BrowserStack's SDK executor to provide real-time test status
        updates for enhanced test reporting and debugging capabilities.

        Args:
            driver: WebDriver instance connected to BrowserStack
            status: Test execution status ('started', 'passed', 'failed')
            reason: Descriptive message explaining the status change
        """
        try:
            # BrowserStack SDK status marking
            driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "{status}", "reason": "{reason}"}}}}'
            )
            self.logger.info(f"📊 BrowserStack status marked: {status} - {reason}")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not mark BrowserStack status: {str(e)}")

    def _run_favorite_workflow(self, driver, wait, platform_name):
        """
        Execute the complete product favoriting workflow.

        Performs the end-to-end user journey: login, product filtering,
        device favoriting, and verification on favorites page.

        Args:
            driver: WebDriver instance for browser automation
            wait: WebDriverWait instance for element synchronization
            platform_name: Browser/platform identifier for logging context
        """
        # Navigate to bstackdemo.com
        self.logger.info(f"📝 [{platform_name}] Navigate to bstackdemo.com")
        driver.get(config.base_url)

        # Click Sign In
        self.logger.info(f"🔐 [{platform_name}] Click Sign In")
        sign_in = wait.until(EC.element_to_be_clickable((By.ID, "signin")))
        sign_in.click()

        # Click username container to open dropdown, then type
        self.logger.info(f"👤 [{platform_name}] Select Username")
        username_container = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_container.click()

        # Send keys directly to the input without clicking it
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "react-select-2-input"))
        )
        username_input.send_keys(config.test_username)
        username_input.send_keys(Keys.ENTER)

        # Click password container to open dropdown, then type
        self.logger.info(f"🔑 [{platform_name}] Select Password")
        password_container = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_container.click()

        # Send keys directly to the input without clicking it
        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "react-select-3-input"))
        )
        password_input.send_keys(config.test_password)
        password_input.send_keys(Keys.ENTER)

        # Click Log In button
        self.logger.info(f"✅ [{platform_name}] Click Log In")
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
        login_btn.click()

        # Wait for login to complete
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shelf-item")))

        # Click brand filter
        self.logger.info(f"🔍 [{platform_name}] Apply {config.target_brand} filter")
        brand_filter = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@class='filters-available-size']//input[@value='{config.target_brand}']/parent::label",
                )
            )
        )
        brand_filter.click()

        # Wait for filtered products to load
        wait.until(EC.presence_of_element_located((By.ID, config.target_product_id)))

        # Click favorite button for target product
        self.logger.info(f"❤️ [{platform_name}] Favorite {config.target_product_name}")
        favorite_btn = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    f"[id='{config.target_product_id}'] .shelf-stopper button",
                )
            )
        )
        favorite_btn.click()

        # Click Favourites link
        self.logger.info(f"📄 [{platform_name}] Navigate to Favourites page")
        favourites_link = wait.until(EC.element_to_be_clickable((By.ID, "favourites")))
        favourites_link.click()

        # Verify target product is visible on favourites page
        self.logger.info(
            f"✅ [{platform_name}] Verify {config.target_product_name} is visible"
        )
        target_product = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//p[text()='{config.target_product_name}']")
            )
        )

        assert (
            target_product.is_displayed()
        ), f"{config.target_product_name} should be visible on favourites page on {platform_name}"

        self.logger.info(
            f"🎉 [{platform_name}] {config.target_product_name} favoriting test completed successfully!"
        )
