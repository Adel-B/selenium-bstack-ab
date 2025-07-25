"""Product page object for bstackdemo.com."""

from typing import Any, List, Optional

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger_config import get_test_logger


class ProductPage(BasePage):
    """Page object for bstackdemo.com product listing and filtering functionality."""

    def __init__(
        self,
        execution_mode: Optional[str] = None,
        browser: str = "chrome",
        capability_name: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """Initialize ProductPage.

        Args:
            execution_mode: "local" or "browserstack"
            browser: Browser name for local mode
            capability_name: BrowserStack capability name
            timeout: Default timeout for operations
        """
        super().__init__(execution_mode, browser, capability_name, timeout)
        self.logger = get_test_logger("product_page")

    # Page Elements (Locators) - Based on actual bstackdemo.com HTML structure
    VENDOR_FILTERS_CONTAINER = (By.CSS_SELECTOR, ".filters")

    # Samsung filter - click the label element (checkbox input is hidden by CSS)
    SAMSUNG_FILTER_LABEL_XPATH = (
        By.XPATH,
        "//div[@class='filters-available-size']//input[@value='Samsung']/parent::label",
    )
    SAMSUNG_FILTER_SPAN_XPATH = (
        By.XPATH,
        "//div[@class='filters-available-size']//span[@class='checkmark' and text()='Samsung']",
    )
    # Simple direct selectors
    SAMSUNG_FILTER_INPUT = (By.CSS_SELECTOR, "input[value='Samsung']")
    SAMSUNG_FILTER_CONTAINER_XPATH = (
        By.XPATH,
        "//div[@class='filters-available-size'][.//input[@value='Samsung']]",
    )

    # Product elements
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".shelf-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".shelf-item__title")
    FAVORITE_BUTTONS = (By.CSS_SELECTOR, ".shelf-item button[aria-label='delete']")

    # Galaxy S20+ specific - using stable ID and data attributes from actual HTML
    GALAXY_S20_PLUS_ID = "11"
    GALAXY_S20_PLUS_SKU = "samsung-S20+-device-info.png"

    # Galaxy S20+ locators using stable attributes - properly escaped CSS for numeric ID
    GALAXY_S20_PLUS_CARD = (By.ID, GALAXY_S20_PLUS_ID)
    GALAXY_S20_PLUS_BY_SKU = (By.CSS_SELECTOR, f"[data-sku='{GALAXY_S20_PLUS_SKU}']")
    GALAXY_S20_PLUS_FAVORITE = (
        By.XPATH,
        "//div[@id='11']//button[contains(@class, 'delete') or @aria-label='delete']",
    )
    GALAXY_S20_PLUS_TITLE_ELEMENT = (
        By.CSS_SELECTOR,
        f"[id='{GALAXY_S20_PLUS_ID}'] .shelf-item__title",
    )

    # Alternative stable locators
    FAVORITE_BUTTON_ACTIVE = (By.CSS_SELECTOR, ".shelf-item button.clicked")
    FAVORITED_ITEM_COUNT = (By.CSS_SELECTOR, ".float-cart__header .bag__quantity")

    # Navigation elements
    FAVORITES_LINK = (By.ID, "favourites")

    def wait_for_products_to_load(self, timeout: Optional[int] = None) -> None:
        """Wait for product cards to load on the page.

        Args:
            timeout: Optional timeout override
        """
        self.logger.info("Waiting for products to load")
        wait_time = timeout or self.timeout
        self.wait_for_element_visible(self.PRODUCT_CARDS, timeout=wait_time)
        self.logger.info("✅ Products loaded successfully")

    def get_vendor_filters_container(self) -> Any:
        """Get the vendor filters container element.

        Returns:
            WebElement for the vendor filters container
        """
        self.logger.info("Locating vendor filters container")
        return self.wait_for_element_visible(self.VENDOR_FILTERS_CONTAINER)

    def filter_by_samsung(self) -> None:
        """Filter products to show only Samsung devices by clicking the Samsung checkbox."""
        self.logger.info("Filtering products by Samsung vendor")

        # Wait for products to load first
        self.wait_for_products_to_load()

        # Get the filters container to ensure it's loaded
        self.get_vendor_filters_container()
        self.logger.info("✅ Vendor filters container found")

        # Click the Samsung filter using clickable elements (not hidden input)
        try:
            self.logger.info(
                "Clicking Samsung filter label (parent of hidden checkbox)"
            )
            samsung_label = self.wait_for_element_clickable(
                self.SAMSUNG_FILTER_LABEL_XPATH, timeout=10
            )
            samsung_label.click()
            self.logger.info("✅ Samsung filter label clicked")

        except Exception as e:
            # Fallback to span element
            self.logger.warning(f"Samsung label failed: {str(e)}")
            try:
                self.logger.info("Trying Samsung filter span element")
                samsung_span = self.wait_for_element_clickable(
                    self.SAMSUNG_FILTER_SPAN_XPATH, timeout=5
                )
                samsung_span.click()
                self.logger.info("✅ Samsung filter span clicked")
            except Exception as e2:
                # Final fallback to container
                self.logger.warning(f"Samsung span failed: {str(e2)}")
                try:
                    self.logger.info("Trying Samsung filter container")
                    samsung_container = self.wait_for_element_clickable(
                        self.SAMSUNG_FILTER_CONTAINER_XPATH, timeout=5
                    )
                    samsung_container.click()
                    self.logger.info("✅ Samsung filter container clicked")
                except Exception as e3:
                    self.logger.error(f"All Samsung filter selectors failed: {str(e3)}")
                    raise Exception("Could not find or click Samsung filter checkbox")

        # Wait for filtered results to load
        self.wait_for_filtered_products_to_load()
        self.logger.info("✅ Samsung filter applied successfully")

    def wait_for_filtered_products_to_load(self, timeout: Optional[int] = None) -> None:
        """Wait for filtered products to load after applying filter.

        Args:
            timeout: Optional timeout override
        """
        wait_time = timeout or 10
        self.logger.info("Waiting for filtered products to load")

        # Wait a moment for the filter to take effect
        import time

        time.sleep(2)

        # Verify products are still visible
        self.wait_for_element_visible(self.PRODUCT_CARDS, timeout=wait_time)
        self.logger.info("✅ Filtered products loaded")

    def get_product_titles(self) -> List[str]:
        """Get all visible product titles.

        Returns:
            List of product title strings
        """
        self.logger.info("Getting all product titles")

        title_elements = self.find_elements(self.PRODUCT_TITLES)
        titles = [element.text for element in title_elements]

        self.logger.info(f"Found {len(titles)} products: {titles}")
        return titles

    def is_galaxy_s20_plus_visible(self) -> bool:
        """Check if Galaxy S20+ is visible in the product list using stable ID selector.

        Returns:
            True if Galaxy S20+ is visible, False otherwise
        """
        self.logger.info("Checking if Galaxy S20+ is visible")

        try:
            # Use the stable ID selector first
            galaxy_card = self.find_element(self.GALAXY_S20_PLUS_CARD, timeout=5)
            is_visible = bool(galaxy_card.is_displayed())

            if is_visible:
                self.logger.info("✅ Galaxy S20+ is visible in product list (by ID)")
            else:
                self.logger.warning("Galaxy S20+ card found by ID but not visible")

            return is_visible

        except Exception as e:
            self.logger.warning(f"Galaxy S20+ not found by ID: {str(e)}")

            # Fallback to data-sku attribute
            try:
                galaxy_card_sku = self.find_element(
                    self.GALAXY_S20_PLUS_BY_SKU, timeout=3
                )
                is_visible = bool(galaxy_card_sku.is_displayed())

                if is_visible:
                    self.logger.info(
                        "✅ Galaxy S20+ is visible in product list (by data-sku)"
                    )
                else:
                    self.logger.warning("Galaxy S20+ found by data-sku but not visible")

                return is_visible

            except Exception as e2:
                self.logger.warning(
                    f"Galaxy S20+ not found by data-sku either: {str(e2)}"
                )
                return False

    def click_galaxy_s20_plus_favorite(self) -> None:
        """Click the favorite (heart) button for Galaxy S20+ using stable selectors."""
        self.logger.info("Clicking favorite button for Galaxy S20+")

        # First verify the product is visible
        if not self.is_galaxy_s20_plus_visible():
            raise Exception("Galaxy S20+ is not visible in the product list")

        # Click the favorite button using stable ID + aria-label selector
        try:
            self.logger.info("Clicking Galaxy S20+ favorite button using ID selector")
            favorite_button = self.wait_for_element_clickable(
                self.GALAXY_S20_PLUS_FAVORITE, timeout=10
            )
            favorite_button.click()
            self.logger.info("✅ Galaxy S20+ favorite button clicked")

            # Wait a moment for the favorite action to register
            import time

            time.sleep(1)

        except Exception as e:
            self.logger.error(f"Failed to click Galaxy S20+ favorite button: {str(e)}")
            raise

    def verify_samsung_products_only(self) -> bool:
        """Verify that only Samsung products are displayed after filtering.

        Returns:
            True if only Samsung products are visible, False otherwise
        """
        self.logger.info("Verifying only Samsung products are displayed")

        product_titles = self.get_product_titles()

        # Check if all products contain Samsung-related keywords
        samsung_keywords = ["Galaxy", "Samsung"]
        samsung_products = []

        for title in product_titles:
            is_samsung = any(keyword in title for keyword in samsung_keywords)
            if is_samsung:
                samsung_products.append(title)

        all_samsung = len(samsung_products) == len(product_titles)

        if all_samsung:
            self.logger.info(
                f"✅ All {len(product_titles)} products are Samsung devices"
            )
        else:
            non_samsung = len(product_titles) - len(samsung_products)
            self.logger.warning(
                f"Found {non_samsung} non-Samsung products out of {len(product_titles)} total"
            )

        return all_samsung

    def get_favorited_items_count(self) -> int:
        """Get the count of favorited items from the cart header.

        Returns:
            Number of favorited items
        """
        try:
            count_element = self.find_element(self.FAVORITED_ITEM_COUNT, timeout=5)
            count_text = count_element.text
            count = int(count_text) if count_text.isdigit() else 0

            self.logger.info(f"Favorited items count: {count}")
            return count

        except Exception as e:
            self.logger.warning(f"Could not get favorited items count: {str(e)}")
            return 0

    def is_galaxy_s20_plus_favorited(self) -> bool:
        """Check if Galaxy S20+ has been favorited using stable selectors.

        Returns:
            True if Galaxy S20+ is favorited, False otherwise
        """
        self.logger.info("Checking if Galaxy S20+ is favorited")

        try:
            # Look for the favorite button with clicked class using ID
            favorited_button = self.driver.find_element(
                By.CSS_SELECTOR,
                f"[id='{self.GALAXY_S20_PLUS_ID}'] button.Button.clicked",
            )

            is_favorited = bool(favorited_button.is_displayed())

            if is_favorited:
                self.logger.info("✅ Galaxy S20+ is favorited")
            else:
                self.logger.info(
                    "Galaxy S20+ favorite button found but not in favorited state"
                )

            return is_favorited

        except Exception:
            self.logger.info("Galaxy S20+ favorite button not in favorited state")
            return False

    def search_for_product(self, product_name: str) -> bool:
        """Search for a specific product by name.

        Args:
            product_name: Name of the product to search for

        Returns:
            True if product is found, False otherwise
        """
        self.logger.info(f"Searching for product: {product_name}")

        product_titles = self.get_product_titles()
        found = any(product_name in title for title in product_titles)

        if found:
            self.logger.info(f"✅ Product '{product_name}' found in listing")
        else:
            self.logger.warning(f"Product '{product_name}' not found in listing")

        return found

    def navigate_to_favorites(self) -> None:
        """Navigate to the favorites page using the stable favorites link."""
        self.logger.info("Navigating to favorites page")

        try:
            favorites_link = self.wait_for_element_clickable(
                self.FAVORITES_LINK, timeout=10
            )
            favorites_link.click()
            self.logger.info("✅ Navigated to favorites page")

            # Wait for favorites page to load
            import time

            time.sleep(2)

        except Exception as e:
            self.logger.error(f"Failed to navigate to favorites page: {str(e)}")
            raise

    def get_galaxy_s20_plus_title(self) -> str:
        """Get the Galaxy S20+ title text using stable selectors.

        Returns:
            The title text of Galaxy S20+ product
        """
        self.logger.info("Getting Galaxy S20+ title")

        try:
            title_element = self.find_element(
                self.GALAXY_S20_PLUS_TITLE_ELEMENT, timeout=5
            )
            title_text = str(title_element.text)
            self.logger.info(f"Galaxy S20+ title: {title_text}")
            return title_text

        except Exception as e:
            self.logger.warning(f"Could not get Galaxy S20+ title: {str(e)}")
            return "Galaxy S20+"  # fallback

    def is_product_favorited_by_id(self, product_id: str) -> bool:
        """Check if a product is favorited by its ID.

        Args:
            product_id: The product ID to check

        Returns:
            True if the product is favorited, False otherwise
        """
        try:
            favorited_button = self.driver.find_element(
                By.CSS_SELECTOR, f"[id='{product_id}'] button.Button.clicked"
            )
            return bool(favorited_button.is_displayed())
        except Exception:
            return False
