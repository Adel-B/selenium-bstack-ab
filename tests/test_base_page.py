"""Tests for BasePage class functionality and mode selection."""

import pytest
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.env_loader import config
from utils.logger_config import get_test_logger


class TestBasePage:
    """Test BasePage functionality and mode selection."""

    def test_local_mode_initialization_chrome(self) -> None:
        """Test BasePage initialization in local mode with Chrome."""
        logger = get_test_logger("test_local_chrome")

        logger.info("Testing BasePage local Chrome initialization...")

        with BasePage(execution_mode="local", browser="chrome") as page:
            assert page.execution_mode == "local"
            assert page.browser == "chrome"
            assert page.driver is not None
            assert page.timeout == 30

            # Test basic navigation
            page.navigate_to("https://www.google.com")
            assert "google" in page.get_current_url().lower()

            title = page.get_page_title()
            assert "Google" in title

            logger.info(f"✅ Local Chrome test passed - Title: {title}")

    def test_local_mode_initialization_firefox(self) -> None:
        """Test BasePage initialization in local mode with Firefox."""
        logger = get_test_logger("test_local_firefox")

        logger.info("Testing BasePage local Firefox initialization...")

        with BasePage(execution_mode="local", browser="firefox") as page:
            assert page.execution_mode == "local"
            assert page.browser == "firefox"
            assert page.driver is not None

            # Test basic navigation
            page.navigate_to("https://www.google.com")
            assert "google" in page.get_current_url().lower()

            title = page.get_page_title()
            assert "Google" in title

            logger.info(f"✅ Local Firefox test passed - Title: {title}")

    def test_mode_selection_from_env(self) -> None:
        """Test that execution mode is read from environment when not specified."""
        logger = get_test_logger("test_env_mode")

        logger.info("Testing mode selection from environment...")

        # Test default mode (should be 'local')
        with BasePage(browser="chrome") as page:
            expected_mode = config.get_optional_env("EXECUTION_MODE", "local")
            assert page.execution_mode == expected_mode

            logger.info(f"✅ Environment mode test passed - Mode: {expected_mode}")

    def test_unsupported_execution_mode(self) -> None:
        """Test error handling for unsupported execution mode."""
        logger = get_test_logger("test_unsupported_mode")

        logger.info("Testing unsupported execution mode...")

        with pytest.raises(ValueError, match="Unsupported execution mode"):
            BasePage(execution_mode="invalid_mode", browser="chrome")

        logger.info("✅ Unsupported mode test passed")

    def test_unsupported_local_browser(self) -> None:
        """Test error handling for unsupported local browser."""
        logger = get_test_logger("test_unsupported_browser")

        logger.info("Testing unsupported local browser...")

        with pytest.raises(ValueError, match="Unsupported local browser"):
            BasePage(execution_mode="local", browser="safari")

        logger.info("✅ Unsupported browser test passed")

    @pytest.mark.skipif(
        not config.validate_browserstack_credentials(),
        reason="BrowserStack credentials not configured",
    )
    def test_browserstack_mode_windows_chrome(self) -> None:
        """Test BasePage initialization in BrowserStack mode."""
        logger = get_test_logger("test_browserstack_chrome")

        logger.info("Testing BasePage BrowserStack mode...")

        with BasePage(
            execution_mode="browserstack", capability_name="Windows_10_Chrome"
        ) as page:
            assert page.execution_mode == "browserstack"
            assert page.capability_name == "Windows_10_Chrome"
            assert page.driver is not None

            # Test basic navigation
            page.navigate_to(config.base_url)
            assert "bstackdemo" in page.get_current_url().lower()

            title = page.get_page_title()
            logger.info(f"✅ BrowserStack test passed - Title: {title}")

    @pytest.mark.skipif(
        not config.validate_browserstack_credentials(),
        reason="BrowserStack credentials not configured",
    )
    def test_browserstack_browser_mapping(self) -> None:
        """Test BrowserStack browser name mapping."""
        logger = get_test_logger("test_browserstack_mapping")

        logger.info("Testing BrowserStack browser mapping...")

        with BasePage(execution_mode="browserstack", browser="firefox") as page:
            # Should map firefox to macOS_Ventura_Firefox
            assert page.execution_mode == "browserstack"
            assert page.browser == "firefox"

            page.navigate_to(config.base_url)
            logger.info("✅ BrowserStack mapping test passed")

    def test_common_utility_methods(self) -> None:
        """Test common utility methods with local driver."""
        logger = get_test_logger("test_utility_methods")

        logger.info("Testing common utility methods...")

        with BasePage(execution_mode="local", browser="chrome") as page:
            # Navigate to a more reliable test page
            page.navigate_to("https://httpbin.org/forms/post")

            # Test element finding
            from selenium.webdriver.common.by import By

            # Test find_element - look for form elements
            customer_name_field = page.find_element((By.NAME, "custname"))
            assert customer_name_field is not None

            # Test send_keys_to_element
            page.send_keys_to_element((By.NAME, "custname"), "Test Customer")

            # Test get_element_text - get the value we just entered
            current_value = customer_name_field.get_attribute("value")
            assert "Test Customer" in current_value

            # Test is_element_present
            assert page.is_element_present((By.NAME, "custname")) is True
            assert page.is_element_present((By.ID, "nonexistent")) is False

            # Test find_elements - should find multiple form inputs
            form_inputs = page.find_elements((By.TAG_NAME, "input"))
            assert len(form_inputs) > 0

            # Test URL and title methods
            url = page.get_current_url()
            title = page.get_page_title()

            assert "httpbin" in url.lower()
            assert title is not None

            logger.info("✅ Utility methods test passed")

    def test_timeout_handling(self) -> None:
        """Test timeout handling for element operations."""
        logger = get_test_logger("test_timeout")

        logger.info("Testing timeout handling...")

        with BasePage(execution_mode="local", browser="chrome", timeout=5) as page:
            page.navigate_to("https://www.google.com")

            from selenium.webdriver.common.by import By

            # Test timeout with non-existent element
            with pytest.raises(TimeoutException):
                page.find_element((By.ID, "definitely-does-not-exist"), timeout=2)

            logger.info("✅ Timeout handling test passed")

    def test_context_manager_cleanup(self) -> None:
        """Test that context manager properly cleans up resources."""
        logger = get_test_logger("test_cleanup")

        logger.info("Testing context manager cleanup...")

        page = BasePage(execution_mode="local", browser="chrome")
        driver_instance = page.driver

        # Verify driver is active
        assert driver_instance is not None
        driver_instance.get("https://www.google.com")

        # Use context manager
        with page:
            pass  # Just test cleanup

        # Driver should be closed now
        # Note: We can't easily test if driver is closed without exceptions
        # but the test validates no exceptions during cleanup

        logger.info("✅ Context manager cleanup test passed")

    def test_capability_name_validation(self) -> None:
        """Test capability name validation."""
        logger = get_test_logger("test_capability_validation")

        logger.info("Testing capability name validation...")

        page = BasePage(execution_mode="local", browser="chrome")

        # Test valid capability names
        valid_caps = page._get_capability_by_name("Windows_10_Chrome")
        assert "browserName" in valid_caps
        assert valid_caps["browserName"] == "Chrome"

        # Test invalid capability name
        with pytest.raises(ValueError, match="Unknown capability name"):
            page._get_capability_by_name("Invalid_Capability")

        page.close()

        logger.info("✅ Capability validation test passed")

    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_parametrized_local_browsers(self, browser: str) -> None:
        """Test both browsers with parametrized test."""
        logger = get_test_logger(f"test_param_{browser}")

        logger.info(f"Testing parametrized {browser} browser...")

        with BasePage(execution_mode="local", browser=browser) as page:
            assert page.browser == browser
            assert page.execution_mode == "local"

            page.navigate_to("https://jsonplaceholder.typicode.com/")
            assert "typicode" in page.get_current_url()

            logger.info(f"✅ Parametrized {browser} test passed")

    def test_window_size_consistency(self) -> None:
        """Test that window size is set consistently for local drivers."""
        logger = get_test_logger("test_window_size")

        logger.info("Testing window size consistency...")

        with BasePage(execution_mode="local", browser="chrome") as page:
            # Check window size is set to 1920x1080
            size = page.driver.get_window_size()
            assert size["width"] == 1920
            assert size["height"] == 1080

            logger.info(f"✅ Window size test passed - Size: {size}")
