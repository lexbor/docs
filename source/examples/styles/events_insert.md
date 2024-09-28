# Events Insert Example

This article explains the C code found in
[lexbor/styles/events_insert.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/styles/events_insert.c),
which demonstrates the process of manipulating HTML documents and applying CSS
styles using the `lexbor` library. The code operates on a simple HTML structure
and applies specific styles based on a CSS stylesheet.

## Overview

The provided code initializes an HTML document representation, parses a
predefined HTML string, applies a CSS stylesheet, and manipulates the DOM to
insert a new HTML element. Here's a breakdown of the major sections of the code.

## Code Breakdown

### Includes and Definitions

The code begins with the inclusion of necessary header files from the `lexbor`
library, which are essential for HTML, CSS, and selector functionalities:

```c
#include <lexbor/html/html.h>
#include <lexbor/css/css.h>
#include <lexbor/selectors/selectors.h>
```

These headers allow access to functions and data structures needed to create and
manipulate HTML and CSS documents.

### Callback Function

A callback function named `callback` is implemented to handle data output when
invoked. This function prints data received from serialized output processes:

```c
lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx) {
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

Its purpose is to print formatted strings, assisting in visual output of the
document processes.

### Main Function

The `main` function encapsulates the program logic. It starts by defining
various variables and static data for HTML and CSS. 

```c
static const lexbor_str_t html = lexbor_str("<div class=father>...</div>");
static const lexbor_str_t slctrs = lexbor_str("div.father {...}");
```

Here, `html` contains a `<div>` with class "father" and some child elements,
while `slctrs` defines CSS rules for styling the div and its child paragraphs.

### Document Creation and Parsing

An HTML document is created using:

```c
document = lxb_html_document_create();
```

The document is then parsed with the defined HTML string:

```c
status = lxb_html_document_parse(document, html.data, html.length);
```

If any operation fails, the program exits to ensure that no subsequent
operations are performed on an invalid document structure.

### CSS Initialization and Parsing

Next, the code initializes the CSS subsystem of the document:

```c
status = lxb_html_document_css_init(document);
```

After this initialization, a CSS parser is created and initialized. The CSS
stylesheet is parsed and attached to the HTML document:

```c
sst = lxb_css_stylesheet_parse(parser, slctrs.data, slctrs.length);
status = lxb_html_document_stylesheet_attach(document, sst);
```

At this stage, all elements in the document receive styles defined in the
stylesheet.

### Element Creation and Attribute Setting

The code then seeks to manipulate the DOM by creating a new paragraph element
(`<p>`). This process involves setting attributes that apply styles from the
stylesheet:

```c
np = lxb_html_document_create_element(document, p_str.data, p_str.length, NULL);
attr = lxb_dom_element_set_attribute(lxb_dom_interface_element(np), class_str.data, class_str.length, best_str.data, best_str.length);
```

Here, the element is given a class of "best" for styling purposes, followed by
another attribute for inline styling.

### Inserting the New Element

Once the new element is fully prepared with the appropriate attributes, it is
appended to the "father" div:

```c
lxb_html_element_insert_child(div, np);
```

This action makes it part of the document's tree structure, and consequently, it
inherits styling based on CSS rules.

### Final Serialization and Resource Cleanup

The program serializes the new element and produces output that reflects the
changes made:

```c
status = lxb_html_serialize_cb(lxb_dom_interface_node(np), callback, NULL);
```

Finally, all allocated resources are cleaned up to prevent memory leaks by
destroying collections, stylesheets, and the document itself.

## Conclusion

The code in
[lexbor/styles/events_insert.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/styles/events_insert.c)
illustrates an effective use of the `lexbor` library to manipulate HTML and apply
CSS. By parsing, creating elements, setting attributes, and attaching styles, it
provides a clear example of dynamic document editing and processing. This
showcases both the capabilities and convenience of the `lexbor` framework in
handling web technologies programmatically.