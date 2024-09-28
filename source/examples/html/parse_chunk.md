# HTML Chunk Parsing Example

This article provides an overview of the HTML chunk parsing example implemented
in the source file
[lexbor/html/parse_chunk.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/parse_chunk.c).
The example demonstrates how to utilize the Lexbor HTML parsing library to
handle HTML data in incremental chunks. By breaking the input into smaller
pieces, it showcases the parser's versatility and ability to manage partial data
streams effectively.

## Code Overview

The main function serves as the entry point for the program. Here, several
significant components of the Lexbor library are employed, such as creating a
parser, managing HTML documents, and serializing the parsed content.

### Initialization

The first step involves initializing the parser:

```c
parser = lxb_html_parser_create();
status = lxb_html_parser_init(parser);
```

In this section, `lxb_html_parser_create()` is called to create a new HTML
parser instance. It's crucial to check if the parser was successfully created by
examining `status`. If initialization fails, a failure message is displayed.

### Parsing Chunks

After initialization, the code prepares to parse the HTML content chunk by
chunk:

```c
document = lxb_html_parse_chunk_begin(parser);
```

This line initializes parsing by creating a document object that will hold the
parsed data. If the document object is not successfully created, an error
message is emitted, halting further execution.

The program then enters a loop to process the defined HTML chunks stored in a
static array:

```c
for (size_t i = 0; html[i][0] != '\0'; i++) {
    status = lxb_html_parse_chunk_process(parser, html[i],
                                          strlen((const char *) html[i]));
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to parse HTML chunk");
    }
}
```

Here, `lxb_html_parse_chunk_process()` is called for each chunk of HTML until
the end of the array is reached. The function takes two parameters: the parser
instance and the length of each HTML chunk. If parsing any chunk fails, it
reports the error via the `FAILED` macro.

### Finishing the Parsing

After processing all the chunks, the parsing is concluded with:

```c
status = lxb_html_parse_chunk_end(parser);
```

This function finalizes the parsing operation. Like the other stages, it checks
if the operation succeeded, and handles any errors accordingly.

### Serialization

Once the parsing is complete, the document's contents need to be serialized:

```c
status = lxb_html_serialize_pretty_tree_cb(lxb_dom_interface_node(document),
                                           LXB_HTML_SERIALIZE_OPT_UNDEF,
                                           0, serializer_callback, NULL);
```

This line serializes the parsed HTML tree into a human-readable format. The
`lxb_dom_interface_node(document)` retrieves the root node of the parsed
document for serialization. The use of the callback function allows for
customization in how the output is processed.

### Cleanup

Finally, resource management is handled to prevent memory leaks:

```c
lxb_html_document_destroy(document);
lxb_html_parser_destroy(parser);
```

These calls ensure that the allocated parser and document objects are properly
destroyed, freeing resources that are no longer needed.

## Conclusion

The example provided in
[lexbor/html/parse_chunk.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/parse_chunk.c)
is a straightforward illustration of how to parse HTML data incrementally with
the Lexbor library. By breaking the input into manageable chunks, the parser can
efficiently handle larger HTML documents and offers developers flexibility when
processing dynamic or streamed data. This method is particularly useful in web
environments where HTML content may not always be available as a single,
complete document.