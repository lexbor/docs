# Querying Elements by Class Name

File: `lexbor/html/elements_by_class_name.c`

This example demonstrates how to use the `lexbor` library to parse an HTML
document and retrieve all elements with a specific class name. The example
focuses on finding elements with the class name `"best"` from a given HTML
string and serializing them for output.

## Key Code Sections

### Parsing the HTML Document

The first step involves parsing a hard-coded HTML string into a
`lxb_html_document_t` object that can be manipulated through the `lexbor`
library.

```c
const lxb_char_t html[] = "<div class=\"best blue some\"><span></div>"
    "<div class=\"red pref_best grep\"></div>"
    "<div class=\"red best grep\"></div>"
    "<div class=\"red c++ best\"></div>";

size_t html_szie = sizeof(html) - 1;

document = parse(html, html_szie);
```

Here, the HTML string contains multiple `<div>` elements with different class
names. The `parse` function is used to convert this HTML string into a
`document` object, which can then be queried.

### Creating a Collection

To store the elements that match a specific query, a collection object is
created using `lxb_dom_collection_make`.

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
if (collection == NULL) {
    FAILED("Failed to create Collection object");
}
```

The collection is initialized with a capacity of 128 elements, a reasonable
default size for various use cases.

### Querying by Class Name

The core functionality of this example is querying the parsed document by a
specific class name using `lxb_dom_elements_by_class_name`.

```c
status = lxb_dom_elements_by_class_name(lxb_dom_interface_element(document->body),
                                        collection, (const lxb_char_t *) "best", 4);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
```

Here, the function `lxb_dom_elements_by_class_name` is called with the root
element of the document's body, the collection to store results, the class name
`"best"` (as a `const lxb_char_t *`), and the length of the class name (which is
`4`). This function searches for all elements with the class name `"best"` and
stores them in the collection.

### Serializing and Printing the Results

Once the elements are found, they are iterated over and serialized for output.

```c
for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
    element = lxb_dom_collection_element(collection, i);
    serialize_node(lxb_dom_interface_node(element));
}
```

Each element in the collection is retrieved using
`lxb_dom_collection_element` and passed to the `serialize_node` function, which
handles the process of serialization into a string format for printing.

### Cleaning Up

Finally, the collection and document are properly destroyed to free up memory.

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

## Notes

- **Memory Management**: Proper memory management is crucial. Ensure that all
  created objects are destroyed to prevent memory leaks.
- **Error Handling**: Always check the return status of functions, especially
  those that create objects or perform searches, to handle errors gracefully.
- **Collection Size**: The initial size of the collection can be adjusted based
  on the expected number of elements to optimize performance.

## Summary

This example illustrates how to effectively use the `lexbor` library for
searching and manipulating elements in an HTML document. By understanding how to
parse the document, query elements by class name, and handle them appropriately,
you can leverage `lexbor` for various web scraping or HTML manipulation tasks.
The key takeaway is the efficient and accurate way `lexbor` allows querying and
handling elements based on class names, showcasing its robust capabilities for
document object model manipulation.