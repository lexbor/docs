# DOM Module

* **Version:** 2.0.0
* **Path:** `source/lexbor/dom`
* **Base Includes:** `lexbor/dom/dom.h`
* **Examples:** `examples/lexbor/html` (DOM is used through the HTML module)
* **Specification:** [WHATWG DOM Living Standard](https://dom.spec.whatwg.org/)

## Overview

The DOM module implements the Document Object Model specification, providing a tree structure for representing and manipulating HTML documents. It defines the node hierarchy, tree operations, element attributes, and namespace handling used throughout lexbor.

In practice, the DOM module is most commonly used via the [HTML module](html.md). After parsing HTML with `lxb_html_document_parse()`, you interact with the resulting tree using DOM types and functions.

## Key Types

### Node Types

Every node in the DOM tree has a type defined by `lxb_dom_node_type_t`:

```c
typedef enum {
    LXB_DOM_NODE_TYPE_UNDEF                  = 0x00,
    LXB_DOM_NODE_TYPE_ELEMENT                = 0x01,
    LXB_DOM_NODE_TYPE_ATTRIBUTE              = 0x02,
    LXB_DOM_NODE_TYPE_TEXT                    = 0x03,
    LXB_DOM_NODE_TYPE_CDATA_SECTION          = 0x04,
    LXB_DOM_NODE_TYPE_ENTITY_REFERENCE       = 0x05, // historical
    LXB_DOM_NODE_TYPE_ENTITY                 = 0x06, // historical
    LXB_DOM_NODE_TYPE_PROCESSING_INSTRUCTION = 0x07,
    LXB_DOM_NODE_TYPE_COMMENT                = 0x08,
    LXB_DOM_NODE_TYPE_DOCUMENT               = 0x09,
    LXB_DOM_NODE_TYPE_DOCUMENT_TYPE          = 0x0A,
    LXB_DOM_NODE_TYPE_DOCUMENT_FRAGMENT      = 0x0B,
    LXB_DOM_NODE_TYPE_NOTATION               = 0x0C, // historical
    LXB_DOM_NODE_TYPE_CHARACTER_DATA,
    LXB_DOM_NODE_TYPE_SHADOW_ROOT,
    LXB_DOM_NODE_TYPE_LAST_ENTRY
} lxb_dom_node_type_t;
```

### Interface Hierarchy

The DOM module uses a "poor man's inheritance" pattern where each structure embeds its parent as the first field, allowing safe casting between types:

```
lxb_dom_event_target_t
  └── lxb_dom_node_t
        ├── lxb_dom_element_t
        ├── lxb_dom_document_t
        ├── lxb_dom_character_data_t
        │     ├── lxb_dom_text_t
        │     ├── lxb_dom_comment_t
        │     ├── lxb_dom_cdata_section_t
        │     └── lxb_dom_processing_instruction_t
        ├── lxb_dom_document_type_t
        ├── lxb_dom_document_fragment_t
        ├── lxb_dom_shadow_root_t
        └── lxb_dom_attr_t
```

### Interface Casting Macros

Because of the inheritance pattern, casting macros are provided in `lexbor/dom/interface.h`:

```c
lxb_dom_interface_node(obj)      /* cast to lxb_dom_node_t *    */
lxb_dom_interface_element(obj)   /* cast to lxb_dom_element_t * */
lxb_dom_interface_document(obj)  /* cast to lxb_dom_document_t * */
lxb_dom_interface_text(obj)      /* cast to lxb_dom_text_t *    */
lxb_dom_interface_comment(obj)   /* cast to lxb_dom_comment_t * */
lxb_dom_interface_attr(obj)      /* cast to lxb_dom_attr_t *    */
```

For example, to get the node type of an element:

```c
lxb_dom_element_t *element = /* ... */;
lxb_dom_node_type_t type = lxb_dom_node_type(lxb_dom_interface_node(element));
```


## Node (`lxb_dom_node_t`)

The fundamental type for all DOM tree nodes. Defined in `lexbor/dom/interfaces/node.h`.

### Tree Traversal

Navigate the tree using these inline functions:

```c
lxb_dom_node_t *
lxb_dom_node_first_child(lxb_dom_node_t *node);

lxb_dom_node_t *
lxb_dom_node_last_child(lxb_dom_node_t *node);

lxb_dom_node_t *
lxb_dom_node_next(lxb_dom_node_t *node);

lxb_dom_node_t *
lxb_dom_node_prev(lxb_dom_node_t *node);

lxb_dom_node_t *
lxb_dom_node_parent(lxb_dom_node_t *node);
```

All return `NULL` when no such node exists.

### Node Properties

```c
/* Get the node type */
lxb_dom_node_type_t
lxb_dom_node_type(lxb_dom_node_t *node);

/* Get the tag ID (element local name as numeric ID) */
lxb_tag_id_t
lxb_dom_node_tag_id(lxb_dom_node_t *node);

/* Get the node name as a string */
const lxb_char_t *
lxb_dom_node_name(lxb_dom_node_t *node, size_t *len);
```

### Tree Modification

**Low-level operations** — These insert/remove nodes directly without DOM spec validation:

```c
/* Insert node as the last child of 'to' */
void
lxb_dom_node_insert_child(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Insert node immediately before 'to' */
void
lxb_dom_node_insert_before(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Insert node immediately after 'to' */
void
lxb_dom_node_insert_after(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Remove node from its parent */
void
lxb_dom_node_remove(lxb_dom_node_t *node);
```

**Spec-compliant operations** — These perform DOM spec validation before modifying the tree, returning an exception code:

```c
/* Node.appendChild(node) — validates, then appends child */
lxb_dom_exception_code_t
lxb_dom_node_append_child(lxb_dom_node_t *parent, lxb_dom_node_t *node);

/* Node.insertBefore(node, child) — validates, then inserts */
lxb_dom_exception_code_t
lxb_dom_node_insert_before_spec(lxb_dom_node_t *dst, lxb_dom_node_t *node,
                                lxb_dom_node_t *child);

/* Node.removeChild(child) — validates, then removes */
lxb_dom_exception_code_t
lxb_dom_node_remove_child(lxb_dom_node_t *parent, lxb_dom_node_t *child);

/* Node.replaceChild(node, child) — validates, then replaces */
lxb_dom_exception_code_t
lxb_dom_node_replace_child(lxb_dom_node_t *parent, lxb_dom_node_t *node,
                           lxb_dom_node_t *child);
```

Returns `LXB_DOM_EXCEPTION_OK` on success.

### Text Content

```c
/* Get text content of the node and its descendants.
 * Memory is freed when the document is destroyed.
 * To free earlier, call lxb_dom_document_destroy_text(). */
lxb_char_t *
lxb_dom_node_text_content(lxb_dom_node_t *node, size_t *len);

/* Set text content, replacing all children */
lxb_status_t
lxb_dom_node_text_content_set(lxb_dom_node_t *node,
                              const lxb_char_t *content, size_t len);
```

### Tree Walking

Walk all descendants of a node using a callback:

```c
typedef lexbor_action_t
(*lxb_dom_node_simple_walker_f)(lxb_dom_node_t *node, void *ctx);

void
lxb_dom_node_simple_walk(lxb_dom_node_t *root,
                         lxb_dom_node_simple_walker_f walker_cb, void *ctx);
```

The callback should return `LEXBOR_ACTION_OK` to continue or `LEXBOR_ACTION_STOP` to stop.

### Search Functions

Find nodes within a subtree:

```c
/* Find the first element with the given ID */
lxb_dom_node_t *
lxb_dom_node_by_id(lxb_dom_node_t *root,
                   const lxb_char_t *qualified_name, size_t len);

/* Collect all elements with the given tag name */
lxb_status_t
lxb_dom_node_by_tag_name(lxb_dom_node_t *root, lxb_dom_collection_t *collection,
                         const lxb_char_t *qualified_name, size_t len);

/* Collect all elements with the given class name */
lxb_status_t
lxb_dom_node_by_class_name(lxb_dom_node_t *root,
                           lxb_dom_collection_t *collection,
                           const lxb_char_t *class_name, size_t len);

/* Collect elements by attribute name and value (exact match) */
lxb_status_t
lxb_dom_node_by_attr(lxb_dom_node_t *root, lxb_dom_collection_t *collection,
                     const lxb_char_t *qualified_name, size_t qname_len,
                     const lxb_char_t *value, size_t value_len,
                     bool case_insensitive);

/* Collect elements by attribute value prefix */
lxb_status_t
lxb_dom_node_by_attr_begin(lxb_dom_node_t *root,
                           lxb_dom_collection_t *collection,
                           const lxb_char_t *qualified_name, size_t qname_len,
                           const lxb_char_t *value, size_t value_len,
                           bool case_insensitive);

/* Collect elements by attribute value suffix */
lxb_status_t
lxb_dom_node_by_attr_end(lxb_dom_node_t *root, lxb_dom_collection_t *collection,
                         const lxb_char_t *qualified_name, size_t qname_len,
                         const lxb_char_t *value, size_t value_len,
                         bool case_insensitive);

/* Collect elements by attribute value substring */
lxb_status_t
lxb_dom_node_by_attr_contain(lxb_dom_node_t *root,
                             lxb_dom_collection_t *collection,
                             const lxb_char_t *qualified_name, size_t qname_len,
                             const lxb_char_t *value, size_t value_len,
                             bool case_insensitive);
```

### Destroy

```c
/* Destroy a single node (does not remove children) */
lxb_dom_node_t *
lxb_dom_node_destroy(lxb_dom_node_t *node);

/* Destroy a node and all its descendants */
lxb_dom_node_t *
lxb_dom_node_destroy_deep(lxb_dom_node_t *root);

/* Clone a node, optionally with all descendants */
lxb_dom_node_t *
lxb_dom_node_clone(lxb_dom_node_t *node, bool deep);
```


## Element (`lxb_dom_element_t`)

Extends `lxb_dom_node_t` for elements. Defined in `lexbor/dom/interfaces/element.h`.

### Element Names

```c
/* Original qualified name (e.g. "LalAla:DiV") */
const lxb_char_t *
lxb_dom_element_qualified_name(lxb_dom_element_t *element, size_t *len);

/* Uppercase qualified name */
const lxb_char_t *
lxb_dom_element_qualified_name_upper(lxb_dom_element_t *element, size_t *len);

/* Local name only (without prefix) */
const lxb_char_t *
lxb_dom_element_local_name(lxb_dom_element_t *element, size_t *len);

/* Tag name (uppercase qualified name) */
const lxb_char_t *
lxb_dom_element_tag_name(lxb_dom_element_t *element, size_t *len);

/* Namespace prefix */
const lxb_char_t *
lxb_dom_element_prefix(lxb_dom_element_t *element, size_t *len);

/* Tag ID and namespace ID as numeric values */
lxb_tag_id_t
lxb_dom_element_tag_id(lxb_dom_element_t *element);

lxb_ns_id_t
lxb_dom_element_ns_id(lxb_dom_element_t *element);
```

### Attribute Operations

```c
/* Set or create an attribute */
lxb_dom_attr_t *
lxb_dom_element_set_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len,
                              const lxb_char_t *value, size_t value_len);

/* Get an attribute value */
const lxb_char_t *
lxb_dom_element_get_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len,
                              size_t *value_len);

/* Remove an attribute */
lxb_status_t
lxb_dom_element_remove_attribute(lxb_dom_element_t *element,
                                 const lxb_char_t *qualified_name, size_t qn_len);

/* Check if attribute exists */
bool
lxb_dom_element_has_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len);

/* Check if element has any attributes */
bool
lxb_dom_element_has_attributes(lxb_dom_element_t *element);
```

### Attribute Iteration

```c
lxb_dom_attr_t *
lxb_dom_element_first_attribute(lxb_dom_element_t *element);

lxb_dom_attr_t *
lxb_dom_element_last_attribute(lxb_dom_element_t *element);

lxb_dom_attr_t *
lxb_dom_element_next_attribute(lxb_dom_attr_t *attr);

lxb_dom_attr_t *
lxb_dom_element_prev_attribute(lxb_dom_attr_t *attr);
```

### ID and Class Access

```c
/* Get the element's "id" attribute value */
const lxb_char_t *
lxb_dom_element_id(lxb_dom_element_t *element, size_t *len);

/* Get the element's "class" attribute value */
const lxb_char_t *
lxb_dom_element_class(lxb_dom_element_t *element, size_t *len);

/* Direct access to the id/class attribute objects */
lxb_dom_attr_t *
lxb_dom_element_id_attribute(lxb_dom_element_t *element);

lxb_dom_attr_t *
lxb_dom_element_class_attribute(lxb_dom_element_t *element);
```

### Element Search

These functions search from the element downward and collect results into a collection:

```c
/* Find the first element with the given ID */
lxb_dom_element_t *
lxb_dom_element_by_id(lxb_dom_element_t *root,
                      const lxb_char_t *qualified_name, size_t len);

/* Collect elements by tag name */
lxb_status_t
lxb_dom_elements_by_tag_name(lxb_dom_element_t *root,
                             lxb_dom_collection_t *collection,
                             const lxb_char_t *qualified_name, size_t len);

/* Collect elements by class name */
lxb_status_t
lxb_dom_elements_by_class_name(lxb_dom_element_t *root,
                               lxb_dom_collection_t *collection,
                               const lxb_char_t *class_name, size_t len);

/* Collect elements by attribute (exact, prefix, suffix, substring) */
lxb_status_t
lxb_dom_elements_by_attr(lxb_dom_element_t *root,
                         lxb_dom_collection_t *collection,
                         const lxb_char_t *qualified_name, size_t qname_len,
                         const lxb_char_t *value, size_t value_len,
                         bool case_insensitive);
```

Variants `lxb_dom_elements_by_attr_begin()`, `lxb_dom_elements_by_attr_end()`, and `lxb_dom_elements_by_attr_contain()` match by attribute value prefix, suffix, and substring respectively.

### Lifecycle

```c
lxb_dom_element_t *
lxb_dom_element_create(lxb_dom_document_t *document,
                       const lxb_char_t *local_name, size_t lname_len,
                       const lxb_char_t *ns_name, size_t ns_len,
                       const lxb_char_t *prefix, size_t prefix_len,
                       const lxb_char_t *is, size_t is_len,
                       bool sync_custom);

lxb_dom_element_t *
lxb_dom_element_destroy(lxb_dom_element_t *element);
```

In most cases, prefer `lxb_dom_document_create_element()` (see below) instead of calling `lxb_dom_element_create()` directly.


## Attribute (`lxb_dom_attr_t`)

Represents a single attribute on an element. Defined in `lexbor/dom/interfaces/attr.h`.

```c
/* Get the local name of the attribute */
const lxb_char_t *
lxb_dom_attr_local_name(lxb_dom_attr_t *attr, size_t *len);

/* Get the qualified name (including prefix) */
const lxb_char_t *
lxb_dom_attr_qualified_name(lxb_dom_attr_t *attr, size_t *len);

/* Get the attribute value */
const lxb_char_t *
lxb_dom_attr_value(lxb_dom_attr_t *attr, size_t *len);

/* Set the attribute value */
lxb_status_t
lxb_dom_attr_set_value(lxb_dom_attr_t *attr,
                       const lxb_char_t *value, size_t value_len);
```


## Document (`lxb_dom_document_t`)

The document node — the root of the DOM tree. Defined in `lexbor/dom/interfaces/document.h`.

When working with HTML, you typically use `lxb_html_document_t` (from the [HTML module](html.md)) rather than `lxb_dom_document_t` directly.

### Compatibility Mode

```c
typedef enum {
    LXB_DOM_DOCUMENT_CMODE_NO_QUIRKS       = 0x00,
    LXB_DOM_DOCUMENT_CMODE_QUIRKS          = 0x01,
    LXB_DOM_DOCUMENT_CMODE_LIMITED_QUIRKS  = 0x02
} lxb_dom_document_cmode_t;
```

### Factory Methods

Create new DOM nodes owned by the document:

```c
lxb_dom_element_t *
lxb_dom_document_create_element(lxb_dom_document_t *document,
                                const lxb_char_t *local_name, size_t lname_len,
                                void *reserved_for_opt);

lxb_dom_text_t *
lxb_dom_document_create_text_node(lxb_dom_document_t *document,
                                  const lxb_char_t *data, size_t len);

lxb_dom_comment_t *
lxb_dom_document_create_comment(lxb_dom_document_t *document,
                                const lxb_char_t *data, size_t len);

lxb_dom_cdata_section_t *
lxb_dom_document_create_cdata_section(lxb_dom_document_t *document,
                                      const lxb_char_t *data, size_t len);

lxb_dom_processing_instruction_t *
lxb_dom_document_create_processing_instruction(lxb_dom_document_t *document,
                                               const lxb_char_t *target, size_t target_len,
                                               const lxb_char_t *data, size_t data_len);

lxb_dom_document_fragment_t *
lxb_dom_document_create_document_fragment(lxb_dom_document_t *document);
```

### Document Access

```c
/* Get the root node of the document tree */
lxb_dom_node_t *
lxb_dom_document_root(lxb_dom_document_t *document);

/* Get the document element (e.g. <html>) */
lxb_dom_element_t *
lxb_dom_document_element(lxb_dom_document_t *document);

/* Import a node from another document */
lxb_dom_node_t *
lxb_dom_document_import_node(lxb_dom_document_t *doc, lxb_dom_node_t *node,
                             bool deep);
```

### Lifecycle

```c
lxb_dom_document_t *
lxb_dom_document_create(lxb_dom_document_t *owner);

lxb_status_t
lxb_dom_document_init(lxb_dom_document_t *document, lxb_dom_document_t *owner,
                      lxb_dom_interface_create_f create_interface,
                      lxb_dom_interface_clone_f clone_interface,
                      lxb_dom_interface_destroy_f destroy_interface,
                      lxb_dom_document_dtype_t type, unsigned int ns);

lxb_status_t
lxb_dom_document_clean(lxb_dom_document_t *document);

lxb_dom_document_t *
lxb_dom_document_destroy(lxb_dom_document_t *document);
```


## Collection (`lxb_dom_collection_t`)

A dynamic array for holding references to multiple DOM nodes. Used with search functions that return multiple results. Defined in `lexbor/dom/collection.h`.

### Lifecycle

```c
lxb_dom_collection_t *
lxb_dom_collection_create(lxb_dom_document_t *document);

lxb_status_t
lxb_dom_collection_init(lxb_dom_collection_t *col, size_t start_list_size);

lxb_dom_collection_t *
lxb_dom_collection_destroy(lxb_dom_collection_t *col, bool self_destroy);
```

Or use the convenience function that creates and initializes in one call:

```c
lxb_dom_collection_t *
lxb_dom_collection_make(lxb_dom_document_t *document, size_t start_list_size);
```

### Usage

```c
void
lxb_dom_collection_clean(lxb_dom_collection_t *col);

lxb_status_t
lxb_dom_collection_append(lxb_dom_collection_t *col, void *value);

lxb_dom_element_t *
lxb_dom_collection_element(lxb_dom_collection_t *col, size_t idx);

lxb_dom_node_t *
lxb_dom_collection_node(lxb_dom_collection_t *col, size_t idx);

size_t
lxb_dom_collection_length(lxb_dom_collection_t *col);
```


## Namespace Support

The DOM module supports six XML namespaces, managed by the NS module:

- **HTML** (`LXB_NS_HTML`)
- **SVG** (`LXB_NS_SVG`)
- **MathML** (`LXB_NS_MATH`)
- **XLink** (`LXB_NS_XLINK`)
- **XML** (`LXB_NS_XML`)
- **XMLNS** (`LXB_NS_XMLNS`)

Namespace IDs are accessed via `lxb_dom_element_ns_id()` or the `ns` field of `lxb_dom_node_t`.


## Examples

### Iterating Child Elements

```c
#include <lexbor/html/parser.h>
#include <lexbor/dom/interfaces/element.h>

int
main(void)
{
    lxb_status_t status;
    lxb_html_document_t *document;
    lxb_dom_element_t *body;
    lxb_dom_node_t *child;

    static const lxb_char_t html[] =
        "<div>First</div><p>Second</p><span>Third</span>";

    document = lxb_html_document_create();
    status = lxb_html_document_parse(document, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    body = lxb_dom_interface_element(document->body);

    child = lxb_dom_node_first_child(lxb_dom_interface_node(body));
    while (child != NULL) {
        if (lxb_dom_node_type(child) == LXB_DOM_NODE_TYPE_ELEMENT) {
            const lxb_char_t *name;
            name = lxb_dom_element_local_name(lxb_dom_interface_element(child),
                                              NULL);
            printf("Element: %s\n", (const char *) name);
        }

        child = lxb_dom_node_next(child);
    }

    lxb_html_document_destroy(document);
    return EXIT_SUCCESS;

failed:
    lxb_html_document_destroy(document);
    return EXIT_FAILURE;
}
```

Expected output:
```
Element: div
Element: p
Element: span
```

### Searching by Attribute

```c
#include <lexbor/html/parser.h>
#include <lexbor/dom/interfaces/element.h>

int
main(void)
{
    lxb_status_t status;
    lxb_html_document_t *document;
    lxb_dom_collection_t *collection;

    static const lxb_char_t html[] =
        "<div class=\"active\">One</div>"
        "<p class=\"active\">Two</p>"
        "<span>Three</span>";

    document = lxb_html_document_create();
    status = lxb_html_document_parse(document, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    collection = lxb_dom_collection_make(
        lxb_dom_interface_document(document), 16);
    if (collection == NULL) {
        goto failed;
    }

    status = lxb_dom_elements_by_class_name(
        lxb_dom_interface_element(document->body),
        collection,
        (const lxb_char_t *) "active", 6);
    if (status != LXB_STATUS_OK) {
        goto cleanup;
    }

    for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
        lxb_dom_element_t *el = lxb_dom_collection_element(collection, i);
        const lxb_char_t *name = lxb_dom_element_local_name(el, NULL);
        printf("Found: %s\n", (const char *) name);
    }

    lxb_dom_collection_destroy(collection, true);
    lxb_html_document_destroy(document);
    return EXIT_SUCCESS;

cleanup:
    lxb_dom_collection_destroy(collection, true);
failed:
    lxb_html_document_destroy(document);
    return EXIT_FAILURE;
}
```

Expected output:
```
Found: div
Found: p
```

### Walking the DOM Tree

```c
#include <lexbor/html/parser.h>
#include <lexbor/dom/interfaces/element.h>

static lexbor_action_t
walker(lxb_dom_node_t *node, void *ctx)
{
    size_t *count = (size_t *) ctx;
    if (lxb_dom_node_type(node) == LXB_DOM_NODE_TYPE_ELEMENT) {
        (*count)++;
    }
    return LEXBOR_ACTION_OK;
}

int
main(void)
{
    lxb_status_t status;
    lxb_html_document_t *document;
    size_t count = 0;

    static const lxb_char_t html[] =
        "<div><p><span>text</span></p></div><ul><li>item</li></ul>";

    document = lxb_html_document_create();
    status = lxb_html_document_parse(document, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_html_document_destroy(document);
        return EXIT_FAILURE;
    }

    lxb_dom_node_simple_walk(
        lxb_dom_interface_node(document->body), walker, &count);

    /* count includes <body> itself */
    printf("Elements in body: %zu\n", count);

    lxb_html_document_destroy(document);
    return EXIT_SUCCESS;
}
```

Expected output:
```
Elements in body: 6
```

The count includes `<body>`, `<div>`, `<p>`, `<span>`, `<ul>`, and `<li>`.
