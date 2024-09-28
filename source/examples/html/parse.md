# Parsing and Serializing HTML: Example

This article explains the purpose and functionality of a code example from the `lexbor` library, specifically located in the `lexbor/html/parse.c` file. The example demonstrates how to initialize an HTML parser, parse HTML strings into document objects, serialize those documents, and destroy the allocated resources properly. We will break down the code and discuss the important aspects and rationale behind each significant section.

## Key Code Sections

### Initialization

The first step is to initialize the HTML parser. This is done using the `lxb_html_parser_create` and `lxb_html_parser_init` functions. 

```c
parser = lxb_html_parser_create();
status = lxb_html_parser_init(parser);

if (status != LXB_STATUS_OK) {
    FAILED("Failed to create HTML parser");
}
```

Here, `lxb_html_parser_create` allocates memory for the parser, while `lxb_html_parser_init` initializes it. The status is checked to ensure the parser is created successfully.

### Parsing HTML Strings

Once the parser is initialized, the example proceeds to parse two HTML strings into document objects.

```c
doc_one = lxb_html_parse(parser, html_one, html_one_len);
if (doc_one == NULL) {
    FAILED("Failed to create Document object");
}

doc_two = lxb_html_parse(parser, html_two, html_two_len);
if (doc_two == NULL) {
    FAILED("Failed to create Document object");
}
```

The `lxb_html_parse` function takes the parser, an HTML string, and its length as parameters, and returns a document object. It is important to check if the document object is created successfully before proceeding.

### Destroying the Parser

After parsing, the parser is no longer needed and should be destroyed to free resources.

```c
lxb_html_parser_destroy(parser);
```

This is done using the `lxb_html_parser_destroy` function.

### Serialization

The parsed documents are then serialized to produce a human-readable representation of the HTML tree.

```c
status = lxb_html_serialize_pretty_tree_cb(lxb_dom_interface_node(doc_one),
                                           LXB_HTML_SERIALIZE_OPT_UNDEF,
                                           0, serializer_callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialization HTML tree");
}

printf("\nSecond Document:\n");

status = lxb_html_serialize_pretty_tree_cb(lxb_dom_interface_node(doc_two),
                                           LXB_HTML_SERIALIZE_OPT_UNDEF,
                                           0, serializer_callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialization HTML tree");
}
```

The `lxb_html_serialize_pretty_tree_cb` function is used to serialize the document object. It takes the root node of the document and a callback function (`serializer_callback`) to handle the serialization process. The status is checked to ensure the serialization is successful.

### Cleaning Up

Finally, the document objects are destroyed to free the allocated memory.

```c
lxb_html_document_destroy(doc_one);
lxb_html_document_destroy(doc_two);
```

This is done using the `lxb_html_document_destroy` function.

## Notes

- The `lxb_html_parser_create` and `lxb_html_parser_init` functions are essential for setting up the parser.
- Always check the return values of parser and document creation functions to ensure they are successful.
- The parser should be destroyed after parsing to free resources.
- Proper serialization of the document objects involves using a callback function to handle the output.
- Document objects must be destroyed to avoid memory leaks.

## Summary

This example from the `lexbor/html/parse.c` file showcases the process of initializing an HTML parser, parsing HTML strings, serializing the parsed documents, and managing memory by destroying the parser and document objects. These steps are crucial for efficient HTML parsing and manipulation when using the `lexbor` library. Understanding this example helps users to correctly implement and handle HTML parsing and serialization in their own applications, ensuring both functionality and performance.