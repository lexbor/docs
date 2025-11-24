# Converting HTML Tag Tree to S-Expressions

This article provides an in-depth explanation of the code from the file [lexbor/html/html2sexpr.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/html2sexpr.c). The example demonstrates how to use the `lexbor` library to convert an HTML tag tree into an s-expression string, which is output to `stdout`. It covers the process of reading an HTML file, parsing it into a DOM tree, traversing the tree, and then serializing it into s-expressions.

## Key Code Sections

### Main Function Logic

The `main` function initializes the HTML document, parses the input file, and invokes the traversal and serialization process. The core of the main function is structured as follows:

```c
int
main(int argc, const char *argv[])
{
    if (argc != 2) {
        usage();
        FAILED("Invalid number of arguments");
    }

    lxb_status_t status;
    lxb_html_document_t *document;
    lxb_char_t *html;
    size_t html_len;

    html = lexbor_fs_file_easy_read((const lxb_char_t *) argv[1], &html_len);
    if (html == NULL) {
        FAILED("Failed to read HTML file");
    }

    document = lxb_html_document_create();
    if (document == NULL) {
        PRINT("Failed to create HTML Document");
        goto failed;
    }

    status = lxb_html_document_parse(document, html, html_len);
    if (status != LXB_STATUS_OK) {
        PRINT("Failed to parse HTML");
        goto failed;
    }

    status = tree_walker(lxb_dom_interface_node(document)->first_child,
                         serialize_cb, NULL);
    if (status != LXB_STATUS_OK) {
        PRINT("Failed to convert HTML to S-Expression");
        goto failed;
    }

    lxb_html_document_destroy(document);
    lexbor_free(html);

    return EXIT_SUCCESS;

failed:

    lxb_html_document_destroy(document);
    lexbor_free(html);

    return EXIT_FAILURE;
}
```

In this sequence, the key steps are:
1. **Reading the HTML File**: The `lexbor_fs_file_easy_read` function reads the HTML file and stores its content in `html`.
2. **Document Creation and Parsing**: The document is created using `lxb_html_document_create` and parsed with `lxb_html_document_parse`.
3. **Tree Traversal**: The `tree_walker` is called to traverse the HTML tree and serialize it.

### Tree Walking and Serialization

The `tree_walker` function recursively traverses the HTML DOM tree and calls the provided callback to serialize each node and its attributes into s-expressions.

```c
static lxb_status_t
tree_walker(lxb_dom_node_t *node, lxb_html_serialize_cb_f cb, void *ctx)
{
    lxb_status_t status;
    lxb_dom_node_t *root = node->parent;

    const lxb_char_t *name;
    size_t name_len = 0;

    while (node != NULL) {
        if (node->type == LXB_DOM_NODE_TYPE_ELEMENT) {
            status = cb((const lxb_char_t *) "(", 1, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }

            name = lxb_dom_element_qualified_name(lxb_dom_interface_element(node),
                                                  &name_len);

            status = cb(name, name_len, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }

            status = attributes(node, cb, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }

            if (node->local_name == LXB_TAG_TEMPLATE) {
                lxb_html_template_element_t *temp = lxb_html_interface_template(node);
                if (temp->content != NULL && temp->content->node.first_child != NULL) {
                    status = tree_walker(&temp->content->node, cb, ctx);
                    if (status != LXB_STATUS_OK) {
                        return status;
                    }
                }
            }
        }

        if (node->first_child != NULL) {
            node = node->first_child;
        }
        else {
            // Closing tag
            while (node != root && node->next == NULL) {
                if (node->type == LXB_DOM_NODE_TYPE_ELEMENT) {
                    status = cb((const lxb_char_t *) ")", 1, ctx);
                    if (status != LXB_STATUS_OK) {
                        return status;
                    }
                }
                    
                node = node->parent;
            }

            if (node->type == LXB_DOM_NODE_TYPE_ELEMENT) {
                status = cb((const lxb_char_t *) ")", 1, ctx);
                if (status != LXB_STATUS_OK) {
                    return status;
                }
            }

            if (node == root) {
                break;
            }

            node = node->next;
        }
    }

    return LXB_STATUS_OK;
}
```

This function:
1. **Starts the S-Expression Serialization**: Outputs a `(` followed by the element's name.
2. **Calls `attributes` Function**: Serializes each attribute into s-expressions.
3. **Recursively Processes Template Content**: Handles the special case of `<template>` elements.
4. **Navigates the Tree**: Traverses child nodes and handles the closing `)` for each element.

### Attribute Serialization

The `attributes` function processes the attributes of a node, serializing each one into an s-expression.

```c
static lxb_status_t
attributes(lxb_dom_node_t *node, lxb_html_serialize_cb_f cb, void *ctx)
{
    lxb_status_t status;
    lxb_dom_attr_t *attr;
    const lxb_char_t *data;
    size_t data_len;

    attr = lxb_dom_element_first_attribute(lxb_dom_interface_element(node));
    while (attr != NULL) {
        status = cb((const lxb_char_t *) "(", 1, ctx);
        if (status != LXB_STATUS_OK) {
            return status;
        }

        data = lxb_dom_attr_qualified_name(attr, &data_len);
        status = cb(data, data_len, ctx);
        if (status != LXB_STATUS_OK) {
            return status;
        }

        data = lxb_dom_attr_value(attr, &data_len);
        if (data != NULL) {
            status = cb((const lxb_char_t *) " '", 2, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }

            status = cb(data, data_len, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }

            status = cb((const lxb_char_t *) "'", 1, ctx);
            if (status != LXB_STATUS_OK) {
                return status;
            }
        }

        status = cb((const lxb_char_t *) ")", 1, ctx);
        if (status != LXB_STATUS_OK) {
            return status;
        }

        attr = lxb_dom_element_next_attribute(attr);
    }

    return LXB_STATUS_OK;
}
```

This function:
1. **Iterates Over Attributes**: Processes each attribute of a node.
2. **Serializes Attribute Names and Values**: Outputs the name and value in s-expression format.

### Serialize Callback

The `serialize_cb` function is the callback used during tree traversal to output data.

```c
static lxb_status_t
serialize_cb(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

This simple function formats and prints the data.

## Notes

- The example assumes the input file is well-formed HTML.
- The `tree_walker` correctly handles nested elements and template content.
- Attribute values are properly quoted in the s-expression output.
- The code includes comprehensive error handling, with cleanup in case of failure.

## Summary

This example demonstrates a practical usage of the `lexbor` library to convert an HTML document into s-expressions. The key takeaways are:
1. **Initialization and Parsing**: How to read and parse an HTML file with `lexbor`.
2. **Tree Traversal**: Using recursion to traverse and process the DOM tree.
3. **Serialization**: Techniques to serialize nodes and attributes efficiently.

This knowledge is essential for developers working with HTML parsing and needing to convert DOM structures into different representations using the `lexbor` library.