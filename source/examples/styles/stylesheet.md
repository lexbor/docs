# CSS Stylesheet Parsing and Application Example

In this article, we will explore the implementation of CSS stylesheet parsing and application to HTML elements using the Lexbor library. The following example is derived from the source file `lexbor/styles/stylesheet.c`. The code illustrates how to create an HTML document, parse CSS styles, attach these styles to the HTML document, and finally retrieve and serialize specific style declarations from an element.

## Overview

The core of the example revolves around creating a minimal HTML document that contains a `<div>` element with inline CSS styles. The code then initializes the Lexbor HTML and CSS parsers, processes the provided CSS, and attaches the styles to the HTML document. Finally, it retrieves specific CSS properties (width and height) from the `<div>` element and serializes them for output.

## Code Breakdown

### Creating the HTML Document

Initially, the program creates an HTML document by calling `lxb_html_document_create()`. If the document creation fails, it triggers a failure message:

```c
doc = lxb_html_document_create();
if (doc == NULL) {
    FAILED("Failed to create HTML Document");
}
```

This part is crucial as it establishes a context for parsing HTML and applying styles.

### Initializing the CSS Parser

Next, the code initializes the CSS system for the document with:

```c
status = lxb_html_document_css_init(doc);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to CSS initialization");
}
```

Proper initialization allows the program to manage CSS styles associated with the HTML document confidently.

### Parsing the CSS Stylesheet

The CSS stylesheet is then created and parsed. The process involves instantiating a CSS parser with:

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization CSS parser");
}
```

Once the parser is initialized, the `lxb_css_stylesheet_parse()` function gets called to parse the provided CSS string, which contains styling rules for the `<div>`:

```c
sst = lxb_css_stylesheet_parse(parser, css.data, css.length);
if (sst == NULL) {
    FAILED("Failed to parse CSS StyleSheet");
}
```

Successfully parsing the stylesheet is essential for associating styles with the HTML elements.

### Parsing the HTML Document

Following the CSS parsing, the example proceeds to parse the HTML content:

```c
status = lxb_html_document_parse(doc, html.data, html.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

This transformation processes the HTML string into a structure that can be navigated and manipulated.

### Attaching the Stylesheet

The program then links the parsed CSS stylesheet to the HTML document:

```c
status = lxb_html_document_stylesheet_attach(doc, sst);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

This attachment allows the styles to take effect when querying elements.

### Retrieving Element Styles

To get the styles applied to the `<div>`, the code initializes a collection to store the gathered elements:

```c
memset(&collection, 0, sizeof(lxb_dom_collection_t));

status = lxb_dom_node_by_tag_name(lxb_dom_interface_node(doc), &collection,
                                  str_div.data, str_div.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get element by name");
}
```

By calling `lxb_dom_node_by_tag_name()`, the program fetches the `<div>` element, which is then referenced to retrieve style declarations for specific properties:

```c
width = lxb_html_element_style_by_name(lxb_html_interface_element(div),
                                       str_width.data, str_width.length);
height = lxb_html_element_style_by_id(lxb_html_interface_element(div),
                                       LXB_CSS_PROPERTY_HEIGHT);
```

This logic effectively retrieves both width and height style settings applied to the element.

### Serializing Styles

To output the retrieved styles, the code serializes each one using the `lxb_css_rule_declaration_serialize()` function, which takes a callback function to handle the output:

```c
status = lxb_css_rule_declaration_serialize(width, callback, NULL);
status = lxb_css_rule_declaration_serialize(height, callback, NULL);
```

Here, the `callback` function simply prints the CSS properties to the console.

### Cleanup

As part of good coding practice, the program ends by freeing allocated resources, ensuring there are no memory leaks:

```c
(void) lxb_dom_collection_destroy(&collection, false);
(void) lxb_css_stylesheet_destroy(sst, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_html_document_destroy(doc);
```

## Conclusion

The presented example demonstrates the process of parsing and applying CSS styles to an HTML document using the Lexbor library. By following through each part of the code, one can gain insights into how to effectively manage CSS properties within a structured HTML environment, allowing for flexible design and styling in modern web applications.