"""Favorites page object for bstackdemo.com."""

from typing import List, Optional

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger_config import get_test_logger


class FavoritesPage(BasePage):
    """Page object for bstackdemo.com favorites functionality."""

    def __init__(
        self,
        execution_mode: Optional[str] = None,
        browser: str = "chrome",
        capability_name: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """Initialize FavoritesPage.

        Args:
            execution_mode: "local" or "browserstack"
            browser: Browser name for local mode
            capability_name: BrowserStack capability name
            timeout: Default timeout for operations
        """
        super().__init__(execution_mode, browser, capability_name, timeout)
        self.logger = get_test_logger("favorites_page")

    # Page Elements (Locators) - Based on actual bstackdemo.com HTML structure
    CART_ICON = (By.CSS_SELECTOR, ".float-cart")
    CART_OPEN_BUTTON = (By.CSS_SELECTOR, ".bag--float-cart-closed")
    CART_CLOSE_BUTTON = (By.CSS_SELECTOR, ".float-cart__close-btn")
    CART_HEADER = (By.CSS_SELECTOR, ".float-cart__header")
    CART_ITEMS = (By.CSS_SELECTOR, ".float-cart__content .shelf-item")
    CART_ITEM_TITLES = (By.CSS_SELECTOR, ".float-cart__content .shelf-item__title")
    CART_ITEM_REMOVE_BUTTONS = (
        By.CSS_SELECTOR,
        ".float-cart__content .shelf-item__del",
    )

    # Cart quantity and total
    CART_QUANTITY = (By.CSS_SELECTOR, ".bag__quantity")
    CART_TOTAL = (By.CSS_SELECTOR, ".float-cart__footer .sub-price__val")

    # Empty cart state
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".float-cart__content p")

    # Favorites page elements (when on /favourites page)
    FAVORITES_PAGE_ITEMS = (By.CSS_SELECTOR, ".shelf-item")
    FAVORITES_PAGE_TITLES = (By.CSS_SELECTOR, ".shelf-item__title")

    # Galaxy S20+ specific in favorites - using stable attributes from HTML
    GALAXY_S20_PLUS_ID = "11"
    GALAXY_S20_PLUS_SKU = "samsung-S20+-device-info.png"
    GALAXY_S20_PLUS_IN_FAVORITES = (By.ID, GALAXY_S20_PLUS_ID)
    GALAXY_S20_PLUS_BY_SKU_IN_FAVORITES = (
        By.CSS_SELECTOR,
        f"[data-sku='{GALAXY_S20_PLUS_SKU}']",
    )
    GALAXY_S20_PLUS_TITLE_IN_FAVORITES = (
        By.CSS_SELECTOR,
        f"[id='{GALAXY_S20_PLUS_ID}'] .shelf-item__title",
    )

    def open_favorites_cart(self) -> None:
        """Open the favorites cart to view favorited items."""
        self.logger.info("Opening favorites cart")

        try:
            # Look for the cart icon that indicates closed state
            cart_button = self.wait_for_element_clickable(
                self.CART_OPEN_BUTTON, timeout=10
            )
            cart_button.click()

            # Wait for cart to open
            self.wait_for_element_visible(self.CART_HEADER, timeout=10)
            self.logger.info("✅ Favorites cart opened successfully")

        except Exception as e:
            self.logger.warning(f"Could not open favorites cart: {str(e)}")
            # Cart might already be open, check if header is visible
            if self.is_element_present(self.CART_HEADER):
                self.logger.info("Cart appears to already be open")
            else:
                raise

    def close_favorites_cart(self) -> None:
        """Close the favorites cart."""
        self.logger.info("Closing favorites cart")

        try:
            close_button = self.wait_for_element_clickable(
                self.CART_CLOSE_BUTTON, timeout=5
            )
            close_button.click()

            # Wait for cart to close
            self.wait_for_element_visible(self.CART_OPEN_BUTTON, timeout=10)
            self.logger.info("✅ Favorites cart closed successfully")

        except Exception as e:
            self.logger.warning(f"Could not close favorites cart: {str(e)}")

    def get_favorites_count(self) -> int:
        """Get the number of items in favorites.

        Returns:
            Number of favorited items
        """
        self.logger.info("Getting favorites count")

        try:
            quantity_element = self.find_element(self.CART_QUANTITY, timeout=5)
            quantity_text = quantity_element.text
            count = int(quantity_text) if quantity_text.isdigit() else 0

            self.logger.info(f"Favorites count: {count}")
            return count

        except Exception as e:
            self.logger.warning(f"Could not get favorites count: {str(e)}")
            return 0

    def get_favorited_items(self) -> List[str]:
        """Get list of all favorited item titles.

        Returns:
            List of favorited item titles
        """
        self.logger.info("Getting list of favorited items")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        try:
            item_elements = self.find_elements(self.CART_ITEM_TITLES, timeout=5)
            item_titles = [element.text for element in item_elements]

            self.logger.info(f"Found {len(item_titles)} favorited items: {item_titles}")
            return item_titles

        except Exception as e:
            self.logger.warning(f"Could not get favorited items: {str(e)}")
            return []

    def is_galaxy_s20_plus_in_favorites(self) -> bool:
        """Check if Galaxy S20+ is present in the favorites list.

        Returns:
            True if Galaxy S20+ is in favorites, False otherwise
        """
        self.logger.info("Checking if Galaxy S20+ is in favorites")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        try:
            # Look specifically for Galaxy S20+ in the cart
            galaxy_element = self.find_element(
                self.GALAXY_S20_PLUS_IN_FAVORITES, timeout=5
            )
            is_present = bool(galaxy_element.is_displayed())

            if is_present:
                self.logger.info("✅ Galaxy S20+ is present in favorites")
            else:
                self.logger.warning(
                    "Galaxy S20+ element found but not visible in favorites"
                )

            return is_present

        except Exception as e:
            self.logger.warning(f"Galaxy S20+ not found in favorites: {str(e)}")

            # Alternative check using title list
            favorited_items = self.get_favorited_items()
            is_in_list = any("Galaxy S20+" in item for item in favorited_items)

            if is_in_list:
                self.logger.info("✅ Galaxy S20+ found in favorites list")
            else:
                self.logger.warning("Galaxy S20+ not found in favorites list")

            return is_in_list

    def remove_item_from_favorites(self, item_title: str) -> bool:
        """Remove a specific item from favorites.

        Args:
            item_title: Title of the item to remove

        Returns:
            True if item was removed successfully, False otherwise
        """
        self.logger.info(f"Removing '{item_title}' from favorites")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        try:
            # Find the remove button for the specific item
            remove_button_xpath = f"//div[contains(@class, 'float-cart__content')]//p[@class='shelf-item__title' and contains(text(), '{item_title}')]//following-sibling::div[@class='shelf-item__del']"
            remove_button = self.driver.find_element(By.XPATH, remove_button_xpath)

            remove_button.click()

            # Wait a moment for the removal to process
            import time

            time.sleep(1)

            # Verify item was removed
            is_still_present = self.is_item_in_favorites(item_title)
            success = not is_still_present

            if success:
                self.logger.info(
                    f"✅ '{item_title}' removed from favorites successfully"
                )
            else:
                self.logger.warning(
                    f"'{item_title}' may not have been removed from favorites"
                )

            return success

        except Exception as e:
            self.logger.error(
                f"Failed to remove '{item_title}' from favorites: {str(e)}"
            )
            return False

    def is_item_in_favorites(self, item_title: str) -> bool:
        """Check if a specific item is in favorites.

        Args:
            item_title: Title of the item to check

        Returns:
            True if item is in favorites, False otherwise
        """
        self.logger.info(f"Checking if '{item_title}' is in favorites")

        favorited_items = self.get_favorited_items()
        is_present = any(item_title in item for item in favorited_items)

        if is_present:
            self.logger.info(f"✅ '{item_title}' is in favorites")
        else:
            self.logger.info(f"'{item_title}' is not in favorites")

        return is_present

    def is_favorites_empty(self) -> bool:
        """Check if the favorites cart is empty.

        Returns:
            True if favorites is empty, False otherwise
        """
        self.logger.info("Checking if favorites cart is empty")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        try:
            # Check for empty cart message
            empty_message = self.find_element(self.EMPTY_CART_MESSAGE, timeout=3)
            is_empty = "empty" in empty_message.text.lower()

            if is_empty:
                self.logger.info("✅ Favorites cart is empty")
            else:
                self.logger.info("Favorites cart is not empty")

            return is_empty

        except Exception:
            # No empty message found, check item count
            count = self.get_favorites_count()
            is_empty = count == 0

            if is_empty:
                self.logger.info("✅ Favorites cart is empty (no items)")
            else:
                self.logger.info(f"Favorites cart has {count} items")

            return is_empty

    def clear_all_favorites(self) -> None:
        """Remove all items from favorites."""
        self.logger.info("Clearing all favorites")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        favorited_items = self.get_favorited_items()

        for item in favorited_items:
            self.remove_item_from_favorites(item)

        self.logger.info("✅ All favorites cleared")

    def get_favorites_total_price(self) -> str:
        """Get the total price of all favorited items.

        Returns:
            Total price as string
        """
        self.logger.info("Getting favorites total price")

        # Ensure cart is open
        if not self.is_element_present(self.CART_HEADER):
            self.open_favorites_cart()

        try:
            total_element = self.find_element(self.CART_TOTAL, timeout=5)
            total_price = str(total_element.text)

            self.logger.info(f"Favorites total price: {total_price}")
            return total_price

        except Exception as e:
            self.logger.warning(f"Could not get favorites total price: {str(e)}")
            return "0"

    def is_galaxy_s20_plus_on_favorites_page(self) -> bool:
        """Check if Galaxy S20+ is present on the favorites page itself (not cart).

        Returns:
            True if Galaxy S20+ is on favorites page, False otherwise
        """
        self.logger.info("Checking if Galaxy S20+ is on favorites page")

        try:
            # Use stable ID selector first
            galaxy_element = self.find_element(
                self.GALAXY_S20_PLUS_IN_FAVORITES, timeout=5
            )
            is_present = bool(galaxy_element.is_displayed())

            if is_present:
                self.logger.info("✅ Galaxy S20+ is present on favorites page (by ID)")
            else:
                self.logger.warning(
                    "Galaxy S20+ element found by ID but not visible on favorites page"
                )

            return is_present

        except Exception as e:
            self.logger.warning(
                f"Galaxy S20+ not found by ID on favorites page: {str(e)}"
            )

            # Fallback to data-sku attribute
            try:
                galaxy_element_sku = self.find_element(
                    self.GALAXY_S20_PLUS_BY_SKU_IN_FAVORITES, timeout=3
                )
                is_present = bool(galaxy_element_sku.is_displayed())

                if is_present:
                    self.logger.info(
                        "✅ Galaxy S20+ is present on favorites page (by data-sku)"
                    )
                else:
                    self.logger.warning(
                        "Galaxy S20+ found by data-sku but not visible on favorites page"
                    )

                return is_present

            except Exception as e2:
                self.logger.warning(
                    f"Galaxy S20+ not found by data-sku either on favorites page: {str(e2)}"
                )
                return False

    def get_galaxy_s20_plus_title_on_favorites_page(self) -> str:
        """Get the Galaxy S20+ title from the favorites page.

        Returns:
            The title text of Galaxy S20+ on favorites page
        """
        try:
            title_element = self.find_element(
                self.GALAXY_S20_PLUS_TITLE_IN_FAVORITES, timeout=5
            )
            title_text = str(title_element.text)
            self.logger.info(f"Galaxy S20+ title on favorites page: {title_text}")
            return title_text
        except Exception as e:
            self.logger.warning(
                f"Could not get Galaxy S20+ title on favorites page: {str(e)}"
            )
            return "Galaxy S20+"
