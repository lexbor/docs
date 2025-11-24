# CSS Selectors Handling in `lexbor`

This article explains the purpose and functionality of the [lexbor/selectors/normal_way.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/selectors/normal_way.c) example file. The code demonstrates how to work with CSS selectors using the `lexbor` library. We'll dive deep into the primary segments of the code, examining the creation and manipulation of HTML documents, parsing CSS selectors and applying them to an HTML document to find specific nodes.

The example showcases how to parse HTML and CSS, use CSS selectors to find specific elements within the HTML document, and handle these elements via callbacks. By understanding this example, you'll gain insights into utilizing the `lexbor` library for HTML parsing and CSS selector applications.

## Key Code Sections

### Callback Function for Serialization

The `callback` function is used for serializing HTML nodes. It prints the data received from the lexbor functions.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

### Callback Function for Found Nodes

The `find_callback` function gets invoked for each HTML node found by the CSS selectors. It increments a count and serializes the node.

```c
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

### HTML Document Creation and Parsing

The example starts by creating and parsing an HTML document.

```c
document = lxb_html_document_create();
status = lxb_html_document_parse(document, html,
                                 sizeof(html) / sizeof(lxb_char_t) - 1);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
body = lxb_dom_interface_node(document);
```

### Memory and CSS Parser Initialization

Memory for parsed structures and the CSS parser are initialized next. This ensures that the CSS parser has a working memory pool for operations.

```c
memory = lxb_css_memory_create();
status = lxb_css_memory_init(memory, 128);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

lxb_css_parser_memory_set(parser, memory);
```

### CSS Selectors Parsing

Two sets of CSS selectors are parsed to create selector lists that will later be used to query the HTML document.

```c
list_one = lxb_css_selectors_parse(parser, slctrs_one,
                                   sizeof(slctrs_one) / sizeof(lxb_char_t) - 1);
if (list_one == NULL) {
    return EXIT_FAILURE;
}

list_two = lxb_css_selectors_parse(parser, slctrs_two,
                                   sizeof(slctrs_two) / sizeof(lxb_char_t) - 1);
if (list_two == NULL) {
    return EXIT_FAILURE;
}
```

### Applying Selectors to Find Nodes

The parsed selectors are applied to the HTML document to find nodes matching the criteria. The `find_callback` function is used to process each found node.

```c
status = lxb_selectors_find(selectors, body, list_one,
                            find_callback, &count);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

status = lxb_selectors_find(selectors, body, list_two,
                            find_callback, &count);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

### Cleanup

Finally, cleanup code ensures that all allocated objects are properly destroyed.

```c
(void) lxb_selectors_destroy(selectors, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_css_memory_destroy(memory, true);
(void) lxb_css_selectors_destroy(css_selectors, true);
(void) lxb_html_document_destroy(document);
```

## Notes

- The parser and memory are initialized with conjunction to minimize memory allocations.
- The `find_callback` function is used to process each matched node, giving flexibility in handling the results.
- Proper cleanup ensures no memory leaks, critical in long-running or resource-constrained applications.

## Summary

This example illustrates the process of parsing HTML and CSS, applying CSS selectors to identify HTML nodes, and using callbacks to handle these nodes in the `lexbor` library. Understanding this sequence is crucial for effectively leveraging lexbor in projects requiring sophisticated HTML and CSS manipulations.