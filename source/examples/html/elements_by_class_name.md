# Getting Elements by Class Name Example

In this article, we will explore the implementation details and functionality of
the `elements_by_class_name` example, found in the
[lexbor/html/elements_by_class_name.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/elements_by_class_name.c)
source file. The code demonstrates how to parse an HTML string and retrieve
elements with a specific class name using the `lexbor` library. This example is
essential for developers seeking to manipulate and query DOM elements in a
structured manner.

## Overview

The `main` function begins by initializing variables, including `status`,
`element`, `document`, and `collection`. It then assigns an HTML string to the
`html` variable, which contains multiple `<div>` elements with various class
names. The length of the HTML string is calculated and stored in `html_size`.

```c
const lxb_char_t html[] = "<div class=\"best blue some\"><span></div>"
    "<div class=\"red pref_best grep\"></div>"
    "<div class=\"red best grep\"></div>"
    "<div class=\"red c++ best\"></div>";

size_t html_size = sizeof(html) - 1;
```

## Parsing the HTML Document

Next, the code invokes the `parse` function to parse the HTML string and create
a DOM document. This document serves as the basis for subsequent operations on
the DOM elements contained within the HTML.

```c
document = parse(html, html_size);
```

## Creating a Collection for DOM Elements

Once the document is obtained, the next step is to create a collection to hold
the elements retrieved by class name. The `lxb_dom_collection_make` function is
called with the document's DOM and an initial capacity of 128. If the collection
cannot be created, an error message is triggered.

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
if (collection == NULL) {
    FAILED("Failed to create Collection object");
}
```

## Retrieving Elements by Class Name

The `lxb_dom_elements_by_class_name` function enables the search for elements
with a specified class name. In this instance, it looks for elements with the
class name "best". The function leverages the interface of the document's body
to initiate the retrieval process and populate the `collection`.

```c
status = lxb_dom_elements_by_class_name(lxb_dom_interface_element(document->body),
                                        collection, (const lxb_char_t *) "best", 4);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
```

After ensuring the retrieval is successful, the code proceeds to print the
original HTML and details about the found elements.

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
PRINT("\nFind all 'div' elements by class name 'best'.");
PRINT("Elements found:");
```

## Serializing and Printing Found Elements

A loop iterates through the collection of found elements, invoking the
`serialize_node` function to output each element's details. This demonstrates
how easy it is to interact with the elements returned by the class name query.

```c
for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
    element = lxb_dom_collection_element(collection, i);
    serialize_node(lxb_dom_interface_node(element));
}
```

## Cleanup

Finally, the `collection` and `document` are cleaned up to free allocated
resources. This step is crucial for managing memory within the application,
especially when dealing with large or complex documents.

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

## Conclusion

The `elements_by_class_name` example illustrates how to use the `lexbor` library
to parse HTML content, search for elements by class name, and efficiently manage
those elements. The critical sections of the code demonstrate proper document
handling, error management, and systematic cleanup, providing a solid foundation
for developers exploring DOM manipulation within C.