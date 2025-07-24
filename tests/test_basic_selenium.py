"""Basic Selenium validation test."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.logger_config import get_test_logger


class TestBasicSelenium:
    """Basic Selenium functionality tests."""

    def test_chrome_can_open_google(self) -> None:
        """Test that Chrome WebDriver can open Google homepage."""
        logger = get_test_logger("test_chrome")

        logger.info("Starting Chrome WebDriver test")

        # Setup Chrome driver
        chrome_service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service)

        try:
            # Open Google
            logger.info("Opening Google homepage")
            driver.get("https://www.google.com")

            # Wait for page to load and verify title
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            assert "Google" in driver.title
            logger.info(f"✅ Page title: {driver.title}")

            # Verify search box exists
            search_box = driver.find_element(By.NAME, "q")
            assert search_box is not None
            logger.info("✅ Search box found")

            logger.info("Chrome WebDriver test completed successfully")

        finally:
            driver.quit()
            logger.info("Chrome WebDriver closed")

    def test_firefox_can_open_google(self) -> None:
        """Test that Firefox WebDriver can open Google homepage."""
        logger = get_test_logger("test_firefox")

        logger.info("Starting Firefox WebDriver test")

        # Setup Firefox driver
        firefox_service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=firefox_service)

        try:
            # Open Google
            logger.info("Opening Google homepage")
            driver.get("https://www.google.com")

            # Wait for page to load and verify title
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            assert "Google" in driver.title
            logger.info(f"✅ Page title: {driver.title}")

            # Verify search box exists
            search_box = driver.find_element(By.NAME, "q")
            assert search_box is not None
            logger.info("✅ Search box found")

            logger.info("Firefox WebDriver test completed successfully")

        finally:
            driver.quit()
            logger.info("Firefox WebDriver closed")

    @pytest.mark.parametrize("browser", ["chrome", "firefox"])
    def test_basic_navigation(self, browser: str) -> None:
        """Test basic navigation works across browsers."""
        logger = get_test_logger(f"test_navigation_{browser}")

        logger.info(f"Starting navigation test with {browser}")

        # Create driver based on browser - use base WebDriver type for mypy
        driver: WebDriver
        if browser == "chrome":
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        else:  # firefox
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )

        try:
            # Test navigation
            logger.info("Testing navigation to jsonplaceholder.typicode.com")
            driver.get("https://jsonplaceholder.typicode.com/")

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # JSONPlaceholder has a simple page, just verify we got a response
            assert driver.title is not None and len(driver.title) > 0
            logger.info(f"✅ Navigation successful: {driver.title}")

            # Test element finding
            body = driver.find_element(By.TAG_NAME, "body")
            assert body is not None
            logger.info("✅ Body element found")

            logger.info(f"Navigation test with {browser} completed successfully")

        finally:
            driver.quit()
            logger.info(f"{browser} WebDriver closed")
