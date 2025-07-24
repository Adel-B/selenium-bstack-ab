"""BrowserStack connection validation utilities."""

from typing import Optional, Tuple

import requests
from requests.auth import HTTPBasicAuth

from utils.env_loader import config
from utils.logger_config import get_test_logger


class BrowserStackValidator:
    """Validates BrowserStack connectivity and credentials."""

    def __init__(self) -> None:
        """Initialize validator with environment configuration."""
        self.logger = get_test_logger("browserstack_validator")
        self.username = config.browserstack_username
        self.access_key = config.browserstack_access_key
        self.auth = HTTPBasicAuth(self.username, self.access_key)

    def validate_credentials(self) -> Tuple[bool, str]:
        """Validate BrowserStack credentials by checking account status.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.logger.info("Validating BrowserStack credentials...")

            # Test credentials with account status API
            url = "https://api.browserstack.com/automate/plan.json"
            response = requests.get(url, auth=self.auth, timeout=10)

            if response.status_code == 200:
                data = response.json()
                plan_name = data.get("automate_plan", "Unknown")
                parallel_sessions = data.get("parallel_sessions_max_allowed", "Unknown")

                self.logger.info("✅ BrowserStack credentials valid")
                self.logger.info(f"Plan: {plan_name}")
                self.logger.info(f"Max parallel sessions: {parallel_sessions}")

                return (
                    True,
                    f"Valid credentials - Plan: {plan_name}, Max sessions: {parallel_sessions}",
                )

            elif response.status_code == 401:
                self.logger.error("❌ Invalid BrowserStack credentials")
                return False, "Invalid username or access key"

            else:
                self.logger.error(f"❌ Unexpected response: {response.status_code}")
                return False, f"API returned status code: {response.status_code}"

        except requests.exceptions.Timeout:
            self.logger.error("❌ Connection timeout to BrowserStack API")
            return False, "Connection timeout - check network connectivity"

        except requests.exceptions.ConnectionError:
            self.logger.error("❌ Failed to connect to BrowserStack API")
            return False, "Connection error - check network connectivity"

        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {str(e)}")
            return False, f"Unexpected error: {str(e)}"

    def get_available_browsers(self) -> Optional[list]:
        """Get list of available browsers from BrowserStack.

        Returns:
            List of available browsers or None if failed
        """
        try:
            self.logger.info("Fetching available browsers from BrowserStack...")

            url = "https://api.browserstack.com/automate/browsers.json"
            response = requests.get(url, auth=self.auth, timeout=15)

            if response.status_code == 200:
                browsers: list = response.json()
                self.logger.info(f"✅ Retrieved {len(browsers)} available browsers")
                return browsers
            else:
                self.logger.error(
                    f"❌ Failed to fetch browsers: {response.status_code}"
                )
                return None

        except Exception as e:
            self.logger.error(f"❌ Error fetching browsers: {str(e)}")
            return None

    def validate_capability(self, capability: dict) -> Tuple[bool, str]:
        """Validate that a specific capability is supported.

        Args:
            capability: BrowserStack capability dictionary

        Returns:
            Tuple of (supported: bool, message: str)
        """
        browsers = self.get_available_browsers()
        if not browsers:
            return False, "Could not fetch available browsers"

        # For mobile devices
        if "deviceName" in capability:
            device_name = capability["deviceName"]
            platform_version = capability.get("platformVersion", "")

            for browser in browsers:
                if (
                    browser.get("device") == device_name
                    and browser.get("os_version") == platform_version
                ):
                    return (
                        True,
                        f"Mobile device {device_name} {platform_version} is supported",
                    )

            return False, f"Mobile device {device_name} {platform_version} not found"

        # For desktop browsers
        else:
            browser_name = capability.get("browserName", "")
            os_name = capability.get("os", "")
            os_version = capability.get("osVersion", "")

            for browser in browsers:
                if (
                    browser.get("browser") == browser_name.lower()
                    and browser.get("os") == os_name
                    and browser.get("os_version") == os_version
                ):
                    return (
                        True,
                        f"Desktop {os_name} {os_version} {browser_name} is supported",
                    )

            return False, f"Desktop {os_name} {os_version} {browser_name} not found"

    def full_validation(self) -> bool:
        """Run complete BrowserStack validation.

        Returns:
            True if all validations pass, False otherwise
        """
        self.logger.info("🔍 Starting full BrowserStack validation...")

        # Validate credentials
        cred_valid, cred_msg = self.validate_credentials()
        if not cred_valid:
            self.logger.error(f"Credential validation failed: {cred_msg}")
            return False

        self.logger.info("✅ BrowserStack validation completed successfully")
        return True


def validate_browserstack_connection() -> bool:
    """Convenience function to validate BrowserStack connection.

    Returns:
        True if validation passes, False otherwise
    """
    validator = BrowserStackValidator()
    return validator.full_validation()
