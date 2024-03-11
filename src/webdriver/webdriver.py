from playwright.sync_api import sync_playwright
from src.configs.logging.logging_config import setup_logging
import locale
from tzlocal import get_localzone_name
import logging

setup_logging()
logger = logging.getLogger()


class WebDriver:
    """
    A singleton class representing a web driver instance.

    Methods:
        getInstance(*args, **kwargs) -> WebDriver:
            Returns the singleton instance of the WebDriver class.
        __init__(*args, **kwargs) -> None:
            Initializes the WebDriver class.
        createDriver(*args, **kwargs) -> None:
            Creates a new browser instance and sets up the page.
        getDriver() -> Page:
            Returns the current page instance.
        closeDriver() -> None:
            Closes the browser instance and stops Playwright.
        closeCurrentTab() -> None:
            Closes the current tab (page) without affecting the browser instance.
    """

    __instance = None

    @staticmethod
    def getInstance(*args, **kwargs):
        """
        Returns the singleton instance of the WebDriver class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The singleton instance of the WebDriver class.
        """
        if WebDriver.__instance is None:
            WebDriver.__instance = WebDriver(*args, **kwargs)
        return WebDriver.__instance

    def __init__(self, *args, **kwargs):
        """
        Initializes the WebDriver class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if WebDriver.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            WebDriver.__instance = self
            self.createDriver(*args, **kwargs)

    def createDriver(self, *args, **kwargs):
        """
        Creates a new browser instance and sets up the page.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        timezone_id = get_localzone_name()
        system_locale = locale.getdefaultlocale()

        try:
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir="src/data/chrome_profile",
                headless=False,
                args=[
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-web-security",
                    "--allow-running-insecure-content",
                ],
                locale=system_locale[0],
                timezone_id=timezone_id,
            )
            self.playwright = playwright
            self.browser = browser
            self.page = browser.new_page()
            self.page.set_viewport_size({"width": 960, "height": 1080})
            logger.info("Browser instance created successfully.")
        except Exception as e:
            logger.error("Failed to create browser instance.", exc_info=True)
            raise e

    def getDriver(self):
        """
        Returns the current page instance.

        Args:
            None

        Returns:
            Page: The current page instance.
        """
        return self.page

    def closeDriver(self):
        """
        Closes the browser instance and stops Playwright.

        Args:
            None

        Returns:
            None
        """
        try:
            self.browser.close()
            self.playwright.stop()
            logger.info("Browser instance closed successfully.")
        except Exception as e:
            logger.error("Failed to close browser instance.", exc_info=True)
            raise e

    def closeCurrentTab(self):
        """
        Closes the current tab (page) without affecting the browser instance.

        Args:
            None

        Returns:
            None
        """
        if self.page and not self.page.is_closed():
            try:
                self.page.close()
                self.page = self.browser.new_page()
                self.page.set_viewport_size({"width": 960, "height": 1080})
                logger.info("Current tab closed successfully.")
            except Exception as e:
                logger.error("Failed to close current tab.", exc_info=True)
                raise e
