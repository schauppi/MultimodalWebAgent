import unittest
from unittest.mock import patch, MagicMock
from src.webdriver.webdriver import WebDriver
import locale
from tzlocal import get_localzone_name


class TestWebDriver(unittest.TestCase):

    def setUp(self):
        self.webdriver = WebDriver.getInstance()

    def tearDown(self):
        self.webdriver.closeDriver()

    @patch('src.webdriver.webdriver.sync_playwright')
    def test_createDriver(self, mock_sync_playwright):
        mock_playwright = MagicMock()
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright
        mock_playwright.chromium.launch_persistent_context.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        self.webdriver.createDriver()

        mock_sync_playwright.assert_called_once()
        timezone_id = get_localzone_name()
        system_locale = locale.getlocale()
        mock_sync_playwright.return_value.start.assert_called_once()
        mock_playwright.chromium.launch_persistent_context.assert_called_once_with(
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
        mock_browser.new_page.assert_called_once()
        mock_page.set_viewport_size.assert_called_once_with(
            {"width": 960, "height": 1080})

    def test_getDriver(self):
        page = self.webdriver.getDriver()
        self.assertIsNotNone(page)

    def test_closeCurrentTab(self):
        self.webdriver.closeCurrentTab()
        page = self.webdriver.getDriver()
        self.assertIsNotNone(page)


if __name__ == '__main__':
    unittest.main()
