from src.webdriver.webdriver import WebDriver

import time

from src.tools.read_url import read_url
from src.tools.scroll import scroll
from src.tools.jump_to_search_engine import jump_to_search_engine
from src.tools.go_back import go_back
from src.tools.wait import wait
from src.tools.click_element import click_element

read_url("orf.at")

time.sleep(5)

click_element("CLick on the 'Sports' banner with the football player")

time.sleep(5)
