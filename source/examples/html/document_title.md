# Manipulating HTML Document Title

This article provides an in-depth explanation of the example code in 
`lexbor/html/document_title.c`, which demonstrates how to work with HTML 
document titles using the `lexbor` library. The code illustrates initializing a 
document, parsing an HTML string, extracting and modifying the title, and 
printing the tree structure before and after the change.

## Key Code Sections

### Initializing the HTML Document

The first critical step in the example is the creation of an HTML document 
object. This object will represent the entire HTML structure that the lexbor 
library manages.

```c
document = lxb_html_document_create();
if (document == NULL) {
    FAILED("Failed to create HTML Document");
}
```

Here, the function `lxb_html_document_create` is used to allocate and 
initialize a new `lxb_html_document_t` structure. If the initialization fails, 
the program will print an error message and terminate.

### Parsing the HTML String

Once the document is created, the example code parses a provided HTML string. 

```c
status = lxb_html_document_parse(document, html, html_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

The `lxb_html_document_parse` function takes the document object and the HTML 
string along with its length to populate the document with the appropriate 
nodes and structure. Proper error handling is shown to ensure that parsing 
completes successfully.

### Retrieving the Document Title

The example demonstrates two methods for retrieving the document title: 
formatted and raw. 

```c
title = lxb_html_document_title(document, &title_len);
if (title == NULL) {
    PRINT("\nTitle is empty");
}
else {
    PRINT("\nTitle: %s", title);
}

...

title = lxb_html_document_title_raw(document, &title_len);
if (title == NULL) {
    PRINT("Raw title is empty");
}
else {
    PRINT("Raw title: %s", title);
}
```

The `lxb_html_document_title` function retrieves the title after trimming 
whitespace and normalizing spaces. Conversely, `lxb_html_document_title_raw` 
returns the title exactly as it appears in the document, preserving all 
original formatting and whitespace.

### Modifying the Document Title

Next, the example code changes the document title to a new value provided by 
`new_title`.

```c
status = lxb_html_document_title_set(document, new_title, new_title_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to change HTML title");
}
```

Here, the `lxb_html_document_title_set` function is called with the new title 
and its length. This function updates the document's title element, and error 
handling ensures the operation completes successfully.

### Serializing and Printing the HTML Tree

After modifying the title, the example prints the document's tree structure 
before and after the title change.

```c
PRINT("HTML Tree: ");
serialize(lxb_dom_interface_node(document));

...

PRINT("\nHTML Tree after change title: ");
serialize(lxb_dom_interface_node(document));
```

The `serialize` function is used to output the tree structure, showing all 
nodes and their relationships. This helps visualize the changes made to the 
document.

### Cleaning Up

Finally, the code cleans up by destroying the document object, freeing any 
resources allocated during its creation and manipulation.

```c
lxb_html_document_destroy(document);
```

This is crucial to prevent memory leaks and ensure proper program termination.

## Notes

- **Error Handling**: Robust error handling ensures that each operation 
  (creation, parsing, modification) completes successfully or produces useful 
  output if it fails.
- **Title Retrieval vs. Raw Title**: The distinction between normalizing 
  whitespaces in the title versus retrieving it as-is can be important for 
  different application needs.
- **Resource Management**: Proper allocation and deallocation of resources are 
  demonstrated to maintain program stability and efficiency.

## Summary

In this example, we've explored the use of the `lexbor` library to manipulate an 
HTML document's title. The code demonstrates document creation, HTML parsing, 
title extraction, title modification, and tree serialization. Key takeaways 
include understanding lexbor's various functions for title handling and the 
importance of resource management and error handling. This example is a helpful 
reference for developers looking to programmatically control HTML content using 
lexbor.