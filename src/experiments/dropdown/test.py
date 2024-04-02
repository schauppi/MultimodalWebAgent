
from src.tools.read_url import read_url
from src.tools.click_element import click_element
from src.tools.utils.get_webdriver_instance import get_webdriver_instance
from src.tools.utils.get_b64_screenshot import get_b64_screenshot
from src.experiments.dropdown.highlight_dropdown_elements import highlight_elements

import json
import time

url = "https://www.amazon.de/JustSun-Trousers-Casual-Elastic-Drawstring/dp/B0CG1L9M5T/ref=sr_1_3_sspa?crid=28BQ4759MI9WD&dib=eyJ2IjoiMSJ9.cnQ2pFKcqrLzn4gPOR0XVq0elcgJLPMmpxIyc06mjyRgxRE3Y9W_6HVtk0p4q_HCUbo82lV7XrzPgZUTtA8xLNiUpqP_Lgx6M7ueAPNHYN-O8qDdXLIuOSGsIaDV09T-xOqqS7PNGDeAViTdq3RIFUho6JNb_pbDMErbg9y-m7x8TInfB3_8mP5n1EEj8xlxLRhS9EgyYvRmL4WiTfnhZUK9qvs6F6xSUrsEWT13VBuX0reekBG1II2SfBFKrO-RnarSG6KuP-_uZbiKyuqvTelT6HAh7R8TkSMquOaQNmo.kS3zVowhYSNXPnN0d7MRUO0CMNzktie-p_eQcS2P5lQ&dib_tag=se&keywords=trousers&qid=1712058349&sprefix=trouser%2Caps%2C140&sr=8-3-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

read_url(url)

time.sleep(10)

driver = get_webdriver_instance()

with open("src/experiments/dropdown/mark_page_dropdown.js") as f:
    driver.evaluate(f.read())

rects = driver.evaluate("MultimodalWebSurfer.getInteractiveRects();")

with open("src/experiments/dropdown/data/rects.json", "w") as f:
    f.write(json.dumps(rects))


