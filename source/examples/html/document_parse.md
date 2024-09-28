# HTML Document Parsing Example

This article explains an example of parsing an HTML document using the Lexbor
library. The purpose of this example, located in the source file
[lexbor/html/document_parse.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/document_parse.c),
is to illustrate the steps necessary to create an HTML document, parse a string
of HTML, and serialize the resulting DOM tree.

## Example Overview

The example demonstrates the following key steps:

1. **Creating the HTML Document**: Initializing a new HTML document.
2. **Parsing the HTML**: Taking an HTML string and processing it to generate a
   DOM tree.
3. **Outputting the Results**: Printing the original HTML and the resulting DOM
   structure.
4. **Cleaning Up**: Destroying the document to free allocated resources.

## Code Explanation

### Main Function

The program starts in the `main` function, where it declares a variable for the
document status and a pointer to the HTML document.

```c
lxb_status_t status;
lxb_html_document_t *document;
```

### Defining HTML Content

A static character array contains the HTML to be parsed. The length of this HTML
string is also calculated.

```c
static const lxb_char_t html[] = "<div><p>blah-blah-blah</div>";
size_t html_len = sizeof(html) - 1;
```

### Document Initialization

The next segment involves initializing a new HTML document using the
`lxb_html_document_create` function. This function allocates necessary memory
and sets up internal structures to hold the document data.

```c
document = lxb_html_document_create();
if (document == NULL) {
    FAILED("Failed to create HTML Document");
}
```

If the document creation fails, an error message is printed, allowing for
debugging.

### HTML Parsing

Once the document is created, the program parses the HTML content. The
`lxb_html_document_parse` function is responsible for parsing the input HTML
string. 

```c
status = lxb_html_document_parse(document, html, html_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```

If the status indicates a failure, an appropriate message is shown. This
rigorous checking ensures that errors during parsing do not go unnoticed.

### Output the Results

After successfully parsing the HTML, the program prints the original HTML string
and serializes the resulting DOM tree. The `PRINT` macro is used for outputting
the HTML content.

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
```

It then calls a serialization function to visualize the structure of the parsed
HTML document:

```c
PRINT("\nHTML Tree:");
serialize(lxb_dom_interface_node(document));
```

This step helps developers understand how the HTML input is translated into a
DOM tree structure, which is crucial for many web development tasks.

### Document Cleanup

Finally, the program cleans up by destroying the HTML document to avoid memory
leaks. This is done using the `lxb_html_document_destroy` function:

```c
lxb_html_document_destroy(document);
```

Ensuring proper resource management is important in C programming, as it helps
maintain system performance and stability.

## Conclusion

The example provided in
[lexbor/html/document_parse.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/document_parse.c)
serves as a clear demonstration of how to create, parse, and handle an HTML
document using Lexbor. Through careful initialization, parsing, result
outputting, and cleanup, this code illustrates best practices for managing HTML
documents in a C environment.