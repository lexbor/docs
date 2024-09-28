# HTML Element Creation and Traversal

In this example, sourced from the `lexbor/html/element_create.c` file, we will 
delve into creating and manipulating HTML elements using the `lexbor` library. 
This article provides a deep dive into the code, explaining how to dynamically 
create every standardized HTML element, insert them into the document tree and 
serialize the current structure. This example is pivotal for those seeking to 
comprehend the intricacies of DOM manipulation with lexbor.

## Key Code Sections

### Initial Document Parsing

First, we see the creation and initialization of an HTML document.

```c
document = parse((const lxb_char_t *) "", 0);
body = lxb_html_document_body_element(document);
```

The `parse` function initializes an empty HTML document. The subsequent 
call to `lxb_html_document_body_element` retrieves the body element of 
the document.

### Initial HTML Tree Serialization

To observe the initial state of the HTML document, the code serializes and 
prints the document.

```c
PRINT("Inital HTML Tree:");
serialize(lxb_dom_interface_node(document));
printf("\n");
```

Here, the `serialize` function outputs the current structure of the document 
tree, which is initially empty.

### Creating and Inserting HTML Elements

Next, the code iterates over all known HTML tag IDs and creates corresponding 
elements.

```c
for (tag_id = LXB_TAG_A; tag_id < LXB_TAG__LAST_ENTRY; tag_id++)
{
    tag_name = lxb_tag_name_by_id(tag_id, &tag_name_len);
    // Error handling omitted for brevity

    element = lxb_dom_document_create_element(&document->dom_document,
                                              tag_name, tag_name_len, NULL);
    // Error handling omitted for brevity

    if (lxb_html_tag_is_void(tag_id)) {
        // Handling void elements
    }
    else {
        text = lxb_dom_document_create_text_node(&document->dom_document,
                                                 tag_name, tag_name_len);
        // Error handling omitted for brevity

        lxb_dom_node_insert_child(lxb_dom_interface_node(element),
                                  lxb_dom_interface_node(text));
    }
    serialize_node(lxb_dom_interface_node(element));
    lxb_dom_node_insert_child(lxb_dom_interface_node(body),
                              lxb_dom_interface_node(element));
}
```

In this loop:

1. `lxb_tag_name_by_id` retrieves the tag name associated with `tag_id`.
2. `lxb_dom_document_create_element` creates an element node for the tag.
3. If the tag is not a void element (based on the specification), a text node 
   with the tag name is created and appended as a child to the element.
4. `serialize_node` outputs the newly created element.
5. Finally, the element is appended to the body of the document.

### Final HTML Tree Serialization

After all elements are created and inserted into the document, the resulting 
HTML structure is serialized and printed.

```c
PRINT("\nTree after create elements:");
serialize(lxb_dom_interface_node(document));
```

This section provides a clear view of how the document looks after all 
operations.

### Document Cleanup

Proper resource management is crucial. The example concludes by destroying 
the document to free up memory.

```c
lxb_html_document_destroy(document);
```

## Notes

- **Document Initialization**: Creating an empty document and retrieving the body 
  element is fundamental for subsequent operations.
- **Element Creation**: Iterating through tag IDs systematically to create all 
  HTML elements showcases lexbor's comprehensive coverage of HTML tags.
- **Void Elements Handling**: Differentiation between void and non-void elements 
  is essential to comply with HTML specifications.
- **Serialization**: The serialization function is valuable for debugging and 
  inspecting the document structure.

## Summary

This example demonstrates the power and flexibility of the `lexbor` library for 
HTML document manipulation. It covers essential operations such as parsing, 
element creation, and serialization, and highlights best practices like resource 
management and adherence to HTML specifications. Understanding this example is 
crucial for anyone looking to effectively use lexbor for DOM manipulation tasks.