# CSS Selectors Usage Example

This article explains an example program found in the file [lexbor/selectors/easy_way.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/selectors/easy_way.c), which demonstrates how to use the Lexbor library to parse HTML and match it against CSS selectors. The example involves creating an HTML document, defining CSS selectors, and then finding matching nodes in the document.

## Overview of the Code

The program begins with the inclusion of necessary headers from the Lexbor library, specifically for handling HTML documents and CSS selectors. The primary functionalities are encapsulated in multiple functions, including the `callback` function, which prints matched nodes, and the `find_callback` function, which keeps track of the count of found nodes.

### Function Definitions

- **callback**: This function acts as a callback for serializing HTML nodes. It takes a pointer to data representing the node's content and its length, printing the content to the standard output.

- **find_callback**: This callback function is invoked for each matching node found by the CSS selectors. It increments the count of matched nodes, prints the count, and calls the serialization callback to output the node’s content.

### Main Function Breakdown

1. **Initialization**: The `main` function begins by declaring variables for counting matches, managing the status of various operations, and holding references to the document, selectors, parser, and selector list.

2. **HTML and CSS Data**: The example defines a string of HTML containing a `div` with two `p` elements and a string of CSS selectors to match. Specifically, the selectors include a class selector (`.x`) and a compound selector that checks for a `p` element with an `id` of 'y'.

3. **Creating an HTML Document**: An HTML document object is created and initialized with the HTML string. The document must be parsed successfully; otherwise, the program exits with a failure status.

4. **CSS Parser Setup**: A CSS parser object is created and initialized, which is necessary for processing the selector strings.

5. **Selectors Creation**: A selectors object is initialized to handle the parsing of the CSS selectors. This involves calling `lxb_selectors_create` and then initializing it with `lxb_selectors_init`.

6. **Parsing Selectors**: The CSS selectors string is parsed, and a list of selectors is generated using `lxb_css_selectors_parse`. The status is checked to ensure that parsing was successful.

7. **Serialization of Selectors**: The program prints out the serialized selectors using `lxb_css_selector_serialize_list_chain`, which utilizes the previously defined `callback` function to output each selector.

8. **Finding Matching Nodes**: The program identifies the body of the HTML document and utilizes the `lxb_selectors_find` function to locate nodes that match the defined selectors. The `find_callback` function processes each matching node.

9. **Memory Management**: After processing, the program properly deallocates memory used for selectors, the CSS parser, and the HTML document to prevent memory leaks.

### Conclusion

This example demonstrates the effective use of the Lexbor library for manipulating and selecting elements within HTML documents based on CSS selectors. By understanding how to parse both HTML and CSS, and by using callback functions to manage matched nodes, developers can efficiently implement feature-rich web applications. The careful structure of the code ensures maintainability and readability, adhering to best practices in C programming.