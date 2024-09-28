# CSS Selectors and HTML Node Selection Example

This article discusses the functionality of the `unique_nodes.c` source file,
which implements a basic example of parsing HTML and CSS selectors using the
lexbor library. The example illustrates how to create an HTML document, parse
CSS selectors, and find nodes within the document that match those selectors.

## Key Components

### HTML and CSS Data

At the beginning of the main function, HTML and CSS data are defined. The HTML
consists of a `<div>` containing two `<p>` elements, while the CSS contains
several selectors, including class selectors, id selectors, and pseudo-class
selectors. This data is crucial as it lays the groundwork for the subsequent
parsing and node selection processes.

### Creating an HTML Document

The code then creates an HTML document using `lxb_html_document_create()` and
populates it with the previously defined HTML data. The
`lxb_html_document_parse()` function is called to parse the HTML data into a
structured format. If parsing fails, the program exits with a failure status.
This step transforms the provided HTML string into a DOM (Document Object Model)
representation that can be interacted with programmatically.

### Creating a CSS Parser

Following the creation of the HTML document, a CSS parser is instantiated with
`lxb_css_parser_create()`. This is complemented by an initialization call to
`lxb_css_parser_init()`. The parser is necessary for interpreting the CSS
selectors provided in the string format. The proper functioning of the parsing
depends on successful initialization, and any failure at this stage leads to an
exit.

### CSS Selector Processing

A CSS selector object is created using `lxb_css_selectors_create()`, and
similarly initialized to prepare for parsing operations. It is important to note
that the program avoids creating new selector objects each time the parser is
called by setting the CSS selectors on the parser with
`lxb_css_parser_selectors_set()`. This optimization ensures efficient memory
usage and performance.

### Parsing the Selectors

The CSS selectors are parsed using `lxb_css_selectors_parse()`, which generates
a list of selectors ready for matching with the document's nodes. If parsing
fails, the program exits. This list is critical for the next steps, allowing the
program to identify nodes that match the defined selectors.

### Serializing HTML and Selectors

The program outputs the serialized format of the HTML document using
`lxb_html_serialize_pretty_deep_cb()`, which calls a callback function to print
each node. This is useful for visual verification of the document structure.
Similarly, the selectors are serialized with
`lxb_css_selector_serialize_list_chain()`, enabling the user to see which
selectors have been parsed and are ready for matching.

### Finding HTML Nodes

The core functionality of this example is encapsulated in the
`lxb_selectors_find()` function, which takes the selectors and attempts to match
them against the nodes in the document's body. A callback function,
`find_callback`, is provided to handle each found node, incrementing a count and
processing each matched node individually. If any part of this process fails,
the program suitably returns an error status.

### Cleanup

Finally, the program ensures that all allocated resources are correctly disposed
of. Various destroy functions are called for the selectors, CSS parser, and the
HTML document to prevent memory leaks. This step is essential in any robust
application to maintain system performance and reliability.

## Conclusion

The `unique_nodes.c` example illustrates a practical application of the lexbor
library to handle HTML documents and CSS selectors. By showcasing the entire
lifecycle from parsing HTML to finding nodes based on CSS selectors, this
example serves as an informative foundation for developers looking to work with
document structures and styles in C using the lexbor library. The implemented
logic emphasizes efficiency and clarity, ensuring that the handling of selectors
and nodes is both effective and straightforward.