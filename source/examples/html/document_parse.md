# Parsing an HTML Document

In this example, located in the `lexbor/html/document_parse.c` file, we see a typical usage scenario of the `lexbor` library for parsing an HTML document. This example demonstrates the creation of an HTML document object, basic parsing of HTML content, and serialization of the resulting DOM tree.

The example provides a clear, concise illustration of how to initialize and use the `lexbor` library to parse an HTML document. The example highlights crucial library functions and demonstrates error handling during document creation and HTML parsing. We will analyze several important sections of the code to understand its workings.

## Key Code Sections

### Creating an HTML Document

First, the code initializes the `lexbor` HTML document object. This is important because the document object forms the anchor point for subsequent parsing and manipulation operations.

```c
document = lxb_html_document_create();
if (document == NULL) {
    FAILED("Failed to create HTML Document");
}
```

Here, the `lxb_html_document_create()` function is called to allocate and initialize a new HTML document object. If the allocation fails, the program prints an error message and terminates.

### Parsing the HTML

Next, the example proceeds to parse a static HTML string.

```c
status = lxb_html_document_parse(document, html, html_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

The `lxb_html_document_parse()` function is used to parse the HTML content. The function takes the document object, a pointer to the HTML data, and the length of this data. If parsing fails (indicated by a status other than `LXB_STATUS_OK`), an error message is printed, and the program halts.

### Outputting the Parsed Content

To aid understanding, the code prints both the original HTML content and the resulting parsed DOM tree. 

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
```

```c
PRINT("\nHTML Tree:");
serialize(lxb_dom_interface_node(document));
```

The `PRINT` macro is used to output the HTML content and the resulting DOM tree. The `serialize` function (not fully shown in the excerpt) is responsible for serializing the DOM tree to a human-readable format, providing insight into the structure of the parsed document.

### Cleaning Up

Finally, the example demonstrates proper resource management by destroying the created HTML document.

```c
lxb_html_document_destroy(document);
```

This call to `lxb_html_document_destroy()` ensures that all resources allocated to the document object are released, preventing memory leaks.

## Notes

- **Error Handling**: The example employs a clear error handling strategy, checking the success of crucial library calls and halting execution when failures occur.
- **Serialization**: The use of a custom `serialize` function (assumed to be defined elsewhere in the code) helps visualize the resulting DOM tree, which is beneficial for both debugging and learning purposes.

## Summary

This example code from `lexbor/html/document_parse.c` serves as an excellent starting point for understanding basic document parsing using the `lexbor` library. It covers essential aspects such as initialization, parsing, and cleanup, while also demonstrating how to handle errors effectively. Typical `lexbor` users can draw valuable insights from this example to incorporate into their own projects, particularly concerning proper resource management and direct interaction with the HTML DOM.