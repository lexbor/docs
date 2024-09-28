# Parsing Inline CSS Styles: Example

This article provides an in-depth explanation of an example program available in the file `lexbor/styles/attribute_style.c`, which demonstrates how to parse inline CSS styles within HTML elements using the `lexbor` library. The example focuses specifically on extracting and serializing the `width` and `height` CSS properties from a `<div>` element. This task involves HTML parsing, CSS preprocessing, and style extraction using various functions provided by `lexbor`.

## Key Code Sections

### Creating the HTML Document

The first core part of the code initializes an HTML document using `lexbor`.

```c
lxb_html_document_t *doc;

doc = lxb_html_document_create();
if (doc == NULL) {
    FAILED("Failed to create HTML Document");
}

status = lxb_html_document_css_init(doc);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to CSS initialization");
}
```

**Explanation**:  
This section creates an HTML document object `doc` using `lxb_html_document_create()`, and checks for successful creation. Following that, it initializes the CSS subsystem of the document with `lxb_html_document_css_init(doc)`, which is necessary before performing any CSS-related operations.

### Parsing the HTML Content

Next, the HTML content is parsed to fill the document with nodes.

```c
static const lexbor_str_t html = lexbor_str(
    "<div style='width: 10px; width: 123%; height: 20pt !important; height: 10px'></div>"
);

status = lxb_html_document_parse(doc, html.data, html.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

**Explanation**:  
This section defines a static HTML string and uses `lxb_html_document_parse()` to parse this HTML content and populate the `doc` with the corresponding DOM tree structure. The function takes the document pointer and the raw HTML data along with its length.

### Finding the `<div>` Element

With the document populated, the code proceeds to find the specific `<div>` element.

```c
static const lexbor_str_t str_div = lexbor_str("div");
lxb_dom_collection_t collection;

memset(&collection, 0, sizeof(lxb_dom_collection_t));

status = lxb_dom_node_by_tag_name(lxb_dom_interface_node(doc), &collection,
                                  str_div.data, str_div.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get element by name");
}
```

**Explanation**:  
This code initializes a DOM collection to gather all nodes with the tag name `div`. It uses the `lxb_dom_node_by_tag_name()` function, which searches the DOM tree starting from the document node and fills the collection with the matching nodes.

### Extracting the CSS Styles

Here, the specific CSS properties `width` and `height` are extracted from the found `<div>` element.

```c
const lxb_css_rule_declaration_t *width, *height;
static const lexbor_str_t str_width = lexbor_str("width");

div = lxb_dom_collection_element(&collection, 0);
if (div == NULL) {
    FAILED("Failed to get element by name");
}

width = lxb_html_element_style_by_name(lxb_html_interface_element(div),
                                       str_width.data, str_width.length);
if (width == NULL) {
    FAILED("Failed to get style by name");
}

height = lxb_html_element_style_by_id(lxb_html_interface_element(div),
                                      LXB_CSS_PROPERTY_HEIGHT);
if (height == NULL) {
    FAILED("Failed to get style by id");
}
```

**Explanation**:  
`lxb_dom_collection_element(&collection, 0)` retrieves the first `<div>` node in the collection. The `lxb_html_element_style_by_name()` function fetches the CSS rule for the style property `width` by name, while `lxb_html_element_style_by_id()` retrieves the rule for the `height` property using a predefined constant `LXB_CSS_PROPERTY_HEIGHT`. Both functions operate on an HTML element interface.

### Serializing the CSS Declarations

Finally, the retrieved CSS declarations are serialized back to strings for printing.

```c
status = lxb_css_rule_declaration_serialize(width, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize width declaration");
}

printf("\n");

status = lxb_css_rule_declaration_serialize(height, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize height declaration");
}
```

**Explanation**:  
The `lxb_css_rule_declaration_serialize()` function is employed to serialize the CSS rule declarations for `width` and `height`. The `callback` function defined at the outset is used to handle the serialized output, which is printed to the console. This demonstrates the final step of extracting and exporting CSS property values.

## Notes

- The `lxb_html_document_css_init()` is crucial for preparing the document object to handle CSS-specific tasks.
- Proper error handling ensures the robustness of the code, exiting gracefully if any of the critical steps fail.
- Initialization of the DOM collection and searching nodes with `lxb_dom_node_by_tag_name()` showcases the flexibility of `lexbor` in DOM traversal and manipulation.

## Summary

This example demonstrates the process of initialization, parsing, and CSS extraction using the `lexbor` library. By leveraging various `lexbor` functions, the example showcases practical use cases for HTML and CSS manipulation. The ability to decode, search, and serialize CSS properties within HTML documents is highly beneficial for applications involving web scraping, automated style audits, or dynamic content adjustments. Understanding these core functionalities can significantly enhance a developer's toolkit in handling complex HTML and CSS scenarios.