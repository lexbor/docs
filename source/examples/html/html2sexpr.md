# HTML to S-Expression Converter Example

This article provides an overview of a code example found in the file `lexbor/html/html2sexpr.c`. The program is designed to convert an HTML tag tree into an S-expression string and output it to standard output. The program utilizes the Lexbor library to handle parsing and manipulating HTML documents.

## Overview

The program first checks if the correct number of command-line arguments is provided. It expects one argument: the path to an HTML file. It reads the contents of this file and initializes an HTML document object using Lexbor's API. After parsing the HTML, the program invokes a tree-walking function to serialize the HTML structure into an S-expression format. The serialized output is then printed to the console.

## Major Code Sections

### Argument Handling and File Reading

The `main` function begins with argument validation. It ensures that exactly one argument is received; otherwise, it calls the `usage` function, which prints the program's usage instructions to standard error.

```c
if (argc != 2) {
    usage();
    FAILED("Invalid number of arguments");
}
```

Upon validation, the program proceeds to read the HTML file using the `lexbor_fs_file_easy_read` function, which simplifies file reading:

```c
html = lexbor_fs_file_easy_read((const lxb_char_t *) argv[1], &html_len);
```

If file reading fails, it reports an error and resizes relevant resources.

### HTML Document Initialization and Parsing

Next, the code creates an HTML document object with `lxb_html_document_create`. If this allocation fails, it destroys any previously allocated document and frees the memory associated with the HTML content:

```c
document = lxb_html_document_create();
```

After successfully creating the document, the program parses the HTML content:

```c
status = lxb_html_document_parse(document, html, html_len);
```

This step processes the HTML string and builds a structured representation of the document.

### Traversing the DOM and Serializing to S-Expression

The `tree_walker` function is the core of the serialization process. It traverses the DOM tree recursively, converting each node into an S-expression format. 

It begins by checking the type of each node. For elements, it calls the serialization callback `cb` to append the opening parenthesis, the node's name, and any attributes:

```c
if (node->type == LXB_DOM_NODE_TYPE_ELEMENT) {
    status = cb((const lxb_char_t *) "(", 1, ctx);
    ...
    // Invokes the attributes function
    status = attributes(node, cb, ctx);
```

The `attributes` function iterates through each node's attributes and formats them as `(attribute_name 'attribute_value)` pairs, again using the callback to transmit this information.

### Handling Template Nodes

The `tree_walker` function includes logic to handle nodes of type `LXB_TAG_TEMPLATE`. If a node is a template and contains child nodes, it recursively calls `tree_walker` on them, ensuring that the contents of the template are also serialized:

```c
if (node->local_name == LXB_TAG_TEMPLATE) {
    ...
    if (temp->content->node.first_child != NULL) {
        status = tree_walker(&temp->content->node, cb, ctx);
    }
}
```

### Cleanup and Exit Status

After serialization is complete, the `main` function cleans up by destroying the document and freeing allocated memory. The program concludes by returning an appropriate exit status based on whether the operations succeeded or failed:

```c
lxb_html_document_destroy(document);
lexbor_free(html);
return EXIT_SUCCESS;
```

In the case of failure at any point, the program proceeds to the `failed` label, ensuring resources are released before terminating.

## Conclusion

This example demonstrates a straightforward implementation of converting an HTML document structure into S-expressions using the Lexbor library. The program is structured to handle input validation, document parsing, tree traversal, and serialization efficiently while providing clear feedback in the case of errors. It showcases the use of Lexbor's DOM manipulation capabilities and highlights how to build a recursive tree-walking algorithm for tree serialization.