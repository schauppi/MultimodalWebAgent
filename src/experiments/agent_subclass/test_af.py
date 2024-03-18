from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
import os
import time
import json


def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    visit(page, "https://www.google.com")
    client = page.context.new_cdp_session(page)
    while True:
        reHighlight(page, client)
        input("Press any key to continue.")


def visit(page, url):
    page.goto(url)


def reHighlight(page, client):
    client.send("DOM.getDocument")
    axtree = client.send('Accessibility.getFullAXTree')

    nodesToResolve = []
    for node in axtree["nodes"]:
        properties = node.get("properties", [])
        property_dict = {}
        for p in properties:
            if "name" in p:
                property_dict[p["name"]] = p.get("value", {}).get("value")
        if "backendDOMNodeId" in node:
            if property_dict.get("focusable"):
                nodesToResolve.append(int(node["backendDOMNodeId"]))

    IDs = client.send("DOM.pushNodesByBackendIdsToFrontend",
                      {"backendNodeIds": nodesToResolve})

    for _id in IDs["nodeIds"]:
        try:
            client.send('DOM.setAttributeValue', {
                        "nodeId": _id, "name": "focusId", "value": str(_id)})
        except:
            pass

    page.evaluate(""" () => {
    let elements = document.querySelectorAll("[focusId]");
    for (let i = 0; i < elements.length; i++) {
        var elm = elements[i];
        var isInput = elm.tagName.toLowerCase() === 'input';
        var hasInteractiveRole = ['button', 'link', 'checkbox', 'radio', 'textbox'].includes(elm.getAttribute('role'));

        if (isInput || hasInteractiveRole) {
            // Highlight input elements or elements with interactive roles in red
            elm.style.outlineWidth = "2px";
            elm.style.outlineStyle = "solid";
            elm.style.outlineColor = "red";
        } else {
            // Highlight other focusable elements in green
            elm.style.outlineWidth = "2px";
            elm.style.outlineStyle = "solid";
            elm.style.outlineColor = "lime";
        }
    }
}
""")


main()
