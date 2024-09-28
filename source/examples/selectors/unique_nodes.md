# Parsing HTML and CSS Selectors in lexbor

This example in `lexbor/selectors/unique_nodes.c` demonstrates how to use the
`lexbor` library to parse HTML content, process CSS selectors, and find HTML
nodes that match the parsed selectors. The key parts of this example include
initializing various lexbor structures, parsing HTML and CSS, serializing the
parsed structures, and finding matching nodes in the HTML document. This example
serves as a comprehensive demonstration for developers looking to understand the
integration of HTML and CSS parsing and selection using lexbor.

## Key Code Sections

### Callback Functions

Two callback functions are defined for handling data serialization and node
finding:

```c
lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx) {
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

lxb_status_t find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec, void *ctx) {
    unsigned *count = ctx;
    *count += 1;
    printf("%u) ", *count);
    (void) lxb_html_serialize_cb(node, callback, NULL);
    printf("\n");
    return LXB_STATUS_OK;
}
```

- `callback`: This function is used for serializing data to be printed to stdout.
  It takes a data block and its length and prints the content.
- `find_callback`: This function is called whenever a matching HTML node is found.
  It increments a counter and serializes the found node.

### HTML Document Creation and Parsing

The code initializes and parses the HTML document:

```c
static const lxb_char_t html[] = "<div><p class='x z'> </p><p id='y'>abc</p></div>";
document = lxb_html_document_create();
status = lxb_html_document_parse(document, html, sizeof(html) / sizeof(lxb_char_t) - 1);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
body = lxb_dom_interface_node(document);
```

- The HTML source string is defined and parsed into an `lxb_html_document_t`.
- If parsing is successful, the document's root node is retrieved.

### CSS Parser and Selector Initialization

The CSS parsing and selector creation are handled as follows:

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

css_selectors = lxb_css_selectors_create();
status = lxb_css_selectors_init(css_selectors);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

lxb_css_parser_selectors_set(parser, css_selectors);
```

- A CSS parser and CSS selector are created and initialized.
- The CSS parser is configured to use the previously created CSS selector.

### Parsing CSS Selectors

CSS selectors from a string are parsed and logged:

```c
static const lxb_char_t slctrs[] = ".x, div:has(p[id=Y i]), p.x, p:blank, div";
list = lxb_css_selectors_parse(parser, slctrs,
                               (sizeof(slctrs) / sizeof(lxb_char_t)) - 1);
if (list == NULL) {
    return EXIT_FAILURE;
}
```

- The selectors defined in the string are parsed into an `lxb_css_selector_list_t`.
- If parsing fails, the program exits with an error.

### Serializing and Finding Nodes

The HTML content and CSS selectors are serialized, and matching nodes are found:

```c
printf("HTML:\n");
(void) lxb_html_serialize_pretty_deep_cb(body, 0, 0, callback, NULL);
printf("\n");

printf("Selectors: ");
(void) lxb_css_selector_serialize_list_chain(list, callback, NULL);
printf("\n");

count = 0;
lxb_selectors_opt_set(selectors, LXB_SELECTORS_OPT_MATCH_FIRST);
status = lxb_selectors_find(selectors, body, list, find_callback, &count);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

- The HTML content is serialized and printed.
- The parsed CSS selector list is serialized and printed.
- The `lxb_selectors_find` function is used to find matching HTML nodes based on
  the parsed selectors and the `find_callback` function is called for each match.

### Cleanup

Finally, the initialized structures are destroyed to free resources:

```c
(void) lxb_selectors_destroy(selectors, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_css_memory_destroy(list->memory, true);
(void) lxb_css_selectors_destroy(css_selectors, true);
(void) lxb_html_document_destroy(document);
```

- This ensures that all allocated resources are properly cleaned up.

## Notes

- The sample uses multiple `lexbor` subsystems: HTML, CSS, and selectors.
- Proper error handling is employed after each initialization and parsing step.
- The example demonstrates both parsing and serialization tasks.

## Summary

This example illustrates how to integrate various `lexbor` subsystems to parse
and process HTML and CSS content. Understanding these interactions is essential
for developers looking to build robust applications that manipulate web content.
This example emphasizes resource management and error checking strategies,
providing a solid foundation for more complex tasks in `lexbor`.