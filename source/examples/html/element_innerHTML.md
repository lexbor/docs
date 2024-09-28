# Setting innerHTML Example

This article will explain the `innerHTML` manipulation in the context of the
`lexbor` HTML parser, as illustrated in the source file
[lexbor/html/element_innerHTML.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/element_innerHTML.c).
This example demonstrates how to parse HTML content, modify an element's inner
HTML, and serialize the result.

## Code Overview

The code starts with the inclusion of the necessary header file, `base.h`, which
likely contains the essential definitions and functions for the `lexbor` library.
The `main` function serves as the entry point for the execution of this program.

### HTML Parsing

The program begins by defining a simple HTML string containing a `<div>` with a
nested `<span>` element. The length of this string is calculated using
`sizeof(html) - 1` to exclude the null terminator from the count. The predefined
HTML string is as follows:

```c
static const lxb_char_t html[] = "<div><span>blah-blah-blah</div>";
```

Next, the `parse` function is called with the HTML string and its length. This
function processes the HTML and generates a document object model (DOM),
representing the structure of the HTML document in memory.

### Printing the Parsed HTML

The program checks the output of the `parse` function and prints the original
HTML and the resulting DOM tree. This is accomplished with the `PRINT` macro,
which appears to be a utility for outputting messages. The serialized DOM is
obtained using the `serialize` function on the document's root node:

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
PRINT("\nTree after parse:");
serialize(lxb_dom_interface_node(document));
```

### Inner HTML Modification

Subsequently, a second HTML string is defined, which will be set as the inner
HTML of the body element. This inner HTML is specified as follows:

```c
static const lxb_char_t inner[] = "<ul><li>1<li>2<li>3</ul>";
```

The program retrieves the body element of the document using
`lxb_html_document_body_element(document)`. The inner HTML of the body is then
set using the `lxb_html_element_inner_html_set` function, which takes the body
element and the inner HTML string along with its length as arguments:

```c
element = lxb_html_element_inner_html_set(lxb_html_interface_element(body),
                                          inner, inner_len);
```

If the `element` is `NULL`, indicating a failure in setting the inner HTML, a
failure message is printed through the `FAILED` macro.

### Final Output

After setting the inner HTML, the program serializes the modified DOM tree and
prints the result. This demonstrates the changes made by the inner HTML
operation. Finally, the code cleans up by destroying the document to release
resources allocated for the DOM.

```c
PRINT("\nTree after innerHTML set:");
serialize(lxb_dom_interface_node(document));
lxb_html_document_destroy(document);
```

## Conclusion

The example provided illustrates how to parse an HTML string, modify an
element's inner HTML content, and serialize the resulting DOM structure using
`lexbor`'s capabilities. This demonstrates an essential functionality often used
in web development for DOM manipulation, showcasing the ease of use of the
`lexbor` library for such tasks.