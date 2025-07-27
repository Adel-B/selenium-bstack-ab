"""Login page object for bstackdemo.com."""

from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from utils.env_loader import config
from utils.logger_config import get_test_logger


class LoginPage(BasePage):
    """Page object for bstackdemo.com login functionality."""

    def __init__(
        self,
        execution_mode: Optional[str] = None,
        browser: str = "chrome",
        capability_name: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """Initialize LoginPage.

        Args:
            execution_mode: "local" or "browserstack"
            browser: Browser name for local mode
            capability_name: BrowserStack capability name
            timeout: Default timeout for operations
        """
        super().__init__(execution_mode, browser, capability_name, timeout)
        self.logger = get_test_logger("login_page")

    # Page Elements (Locators) - Based on actual bstackdemo.com HTML
    SIGN_IN_BUTTON = (
        By.ID,
        "signin",
    )  # <span id="signin" class="Navbar_link__3Blki logout-link mt-2" role="link">
    LOGIN_BUTTON = (
        By.ID,
        "login-btn",
    )  # <button id="login-btn" type="submit" class="Button_root__24MxS Button_slim__2caxo">
    LOGOUT_LINK = (
        By.CSS_SELECTOR,
        ".logout-link",
    )  # When logged in, signin becomes logout

    # React Select containers - using stable IDs
    USERNAME_CONTAINER = (
        By.ID,
        "username",
    )  # <div id="username" class=" css-2b097c-container">
    PASSWORD_CONTAINER = (
        By.ID,
        "password",
    )  # <div id="password" class=" css-2b097c-container">

    # React Select inputs - these IDs may change, but pattern is consistent
    USERNAME_DROPDOWN = (
        By.CSS_SELECTOR,
        "#username input",
    )  # Input within username container
    PASSWORD_DROPDOWN = (
        By.CSS_SELECTOR,
        "#password input",
    )  # Input within password container

    # Username and password option patterns - these will be dynamic
    USERNAME_OPTION_LOCATOR = "react-select-4-option-"  # Note: numbers may vary
    PASSWORD_OPTION_LOCATOR = "react-select-5-option-"  # Note: numbers may vary

    def navigate_to_login_page(self) -> None:
        """Navigate to the bstackdemo.com homepage."""
        self.logger.info("Navigating to bstackdemo.com")
        self.navigate_to(config.base_url)

        # Wait for page to load
        self.wait_for_element_visible(self.SIGN_IN_BUTTON)
        self.logger.info("✅ Login page loaded successfully")

    def click_sign_in(self) -> None:
        """Click the sign in button to open login modal."""
        self.logger.info("Clicking Sign In button")
        self.click_element(self.SIGN_IN_BUTTON)

        # Wait for login modal to appear
        self.wait_for_element_visible(self.USERNAME_CONTAINER, timeout=10)
        self.logger.info("✅ Login modal opened")

    def select_username(self, username: Optional[str] = None) -> None:
        """Select username from React Select dropdown.

        Args:
            username: Username to select (defaults to config.test_username)
        """
        username = username or config.test_username
        self.logger.info(f"Selecting username: {username}")

        # Click on username dropdown to open it
        username_dropdown = self.wait_for_element_clickable(self.USERNAME_CONTAINER)
        username_dropdown.click()

        # Send keys directly to the input field (more reliable than clicking options)
        # The input ID is typically react-select-2-input but can vary
        username_input = self.wait_for_element_visible(
            (By.CSS_SELECTOR, "#username input"), timeout=10
        )
        username_input.send_keys(username)
        username_input.send_keys(Keys.ENTER)

        self.logger.info(f"✅ Username '{username}' selected")

    def select_password(self, password: Optional[str] = None) -> None:
        """Select password from React Select dropdown.

        Args:
            password: Password to select (defaults to config.test_password)
        """
        password = password or config.test_password
        self.logger.info("Selecting password")

        # Click on password dropdown to open it
        password_dropdown = self.wait_for_element_clickable(self.PASSWORD_CONTAINER)
        password_dropdown.click()

        # Send keys directly to the input field (more reliable than clicking options)
        # The input ID is typically react-select-3-input but can vary
        password_input = self.wait_for_element_visible(
            (By.CSS_SELECTOR, "#password input"), timeout=10
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        self.logger.info("✅ Password selected")

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        self.logger.info("Clicking Login button")
        self.click_element(self.LOGIN_BUTTON)

        # Wait for login to complete - logout link should appear
        self.wait_for_element_visible(self.LOGOUT_LINK, timeout=15)
        self.logger.info("✅ Login completed successfully")

    def login(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        """Complete login flow with provided credentials.

        Args:
            username: Username to login with (defaults to config.test_username)
            password: Password to login with (defaults to config.test_password)
        """
        username = username or config.test_username
        password = password or config.test_password
        self.logger.info(f"Starting login process for user: {username}")

        # Navigate to login page if not already there
        if not self.is_element_present(self.SIGN_IN_BUTTON):
            self.navigate_to_login_page()

        # Complete login flow
        self.click_sign_in()
        self.select_username(username)
        self.select_password(password)
        self.click_login_button()

        self.logger.info("✅ Login flow completed successfully")

    def logout(self) -> None:
        """Logout from the application."""
        self.logger.info("Logging out")

        if self.is_element_present(self.LOGOUT_LINK):
            self.click_element(self.LOGOUT_LINK)

            # Wait for sign in button to reappear
            self.wait_for_element_visible(self.SIGN_IN_BUTTON, timeout=10)
            self.logger.info("✅ Logout completed successfully")
        else:
            self.logger.warning("Logout link not found - user may not be logged in")

    def is_logged_in(self) -> bool:
        """Check if user is currently logged in.

        Returns:
            True if logged in, False otherwise
        """
        return self.is_element_present(self.LOGOUT_LINK)

    def get_current_user(self) -> Optional[str]:
        """Get the currently logged in username.

        Returns:
            Username if logged in, None otherwise
        """
        if self.is_logged_in():
            # Return the configured test username as that's what we're using
            # In a real application, this might read from a user profile element
            return config.test_username
        return None

    def wait_for_page_load(self) -> None:
        """Wait for the login page to fully load."""
        self.logger.info("Waiting for login page to load")
        self.wait_for_element_visible(self.SIGN_IN_BUTTON)
        self.logger.info("✅ Login page loaded")
