from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
from PIL import Image, ImageDraw, ImageFont
import io
import os
import time
import json
import random

labels_path = "src/experiments/axtree/utils/add_labels.js"


def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
    visit(page, "https://www.globalsqa.com/demo-site/select-dropdown-menu/")
    client = page.context.new_cdp_session(page)
    while True:
        reHighlight(page, client)
        input("Press any key to continue.")


def visit(page, url):
    page.goto(url)

MAX_SHORT_SIDE = 768
MAX_LONG_SIDE = 2000
SCREENSHOT_HEIGHT = MAX_SHORT_SIDE
SCREENSHOT_WIDTH = int(4 / 3 * MAX_SHORT_SIDE)
VIEWPORT_HEIGHT = SCREENSHOT_HEIGHT - 53 
VIEWPORT_WIDTH = SCREENSHOT_WIDTH

def screenshot(rectangles, page):

    visible_rects = list()

    #load bitmap
    fnt = ImageFont.load_default()
    screenshot_bytes = io.BytesIO(page.screenshot())
    ###
    #NEED FOR TESTS - COLOR OR NON COLOR SCREENSHOT_HEIGHT
    ###
    screenshot = Image.open(screenshot_bytes).convert("RGBA").convert("L")
    screenshot.save("src/experiments/axtree/data/screenshot.png")

    #base to add adress bar and scroll bar
    base = Image.new("RGBA", (SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
    base.paste(screenshot, (0, 53))
    base.save("src/experiments/axtree/data/base.png")

    overlay = Image.new("RGBA", base.size)
    overlay.save("src/experiments/axtree/data/overlay.png")

    #create draw object
    draw = ImageDraw.Draw(overlay)    

    for r in rectangles:
        for rect in rectangles[r]["rects"]:
            if not rect:
                continue
            if rect["width"] * rect["height"] == 0:
                continue

            _rect = {}
            _rect.update(rect)
            _rect["y"] += 53
            _rect["top"] += 53
            _rect["bottom"] += 53

            mid = (_rect["right"] + _rect["left"] / 2.0, _rect["top"] + _rect["bottom"] / 2.0)

            if 0 <= mid[0] and mid[0] < SCREENSHOT_WIDTH and 0 <= mid[1] and mid[1] < SCREENSHOT_HEIGHT:
                visible_rects.append(r)

            draw_roi(draw, int(r), fnt, _rect)

    overlay.save("src/experiments/axtree/data/overlay.png")

    print(visible_rects)

    return None, None

def draw_roi(draw, idx, font, rect):

    color = get_color(idx)
    text_color = (0, 0, 0, 255)
    
    roi = [(rect["left"], rect["top"]), (rect["right"], rect["bottom"])]
    anchor = (rect["right"], rect["top"])

    #box for the interactive element
    draw.rectangle(roi, outline=color, fill=(color[0], color[1], color[2], 48), width=2)

    #box for the text
    bbox = draw.textbbox(anchor, str(idx), font=font, anchor="rb", align="center")
    bbox = (bbox[0] - 3, bbox[1] - 3, bbox[2] + 3, bbox[3] + 3)
    draw.rectangle(bbox, fill=color)

    draw.text(anchor, str(idx), fill=text_color, font=font, anchor="rb", align="center")


def get_color(idx):
    rnd = random.Random(int(idx))
    color = [rnd.randint(0, 255), rnd.randint(125, 255), rnd.randint(0, 50)]
    rnd.shuffle(color)
    color.append(255)
    return tuple(color)



def reHighlight(page, client):
    
    with open(labels_path, "rt") as fh:
        page.evaluate(fh.read())

        rectangles = page.evaluate("MultimodalWebSurfer.getInteractiveRects();")

        for element_id, details in rectangles.items():
            tag_name = details["tag_name"]
            role = details["role"]
            aria_name = details["aria-name"]
            rects = details["rects"]

            print(f"ID: {element_id}, Tag: {tag_name}, Role: {role}, Aria-Name: {aria_name}, Rects: {rects}")
            print("---------")

        #_, visible_rects = screenshot(rectangles, page)
    



main()
