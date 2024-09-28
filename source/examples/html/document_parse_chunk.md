# HTML Document Parsing Example

This article provides an overview of an example implementation of HTML document parsing using the Lexbor library. The example is located in the source file `lexbor/html/document_parse_chunk.c`. This example demonstrates how to create an HTML document, parse it in chunks, and handle the cleaning up of allocated resources.

## Code Overview

The primary function of the code is to illustrate how to process HTML content in segments, allowing for a more flexible parsing technique suitable for scenarios where full documents may not be available in one piece. This chunk-based parsing can be particularly useful for streaming applications or when handling very large HTML documents.

### Initialization

At the beginning of the `main` function, several essential variables are declared, including a status variable of type `lxb_status_t` and a pointer to a `lxb_html_document_t`, which will represent our HTML document. 

```c
lxb_html_document_t *document;
```

The `lxb_html_document_create()` function is called to create an instance of the HTML document. It is essential to check whether the document was created successfully.

```c
document = lxb_html_document_create();
if (document == NULL) {
    FAILED("Failed to create HTML Document");
}
```

If the document creation fails, the program will exit, indicating an error.

### Parsing HTML Chunks

The HTML content is stored in a two-dimensional array of characters. Each string represents a fragment of the HTML document. The fragments are designed to be combined later to form a complete HTML structure.

```c
static const lxb_char_t html[][64] = {
    "<!DOCT", "YPE htm", "l>", "<html><head>", "<ti", "tle>HTML chun",
    "ks parsing</", "title>", "</head><bod", "y><div cla", "ss=",
    "\"bestof", "class", "\">", "good for me", "</div>", "\0"
};
```

After setting up the document, the code initiates the parsing process by calling `lxb_html_document_parse_chunk_begin()`, which prepares the document to accept incoming chunks of HTML.

```c
status = lxb_html_document_parse_chunk_begin(document);
```

The program then enters a loop that iterates over each HTML chunk until it reaches a null-terminating character. For each chunk, it prints the chunk content and attempts to parse it using `lxb_html_document_parse_chunk()`. This function takes the current HTML chunk and its length as input, returning a status that indicates success or failure.

```c
for (size_t i = 0; html[i][0] != '\0'; i++) {
    PRINT("%s", (const char *) html[i]);
    
    status = lxb_html_document_parse_chunk(document, html[i], 
                                           strlen((const char *) html[i]));
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to parse HTML chunk");
    }
}
```

If any chunk fails to parse correctly, the program will exit with an error message.

### Finalization

After processing all HTML chunks, the end of the parsing process is signaled with the call to `lxb_html_document_parse_chunk_end()`. This function finalizes the parsing operation and validates the final structure of the document.

```c
status = lxb_html_document_parse_chunk_end(document);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

### Printing Results

Once parsing is complete, the example demonstrates how to serialize the resulting HTML DOM tree using the `serialize()` function, allowing the user to see the structured representation of the parsed HTML content.

```c
PRINT("\nHTML Tree:");
serialize(lxb_dom_interface_node(document));
```

### Cleanup

Finally, the document is destroyed using `lxb_html_document_destroy()`, which frees the allocated memory associated with the HTML document instance. This resource management step is crucial in avoiding memory leaks.

```c
lxb_html_document_destroy(document);
```

## Conclusion

This example effectively illustrates how to use Lexbor for HTML document parsing in a chunked manner. The structure and logic of the code provide a solid foundation for more advanced HTML processing applications. It encapsulates essential operations such as initialization, incremental parsing, result extraction, and cleanup in a clear and easy-to-follow manner.