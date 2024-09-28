# HTML Chunks Parsing: Example

In this article, we will delve into the `lexbor/html/parse_chunk.c` file, which is designed to demonstrate how to parse HTML in chunks using the `lexbor` library. This approach is useful for handling HTML data that arrives in parts, such as from network streams. We will examine key sections of the code to understand its functionality and the useful features of the `lexbor` library.

## Key Code Sections

### Initialization

The example begins with initializing the HTML parser provided by `lexbor`. Let's take a closer look at the relevant code:

```c
lxb_html_parser_t *parser;
lxb_status_t status;

parser = lxb_html_parser_create();
status = lxb_html_parser_init(parser);

if (status != LXB_STATUS_OK) {
    FAILED("Failed to create HTML parser");
}
```

In this section, the `lxb_html_parser_create` function is called to allocate memory for the parser, and then `lxb_html_parser_init` is used to initialize it. Both functions must succeed for the parsing process to proceed.

### Parsing Chunks

The core of this example is the parsing of HTML in chunks. HTML data is split into parts, stored in an array, and processed in a loop:

```c
static const lxb_char_t html[][64] = {
    "<!DOCT","YPE htm","l>","<html><head>",
    "<ti","tle>HTML chunks parsing</","title>",
    "</head><bod","y><div cla","ss=","\"bestofclass", "\">",
    "good for me","</div>","\0"
};

document = lxb_html_parse_chunk_begin(parser);
if (document == NULL) {
    FAILED("Failed to create Document object");
}

for (size_t i = 0; html[i][0] != '\0'; i++) {
    status = lxb_html_parse_chunk_process(parser, html[i], strlen((const char *)html[i]));
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to parse HTML chunk");
    }
}

status = lxb_html_parse_chunk_end(parser);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

Here, `lxb_html_parse_chunk_begin` initiates chunk-based parsing and returns a `document` object, allowing the `lexbor` library to start processing the HTML data. Each chunk from the `html` array is then processed sequentially with `lxb_html_parse_chunk_process`. Finally, `lxb_html_parse_chunk_end` finalizes the parsing operation.

### Serialization

After parsing, the DOM tree is serialized back to HTML format:

```c
status = lxb_html_serialize_pretty_tree_cb(lxb_dom_interface_node(document),
                                           LXB_HTML_SERIALIZE_OPT_UNDEF,
                                           0, serializer_callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize HTML tree");
}
```

The `lxb_html_serialize_pretty_tree_cb` function is responsible for converting the parsed document structure back to HTML text, providing an option for pretty-printed output. A user-defined `serializer_callback` handles the serialized output.

### Cleanup

Proper cleanup is essential to prevent memory leaks:

```c
lxb_html_document_destroy(document);
lxb_html_parser_destroy(parser);
```

The document and parser are destroyed, freeing the associated resources.

## Notes

- **Chunk Processing**: The example demonstrates how to handle partially received HTML data, which is particularly useful for streaming scenarios.
- **Error Handling**: Proper error checking is performed throughout the example, ensuring that issues are caught and reported early.
- **Serialization**: The ability to serialize the DOM tree back to HTML is useful for various post-processing tasks.

## Summary

The `lexbor/html/parse_chunk.c` example provides a clear illustration of how to use the `lexbor` library to parse HTML data in chunks. This functionality is essential for applications dealing with streaming data or other scenarios where HTML content is received incrementally. Understanding and utilizing these examples can greatly enhance the robustness and efficiency of your HTML processing tasks.