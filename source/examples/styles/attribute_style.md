# CSS Style Attribute Example

This article provides an in-depth explanation of a code example found in the [lexbor/styles/attribute_style.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/styles/attribute_style.c) file. The purpose of this code is to demonstrate how to create an HTML document, parse a specific HTML element, retrieve its CSS style properties, and then serialize those properties for output. 

## Code Breakdown

### Header Files and Function Definition

The code begins with necessary includes, specifically `base.h`, along with lexbor's HTML and CSS header files. This setup ensures that all necessary functions related to HTML document handling and CSS processing are available. 

The `callback` function serves as a utility to print CSS property declarations. It takes a character pointer `data`, the length of data `len`, and a context pointer `ctx`. It uses `printf` to output the string, formatting it based on the provided length. This function is fundamental for logging purposes throughout the serialization process.

### Main Function

The `main` function is where the primary logic occurs:

1. **Document Creation**: 
   The first step is to create a new HTML document using `lxb_html_document_create()`. If the document fails to create, it reports an error and halts execution using the `FAILED` macro.

2. **CSS Initialization**: 
   Following document creation, `lxb_html_document_css_init(doc)` initializes the CSS environment for the document. Again, a failure results in termination.

3. **HTML Parsing**: 
   The code employs `lxb_html_document_parse(doc, html.data, html.length)` to parse a static HTML string that contains a `<div>` with CSS inline styles. The inline styles include various widths and heights in different units. This parsing step builds the DOM structure of the HTML.

4. **Element Retrieval**: 
   A `lxb_dom_collection_t` is initialized to hold results. The function `lxb_dom_node_by_tag_name()` retrieves elements by their tag name, specifically targeting the `<div>` tag. If retrieval fails, execution is halted.

5. **CSS Property Access**: 
   The example seeks to extract specific style properties from the `<div>`. It retrieves the `width` property by name and the `height` property by its corresponding ID using `lxb_html_element_style_by_name` and `lxb_html_element_style_by_id`, respectively. Errors during this stage lead to failure messages.

### Serialization and Output

After acquiring the width and height styles, the example moves to serialize these properties. The `lxb_css_rule_declaration_serialize()` function is called twice, once for each property, passing the `callback` function to handle output. The results are printed to the console, showcasing the values for both properties.

### Cleanup

The `lxb_dom_collection_destroy()` function cleans up the DOM collection used to store the `<div>` elements, while `lxb_html_document_destroy(doc)` releases the memory allocated for the document. This cleanup ensures no memory leaks occur during program execution.

## Conclusion

This code example illustrates how to manipulate and retrieve CSS properties from an HTML element using the lexbor library. It covers creating an HTML document, parsing content, accessing specific elements, and outputting style properties, providing a comprehensive look at handling HTML and CSS in C with lexbor. The example highlights the importance of proper resource management and error reporting within such operations, which is essential for building robust applications.