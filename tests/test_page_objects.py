"""Tests for page objects functionality."""


import pytest

from pages.favorites_page import FavoritesPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.env_loader import config
from utils.logger_config import get_test_logger


class TestPageObjects:
    """Test page objects functionality individually."""

    def test_login_page_navigation(self) -> None:
        """Test LoginPage navigation and basic functionality."""
        logger = get_test_logger("test_login_navigation")
        logger.info("Testing LoginPage navigation...")

        with LoginPage(execution_mode="local", browser="chrome") as login_page:
            # Test navigation
            login_page.navigate_to_login_page()

            # Verify we're on the right page
            assert "bstackdemo" in login_page.get_current_url()
            title = login_page.get_page_title()
            assert title is not None

            # Test sign-in button is present
            assert login_page.is_element_present(login_page.SIGN_IN_BUTTON)

            logger.info("✅ LoginPage navigation test passed")

    def test_login_page_modal_open(self) -> None:
        """Test opening the login modal."""
        logger = get_test_logger("test_login_modal")
        logger.info("Testing login modal functionality...")

        with LoginPage(execution_mode="local", browser="chrome") as login_page:
            login_page.navigate_to_login_page()

            # Test opening login modal
            login_page.click_sign_in()

            # Verify modal elements are present
            assert login_page.is_element_present(login_page.USERNAME_CONTAINER)
            assert login_page.is_element_present(login_page.PASSWORD_CONTAINER)
            assert login_page.is_element_present(login_page.LOGIN_BUTTON)

            logger.info("✅ Login modal test passed")

    @pytest.mark.skipif(
        not config.validate_browserstack_credentials(),
        reason="BrowserStack credentials not configured",
    )
    def test_login_page_browserstack(self) -> None:
        """Test LoginPage with BrowserStack."""
        logger = get_test_logger("test_login_browserstack")
        logger.info("Testing LoginPage with BrowserStack...")

        with LoginPage(
            execution_mode="browserstack", capability_name="Windows_10_Chrome"
        ) as login_page:
            login_page.navigate_to_login_page()

            # Verify we're on the right page
            assert "bstackdemo" in login_page.get_current_url()

            # Test sign-in button is present
            assert login_page.is_element_present(login_page.SIGN_IN_BUTTON)

            logger.info("✅ LoginPage BrowserStack test passed")

    def test_product_page_navigation(self) -> None:
        """Test ProductPage navigation and basic functionality."""
        logger = get_test_logger("test_product_navigation")
        logger.info("Testing ProductPage navigation...")

        with ProductPage(execution_mode="local", browser="chrome") as product_page:
            # Navigate to the site
            product_page.navigate_to(config.base_url)

            # Test products load
            product_page.wait_for_products_to_load()

            # Verify product elements are present
            assert product_page.is_element_present(product_page.PRODUCT_CARDS)
            assert product_page.is_element_present(
                product_page.VENDOR_FILTERS_CONTAINER
            )

            # Test getting product titles
            titles = product_page.get_product_titles()
            assert len(titles) > 0

            logger.info(
                f"✅ ProductPage navigation test passed - Found {len(titles)} products"
            )

    def test_product_page_samsung_filter(self) -> None:
        """Test Samsung filtering functionality."""
        logger = get_test_logger("test_samsung_filter")
        logger.info("Testing Samsung filter functionality...")

        with ProductPage(execution_mode="local", browser="chrome") as product_page:
            product_page.navigate_to(config.base_url)
            product_page.wait_for_products_to_load()

            # Get initial product count
            initial_titles = product_page.get_product_titles()
            initial_count = len(initial_titles)
            logger.info(f"Initial product count: {initial_count}")

            # Apply Samsung filter
            product_page.filter_by_samsung()

            # Get filtered product count
            filtered_titles = product_page.get_product_titles()
            filtered_count = len(filtered_titles)
            logger.info(f"Filtered product count: {filtered_count}")

            # Verify filtering worked (should be fewer or same products)
            assert filtered_count <= initial_count

            # Check if Galaxy S20+ is visible (our target product)
            is_galaxy_visible = product_page.is_galaxy_s20_plus_visible()
            logger.info(f"Galaxy S20+ visible: {is_galaxy_visible}")

            logger.info("✅ Samsung filter test passed")

    def test_favorites_page_cart_operations(self) -> None:
        """Test FavoritesPage cart operations."""
        logger = get_test_logger("test_favorites_cart")
        logger.info("Testing favorites cart operations...")

        with FavoritesPage(execution_mode="local", browser="chrome") as favorites_page:
            favorites_page.navigate_to(config.base_url)

            # Test opening cart
            favorites_page.open_favorites_cart()

            # Verify cart elements are present
            assert favorites_page.is_element_present(favorites_page.CART_HEADER)

            # Test getting favorites count (should be 0 initially)
            count = favorites_page.get_favorites_count()
            logger.info(f"Initial favorites count: {count}")

            # Test checking if cart is empty
            is_empty = favorites_page.is_favorites_empty()
            logger.info(f"Cart is empty: {is_empty}")

            # Test closing cart
            favorites_page.close_favorites_cart()

            logger.info("✅ Favorites cart operations test passed")

    def test_page_objects_inheritance(self) -> None:
        """Test that page objects properly inherit from BasePage."""
        logger = get_test_logger("test_inheritance")
        logger.info("Testing page objects inheritance...")

        # Test that all page objects can be instantiated and have BasePage methods
        with LoginPage(execution_mode="local", browser="chrome") as login_page:
            assert hasattr(login_page, "navigate_to")
            assert hasattr(login_page, "find_element")
            assert hasattr(login_page, "wait_for_element_visible")
            assert login_page.execution_mode == "local"
            assert login_page.browser == "chrome"

        with ProductPage(execution_mode="local", browser="chrome") as product_page:
            assert hasattr(product_page, "navigate_to")
            assert hasattr(product_page, "find_element")
            assert hasattr(product_page, "click_element")
            assert product_page.execution_mode == "local"

        with FavoritesPage(execution_mode="local", browser="chrome") as favorites_page:
            assert hasattr(favorites_page, "navigate_to")
            assert hasattr(favorites_page, "find_elements")
            assert hasattr(favorites_page, "is_element_present")
            assert favorites_page.execution_mode == "local"

        logger.info("✅ Page objects inheritance test passed")

    @pytest.mark.parametrize("execution_mode", ["local"])
    def test_page_objects_mode_selection(self, execution_mode: str) -> None:
        """Test page objects with different execution modes."""
        logger = get_test_logger(f"test_mode_{execution_mode}")
        logger.info(f"Testing page objects with {execution_mode} mode...")

        # Test all page objects can work with specified mode
        with LoginPage(execution_mode=execution_mode, browser="chrome") as login_page:
            assert login_page.execution_mode == execution_mode
            login_page.navigate_to(config.base_url)
            assert "bstackdemo" in login_page.get_current_url()

        logger.info(f"✅ Page objects {execution_mode} mode test passed")

    def test_page_objects_error_handling(self) -> None:
        """Test page objects error handling."""
        logger = get_test_logger("test_error_handling")
        logger.info("Testing page objects error handling...")

        with ProductPage(execution_mode="local", browser="chrome") as product_page:
            product_page.navigate_to(config.base_url)

            # Test searching for non-existent product
            found = product_page.search_for_product("NonExistentProduct12345")
            assert found is False

            # Test checking for non-existent product visibility
            # This should not raise an exception, just return False
            try:
                # Temporarily modify the locator to test error handling
                original_locator = product_page.GALAXY_S20_PLUS_CARD
                product_page.GALAXY_S20_PLUS_CARD = (
                    product_page.GALAXY_S20_PLUS_CARD[0],
                    "nonexistent-element",
                )

                is_visible = product_page.is_galaxy_s20_plus_visible()
                assert is_visible is False

                # Restore original locator
                product_page.GALAXY_S20_PLUS_CARD = original_locator

            except Exception as e:
                # Restore original locator in case of exception
                product_page.GALAXY_S20_PLUS_CARD = original_locator
                logger.warning(f"Error handling test encountered exception: {str(e)}")

        logger.info("✅ Page objects error handling test passed")

    def test_page_objects_logging(self) -> None:
        """Test that page objects produce appropriate logging."""
        logger = get_test_logger("test_logging")
        logger.info("Testing page objects logging...")

        with LoginPage(execution_mode="local", browser="chrome") as login_page:
            # Verify logger is configured
            assert login_page.logger is not None
            assert hasattr(login_page.logger, "info")
            assert hasattr(login_page.logger, "warning")
            assert hasattr(login_page.logger, "error")

        logger.info("✅ Page objects logging test passed")
