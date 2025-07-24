"""BrowserStack configuration validation test."""

import pytest

from utils.browserstack_config import BROWSERSTACK_CONFIG, BrowserStackCapabilities
from utils.browserstack_validator import BrowserStackValidator
from utils.env_loader import config
from utils.logger_config import get_test_logger


class TestBrowserStackConfig:
    """BrowserStack configuration validation tests."""

    def test_capabilities_structure(self) -> None:
        """Test that all capabilities have required structure."""
        logger = get_test_logger("test_capabilities_structure")

        logger.info("Testing BrowserStack capabilities structure...")

        # Test Windows Chrome capabilities
        windows_chrome = BrowserStackCapabilities.get_windows_chrome()
        assert "browserName" in windows_chrome
        assert "os" in windows_chrome
        assert "sessionName" in windows_chrome
        assert windows_chrome["browserName"] == "Chrome"
        assert windows_chrome["os"] == "Windows"
        logger.info("✅ Windows Chrome capabilities valid")

        # Test macOS Firefox capabilities
        macos_firefox = BrowserStackCapabilities.get_macos_firefox()
        assert "browserName" in macos_firefox
        assert "os" in macos_firefox
        assert "sessionName" in macos_firefox
        assert macos_firefox["browserName"] == "Firefox"
        assert macos_firefox["os"] == "OS X"
        logger.info("✅ macOS Firefox capabilities valid")

        # Test Samsung Galaxy S22 capabilities
        galaxy_s22 = BrowserStackCapabilities.get_samsung_galaxy_s22()
        assert "deviceName" in galaxy_s22
        assert "platformName" in galaxy_s22
        assert "sessionName" in galaxy_s22
        assert galaxy_s22["deviceName"] == "Samsung Galaxy S22"
        assert galaxy_s22["platformName"] == "Android"
        logger.info("✅ Samsung Galaxy S22 capabilities valid")

        logger.info("All capability structures are valid")

    def test_capabilities_lists(self) -> None:
        """Test capability list functions."""
        logger = get_test_logger("test_capabilities_lists")

        logger.info("Testing capability list functions...")

        # Test all capabilities
        all_caps = BrowserStackCapabilities.get_all_capabilities()
        assert len(all_caps) == 3
        logger.info(f"✅ Found {len(all_caps)} capability sets")

        # Test capability names
        names = BrowserStackCapabilities.get_capability_names()
        assert len(names) == 3
        assert "Windows_10_Chrome" in names
        assert "macOS_Ventura_Firefox" in names
        assert "Samsung_Galaxy_S22_Chrome" in names
        logger.info(f"✅ Capability names: {names}")

        # Test capabilities with names
        caps_with_names = BrowserStackCapabilities.get_capabilities_with_names()
        assert len(caps_with_names) == 3
        for name, cap in caps_with_names:
            assert isinstance(name, str)
            assert isinstance(cap, dict)
            assert "sessionName" in cap
        logger.info("✅ Capabilities with names structure valid")

    def test_browserstack_config(self) -> None:
        """Test BrowserStack configuration constants."""
        logger = get_test_logger("test_browserstack_config")

        logger.info("Testing BrowserStack configuration...")

        assert "hub_url" in BROWSERSTACK_CONFIG
        assert "timeout" in BROWSERSTACK_CONFIG
        assert (
            BROWSERSTACK_CONFIG["hub_url"]
            == "https://hub-cloud.browserstack.com/wd/hub"
        )
        assert isinstance(BROWSERSTACK_CONFIG["timeout"], int)

        logger.info("✅ BrowserStack configuration valid")

    def test_environment_credentials_available(self) -> None:
        """Test that BrowserStack credentials are configured."""
        logger = get_test_logger("test_environment_credentials")

        logger.info("Testing BrowserStack credentials availability...")

        # Test that we can check for credentials
        has_credentials = config.validate_browserstack_credentials()

        if has_credentials:
            logger.info("✅ BrowserStack credentials are configured")
            assert config.browserstack_username
            assert config.browserstack_access_key
        else:
            logger.warning("⚠️  BrowserStack credentials not configured")
            logger.info(
                "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY in .env file"
            )

    @pytest.mark.skipif(
        not config.validate_browserstack_credentials(),
        reason="BrowserStack credentials not configured",
    )
    def test_browserstack_connection(self) -> None:
        """Test actual connection to BrowserStack (requires credentials)."""
        logger = get_test_logger("test_browserstack_connection")

        logger.info("Testing BrowserStack connection...")

        validator = BrowserStackValidator()

        # Test credential validation
        is_valid, message = validator.validate_credentials()
        assert is_valid, f"BrowserStack connection failed: {message}"

        logger.info(f"✅ BrowserStack connection successful: {message}")

    def test_browserstack_validator_initialization(self) -> None:
        """Test BrowserStack validator can be initialized."""
        logger = get_test_logger("test_validator_init")

        logger.info("Testing BrowserStack validator initialization...")

        # Should not raise exception even without credentials
        validator = BrowserStackValidator()
        assert validator is not None
        assert hasattr(validator, "validate_credentials")
        assert hasattr(validator, "full_validation")

        logger.info("✅ BrowserStack validator initialized successfully")
