# Extracting Elements by Tag Name

In this article, we will delve into the `lexbor/html/elements_by_tag_name.c` example,
which demonstrates how to extract HTML elements by their tag name using the `lexbor`
library. This specific example focuses on parsing an HTML snippet and then retrieving
all `<div>` elements from it. We will analyze the different sections of the code to 
understand how `lexbor` functions and data types facilitate these operations.

## Key Code Sections

### Parsing the HTML Document

The first significant step in the code is parsing an HTML document using the given 
HTML content.

```c
const lxb_char_t html[] = "<div a=b><span></div><div x=z></div>";
size_t html_szie = sizeof(html) - 1;

document = parse(html, html_szie);
```

The `parse` function takes the HTML content and its size to convert the string into 
an `lxb_html_document_t` structure. This document represents the parsed HTML in 
memory, allowing further manipulations.

### Creating and Initializing the Collection

Next, we need a collection to store the elements we find. `lexbor` provides 
mechanisms for creating and managing such collections efficiently.

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
if (collection == NULL) {
    FAILED("Failed to create Collection object");
}
```

Here, `lxb_dom_collection_make` initializes a collection with a preallocated size of 
128 elements. If the creation fails, it returns `NULL`, prompting the program to 
exit with an error message.

### Finding Elements by Tag Name

The critical function `lxb_dom_elements_by_tag_name` performs the task of finding 
all elements with a specific tag name.

```c
status = lxb_dom_elements_by_tag_name(lxb_dom_interface_element(document->body),
                                      collection, (const lxb_char_t *) "div", 3);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
```

In this code snippet:
- `lxb_dom_interface_element(document->body)` converts the body of the document 
  into a generic element interface.
- `collection` is passed to store the found elements.
- The tag name `"div"` is specified along with its length, `3`.

If the function fails to find any elements, it returns a status other than 
`LXB_STATUS_OK`.

### Iterating Over and Serializing Found Elements

Once the elements are found, we iterate over the collection and serialize each node 
for display.

```c
for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
    element = lxb_dom_collection_element(collection, i);

    serialize_node(lxb_dom_interface_node(element));
}
```

We loop through each element in the collection, retrieve it using 
`lxb_dom_collection_element`, and then serialize it for output using the 
`serialize_node` function.

### Cleanup

Proper cleanup of allocated resources is crucial to avoid memory leaks.

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

Here, `lxb_dom_collection_destroy` releases the memory for the collection, and 
`lxb_html_document_destroy` does the same for the document.

## Notes

- The example underscores the importance of checking return values for error 
  handling.
- It showcases the use of `lxb_dom_elements_by_tag_name` to query elements 
  efficiently.

## Summary

The `lexbor/html/elements_by_tag_name.c` example effectively demonstrates how to 
parse an HTML document and extract elements by their tag name. Key takeaways include 
the importance of proper initialization and error handling, as well as the 
simplicity and power of the `lexbor` API for DOM manipulation tasks. This example is 
an excellent starting point for developers looking to utilize the `lexbor` library 
for web scraping or HTML processing tasks.