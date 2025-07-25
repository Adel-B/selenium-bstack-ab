"""BrowserStack capabilities configuration for cross-browser testing."""

import datetime
from typing import Any, Dict, List

# Shared build name for all tests in this run
_SHARED_BUILD_NAME = None


def get_build_name() -> str:
    """Generate timestamped build name for BrowserStack tracking (shared across parallel tests)."""
    global _SHARED_BUILD_NAME
    if _SHARED_BUILD_NAME is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _SHARED_BUILD_NAME = f"samsung-galaxy-favoriting-{timestamp}"
    return _SHARED_BUILD_NAME


class BrowserStackCapabilities:
    """BrowserStack test capabilities definitions."""

    @staticmethod
    def get_windows_chrome() -> Dict[str, Any]:
        """Windows 10 Chrome capabilities for BrowserStack.

        Returns:
            Dictionary containing BrowserStack capabilities for Windows 10 Chrome
        """
        return {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Samsung Galaxy S20+ Favoriting - Windows 10 Chrome",
            "buildName": get_build_name(),
            "projectName": "Samsung Galaxy S20+ Cross-Browser Testing",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
            # SDK recommendations
            "browserstack.debug": True,
            "browserstack.console": "info",
            "browserstack.networkLogs": True,
        }

    @staticmethod
    def get_macos_safari() -> Dict[str, Any]:
        """macOS Safari capabilities for BrowserStack.

        Returns:
            Dictionary containing BrowserStack capabilities for macOS Safari
        """
        return {
            "browserName": "Safari",
            "browserVersion": "latest",
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Samsung Galaxy S20+ Favoriting - macOS Safari",
            "buildName": get_build_name(),
            "projectName": "Samsung Galaxy S20+ Cross-Browser Testing",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
            # SDK recommendations
            "browserstack.debug": True,
            "browserstack.console": "info",
            "browserstack.networkLogs": True,
        }

    @staticmethod
    def get_macos_firefox() -> Dict[str, Any]:
        """macOS Ventura Firefox capabilities for BrowserStack.

        Returns:
            Dictionary containing BrowserStack capabilities for macOS Ventura Firefox
        """
        return {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Samsung Galaxy S20+ Favoriting - macOS Ventura Firefox",
            "buildName": get_build_name(),
            "projectName": "Samsung Galaxy S20+ Cross-Browser Testing",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
            # SDK recommendations
            "browserstack.debug": True,
            "browserstack.console": "info",
            "browserstack.networkLogs": True,
        }

    @staticmethod
    def get_macos_monterey_firefox() -> Dict[str, Any]:
        """macOS Monterey Firefox capabilities for BrowserStack.

        Returns:
            Dictionary containing BrowserStack capabilities for macOS Monterey Firefox
        """
        return {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "os": "OS X",
            "osVersion": "Monterey",
            "sessionName": "Samsung Galaxy S20+ Favoriting - macOS Monterey Firefox",
            "buildName": get_build_name(),
            "projectName": "Samsung Galaxy S20+ Cross-Browser Testing",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
            # SDK recommendations
            "browserstack.debug": True,
            "browserstack.console": "info",
            "browserstack.networkLogs": True,
        }

    @staticmethod
    def get_samsung_galaxy_s22() -> Dict[str, Any]:
        """Samsung Galaxy S22 mobile capabilities for BrowserStack.

        Returns:
            Dictionary containing BrowserStack capabilities for Samsung Galaxy S22
        """
        return {
            "platformName": "Android",
            "platformVersion": "12.0",
            "deviceName": "Samsung Galaxy S22",
            "browserName": "Chrome",
            "sessionName": "Samsung Galaxy S20+ Favoriting - Samsung Galaxy S22",
            "buildName": get_build_name(),
            "projectName": "Samsung Galaxy S20+ Cross-Browser Testing",
            "local": False,
            # SDK recommendations for mobile
            "browserstack.debug": True,
            "browserstack.console": "info",
            "browserstack.networkLogs": True,
            "browserstack.appiumLogs": True,
        }

    @classmethod
    def get_all_capabilities(cls) -> List[Dict[str, Any]]:
        """Get all defined capabilities for parametrized testing.

        Returns:
            List of all capability dictionaries
        """
        return [
            cls.get_windows_chrome(),
            cls.get_macos_safari(),
            cls.get_macos_monterey_firefox(),
            cls.get_samsung_galaxy_s22(),
        ]

    @staticmethod
    def get_capability_names() -> List[str]:
        """Get human-readable names for each capability set.

        Returns:
            List of descriptive names for test parametrization
        """
        return [
            "Windows_10_Chrome",
            "macOS_Safari",
            "macOS_Monterey_Firefox",
            "Samsung_Galaxy_S22_Chrome",
        ]

    @classmethod
    def get_capabilities_with_names(cls) -> List[tuple]:
        """Get capabilities paired with their descriptive names.

        Returns:
            List of tuples (name, capabilities) for pytest parametrization
        """
        capabilities = cls.get_all_capabilities()
        names = cls.get_capability_names()
        return list(zip(names, capabilities))


# Common BrowserStack configuration
BROWSERSTACK_CONFIG = {
    "hub_url": "https://hub-cloud.browserstack.com/wd/hub",
    "timeout": 30,
    "idle_timeout": 300,
    "debug": True,
    "networkLogs": True,
    "consoleLogs": "info",
    "seleniumLogs": "info",
}
