from bs4 import BeautifulSoup
from src.webdriver.webdriver import WebDriver
from src.tools.utils.get_webdriver_instance import get_webdriver_instance
from src.configs.logging.logging_config import setup_logging

from src.tools.read_url import read_url

import markdownify
import re
import logging

setup_logging()
logger = logging.getLogger()


def get_markdown_information() -> str:
    """
    Retrieves the content of a webpage and converts it to a markdown-formatted string.

    Args:
        None

    Returns:
        str: A markdown-formatted string representing the content of a webpage.
    """

    try:

        logger.info(
            "Getting the content of a webpage and converting it to markdown...")
        driver = get_webdriver_instance()

        dom = driver.content()

        soup = BeautifulSoup(dom, 'html.parser')

        main_title = soup.title.string

        for script in soup(["script", "style"]):
            script.extract()

        webpage_text = "# " + main_title + "\n\n" + \
            markdownify.MarkdownConverter().convert_soup(soup)

        webpage_text = re.sub(r"\r\n", "\n", webpage_text)

        webpage_text = (re.sub(r"\n{2,}", "\n\n", webpage_text).strip())

        with open('src/experiments/markdown/data/markdown_text.md', 'w') as f:
            f.write(webpage_text)
        logger.info("Webpage content successfully converted to markdown.")

        return webpage_text

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please check the logs for more details."
