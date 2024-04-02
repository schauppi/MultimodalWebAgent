var MultimodalWebSurfer = MultimodalWebSurfer || (function() {
  let nextLabel = 10;

  let roleMapping = {
      "a": "link",
      "area": "link",
      "button": "button",
      "input, type=button": "button",
      "input, type=checkbox": "checkbox",
      "input, type=email": "textbox",
      "input, type=number": "spinbutton",
      "input, type=radio": "radio",
      "input, type=range": "slider",
      "input, type=reset": "button",
      "input, type=search": "searchbox",
      "input, type=submit": "button",
      "input, type=tel": "textbox",
      "input, type=text": "textbox",
      "input, type=url": "textbox",
      "search": "search",
      "select": "combobox",
      "select, multiple": "listbox",
      "option": "option",
      "textarea": "textbox"
  };

  let getInteractiveElements = function() {

      let results = []
      let roles = ["scrollbar", "searchbox", "slider", "spinbutton", "switch", "tab", "tabpanel", "treeitem", "button", "checkbox", "gridcell", "link", "menuitem", "menuitemcheckbox", "menuitemradio", "option", "progressbar", "radio", "textbox", "combobox", "menu", "menubar", "tablist", "tree", "treegrid", "grid", "listbox", "radiogroup", "widget"];


      // Get the main interactive elements
      let nodeList = document.querySelectorAll("input, select, textarea, button, [href], [onclick], [contenteditable], [tabindex]:not([tabindex='-1'])");
      for (let i=0; i<nodeList.length; i++) { // Copy to something mutable
          results.push(nodeList[i]);
      }

      // Anything not already included that has a suitable role
      nodeList = document.querySelectorAll("[role]");
      for (let i=0; i<nodeList.length; i++) { // Copy to something mutable
          if (results.indexOf(nodeList[i]) == -1) {
              let role = nodeList[i].getAttribute("role");
	      if (roles.indexOf(role) > -1) {
                  results.push(nodeList[i]);
	      }
	  }
      }
      return results;
  };

  let labelElements = function(elements) {
      for (let i=0; i<elements.length; i++) {
          if (!elements[i].hasAttribute("__elementId")) {
              elements[i].setAttribute("__elementId", "" + (nextLabel++));
          }
      }
  };

  let isTopmost = function(element, x, y) {
     let hit = document.elementFromPoint(x, y);
     while (hit) {
         if (hit == element) return true;
         hit = hit.parentNode;
     }
     return false;
  };

  let getFocusedElementId = function() {
     let elm = document.activeElement;
     while (elm) {
         if (elm.hasAttribute && elm.hasAttribute("__elementId")) {
	     return elm.getAttribute("__elementId");
	 }
         elm = elm.parentNode;
     }
     return null;
  };

  let trimmedInnerText = function(element) {
      if (!element) {
          return "";
      }
      let text = element.innerText;
      if (!text) {
          return "";
      }
      return text.trim();
  };

  let getApproximateAriaName = function(element) {
      // Check for aria labels
      if (element.hasAttribute("aria-labelledby")) {
          let buffer = "";
	  let ids = element.getAttribute("aria-labelledby").split(" ");
	  for (let i=0; i<ids.length; i++) {
              let label = document.getElementById(ids[i]);
	      if (label) {
	          buffer = buffer + " " + trimmedInnerText(label);
              }
          }
	  return buffer.trim();
      }

      if (element.hasAttribute("aria-label")) {
	  return element.getAttribute("aria-label");
      }

      // Check for labels
      if (element.hasAttribute("id")) {
          let label_id = element.getAttribute("id");
          let label = "";
          let labels = document.querySelectorAll("label[for='" + label_id + "']");
          for (let j=0; j<labels.length; j++) {
              label += labels[j].innerText + " ";
          }
          label = label.trim();
          if (label != "") {
              return label;
          }
      }

      if (element.parentElement && element.parentElement.tagName == "LABEL") {
          return element.parentElement.innerText;
      }

      // Check for alt text or titles
      if (element.hasAttribute("alt")) {
	  return element.getAttribute("alt")
      }

      if (element.hasAttribute("title")) {
	  return element.getAttribute("title")
      }

      return trimmedInnerText(element);
  };

  let getApproximateAriaRole = function(element) {
      let tag = element.tagName.toLowerCase();
      if (tag == "input" && element.hasAttribute("type")) {
          tag = tag + ", type=" + element.getAttribute("type");
      }

      if (element.hasAttribute("role")) {
          return [element.getAttribute("role"), tag];
      }
      else if (tag in roleMapping) {
          return [roleMapping[tag], tag];
      }
      else {
	  return ["", tag];
      }
  };

  let getInteractiveRects = function() {
      labelElements(getInteractiveElements());
      let elements = document.querySelectorAll("[__elementId]");
      let results = {};
      for (let i=0; i<elements.length; i++) {
         let key = elements[i].getAttribute("__elementId");
         let rects = elements[i].getClientRects();
	 let ariaRole = getApproximateAriaRole(elements[i]);
	 let ariaName = getApproximateAriaName(elements[i]);
	 let vScrollable = elements[i].scrollHeight - elements[i].clientHeight >= 1;

	 let record = {
             "tag_name": ariaRole[1],
	     "role": ariaRole[0],
	     "aria-name": ariaName,
	     "v-scrollable": vScrollable,
	     "rects": []
	 };

         for (const rect of rects) {
	     let x = rect.left + rect.width/2;
             let y = rect.top + rect.height/2;
             if (isTopmost(elements[i], x, y)) {
		 record["rects"].push(JSON.parse(JSON.stringify(rect)));
             }
         }

	 if (record["rects"].length > 0) {
             results[key] = record;
         }
      }
      return results;
  };

  let getVisualViewport = function() {
      let vv = window.visualViewport;
      return {
          "height": vv.height,
	  "width": vv.width,
	  "offsetLeft": vv.offsetLeft,
	  "offsetTop": vv.offsetTop,
	  "pageLeft": vv.pageLeft,
	  "pageTop": vv.pageTop,
	  "scale": vv.scale,
	  "clientWidth": document.documentElement.clientWidth,
	  "clientHeight": document.documentElement.clientHeight,
	  "scrollWidth": document.documentElement.scrollWidth,
	  "scrollHeight": document.documentElement.scrollHeight
      };
  };

  return {
      getInteractiveRects: getInteractiveRects,
      getVisualViewport: getVisualViewport,
      getFocusedElementId: getFocusedElementId
  };
})();
