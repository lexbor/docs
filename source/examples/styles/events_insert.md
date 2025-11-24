# Demonstrating Event Insertions in HTML with CSS

This article elaborates on the [lexbor/styles/events_insert.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/styles/events_insert.c) file from the `lexbor` library. It details how to parse an HTML document, attach a CSS stylesheet to it, and dynamically insert new elements, demonstrating how styles are applied. This example illustrates `lexbor`'s ability to manipulate both HTML and CSS effectively.

## Key Code Sections

### Callback Function

The example begins with a callback function used for serializing and printing the HTML and CSS data.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

This function simply prints a piece of data and returns a status code indicating success. It is used later for serializing and outputting HTML and CSS content.

### HTML and CSS Initialization

Next, the main function initializes HTML and CSS data as well as other necessary variables.

```c
static const lexbor_str_t html = lexbor_str("<div class=father><p class=best>a</p><p>b</p><s>c</s></div>");
static const lexbor_str_t slctrs = lexbor_str("div.father {width: 30%} div.father p.best {width: 20px; height: 10pt}");
```

#### Creating and Parsing HTML Document

The example demonstrates how to create and parse an HTML document from a string.

```c
document = lxb_html_document_create();
if (document == NULL) {
    return EXIT_FAILURE;
}

status = lxb_html_document_parse(document, html.data, html.length);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

The `lxb_html_document_create` function initializes an empty HTML document, and `lxb_html_document_parse` populates it with the provided HTML string.

### Initializing CSS

The example proceeds to initialize CSS-related objects and memory structures for the document.

```c
status = lxb_html_document_css_init(document);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

This ensures that the document is prepared to handle CSS styles.

#### Creating and Attaching CSS Stylesheet

A CSS parser is created and initialized, followed by parsing and attaching the stylesheet to the document.

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

sst = lxb_css_stylesheet_parse(parser, slctrs.data, slctrs.length);
if (sst == NULL) {
    return EXIT_FAILURE;
}

status = lxb_html_document_stylesheet_attach(document, sst);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

These steps ensure that styles defined in the stylesheet are applied to the document elements accordingly.

### Finding and Modifying Elements

The example shows how to use CSS selectors to find elements and then add a new element with specific attributes.

```c
collection = lxb_dom_collection_make(lxb_dom_interface_document(document), 16);
status = lxb_dom_node_by_class_name(lxb_dom_interface_node(document), collection, father_str.data, father_str.length);
div = lxb_html_interface_element(lxb_dom_collection_node(collection, 0));

np = lxb_html_document_create_element(document, p_str.data, p_str.length, NULL);
attr = lxb_dom_element_set_attribute(lxb_dom_interface_element(np), class_str.data, class_str.length, best_str.data, best_str.length);
attr = lxb_dom_element_set_attribute(lxb_dom_interface_element(np), style_name.data, style_name.length, style_value.data, style_value.length);
lxb_html_element_insert_child(div, np);
```

- **Collection Initialization**: Creating a collection and storing elements matching the "father" class.
- **New Element Insertion**: Creating a new `<p>` element with class "best" and inline style settings, and appending it to the `<div>` with the "father" class.

### Serialization and Result Verification

The inserted element and the modified HTML are serialized and printed to verify the results.

```c
status = lxb_html_serialize_cb(lxb_dom_interface_node(np), callback, NULL);
status = lxb_html_serialize_tree_cb(lxb_dom_interface_node(document), callback, NULL);
status = lxb_html_element_style_serialize(np, LXB_HTML_ELEMENT_OPT_UNDEF, callback, NULL);
```

Each function call outputs the current state of the HTML and the styles applied to the inserted element, ensuring correctness.

### Resource Cleanup

Finally, resources allocated during execution are appropriately cleaned up.

```c
(void) lxb_dom_collection_destroy(collection, true);
(void) lxb_css_stylesheet_destroy(sst, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_html_document_destroy(document);
```

Proper resource management is crucial to prevent memory leaks and other issues.

## Notes

- **Proper Initialization**: Ensure HTML and CSS objects are initialized correctly before use.
- **CSS Parsing**: Proper parsing and attachment of stylesheets are essential to apply styles.
- **Dynamic Modifications**: The example illustrates dynamic insertion and modification of elements in a DOM and verifying applied styles.
- **Resource Management**: Always clean up resources to maintain application stability and performance.

## Summary

This example demonstrates how to use the `lexbor` library to dynamically create, modify, and style HTML documents by applying CSS styles. These operations are essential for web developers and engineers who need to manipulate and style DOM elements dynamically. Understanding this example can help developers harness the power of `lexbor` for efficient HTML and CSS manipulation.