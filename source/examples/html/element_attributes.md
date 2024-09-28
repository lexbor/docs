# Handling Element Attributes with `lexbor`

This article explores the `lexbor/html/element_attributes.c` example, which demonstrates parsing an HTML document, manipulating DOM elements, and their attributes using the `lexbor` library. The example focuses on setting, getting, checking for existence, iterating over, changing, and finally removing attributes of a DOM element within a parsed HTML document.

## Key Code Sections

### Parsing the HTML Document

```c
static const lxb_char_t html[] = "<div id=my-best-id></div>";
size_t html_len = sizeof(html) - 1;

/* Parse */
document = parse(html, html_len);
```

The HTML document defined as a static string is parsed using the `parse` function that constructs an `lxb_html_document_t` object. This is the initial step, setting up the environment for further DOM manipulations.

### Creating and Using a Collection

```c
/* Create Collection for elements */
collection = lxb_dom_collection_make(&document->dom_document, 16);
if (collection == NULL) {
    FAILED("Failed to create collection");
}
```

A `lxb_dom_collection_t` is created to store elements found during searching. This is essential for working with multiple elements efficiently. The collection is initialized with a pre-defined capacity of 16 elements.

### Finding and Accessing Elements

```c
/* Get BODY element (root for search) */
body = lxb_html_document_body_element(document);
element = lxb_dom_interface_element(body);

/* Find DIV element */
status = lxb_dom_elements_by_tag_name(element, collection,
                                      (const lxb_char_t *) "div", 3);

if (status != LXB_STATUS_OK || lxb_dom_collection_length(collection) == 0) {
    FAILED("Failed to find DIV element");
}
```

Here, the `body` element serves as the root for the search. The `lxb_dom_elements_by_tag_name` function searches for all `div` tags and stores them in the collection. Error checks ensure that the `div` elements are found successfully.

### Setting and Appending Attributes

```c
attr = lxb_dom_element_set_attribute(element, name, name_size,
                                     (const lxb_char_t *) "oh God", 6);
if (attr == NULL) {
    FAILED("Failed to create and append new attribute");
}
```

A new attribute is appended to the `div` element using `lxb_dom_element_set_attribute`. The attribute name is "my-name" and its value is "oh God". The function creates the attribute if it doesn't already exist and appends it to the element.

### Checking Attribute Existence

```c
is_exist = lxb_dom_element_has_attribute(element, name, name_size);

if (is_exist) {
    PRINT("\nElement has attribute \"%s\": true", (const char *) name);
}
else {
    PRINT("\nElement has attribute \"%s\": false", (const char *) name);
}
```

The `lxb_dom_element_has_attribute` checks whether the given attribute exists on the element. The result is printed accordingly.

### Retrieving Attribute Value

```c
value = lxb_dom_element_get_attribute(element, name, name_size, &value_len);
if (value == NULL) {
    FAILED("Failed to get attribute value by qualified name");
}

PRINT("Get attribute value by qualified name \"%s\": %.*s",
      (const char *) name, (int) value_len, value);
```

`lxb_dom_element_get_attribute` retrieves the value of the specified attribute. If the attribute is found, its value and length are returned and printed. This section shows how to access the values of element attributes.

### Iterating Over Attributes

```c
/* Iterator */
PRINT("\nGet element attributes by iterator:");
attr = lxb_dom_element_first_attribute(element);

while (attr != NULL) {
    tmp = lxb_dom_attr_qualified_name(attr, &tmp_len);
    printf("Name: %s", tmp);

    tmp = lxb_dom_attr_value(attr, &tmp_len);
    if (tmp != NULL) {
        printf("; Value: %s\n", tmp);
    }
    else {
        printf("\n");
    }

    attr = lxb_dom_element_next_attribute(attr);
}
```

Using an iterator, this section retrieves and prints all attributes of the element. `lxb_dom_element_first_attribute` gets the first attribute, and `lxb_dom_element_next_attribute` progresses through the list.

### Changing Attribute Value

```c
attr = lxb_dom_element_attr_by_name(element, name, name_size);
status = lxb_dom_attr_set_value(attr, (const lxb_char_t *) "new value", 9);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to change attribute value");
}
```

Changing an attribute's value involves first retrieving the attribute using `lxb_dom_element_attr_by_name` and then setting the value with `lxb_dom_attr_set_value`. Error checking ensures that the operation is successful.

### Removing Attributes

```c
/* Remove new attribute by name */
lxb_dom_element_remove_attribute(element, name, name_size);
```

The final operation removes the specified attribute from the element using `lxb_dom_element_remove_attribute`. This demonstrates the library's capabilities for cleaning up or updating the DOM.

## Notes

- Proper error handling is crucial when manipulating the DOM to ensure robust and predictable behavior.
- Iterating over attributes can provide useful insights into the current state of an element's attributes, useful for debugging or further manipulation.
- Changing and removing attributes dynamically allows for flexible DOM updates.

## Summary

This example demonstrates how to create, manipulate, and manage element attributes using the `lexbor` library, covering parsing HTML, finding elements, setting, retrieving, iterating over, changing, and removing attributes. These operations form the basis for extensive DOM manipulations in web development and highlight the power and flexibility of `lexbor` for such tasks. Understanding these fundamentals is essential for effectively utilizing `lexbor` in complex web applications.