# HTML Elements by Tag Name Example

This article will explain the code found in the source file [lexbor/html/elements_by_tag_name.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/elements_by_tag_name.c), which demonstrates how to find and print HTML elements by their tag names using the Lexbor DOM library.

## Code Overview

The purpose of this example is to parse a simple HTML string and retrieve all `<div>` elements from the parsed document. It achieves this by leveraging the Lexbor library's DOM capabilities to manage and manipulate the HTML document structure.

## Main Function

The entry point of the program is the `main` function, which begins by declaring several variables essential for the parsing process:

- `status` stores the success or failure status of various operations.
- `element` will point to the current HTML element being processed.
- `document` links to the HTML document that will be created from the parsed input.
- `collection` is intended to hold the collection of elements found in the document.

### Parsing HTML

The HTML string defined as:

```c
const lxb_char_t html[] = "<div a=b><span></div><div x=z></div>";
```

represents a simple HTML fragment which contains two `<div>` elements and a `<span>` element. The size of the HTML string is determined next:

```c
size_t html_size = sizeof(html) - 1;
```

This allows the program to recognize the length of the string without including the null terminator.

The `parse` function is then called to create a `document` from the HTML string:

```c
document = parse(html, html_size);
```

This function interprets the HTML and constructs a corresponding DOM structure. The parsing outcome is crucial; it will dictate the next steps in the program.

### Creating a DOM Collection

A collection is created to hold the resulting nodes:

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
```

This function attempts to allocate memory for a collection that can store up to 128 DOM elements. If memory allocation fails, the program exits with an error message:

```c
if (collection == NULL) {
    FAILED("Failed to create Collection object");
}
```

### Retrieving Elements by Tag Name

The critical operation of this example is retrieving `<div>` elements from the document:

```c
status = lxb_dom_elements_by_tag_name(lxb_dom_interface_element(document->body),
                                      collection, (const lxb_char_t *) "div", 3);
```

Here, `lxb_dom_elements_by_tag_name` takes three parameters:
1. The reference to the body of the document.
2. The collection object to store the found elements.
3. The string `"div"` along with its length, specifying which tags to search for.

If the call is unsuccessful, it again exits with an error message:

```c
if (status != LXB_STATUS_OK) {
    FAILED("Failed to get elements by name");
}
```

### Output the Found Elements

The program then prints the initial HTML string and displays a message indicating that it is about to list the found `<div>` elements:

```c
PRINT("HTML:");
PRINT("%s", (const char *) html);
PRINT("\nFind all 'div' elements by tag name 'div'.");
PRINT("Elements found:");
```

The elements collected are iterated over and serialized for display:

```c
for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
    element = lxb_dom_collection_element(collection, i);
    serialize_node(lxb_dom_interface_node(element));
}
```

This loop retrieves each element from the collection by index and uses the `serialize_node` function to output its representation.

### Cleanup

Finally, memory allocated for the collection and the document is released:

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

This ensures that there are no memory leaks after the program's execution is complete.

## Conclusion

This example serves as a practical demonstration of how to use the Lexbor library to parse HTML and find elements by tag name. By using functions from the library's API, the code effectively processes a document and manages collections of elements, showcasing the utility of the Lexbor framework in web development tasks.