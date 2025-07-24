"""BrowserStack capabilities configuration for cross-browser testing."""

from typing import Any, Dict, List


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
            "sessionName": "Samsung Galaxy S20+ Favorite Test - Windows Chrome",
            "buildName": "selenium-bstack-ab-build",
            "projectName": "Cross-Browser Samsung Galaxy Test",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
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
            "sessionName": "Samsung Galaxy S20+ Favorite Test - macOS Firefox",
            "buildName": "selenium-bstack-ab-build",
            "projectName": "Cross-Browser Samsung Galaxy Test",
            "local": False,
            "seleniumVersion": "4.15.0",
            "resolution": "1920x1080",
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
            "sessionName": "Samsung Galaxy S20+ Favorite Test - Galaxy S22",
            "buildName": "selenium-bstack-ab-build",
            "projectName": "Cross-Browser Samsung Galaxy Test",
            "local": False,
        }

    @classmethod
    def get_all_capabilities(cls) -> List[Dict[str, Any]]:
        """Get all defined capabilities for parametrized testing.

        Returns:
            List of all capability dictionaries
        """
        return [
            cls.get_windows_chrome(),
            cls.get_macos_firefox(),
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
            "macOS_Ventura_Firefox",
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
