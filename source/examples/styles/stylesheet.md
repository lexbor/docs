# Parsing and Applying CSS Stylesheet in HTML: Example

This article explains the intricacies of the `lexbor` library through an example
found in `lexbor/styles/stylesheet.c`. This particular example demonstrates
how to parse an HTML document, attach a CSS stylesheet to it, and then extract
and serialize specific CSS properties applied to an element. The article will
delve into key sections of the code, breaking down the usage and intent of
various `lexbor` functions and structures.

## Key Code Sections

### Creating and Initializing the HTML Document

The code starts by creating an HTML document and initializing the CSS module
for that document:

```c
/* Create Document. */
doc = lxb_html_document_create();
if (doc == NULL) {
    FAILED("Failed to create HTML Document");
}

/* Init CSS. */
status = lxb_html_document_css_init(doc);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to CSS initialization");
}
```

Here, `lxb_html_document_create()` creates a new HTML document object, and
`lxb_html_document_css_init(doc)` initializes the CSS subsystem for that
document. This step is essential to ensure that CSS can be parsed and managed
in the context of the document.

### Parsing a CSS Stylesheet

Next, the code initializes a CSS parser and uses it to parse a stylesheet string:

```c
/* CSS. */
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization CSS parser");
}

sst = lxb_css_stylesheet_parse(parser, css.data, css.length);
if (sst == NULL) {
    FAILED("Failed to parse CSS StyleSheet");
}
```

`lxb_css_parser_create()` and `lxb_css_parser_init(parser, NULL)` are used to
create and initialize a CSS parser. `lxb_css_stylesheet_parse(parser, css.data,
css.length)` then parses the CSS stylesheet defined by `css` and produces a
stylesheet object (`sst`). This object will later be attached to the HTML
document.

### Parsing the HTML Document and Attaching Stylesheet

The code then parses a simple HTML string and attaches the previously parsed
stylesheet to the HTML document:

```c
/* HTML. */
status = lxb_html_document_parse(doc, html.data, html.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}

/* Attach CSS Stylesheet to HTML Document. */
status = lxb_html_document_stylesheet_attach(doc, sst);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to attach CSS stylesheet");
}
```

Here, `lxb_html_document_parse(doc, html.data, html.length)` parses the HTML
string and populates the document structure. `lxb_html_document_stylesheet_attach(doc, sst)`
attaches the CSS stylesheet to the document, effectively applying the styles to
the elements within the HTML.

### Extracting Specific CSS Properties

Once the HTML is parsed and styles are applied, the code looks for a `<div>`
element and extracts its `width` and `height` properties:

```c
/* Get <DIV ...>. */
memset(&collection, 0, sizeof(lxb_dom_collection_t));
status = lxb_dom_node_by_tag_name(lxb_dom_interface_node(doc), &collection, str_div.data, str_div.length);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get element by name");
}

div = lxb_dom_collection_element(&collection, 0);
if (div == NULL) {
    FAILED("Failed to get element by name");
}

/* Get style (declaration) from div element. */
width = lxb_html_element_style_by_name(lxb_html_interface_element(div), str_width.data, str_width.length);
if (width == NULL) {
    FAILED("Failed to get style by name");
}

height = lxb_html_element_style_by_id(lxb_html_interface_element(div), LXB_CSS_PROPERTY_HEIGHT);
if (height == NULL) {
    FAILED("Failed to get style by id");
}
```

In this segment, `lxb_dom_node_by_tag_name()` is used to locate `<div>`
elements, and `lxb_dom_collection_element(&collection, 0)` retrieves the first
one from the collection. The CSS properties `width` and `height` are then
extracted using `lxb_html_element_style_by_name()` and `lxb_html_element_style_by_id()`,
respectively.

### Serializing CSS Properties

Finally, the code serializes the extracted CSS properties and prints them:

```c
status = lxb_css_rule_declaration_serialize(width, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize width declaration");
}

status = lxb_css_rule_declaration_serialize(height, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize height declaration");
}
```

`lxb_css_rule_declaration_serialize()` takes a CSS property and a callback
function to handle the serialized output. In this case, `callback()` simply
prints the serialized property to standard output.

## Notes

- The example demonstrates the comprehensive use of `lexbor` for CSS parsing,
  HTML parsing, and applying styles.
- Proper error handling and memory management are crucial for robust code,
  as illustrated by frequent checks on the return values of `lexbor` functions.

## Summary

This example shows how to use the `lexbor` library for an advanced task:
parsing an HTML document, attaching a CSS stylesheet, and extracting and
serializing specific CSS properties. By following this example, `lexbor` users
can learn how to integrate HTML and CSS parsing into their projects, enabling
richer, style-aware document processing.