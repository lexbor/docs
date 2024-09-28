# CSS Style Walking Example

This article explains the functionality and structure of the code found in [lexbor/styles/walk.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/styles/walk.c). The example focuses on parsing an HTML document, attaching CSS styles to an element, and traversing the applied styles. The primary goal of this example is to demonstrate how to manipulate the Document Object Model (DOM) and apply CSS styling in the Lexbor library.

## Overview of the Code

The provided code is organized into several key sections. Each section serves a significant purpose within the program, which includes parsing HTML, creating a CSS parser, and navigating through the styles associated with specific HTML elements.

### Include Directives and Function Prototypes

The code begins by including essential header files from the Lexbor library, specifically for HTML and CSS functionalities. It defines two primary callback functions:

1. **callback**: This function is executed to print serialized CSS data.
2. **walk_cb**: This function is intended to be called for each CSS style declaration when walking through the styles applied to an HTML element.

### Main Functionality

The `main` function encompasses the workflow of the program, starting with the initialization of the HTML document and CSS objects. Here's a detailed breakdown of its sections:

1. **Document Creation**: 
   The code allocates memory for a new HTML document using `lxb_html_document_create()`. If it fails, the program exits with an error.

2. **CSS Initialization**: 
   The HTML document initiates its CSS functionality through `lxb_html_document_css_init()`. Similar to document creation, any failure leads to program termination.

3. **HTML Parsing**: 
   The program parses a static HTML string containing a `<div>` element using `lxb_html_document_parse()`. Again, error handling ensures that the program only proceeds if parsing is successful.

4. **CSS Parsing**: 
   A CSS parser is created and initialized. The program then attempts to parse a set of CSS selectors and styles. Successful parsing leads to the association of the stylesheet with the HTML document.

5. **DOM Node Selection**: 
   The program searches for HTML elements using the CSS class name through `lxb_dom_node_by_class_name()`. If no elements are found or if an error occurs, the program appropriately exits.

6. **Style Walking**: 
   The function `lxb_html_element_style_walk()` is called to iterate over the styles applied to the `<div>` element selected earlier. The `walk_cb` function is employed as a callback, allowing printing of style information.

### Walking Through Styles

In the `walk_cb` callback function, several actions take place:

- The CSS rule declaration is serialized and printed using `lxb_css_rule_declaration_serialize()`.
- The name and value of each property in the style declaration are serialized and printed through `lxb_css_property_serialize_name()` and `lxb_css_property_serialize()`. This provides complete visibility into the CSS properties applied to the `<div>`.
- The specificity of each CSS rule, including various parameters that determine the importance and origin of the styles, is printed.

### Resource Cleanup

Finally, the program ensures that all allocated resources are correctly destroyed using respective cleanup functions for DOM collections, stylesheets, parsers, and the HTML document itself. This step is crucial for preventing memory leaks and ensuring efficient resource management.

## Conclusion

This code example highlights the integration of HTML parsing and CSS styling using the Lexbor library. By utilizing the provided functions and callback methods, developers can effectively manipulate and inspect styles associated with HTML elements. The careful arrangement of initialization, parsing, walking through styles, and resource cleanup demonstrates best practices in managing dynamic web content.