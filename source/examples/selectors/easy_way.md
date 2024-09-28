# Using Selectors with lexbor

This article delves into the use of CSS selectors within the `lexbor` library, specifically through the example provided in the file `lexbor/selectors/easy_way.c`. This example demonstrates how to create an HTML document, parse it, apply CSS selectors, and find matching HTML elements.

The example illustrates how the `lexbor` library can be utilized to parse an HTML document, apply CSS selectors to it, and then process the matched nodes. This is achieved through several key steps: initializing the HTML document, setting up the CSS parser, creating and parsing selectors, and finally, invoking callbacks when matches are found.

## Key Code Sections

### Setting Up Callbacks

The example defines two crucial callback functions: `callback` and `find_callback`. These functions are used for serialization and handling found nodes, respectively.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

lxb_status_t
find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec,
              void *ctx)
{
    unsigned *count = ctx;
    (*count)++;
    printf("%u) ", *count);
    (void) lxb_html_serialize_cb(node, callback, NULL);
    printf("\n");
    return LXB_STATUS_OK;
}
```

The `callback` function is used to serialize the selector list or nodes. It takes the data and its length, and prints it. `find_callback` increments a counter each time a node is found, prints the count and the serialized node.

### Parsing the HTML Document

The example then proceeds to create an HTML document and parse it using the sample data.

```c
static const lxb_char_t html[] = "<div><p class='x z'></p><p id='y'></p></div>";

document = lxb_html_document_create();
status = lxb_html_document_parse(document, html,
                                 sizeof(html) / sizeof(lxb_char_t) - 1);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

This code snippet initializes the HTML document and parses a small HTML string containing a `<div>` with two `<p>` elements.

### Setting Up and Parsing CSS Selectors

Next, a CSS parser is created, initialized, and used to parse a given CSS selector string.

```c
static const lxb_char_t slctrs[] = ".x, div:has(p[id=Y i])";

parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

selectors = lxb_selectors_create();
status = lxb_selectors_init(selectors);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

list = lxb_css_selectors_parse(parser, slctrs,
                               sizeof(slctrs) / sizeof(lxb_char_t) - 1);
if (parser->status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

This part sets up the CSS parser and parses the selector string which contains two selectors: `.x` and `div:has(p[id=Y i])`. The second selector demonstrates the use of the `:has` pseudo-class and a case insensitivity flag `i`.

### Serializing and Finding Nodes

Selectors are serialized for logging, and the example then finds nodes in the document that match the parsed CSS selectors.

```c
printf("Selectors: ");
(void) lxb_css_selector_serialize_list_chain(list, callback, NULL);
printf("\n");

body = lxb_dom_interface_node(document);

printf("Found:\n");

status = lxb_selectors_find(selectors, body, list, find_callback, &count);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

The `lxb_css_selector_serialize_list_chain` function serializes the selector list. Then, the HTML document's root node is obtained, and `lxb_selectors_find` is used to find and process nodes matching the selectors.

### Cleaning Up

Finally, the example code ensures that all resources are properly cleaned up.

```c
(void) lxb_selectors_destroy(selectors, true);
(void) lxb_css_parser_destroy(parser, true);
lxb_css_selector_list_destroy_memory(list);
lxb_html_document_destroy(document);
```

## Notes

- **Callbacks** are essential for handling and processing matched nodes.
- Proper **Initialization and Destruction** of objects ensure memory management and resource cleanup.
- The example uses **Advanced CSS selectors** like `:has`.

## Summary

This example highlights the core functionalities of the `lexbor` library: parsing HTML documents, using CSS parsers, and handling node selection with callbacks. It demonstrates how to effectively apply complex CSS selectors and manage resources within the library, providing a comprehensive guide for intermediate to advanced users aiming to leverage `lexbor` for DOM manipulation and CSS querying.