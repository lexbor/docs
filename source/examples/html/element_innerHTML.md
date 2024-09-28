# Setting `innerHTML` Property in Lexbor

This example in the file `lexbor/html/element_innerHTML.c` demonstrates how to use the `lexbor` library to parse an HTML document, set the `innerHTML` of a body element, and serialize the resulting DOM tree. The intent of this code is to highlight key operations in manipulating the DOM using `lexbor`, such as document parsing, element selection, and updating the DOM tree.

## Key Code Sections

### Parsing HTML Document

First, we start by parsing the initial HTML document. The `parse` function reads the HTML string and constructs the corresponding DOM tree.

```c
static const lxb_char_t html[] = "<div><span>blah-blah-blah</div>";
size_t html_len = sizeof(html) - 1;

/* Parse */
document = parse(html, html_len);
```

Here, `html` contains our initial HTML code. `html_len` determines the length of this string (excluding the null terminator). Then, the `parse` function returns a `document` representing our HTML document.

### Printing the Parsed Document

Next, the parsed HTML document is printed for verification.

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
PRINT("\nTree after parse:");
serialize(lxb_dom_interface_node(document));
```

This section outputs the original HTML string and the serialized DOM tree after parsing. The `serialize` function converts the DOM tree back to a string and prints it for inspection.

### Obtaining the `body` Element

After parsing, we obtain the `body` element from the document for further manipulation.

```c
/* Get BODY element */
body = lxb_html_document_body_element(document);
```

This retrieves the `body` element of the parsed document, which is required to set its `innerHTML`.

### Setting Inner HTML

We then set the `innerHTML` of the `body` element to a new HTML string. 

```c
static const lxb_char_t inner[] = "<ul><li>1<li>2<li>3</ul>";
size_t inner_len = sizeof(inner) - 1;

element = lxb_html_element_inner_html_set(lxb_html_interface_element(body),
                                          inner, inner_len);
if (element == NULL) {
    FAILED("Failed to parse innerHTML");
}
```

Here, `inner` contains the new HTML to be set as the `innerHTML` of the `body` element. `inner_len` gives the length of this string. The `lxb_html_element_inner_html_set` function updates the `innerHTML` of the targeted element. An error is reported if the function fails.

### Printing the Updated Document

Finally, the modified DOM tree is serialized and printed.

```c
PRINT("\nTree after innerHTML set:");
serialize(lxb_dom_interface_node(document));
```

This helps verify that the new `innerHTML` has been correctly applied to the `body` element.

### Cleaning Up

The last step is to clean up and free the allocated memory for the document.

```c
/* Destroy all */
lxb_html_document_destroy(document);
```

This ensures that all resources used by the document are properly released.

## Notes

- The `parse` function is expected to correctly handle the input HTML and generate a DOM tree.
- The function `lxb_html_element_inner_html_set` is used to set the `innerHTML` of an element and returns the modified element or `NULL` if an error occurs.
- Using `serialize` to print the DOM tree before and after modification is a good practice to verify changes made to the DOM.

## Summary

This example demonstrates the essential steps for manipulating an HTML document using the `lexbor` library: parsing the document, selecting elements, updating the `innerHTML`, and serializing the DOM tree. By following this process, developers can effectively manage the DOM structure of HTML documents using `lexbor`.