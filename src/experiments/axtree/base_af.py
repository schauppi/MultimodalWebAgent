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
    visit(page, "https://www.globalsqa.com/demo-site/select-dropdown-menu/")
    client = page.context.new_cdp_session(page)
    while True:
        reHighlight(page, client)
        input("Press any key to continue.")


def visit(page, url):
    page.goto(url)


def reHighlight(page, client):
    client.send("DOM.getDocument")
    # client.send('DOM.enable')
    axtree = client.send('Accessibility.getFullAXTree')

    with open("src/experiments/axtree/data/axtree.json", "wt") as fh:
        fh.write(json.dumps(axtree, indent=4))
    nodesToResolve = []
    for node in axtree["nodes"]:
        properties = node.get("properties", [])
        property_dict = {}
        for p in properties:
            if "name" in p:
                property_dict[p["name"]] = p.get("value", {}).get("value")
        if "backendDOMNodeId" in node:
            if node.get("role", {}).get("value", "") == "RootWebArea":
                continue
            if property_dict.get("focusable"):
                nodesToResolve.append(int(node["backendDOMNodeId"]))

    IDs = client.send("DOM.pushNodesByBackendIdsToFrontend",
                      {"backendNodeIds": nodesToResolve})
    rectangles = dict()

    for _id in IDs["nodeIds"]:
        try:
            client.send('DOM.setAttributeValue', {
                        "nodeId": _id, "name": "__focusId", "value": str(_id)})

        except:
            pass

        try:
            rectangles[_id] = client.send(
                'DOM.getContentQuads', {"nodeId": _id})
        except:
            pass

    # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    fnt = ImageFont.load_default(14)
    screenshot_bytes = io.BytesIO(page.screenshot())
    with Image.open(screenshot_bytes).convert("L").convert("RGBA") as base:
        overlay = Image.new('RGBA', base.size)

        draw = ImageDraw.Draw(overlay)

        for r in rectangles:
            for quad in rectangles[r]["quads"]:
                top_left = (quad[0], quad[1])
                top_right = (quad[2], quad[3])
                bottom_right = (quad[4], quad[5])
                bottom_left = (quad[6], quad[7])

                height = bottom_left[1] - top_left[1]
                width = top_right[0] - top_left[0]

                color = [random.randint(0, 255), random.randint(
                    125, 255), random.randint(0, 50)]
                random.shuffle(color)
                color.append(255)
                color = tuple(color)
                luminance = color[0] * 0.3 + color[1] * 0.59 + color[2] * 0.11

                text_color = (0, 0, 0, 255) if luminance > 90 else (
                    255, 255, 255, 255)

                draw.rectangle([top_left, bottom_right], outline=color, fill=(
                    color[0], color[1], color[2], 48), width=2)

                # xy = (top_left[0] + 0.5width, top_left[1] + 0.5*height)
                xy = top_right

                bbox = draw.textbbox(xy, str(r), font=fnt,
                                     anchor='rb', align='center')
                bbox = (bbox[0]-3, bbox[1]-3, bbox[2]+3, bbox[3]+3)

                draw.rectangle(bbox, fill=color)
                draw.text(xy, str(r), fill=text_color,
                          font=fnt, anchor='rb', align='center')

        Image.alpha_composite(base, overlay).save(
            "src/experiments/axtree/data/test_image.png")

    # Run code to highlight everything
    page.evaluate(""" () => {
        let elements = document.querySelectorAll("[__focusId]");
        for (let i=0; i<elements.length; i++) {
            var elm = elements[i];
            elm.style.outlineWidth = "2px";
            elm.style.outlineStyle = "solid";
            elm.style.outlineColor = "lime";
        }
    }
    """)


main()
