# CSS Selectors Parsing and Node Finding Example

This example, found in the source file
[lexbor/selectors/normal_way.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/selectors/normal_way.c),
demonstrates how to use the `lexbor` library to parse CSS selectors and find HTML
nodes that match those selectors. The code provides a comprehensive workflow,
from creating an HTML document to parsing selectors and retrieving matching
nodes while handling memory management efficiently.

## Overview of Key Components

The main function serves as the central processing unit of the code,
orchestrating the various tasks. It initializes necessary structures, parses an
HTML string, sets up CSS selectors, and employs the `lexbor` library's
capabilities to find nodes in the document.

### HTML and CSS Data

The example uses the HTML string `"<div><p class='x z'> </p><p
id='y'>abc</p></div>"`, which contains two `<p>` elements, one with class
attributes `x` and `z`, and another with the ID `y`. This HTML will be parsed to
create a document object.

Two CSS selector strings are defined: `".x, div:has(p[id=Y i])"` and
`"p:blank"`. These selectors aim to demonstrate the capabilities of the library
to handle various matching criteria. 

### Document Creation and Parsing

The code begins by creating an HTML document using the function
`lxb_html_document_create()`. It then parses the HTML content with
`lxb_html_document_parse()`. If parsing fails (indicated by a non-OK status),
the function exits, ensuring that subsequent operations are performed on a valid
document.

```c
document = lxb_html_document_create();
status = lxb_html_document_parse(document, html, sizeof(html) / sizeof(lxb_char_t) - 1);
```

### Memory Management 

Proper memory management is crucial in C programming. The code allocates memory
for parsed structures using `lxb_css_memory_create()`, initializing it with a
specified size. This guarantees that the structures can be populated without
running into memory issues.

```c
memory = lxb_css_memory_create();
status = lxb_css_memory_init(memory, 128);
```

### CSS Parser and Selector Setup

A CSS parser is created with `lxb_css_parser_create()`, and its settings are
adjusted to work with the previously created memory. The CSS selectors are set
up with `lxb_css_selectors_create()` and initialized, ensuring that they can
efficiently handle subsequent parsing requests.

Important to note is the line where the parser is instructed not to create a new
selector object for each call, thereby enhancing performance during parsing
iterations:

```c
lxb_css_parser_selectors_set(parser, css_selectors);
```

### Selector Parsing and Serialization

The selectors defined earlier are parsed using `lxb_css_selectors_parse()`. The
resulting lists (`list_one` and `list_two`) contain the parsed representations
of the selectors. If parsing fails, the program exits gracefully.

After parsing, the example demonstrates HTML serialization through
`lxb_html_serialize_pretty_deep_cb()` and outputs the selectors using
`lxb_css_selector_serialize_list_chain()`, allowing for a visual check of the
parsed structures.

### Finding Nodes by Selectors

The example then proceeds to find HTML nodes using the parsed selectors. It
leverages the `lxb_selectors_find()` function, along with a callback function
`find_callback`, to process each matching node. This function simply counts the
nodes found and prints their representation.

```c
status = lxb_selectors_find(selectors, body, list_one, find_callback, &count);
```

### Cleanup and Memory Deallocation

Once all operations are completed, the code carefully deallocates all allocated
resources to prevent memory leaks. It uses the appropriate destroy functions for
each created object, adhering to good practices in C coding.

```c
(void) lxb_selectors_destroy(selectors, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_css_memory_destroy(memory, true);
```

## Conclusion

In summary, this example outlines a practical implementation of HTML and CSS
handling using the `lexbor` library. It emphasizes the importance of robust memory
management, selector parsing, and node finding functionalities, making it a
valuable reference for developers looking to understand or utilize `lexbor` in
their projects.