# Walking Through CSS Properties of an HTML Element

The example code file `lexbor/styles/walk.c` demonstrates how to utilize the `lexbor`
library to parse an HTML document, attach CSS stylesheets, and iterate over the
CSS properties of specific HTML elements. This article will explain the code in
detail, focusing on important sections and functions used within the `lexbor`
ecosystem.

## Key Code Sections

### Callbacks for CSS Property Serialization

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

The `callback` function is used as a generic print callback during CSS property 
serialization. It takes text data and its length, then prints it. This function 
will be passed to `lexbor` serialization functions to output the serialized CSS code.

### Walking and Printing CSS Declarations

```c
static lxb_status_t
walk_cb(lxb_html_element_t *element, const lxb_css_rule_declaration_t *declr,
        void *ctx, lxb_css_selector_specificity_t spec, bool is_weak)
{
    // ... Code to serialize and print declaration and properties ...

    printf("    Primary: %s\n", (is_weak) ? "false" : "true");
    printf("    Specificity (priority): %d %d %d %d %d\n",
           lxb_css_selector_sp_i(spec), lxb_css_selector_sp_s(spec),
           lxb_css_selector_sp_a(spec), lxb_css_selector_sp_b(spec),
           lxb_css_selector_sp_c(spec));

    return LXB_STATUS_OK;
}
```

The `walk_cb` function is a callback provided to the function that walks through 
CSS properties. It receives each `lxb_css_rule_declaration_t` object and 
serialized its name and value using the `callback` function. It also prints 
the specificity and whether the rule is weak.

```c
lxb_css_rule_declaration_serialize(declr, callback, NULL);
lxb_css_property_serialize_name(declr->u.user, declr->type, callback, NULL);
lxb_css_property_serialize(declr->u.user, declr->type, callback, NULL);
```

The above code sections call `lexbor` library functions to serialize various 
CSS rule components using our previously defined `callback`.

### Initialize HTML Document

```c
document = lxb_html_document_create();
if (document == NULL) {
    return EXIT_FAILURE;
}

status = lxb_html_document_css_init(document);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

status = lxb_html_document_parse(document, html.data, html.length);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

Here, an HTML document is created and initialized for CSS handling. The HTML 
data is then parsed into the document structure.

### Parse and Attach Stylesheet

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

sst = lxb_css_stylesheet_parse(parser, slctrs.data, slctrs.length);
if (sst == NULL) {
    return EXIT_FAILURE;
}

status = lxb_html_document_stylesheet_attach(document, sst);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

A CSS parser and stylesheet object are created. The stylesheet is parsed from 
CSS text and attached to the HTML document, allowing style rules to be applied 
to its elements.

### Find Element by Class Name

```c
collection = lxb_dom_collection_make(lxb_dom_interface_document(document), 16);
if (collection == NULL) {
    return EXIT_FAILURE;
}

status = lxb_dom_node_by_class_name(lxb_dom_interface_node(document),
                                    collection, father_str.data, father_str.length);
if (status != LXB_STATUS_OK || lxb_dom_collection_length(collection) == 0) {
    return EXIT_FAILURE;
}

div = lxb_html_interface_element(lxb_dom_collection_node(collection, 0));
```

The DOM is queried for elements with a specific class name, and the first match 
is retrieved and cast to an `lxb_html_element_t` type. This element is used 
later for style walking.

### Walk Through Element's Styles

```c
status = lxb_html_element_style_walk(div, walk_cb, NULL, true);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

The `lxb_html_element_style_walk` function walks through all CSS declarations 
applied to the specific element (`div` in this case) and calls `walk_cb` for 
each declaration.

### Resource Cleanup

```c
(void) lxb_dom_collection_destroy(collection, true);
(void) lxb_css_stylesheet_destroy(sst, true);
(void) lxb_css_parser_destroy(parser, true);
(void) lxb_html_document_destroy(document);
```

Cleaning up created resources properly is crucial to avoid memory leaks. This 
section of the code ensures everything allocated is properly released.

## Notes

1. **Utilization of callbacks**: Callbacks are heavily used for printing 
   during serialization operations.
2. **Specificity calculations**: The code shows how to extract and print 
   specificity details of CSS selectors.
3. **Resource management**: Emphasizes the importance of creating and 
   destroying resources in `lexbor`.

## Summary

This example illustrates the process of creating and parsing an HTML document, 
attaching CSS stylesheets, and iterating through CSS properties of specific 
HTML elements using `lexbor`. The detailed walkthrough highlights key 
functionalities such as serialization callbacks and specificity calculations, 
providing a comprehensive look at how to manage styles in documents with this 
library. For `lexbor` users, mastering these techniques is essential for 
effective manipulation and examination of CSS properties in web documents.