# Extracting Elements by Attribute

The file `lexbor/html/elements_by_attr.c` demonstrates how to use the `lexbor` library to extract and manipulate HTML elements based on their attributes. This example illustrates a range of selection techniques, including full match, starts with, ends with, and contains. Here, we will provide an in-depth explanation of the key sections within this code to better understand its functionality.

## Key Code Sections

### Initialization and Parsing

The example starts by initializing required variables and parsing the HTML document.

```c
lxb_html_document_t *document;
const lxb_char_t html[] = "<div class=\"best blue some\"><span></div>"
    "<div class=\"red pref_best grep\"></div>"
    "<div class=\"green best grep\"></div>"
    "<a href=\"http://some.link/\">ref</a>"
    "<div class=\"red c++ best\"></div>";
size_t html_size = sizeof(html) - 1;

document = parse(html, html_size);
body = lxb_dom_interface_element(document->body);
```

The `parse` function converts the raw HTML string into a structured `document` that `lexbor` can process. The `lxb_dom_interface_element` call retrieves the body element from the document for further manipulation.

### Creating the Collection

Next, the code creates a collection object to hold the selected elements.

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
if (collection == NULL) {
    FAILED("Failed to create Collection object");
}
```

By calling `lxb_dom_collection_make`, a new collection is created with an initial capacity of 128 elements. This collection will be reused for different attribute selection methods.

### Full Match Selection

This section demonstrates how to select elements by an exact attribute match.

```c
status = lxb_dom_elements_by_attr(body, collection,
                                  (const lxb_char_t *) "class", 5,
                                  (const lxb_char_t *) "red c++ best", 12,
                                  true);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
PRINT("\nFull match by 'red c++ best':");
print_collection_elements(collection);
```

The `lxb_dom_elements_by_attr` function is used here to find elements with the `class` attribute exactly matching "red c++ best." The result is stored in the `collection`.

### Begin-Match Selection

```c
status = lxb_dom_elements_by_attr_begin(body, collection,
                                        (const lxb_char_t *) "href", 4,
                                        (const lxb_char_t *) "http", 4,
                                        true);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
PRINT("\nFrom begin by 'http':");
print_collection_elements(collection);
```

In this snippet, `lxb_dom_elements_by_attr_begin` selects elements where the `href` attribute starts with "http". This demonstrates the flexibility of attribute-based selection.

### End-Match Selection

```c
status = lxb_dom_elements_by_attr_end(body, collection,
                                      (const lxb_char_t *) "class", 5,
                                      (const lxb_char_t *) "grep", 4,
                                      true);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
PRINT("\nFrom end by 'grep':");
print_collection_elements(collection);
```

The `lxb_dom_elements_by_attr_end` function selects elements where the `class` attribute ends with "grep."

### Contain-Match Selection

```c
status = lxb_dom_elements_by_attr_contain(body, collection,
                                          (const lxb_char_t *) "class", 5,
                                          (const lxb_char_t *) "c++ b", 5,
                                          true);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
PRINT("\nContain by 'c++ b':");
print_collection_elements(collection);
```

Lastly, `lxb_dom_elements_by_attr_contain` is used to find elements with `class` attributes containing "c++ b."

## Notes

- The `print_collection_elements` function efficiently serializes and prints the details of the selected elements.
- The collection is cleaned after each selection to prepare it for the next usage.
- Error handling ensures that failures in creating the collection or selecting elements are reported.

## Summary

This example showcases various techniques to select HTML elements by attributes using the `lexbor` library. By understanding how to utilize functions like `lxb_dom_elements_by_attr`, `lxb_dom_elements_by_attr_begin`, `lxb_dom_elements_by_attr_end`, and `lxb_dom_elements_by_attr_contain`, developers can effectively manipulate and query HTML documents based on specific attribute criteria. This is essential for tasks involving web scraping, data extraction, and document manipulation.