"""Base page class providing common WebDriver functionality and mode selection."""

from typing import Any, Dict, Optional, Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.browserstack_config import BROWSERSTACK_CONFIG, BrowserStackCapabilities
from utils.env_loader import config
from utils.logger_config import get_test_logger


class BasePage:
    """Base page class providing common WebDriver functionality and mode selection.

    Supports both local and BrowserStack execution modes with unified interface.
    """

    def __init__(
        self,
        execution_mode: Optional[str] = None,
        browser: str = "chrome",
        capability_name: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """Initialize base page with driver creation.

        Args:
            execution_mode: "local" or "browserstack". If None, reads from env var
            browser: Browser name for local mode ("chrome" or "firefox")
            capability_name: BrowserStack capability name (overrides browser for cloud mode)
            timeout: Default timeout for wait operations
        """
        self.logger = get_test_logger(f"base_page_{browser}")
        self.timeout = timeout

        # Determine execution mode
        self.execution_mode = execution_mode or config.get_optional_env(
            "EXECUTION_MODE", "local"
        )
        self.browser = browser
        self.capability_name = capability_name

        self.logger.info(f"Initializing BasePage in {self.execution_mode} mode")

        # Create driver based on mode
        self.driver = self._create_driver()
        self.wait = WebDriverWait(self.driver, self.timeout)

    def _create_driver(self) -> WebDriver:
        """Create WebDriver based on execution mode.

        Returns:
            WebDriver instance (local or remote)
        """
        if self.execution_mode.lower() == "local":
            return self._create_local_driver()
        elif self.execution_mode.lower() == "browserstack":
            return self._create_browserstack_driver()
        else:
            raise ValueError(f"Unsupported execution mode: {self.execution_mode}")

    def _create_local_driver(self) -> WebDriver:
        """Create local WebDriver instance.

        Returns:
            Local WebDriver instance
        """
        self.logger.info(f"Creating local {self.browser} driver")

        # Use base WebDriver type for mypy
        driver: WebDriver
        if self.browser.lower() == "chrome":
            chrome_service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=chrome_service)

        elif self.browser.lower() == "firefox":
            firefox_service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=firefox_service)

        else:
            raise ValueError(f"Unsupported local browser: {self.browser}")

        # Set window size for consistency
        driver.set_window_size(1920, 1080)
        self.logger.info(f"✅ Local {self.browser} driver created successfully")

        return driver

    def _create_browserstack_driver(self) -> WebDriver:
        """Create BrowserStack remote WebDriver instance.

        Returns:
            Remote WebDriver instance connected to BrowserStack
        """
        self.logger.info("Creating BrowserStack remote driver")

        # Get capabilities
        if self.capability_name:
            capabilities = self._get_capability_by_name(self.capability_name)
        else:
            # Default mapping for browser names
            browser_mapping = {
                "chrome": "Windows_10_Chrome",
                "safari": "macOS_Safari",
                "firefox": "macOS_Monterey_Firefox",
                "firefox": "macOS_Ventura_Firefox",
            }
            capability_name = browser_mapping.get(
                self.browser.lower(), "Windows_10_Chrome"
            )
            capabilities = self._get_capability_by_name(capability_name)

        # Add authentication
        capabilities.update(
            {
                "browserstack.user": config.browserstack_username,
                "browserstack.key": config.browserstack_access_key,
            }
        )

        # Create remote driver
        try:
            # Use proper typing for command_executor
            hub_url = str(BROWSERSTACK_CONFIG["hub_url"])

            # For Selenium 4+, use ChromeOptions or FirefoxOptions with capabilities
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            from selenium.webdriver.firefox.options import Options as FirefoxOptions

            # Determine browser type from capabilities
            browser_name = capabilities.get("browserName", "Chrome").lower()

            # Use union type for mypy compatibility
            options: Union[ChromeOptions, FirefoxOptions]
            if browser_name == "chrome":
                options = ChromeOptions()
            elif browser_name == "firefox":
                options = FirefoxOptions()
            else:
                # Default to Chrome options
                options = ChromeOptions()

            # Add all BrowserStack capabilities to options
            for key, value in capabilities.items():
                options.set_capability(key, value)

            # Create remote driver with options
            driver = webdriver.Remote(command_executor=hub_url, options=options)

            self.logger.info("✅ BrowserStack driver created successfully")
            self.logger.info(f"Session: {capabilities.get('sessionName', 'Unknown')}")

            return driver

        except Exception as e:
            self.logger.error(f"❌ Failed to create BrowserStack driver: {str(e)}")
            raise

    def _get_capability_by_name(self, name: str) -> Dict[str, Any]:
        """Get BrowserStack capability by name.

        Args:
            name: Capability name (e.g., "Windows_10_Chrome")

        Returns:
            Capability dictionary
        """
        capability_methods = {
            "Windows_10_Chrome": BrowserStackCapabilities.get_windows_chrome,
            "macOS_Safari": BrowserStackCapabilities.get_macos_safari,
            "macOS_Ventura_Firefox": BrowserStackCapabilities.get_macos_firefox,
            "macOS_Monterey_Firefox": BrowserStackCapabilities.get_macos_monterey_firefox,
            "Samsung_Galaxy_S22_Chrome": BrowserStackCapabilities.get_samsung_galaxy_s22,
        }

        if name not in capability_methods:
            raise ValueError(
                f"Unknown capability name: {name}. Available: {list(capability_methods.keys())}"
            )

        return capability_methods[name]()

    # Common WebDriver utility methods

    def navigate_to(self, url: str) -> None:
        """Navigate to a URL.

        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def find_element(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> Any:
        """Find element with wait.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override

        Returns:
            WebElement if found
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found within {wait_time}s: {locator}")
            raise

    def find_elements(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> list:
        """Find multiple elements with wait.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override

        Returns:
            List of WebElements
        """
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found within {wait_time}s: {locator}")
            return []

    def wait_for_element_visible(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> Any:
        """Wait for element to be visible.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override

        Returns:
            WebElement when visible
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible within {wait_time}s: {locator}")
            raise

    def wait_for_element_clickable(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> Any:
        """Wait for element to be clickable.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override

        Returns:
            WebElement when clickable
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable within {wait_time}s: {locator}")
            raise

    def click_element(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> None:
        """Click an element after waiting for it to be clickable.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        self.logger.debug(f"Clicked element: {locator}")

    def send_keys_to_element(
        self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None
    ) -> None:
        """Send keys to an element after waiting for it to be visible.

        Args:
            locator: Tuple of (By strategy, selector)
            text: Text to send
            timeout: Optional timeout override
        """
        element = self.wait_for_element_visible(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.debug(f"Sent keys '{text}' to element: {locator}")

    def get_element_text(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ) -> str:
        """Get text from an element.

        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Optional timeout override

        Returns:
            Element text content
        """
        element = self.wait_for_element_visible(locator, timeout)
        text = str(element.text)  # Explicitly cast to str for mypy
        self.logger.debug(f"Got text '{text}' from element: {locator}")
        return text

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element is present (no wait).

        Args:
            locator: Tuple of (By strategy, selector)

        Returns:
            True if element exists, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def get_current_url(self) -> str:
        """Get current page URL.

        Returns:
            Current URL
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get current page title.

        Returns:
            Page title
        """
        return self.driver.title

    def close(self) -> None:
        """Close the browser and clean up resources."""
        if hasattr(self, "driver") and self.driver:
            self.logger.info(f"Closing {self.execution_mode} driver")
            self.driver.quit()
            self.logger.info("✅ Driver closed successfully")

    def __del__(self) -> None:
        """Cleanup driver on object destruction."""
        try:
            self.close()
        except Exception:
            # Ignore errors during cleanup
            pass

    def __enter__(self) -> "BasePage":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit with cleanup."""
        self.close()
