from src.tools.utils.get_webdriver_instance import get_webdriver_instance
from src.configs.logging.logging_config import setup_logging

import markdownify
import re
import logging
import os
from bs4 import BeautifulSoup

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

        output_dir = 'src/experiments/markdown/data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, 'markdown_text.md')
        try:
            with open(output_file, 'w') as f:
                f.write(webpage_text)
            logger.info("Webpage content successfully converted to markdown.")
        except Exception as e:
            logger.error(f"An error occurred while writing to file: {str(e)}")

        return webpage_text

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please check the logs for more details."
