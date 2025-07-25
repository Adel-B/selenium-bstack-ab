"""Environment variable loader with validation and type conversion."""

import os

from dotenv import load_dotenv


class EnvironmentConfig:
    """Environment configuration manager with validation."""

    def __init__(self) -> None:
        """Initialize environment configuration by loading .env file."""
        load_dotenv()

    @staticmethod
    def get_required_env(key: str) -> str:
        """Get required environment variable or raise error if missing.

        Args:
            key: Environment variable name

        Returns:
            Environment variable value

        Raises:
            ValueError: If environment variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    @staticmethod
    def get_optional_env(key: str, default: str = "") -> str:
        """Get optional environment variable with default value.

        Args:
            key: Environment variable name
            default: Default value if not set

        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)

    # BrowserStack Configuration
    @property
    def browserstack_username(self) -> str:
        """BrowserStack username."""
        return self.get_required_env("BROWSERSTACK_USERNAME")

    @property
    def browserstack_access_key(self) -> str:
        """BrowserStack access key."""
        return self.get_required_env("BROWSERSTACK_ACCESS_KEY")

    # Test Configuration
    @property
    def base_url(self) -> str:
        """Base URL for testing."""
        return self.get_optional_env("BASE_URL", "https://www.bstackdemo.com")

    @property
    def test_username(self) -> str:
        """Test application username."""
        return self.get_optional_env("TEST_USERNAME", "demouser")

    @property
    def test_password(self) -> str:
        """Test application password."""
        return self.get_optional_env("TEST_PASSWORD", "testingisfun99")

    # Product Test Data
    @property
    def target_brand(self) -> str:
        """Target brand filter for product testing."""
        return self.get_optional_env("TARGET_BRAND", "Samsung")

    @property
    def target_product_name(self) -> str:
        """Target product name for favoriting test."""
        return self.get_optional_env("TARGET_PRODUCT_NAME", "Galaxy S20+")

    @property
    def target_product_id(self) -> str:
        """Target product ID for favoriting test."""
        return self.get_optional_env("TARGET_PRODUCT_ID", "11")

    def validate_browserstack_credentials(self) -> bool:
        """Validate that BrowserStack credentials are available.

        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            self.browserstack_username
            self.browserstack_access_key
            return True
        except ValueError:
            return False


# Global configuration instance
config = EnvironmentConfig()
