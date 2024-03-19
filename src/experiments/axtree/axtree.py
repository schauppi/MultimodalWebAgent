from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
from PIL import Image, ImageDraw, ImageFont
import io
import os
import time
import json
import random


def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    visit(page, "https://www.amazon.com")
    client = page.context.new_cdp_session(page)
    while True:
        reHighlight(page, client)
        input("Press any key to continue.")


def visit(page, url):
    page.goto(url)


def reHighlight(page, client):
    # client.send("DOM.getDocument")
    axtree = client.send('Accessibility.getFullAXTree')
    snapshot = page.accessibility.snapshot()

    with open("src/experiments/axtree/data/axtree_2.json", "wt") as fh:
        fh.write(json.dumps(snapshot, indent=4))


main()
