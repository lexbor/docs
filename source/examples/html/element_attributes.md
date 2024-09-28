# Element Attributes Example

This article explains the implementation found in
[lexbor/html/element_attributes.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/element_attributes.c),
which demonstrates how to manipulate HTML element attributes using the Lexbor
library. The example outlines parsing an HTML snippet, finding an element, and
performing various operations involving element attributes, such as adding,
checking existence, retrieving, modifying, and removing attributes from an
element.

## Code Overview

The code begins by including necessary headers and defining the main function,
which initializes variables for handling the document and its components. The
use of `lxb_status_t` for tracking the status of operations is essential
throughout the code.

### HTML Parsing

The code defines a static HTML string:

```c
static const lxb_char_t html[] = "<div id=my-best-id></div>";
```

A document is parsed from this HTML string with:

```c
document = parse(html, html_len);
```

After parsing, the code outputs the structure of the DOM tree to the console
using a `serialize` function, allowing developers to visualize the parsed HTML
elements.

### Collection Creation

Next, a DOM collection is created to hold references to found elements:

```c
collection = lxb_dom_collection_make(&document->dom_document, 16);
```

If the collection creation fails, an error message is printed, and the program
exits.

### Searching for Elements

To find the `<div>` element in the DOM, the code first obtains the body element
and then calls:

```c
status = lxb_dom_elements_by_tag_name(element, collection, (const lxb_char_t *) "div", 3);
```

This line searches for all `<div>` elements under the specified parent element.
A check for successful status and the collection's length follows, ensuring that
at least one `<div>` is found.

### Adding an Attribute

Once the element is identified, a new attribute is added using:

```c
attr = lxb_dom_element_set_attribute(element, name, name_size, (const lxb_char_t *) "oh God", 6);
```

In this case, the attribute named "my-name" is appended with a value of "oh
God." If the attribute creation fails, an error message is displayed.

### Checking Attribute Existence

The program checks if the newly added attribute exists:

```c
is_exist = lxb_dom_element_has_attribute(element, name, name_size);
```

A printed message confirms whether the attribute is present or not based on the
check.

### Retrieving Attribute Values

The next operation retrieves the value of the specified attribute:

```c
value = lxb_dom_element_get_attribute(element, name, name_size, &value_len);
```

If successful, it prints the value associated with the "my-name" attribute.

### Iterating Through Attributes

The code then demonstrates how to iterate through all attributes of the element:

```c
attr = lxb_dom_element_first_attribute(element);
```

This iterates through attributes using a `while` loop, printing each attribute's
name and value until there are no more attributes in the collection.

### Modifying an Attribute Value

To change the value of an existing attribute, the code retrieves the attribute
by name:

```c
attr = lxb_dom_element_attr_by_name(element, name, name_size);
```

Then, it updates the value to "new value" using:

```c
status = lxb_dom_attr_set_value(attr, (const lxb_char_t *) "new value", 9);
```

### Removing an Attribute

Finally, the example concludes with the removal of the newly added attribute:

```c
lxb_dom_element_remove_attribute(element, name, name_size);
```

This operation is followed by a serialized output of the DOM tree again,
allowing the developer to observe changes.

### Cleanup

The code ensures proper resource management by destroying the collection and the
document at the end of the main function to prevent memory leaks:

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

## Conclusion

The `element_attributes.c` example illustrates fundamental operations in DOM
manipulation provided by the Lexbor library. The code efficiently demonstrates
how to parse HTML, locate and manipulate elements, manage attributes, and ensure
appropriate cleanup of resources, making it a valuable reference for web
developers working with the Lexbor framework.