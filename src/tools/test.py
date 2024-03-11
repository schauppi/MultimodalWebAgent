from src.webdriver.webdriver import WebDriver

import time

from src.tools.read_url import read_url
from src.tools.scroll import scroll
from src.tools.jump_to_search_engine import jump_to_search_engine

read_url("orf.at")

time.sleep(5)

scroll("down")

time.sleep(5)

scroll("up")

time.sleep(5)

jump_to_search_engine()
