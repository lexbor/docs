# DOM Module

* **Version:** 2.0.0
* **Path:** `source/lexbor/dom`
* **Base Includes:** `lexbor/dom/dom.h`
* **Examples:** not present
* **Specification:** [WHATWG DOM Living Standard](https://dom.spec.whatwg.org/)

## Overview

The DOM module implements the [WHATWG DOM Living Standard](https://dom.spec.whatwg.org/) — the tree structure that represents parsed HTML (or XML) documents in memory.

When the HTML parser processes markup like `<div><p>Hello</p></div>`, the result is not a string — it's a tree of DOM nodes. The DOM module defines all the node types, their relationships, and the operations you can perform on them: traversal, insertion, removal, cloning, attribute manipulation, and text content access.

The DOM module is not used directly in most cases — you interact with it through the HTML module, which creates and populates the DOM tree during parsing. But understanding how the DOM is structured is essential for working with parsed documents.

## Key Features

- **Specification Compliant** — follows the WHATWG DOM Living Standard
- **Efficient Tree Structure** — doubly-linked lists for O(1) insertion and removal
- **Memory Pools** — all nodes allocated from document-owned pools for fast allocation and easy cleanup
- **Interface Inheritance** — "poor man's inheritance" via struct embedding for zero-cost type casting
- **Namespace Support** — HTML, SVG, MathML, XML namespaces
- **Node Callbacks** — hook into insert, remove, destroy, and value change events

## What's Inside

- **[Node Types & Hierarchy](#node-types--hierarchy)** — all DOM node types and their inheritance chain
- **[Tree Structure](#tree-structure)** — how nodes are linked together
- **[Tree Traversal](#tree-traversal)** — navigating parent, children, siblings
- **[Tree Manipulation](#tree-manipulation)** — insert, remove, replace, clone operations
- **[Elements & Attributes](#elements--attributes)** — working with elements and their attributes
- **[Finding Elements](#finding-elements)** — search by ID, tag name, class name, attribute
- **[Text Content](#text-content)** — reading and writing text content of nodes
- **[Collections](#collections)** — working with query results
- **[Memory Management](#memory-management)** — how DOM memory is organized

## Node Types & Hierarchy

Every object in the DOM tree is a **node**. Nodes come in different types, each represented by its own C struct. These structs form an inheritance hierarchy using struct embedding — the parent struct is always the **first field** of the child struct, enabling safe zero-cost type casting.

### Inheritance Tree

```
lxb_dom_event_target_t
    +-- lxb_dom_node_t
            +-- lxb_dom_element_t
            +-- lxb_dom_attr_t
            +-- lxb_dom_document_t
            +-- lxb_dom_document_type_t
            +-- lxb_dom_document_fragment_t
            |       +-- lxb_dom_shadow_root_t
            +-- lxb_dom_character_data_t
                    +-- lxb_dom_text_t
                    +-- lxb_dom_cdata_section_t
                    +-- lxb_dom_comment_t
                    +-- lxb_dom_processing_instruction_t
```

### Node Types

Each node has a `type` field that identifies its category:

| Type Constant | Value | Description | C Type |
|---------------|-------|-------------|--------|
| `LXB_DOM_NODE_TYPE_ELEMENT` | 0x01 | Element node (`<div>`, `<p>`, etc.) | `lxb_dom_element_t` |
| `LXB_DOM_NODE_TYPE_ATTRIBUTE` | 0x02 | Attribute node (`class="foo"`) | `lxb_dom_attr_t` |
| `LXB_DOM_NODE_TYPE_TEXT` | 0x03 | Text content | `lxb_dom_text_t` |
| `LXB_DOM_NODE_TYPE_CDATA_SECTION` | 0x04 | CDATA section | `lxb_dom_cdata_section_t` |
| `LXB_DOM_NODE_TYPE_PROCESSING_INSTRUCTION` | 0x07 | Processing instruction | `lxb_dom_processing_instruction_t` |
| `LXB_DOM_NODE_TYPE_COMMENT` | 0x08 | Comment (`<!-- ... -->`) | `lxb_dom_comment_t` |
| `LXB_DOM_NODE_TYPE_DOCUMENT` | 0x09 | Document (root owner) | `lxb_dom_document_t` |
| `LXB_DOM_NODE_TYPE_DOCUMENT_TYPE` | 0x0A | DOCTYPE declaration | `lxb_dom_document_type_t` |
| `LXB_DOM_NODE_TYPE_DOCUMENT_FRAGMENT` | 0x0B | Document fragment | `lxb_dom_document_fragment_t` |

All node type constants are defined in `source/lexbor/dom/interfaces/node.h`.

### Interface Casting

Because of the first-field embedding pattern, you can safely cast between parent and child types. The module provides macros for this:

```C
/* DOM interface casting macros (from dom/interface.h) */
#define lxb_dom_interface_node(obj)              ((lxb_dom_node_t *) (obj))
#define lxb_dom_interface_element(obj)           ((lxb_dom_element_t *) (obj))
#define lxb_dom_interface_attr(obj)              ((lxb_dom_attr_t *) (obj))
#define lxb_dom_interface_document(obj)          ((lxb_dom_document_t *) (obj))
#define lxb_dom_interface_document_type(obj)     ((lxb_dom_document_type_t *) (obj))
#define lxb_dom_interface_document_fragment(obj) ((lxb_dom_document_fragment_t *) (obj))
#define lxb_dom_interface_text(obj)              ((lxb_dom_text_t *) (obj))
#define lxb_dom_interface_comment(obj)           ((lxb_dom_comment_t *) (obj))
#define lxb_dom_interface_character_data(obj)    ((lxb_dom_character_data_t *) (obj))
#define lxb_dom_interface_shadow_root(obj)       ((lxb_dom_shadow_root_t *) (obj))
```

For a detailed explanation of how interface inheritance and safe type casting works, see [Element Interfaces](html.md#element-interfaces) in the HTML module documentation.

## Tree Structure

The DOM tree is built from nodes connected by doubly-linked pointers. Each node has links to its parent, siblings, and children:

```C
struct lxb_dom_node {
    lxb_dom_event_target_t event_target;

    uintptr_t              local_name;     /* Tag/node name ID */
    uintptr_t              prefix;         /* Namespace prefix ID */
    uintptr_t              ns;             /* Namespace ID */

    lxb_dom_document_t     *owner_document;

    lxb_dom_node_t         *next;          /* Next sibling */
    lxb_dom_node_t         *prev;          /* Previous sibling */
    lxb_dom_node_t         *parent;        /* Parent node */
    lxb_dom_node_t         *first_child;   /* First child */
    lxb_dom_node_t         *last_child;    /* Last child */
    void                   *user;          /* User data pointer */

    lxb_dom_node_type_t    type;           /* Node type */
};
```

### Why uintptr_t for local_name, prefix, ns

The `local_name`, `prefix`, and `ns` fields are declared as `uintptr_t` — not as a pointer and not as a plain integer, but as a type that can hold both. This is intentional: these fields store either a **small integer ID** or a **pointer to a hash entry**, depending on whether the value is known at compile time or was created dynamically.

**How it works:**

All known HTML tags (`<div>`, `<p>`, `<span>`, etc.) have predefined integer IDs assigned at compile time:

```C
typedef enum {
    LXB_TAG__UNDEF       = 0x0000,
    LXB_TAG__TEXT        = 0x0002,
    LXB_TAG_DIV          = 0x0033,
    LXB_TAG_INPUT        = 0x006a,
    LXB_TAG_SPAN         = 0x00c0,
    /* ... 190+ known tags ... */
    LXB_TAG__LAST_ENTRY  = 0x00c6   /* Threshold */
} lxb_tag_id_enum_t;
```

When the parser encounters a known tag like `<div>`, the node's `local_name` is simply set to `LXB_TAG_DIV` (0x0033) — a small integer.

But when the parser encounters an unknown tag (like `<my-component>`), there is no predefined ID for it. In this case, the tag name is inserted into a hash table, and the **pointer to the hash entry** is stored directly in `local_name`. Since heap pointers are always much larger than the small predefined IDs, there is no collision.

The lookup function uses the threshold `LXB_TAG__LAST_ENTRY` to distinguish between the two cases:

```C
const lxb_tag_data_t *
lxb_tag_data_by_id(lxb_tag_id_t tag_id)
{
    if (tag_id >= LXB_TAG__LAST_ENTRY) {
        if (tag_id == LXB_TAG__LAST_ENTRY) {
            return NULL;
        }

        /* Above threshold: tag_id is a pointer to lxb_tag_data_t */
        return (const lxb_tag_data_t *) tag_id;
    }

    /* Below threshold: tag_id is an index into static array */
    return &lxb_tag_res_data_default[tag_id];
}
```

The same pattern applies to `ns` (namespace) and `prefix` fields:

| Field | Threshold | Known values | Unknown values |
|-------|-----------|-------------|----------------|
| `local_name` | `LXB_TAG__LAST_ENTRY` (0x00c6) | Small integer, index into static tag array | Pointer to `lxb_tag_data_t` in hash table |
| `ns` | `LXB_NS__LAST_ENTRY` (0x08) | Small integer: `LXB_NS_HTML` (2), `LXB_NS_SVG` (4), etc. | Pointer to `lxb_ns_data_t` in hash table |
| `prefix` | `LXB_NS__LAST_ENTRY` (0x08) | Small integer for known prefixes | Pointer to `lxb_ns_prefix_data_t` in hash table |

**Why this design?** It avoids an extra pointer indirection for the most common case (known tags and namespaces). For `<div>`, `<p>`, `<span>` and all other standard HTML tags, accessing the tag ID is just reading a small integer — no pointer dereference, no hash lookup. Only unknown/custom tags pay the cost of a pointer. This does not require a hash lookup, we can access the value immediately.

### Visual Representation

For the HTML `<div><p>Hello</p><span>World</span></div>`, the tree looks like:

```
              Document
                 |
            +----+----+
           html       ...
            |
         +--+--+
        head  body
               |
              div
               |
         +-----+-----+
         p           span
         |            |
       "Hello"     "World"
```

And the node links for the `div` and its children:

```
        div (parent)
         |
         +-- first_child --> p
         |                   +-- next --> span
         |                   +-- prev --> NULL
         |                   +-- parent > div
         |
         +-- last_child ---> span
                             +-- next --> NULL
                             +-- prev --> p
                             +-- parent > div
```

**Key properties:**
- Siblings form a doubly-linked list (`next`/`prev`)
- Parent has direct pointers to `first_child` and `last_child`
- Every node points back to its `parent`
- Every node knows its `owner_document`
- The `user` field is available for storing your own data

## Tree Traversal

### Basic Navigation

The DOM provides inline functions for efficient tree navigation:

```C
lxb_dom_node_t *lxb_dom_node_first_child(node)   /* First child */
lxb_dom_node_t *lxb_dom_node_last_child(node)    /* Last child */
lxb_dom_node_t *lxb_dom_node_next(node)          /* Next sibling */
lxb_dom_node_t *lxb_dom_node_prev(node)          /* Previous sibling */
lxb_dom_node_t *lxb_dom_node_parent(node)        /* Parent node */
```

**Example — iterating over children:**

```C
lxb_dom_node_t *body = lxb_dom_interface_node(document->body);
lxb_dom_node_t *child = lxb_dom_node_first_child(body);

while (child != NULL) {
    /* Process child node */
    lxb_tag_id_t tag = lxb_dom_node_tag_id(child);

    child = lxb_dom_node_next(child);
}
```

### Walker — Depth-First Traversal

For walking the entire subtree, use `lxb_dom_node_simple_walk()`. It performs a depth-first traversal and calls your callback for every node:

```C
lexbor_action_t
my_walker(lxb_dom_node_t *node, void *ctx)
{
    /* Return LEXBOR_ACTION_OK to continue */
    /* Return LEXBOR_ACTION_STOP to stop */

    if (lxb_dom_node_tag_id(node) == LXB_TAG_DIV) {
        printf("Found a <div>\n");
    }

    return LEXBOR_ACTION_OK;
}

/* Walk the entire subtree starting from body */
lxb_dom_node_simple_walk(lxb_dom_interface_node(document->body),
                         my_walker, NULL);
```

The walker visits every node in the subtree (elements, text nodes, comments, etc.) in document order.

## Tree Manipulation

The DOM module provides two levels of tree manipulation functions:

### Spec-Compliant Functions (Recommended)

These functions follow the WHATWG DOM specification — they validate the operation before performing it and return an exception code:

```C
/* Node.appendChild(node) */
lxb_dom_exception_code_t
lxb_dom_node_append_child(lxb_dom_node_t *parent, lxb_dom_node_t *node);

/* Node.insertBefore(node, child) */
lxb_dom_exception_code_t
lxb_dom_node_insert_before_spec(lxb_dom_node_t *parent, lxb_dom_node_t *node,
                                lxb_dom_node_t *child);

/* Node.removeChild(child) */
lxb_dom_exception_code_t
lxb_dom_node_remove_child(lxb_dom_node_t *parent, lxb_dom_node_t *child);

/* Node.replaceChild(node, child) */
lxb_dom_exception_code_t
lxb_dom_node_replace_child(lxb_dom_node_t *parent, lxb_dom_node_t *node,
                           lxb_dom_node_t *child);
```

The validation checks include:
- Parent can accept children (Elements, Documents, DocumentFragments can; Text, Comments cannot)
- Node type is allowed as a child of the parent (e.g., only one Element child in a Document)
- The insertion doesn't create a cycle (node is not an ancestor of parent)
- The child actually belongs to the parent (for remove/replace)

**Example:**

```C
/* Create a new element */
lxb_dom_element_t *p = lxb_dom_document_create_element(
    &document->dom_document,
    (const lxb_char_t *) "p", 1, NULL
);

/* Append it to body */
lxb_dom_exception_code_t exc;
exc = lxb_dom_node_append_child(
    lxb_dom_interface_node(document->body),
    lxb_dom_interface_node(p)
);

if (exc != LXB_DOM_EXCEPTION_OK) {
    /* Handle validation error */
}
```

### Low-Level Functions (Fast, No Validation)

For performance-critical code where you know the operation is valid, use the low-level functions. These perform the pointer manipulation directly without any checks:

```C
/* Insert as last child (no validation, no events) */
void lxb_dom_node_insert_child_wo_events(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Insert before a sibling (no validation, no events) */
void lxb_dom_node_insert_before_wo_events(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Insert after a sibling (no validation, no events) */
void lxb_dom_node_insert_after_wo_events(lxb_dom_node_t *to, lxb_dom_node_t *node);

/* Remove from tree (no validation, no events) */
void lxb_dom_node_remove_wo_events(lxb_dom_node_t *node);
```

There are also versions that skip validation but still fire node callbacks:

```C
void lxb_dom_node_insert_child(lxb_dom_node_t *to, lxb_dom_node_t *node);
void lxb_dom_node_insert_before(lxb_dom_node_t *to, lxb_dom_node_t *node);
void lxb_dom_node_insert_after(lxb_dom_node_t *to, lxb_dom_node_t *node);
void lxb_dom_node_remove(lxb_dom_node_t *node);
```

### Summary Table

| Function | Validation | Node Callbacks | Use Case |
|----------|-----------|---------------|----------|
| `lxb_dom_node_append_child()` | Yes | Yes | General use, follows specification |
| `lxb_dom_node_insert_child()` | No | Yes | When you know the operation is valid |
| `lxb_dom_node_insert_child_wo_events()` | No | No | Maximum performance |

### DocumentFragment Behavior

When you insert a `DocumentFragment`, its **children** are inserted — not the fragment itself. The fragment becomes empty after insertion. This matches the WHATWG specification behavior.

### Cloning Nodes

```C
/* Shallow clone — copies the node without its children */
lxb_dom_node_t *clone = lxb_dom_node_clone(node, false);

/* Deep clone — copies the node and all its descendants */
lxb_dom_node_t *deep_clone = lxb_dom_node_clone(node, true);
```

The cloned node is not attached to any tree — you need to insert it yourself.

### Destroying Nodes

```C
/* Destroy a single node (does not destroy children) */
lxb_dom_node_destroy(node);

/* Destroy a node and all its descendants */
lxb_dom_node_destroy_deep(node);
```

**Important:** Destroying a node does not remove it from the tree first. If the node is still in the tree, remove it before destroying:

```C
lxb_dom_node_remove(node);
lxb_dom_node_destroy_deep(node);
```

## Elements & Attributes

### Element Structure

An Element extends Node with attribute support and fast access to `id` and `class`:

```C
struct lxb_dom_element {
    lxb_dom_node_t    node;            /* Base node (first field) */

    lxb_dom_attr_id_t upper_name;      /* Uppercase tag name with prefix */
    lxb_dom_attr_id_t qualified_name;  /* Original case tag name with prefix */

    lexbor_str_t      *is_value;       /* Custom element 'is' attribute */

    lxb_dom_attr_t    *first_attr;     /* First attribute in linked list */
    lxb_dom_attr_t    *last_attr;      /* Last attribute */

    lxb_dom_attr_t    *attr_id;        /* Cached pointer to 'id' attribute */
    lxb_dom_attr_t    *attr_class;     /* Cached pointer to 'class' attribute */

    /* ... CSS-related fields ... */
};
```

**Notable design decisions:**
- `attr_id` and `attr_class` are cached pointers, giving O(1) access to the two most commonly accessed attributes
- Attributes form a doubly-linked list (`first_attr` → `last_attr`)
- Tag names are stored as IDs (integers), not strings — the actual strings live in hash tables owned by the document

### Getting Element Information

```C
/* Tag name as a string (e.g., "div", "p") */
const lxb_char_t *name = lxb_dom_element_local_name(element, &len);

/* Tag name with prefix (e.g., "svg:rect") */
const lxb_char_t *qname = lxb_dom_element_qualified_name(element, &len);

/* Uppercase tag name (e.g., "DIV") — for HTML compatibility */
const lxb_char_t *upper = lxb_dom_element_qualified_name_upper(element, &len);

/* Tag ID (numeric identifier, e.g., LXB_TAG_DIV) */
lxb_tag_id_t tag_id = lxb_dom_node_tag_id(lxb_dom_interface_node(element));

/* Namespace ID */
lxb_ns_id_t ns = lxb_dom_element_ns_id(element);

/* ID attribute value (fast, cached) */
const lxb_char_t *id = lxb_dom_element_id(element, &len);

/* Class attribute value (fast, cached) */
const lxb_char_t *cls = lxb_dom_element_class(element, &len);
```

### Working with Attributes

#### Set and Get Attributes

```C
/* Set attribute (creates if not exists, updates if exists) */
lxb_dom_attr_t *attr = lxb_dom_element_set_attribute(element,
    (const lxb_char_t *) "href", 4,
    (const lxb_char_t *) "https://example.com", 19);

/* Get attribute value */
size_t value_len;
const lxb_char_t *value = lxb_dom_element_get_attribute(element,
    (const lxb_char_t *) "href", 4, &value_len);

/* Check if attribute exists */
bool has = lxb_dom_element_has_attribute(element,
    (const lxb_char_t *) "href", 4);

/* Remove attribute */
lxb_dom_element_remove_attribute(element,
    (const lxb_char_t *) "href", 4);

/* Check if element has any attributes */
bool has_attrs = lxb_dom_element_has_attributes(element);
```

#### Iterating Over Attributes

Attributes form a doubly-linked list on each element:

```C
lxb_dom_attr_t *attr = lxb_dom_element_first_attribute(element);

while (attr != NULL) {
    /* Get attribute name */
    size_t name_len;
    const lxb_char_t *name = lxb_dom_attr_local_name(attr, &name_len);

    /* Get attribute value */
    size_t value_len;
    const lxb_char_t *value = lxb_dom_attr_value(attr, &value_len);

    printf("%.*s=\"%.*s\"\n",
           (int) name_len, name,
           (int) value_len, value);

    attr = lxb_dom_element_next_attribute(attr);
}
```

### Attribute Structure

Each attribute is also a node in the DOM hierarchy:

```C
struct lxb_dom_attr {
    lxb_dom_node_t     node;            /* Base node */

    lxb_dom_attr_id_t  upper_name;      /* Uppercase name with prefix */
    lxb_dom_attr_id_t  qualified_name;  /* Original case name with prefix */

    lexbor_str_t       *value;          /* Attribute value string */

    lxb_dom_element_t  *owner;          /* Owning element */

    lxb_dom_attr_t     *next;           /* Next attribute */
    lxb_dom_attr_t     *prev;           /* Previous attribute */
};
```

Attribute names are stored as IDs that reference entries in the document's attribute hash table. Standard HTML attributes (like `id`, `class`, `href`, `src`, `style`, etc.) have predefined IDs defined in `source/lexbor/dom/interfaces/attr_const.h`. Custom attributes are added to the hash table dynamically.

### Creating Elements

```C
/* Create an element by tag name */
lxb_dom_element_t *div = lxb_dom_document_create_element(
    &document->dom_document,
    (const lxb_char_t *) "div", 3,
    NULL  /* reserved */
);

/* Create a text node */
lxb_dom_text_t *text = lxb_dom_document_create_text_node(
    &document->dom_document,
    (const lxb_char_t *) "Hello, World!", 13
);

/* Create a comment node */
lxb_dom_comment_t *comment = lxb_dom_document_create_comment(
    &document->dom_document,
    (const lxb_char_t *) " This is a comment ", 19
);

/* Create a document fragment */
lxb_dom_document_fragment_t *frag =
    lxb_dom_document_create_document_fragment(&document->dom_document);
```

## Finding Elements

The DOM module provides several functions for finding elements in the tree. All search functions (except `by_id`) collect results into a [Collection](#collections).

### By ID

Returns the first element with the matching `id` attribute. Searches the subtree starting from the given root:

```C
/* Find element by ID */
lxb_dom_node_t *node = lxb_dom_node_by_id(
    lxb_dom_interface_node(document->body),
    (const lxb_char_t *) "main-content", 12
);

if (node != NULL) {
    lxb_dom_element_t *element = lxb_dom_interface_element(node);
    /* Work with the element */
}
```

There is also an element-level version:

```C
lxb_dom_element_t *element = lxb_dom_element_by_id(
    lxb_dom_interface_element(document->body),
    (const lxb_char_t *) "main-content", 12
);
```

### By Tag Name

Finds all elements with the given tag name:

```C
lxb_dom_collection_t *col = lxb_dom_collection_make(&document->dom_document, 16);

lxb_dom_elements_by_tag_name(
    lxb_dom_interface_element(document->body), col,
    (const lxb_char_t *) "div", 3
);

for (size_t i = 0; i < lxb_dom_collection_length(col); i++) {
    lxb_dom_element_t *div = lxb_dom_collection_element(col, i);
    /* Process each <div> element */
}

lxb_dom_collection_destroy(col, true);
```

### By Class Name

Finds all elements with the given class name:

```C
lxb_dom_collection_t *col = lxb_dom_collection_make(&document->dom_document, 16);

lxb_dom_elements_by_class_name(
    lxb_dom_interface_element(document->body), col,
    (const lxb_char_t *) "highlight", 9
);

/* Process results... */

lxb_dom_collection_destroy(col, true);
```

### By Attribute

Find elements by attribute name and value with several matching modes:

```C
lxb_dom_collection_t *col = lxb_dom_collection_make(&document->dom_document, 16);

/* Exact match: data-type="primary" */
lxb_dom_elements_by_attr(root, col,
    (const lxb_char_t *) "data-type", 9,
    (const lxb_char_t *) "primary", 7,
    true /* case_insensitive */);

/* Value begins with: href starts with "https" */
lxb_dom_elements_by_attr_begin(root, col,
    (const lxb_char_t *) "href", 4,
    (const lxb_char_t *) "https", 5,
    false);

/* Value ends with: src ends with ".png" */
lxb_dom_elements_by_attr_end(root, col,
    (const lxb_char_t *) "src", 3,
    (const lxb_char_t *) ".png", 4,
    false);

/* Value contains: class contains "btn" */
lxb_dom_elements_by_attr_contain(root, col,
    (const lxb_char_t *) "class", 5,
    (const lxb_char_t *) "btn", 3,
    false);

lxb_dom_collection_destroy(col, true);
```

**Note:** For more advanced element searching, use the [Selectors](selectors.md) module which supports full CSS selector syntax.

## Text Content

### Reading Text Content

The `lxb_dom_node_text_content()` function returns the concatenated text content of a node and all its descendants:

```C
size_t len;
lxb_char_t *text = lxb_dom_node_text_content(node, &len);

if (text != NULL) {
    printf("Text: %.*s\n", (int) len, text);
}
```

The behavior depends on node type:
- **Element, DocumentFragment** — concatenates all descendant text nodes
- **Text, Comment, ProcessingInstruction** — returns the node's own text data
- **Document, DocumentType** — returns NULL

**Memory note:** The returned string is allocated from the document's text memory pool. It will be freed when the document is destroyed. If you need to free it earlier, use `lxb_dom_document_destroy_text(node->owner_document, text)`.

### Setting Text Content

```C
lxb_status_t status = lxb_dom_node_text_content_set(node,
    (const lxb_char_t *) "New text content", 16);
```

For Element nodes, this:
1. Removes all existing children of the element
2. Creates a single Text node with the given content
3. Appends it as the only child

### CharacterData Nodes

Text, Comment, and CDATA Section nodes all extend `lxb_dom_character_data_t`, which holds the text data directly:

```C
struct lxb_dom_character_data {
    lxb_dom_node_t node;
    lexbor_str_t   data;    /* The actual text content */
};
```

You can access the text data through the `data` field after casting:

```C
if (lxb_dom_node_type(node) == LXB_DOM_NODE_TYPE_TEXT) {
    lxb_dom_character_data_t *cdata = lxb_dom_interface_character_data(node);

    printf("Text: %.*s\n",
           (int) cdata->data.length,
           cdata->data.data);
}
```

You can also replace a portion of the text:

```C
/* Replace 5 characters starting at offset 6 with new text */
lxb_dom_character_data_replace(cdata,
    (const lxb_char_t *) "replaced", 8,
    6,  /* offset */
    5   /* count to replace */);
```

## Collections

Collections are simple dynamic arrays used to hold search results. They are used by functions like `lxb_dom_elements_by_tag_name()`, `lxb_dom_elements_by_class_name()`, etc.

### Creating and Using Collections

```C
/* Create a collection (16 is the initial capacity) */
lxb_dom_collection_t *col = lxb_dom_collection_make(&document->dom_document, 16);
if (col == NULL) {
    return EXIT_FAILURE;
}

/* Fill it with search results */
lxb_dom_elements_by_tag_name(root, col,
    (const lxb_char_t *) "a", 1);

/* Access results */
size_t count = lxb_dom_collection_length(col);

for (size_t i = 0; i < count; i++) {
    /* Get as element */
    lxb_dom_element_t *el = lxb_dom_collection_element(col, i);

    /* Or get as node */
    lxb_dom_node_t *node = lxb_dom_collection_node(col, i);
}

/* Reuse for another search */
lxb_dom_collection_clean(col);
lxb_dom_elements_by_tag_name(root, col,
    (const lxb_char_t *) "div", 3);

/* Destroy when done */
lxb_dom_collection_destroy(col, true);
```

**Key points:**
- Collections grow automatically as needed
- `lxb_dom_collection_clean()` resets the collection without freeing memory — efficient for reuse
- The collection does **not** own the nodes it contains — destroying the collection does not destroy the nodes

## Memory Management

### Two-Pool Architecture

The Document owns two separate memory pools:

```C
struct lxb_dom_document {
    /* ... */
    lexbor_mraw_t *mraw;    /* Pool for node structures */
    lexbor_mraw_t *text;    /* Pool for text data (attribute values, text content) */
    /* ... */
};
```

**Why two pools?**
- **Structure pool (`mraw`)** — allocates fixed-size structures (nodes, elements, attributes). These are uniform in size and benefit from pool allocation.
- **Text pool (`text`)** — allocates variable-length strings (text content, attribute values). These vary in size and need different allocation strategy.

### Allocation

All DOM objects must be created through the Document. Never `malloc()` DOM nodes directly:

```C
/* Correct — uses document's memory pool */
lxb_dom_element_t *el = lxb_dom_document_create_element(doc, ...);

/* Also correct — low-level struct allocation */
void *mem = lxb_dom_document_create_struct(doc, sizeof(my_struct));
```

### Cleanup

When you destroy a document, **all** memory allocated from its pools is freed at once — every node, every attribute, every text string. You don't need to destroy individual nodes:

```C
/* This frees everything — all nodes, all text, all attributes */
lxb_html_document_destroy(document);
```

If you need to free an individual node before the document is destroyed (for example, to reduce memory usage), you can:

```C
/* Remove from tree first, then destroy */
lxb_dom_node_remove(node);
lxb_dom_node_destroy_deep(node);
```

### Document Inheritance

Documents can share memory pools. When a document is created with an owner document, it inherits the owner's pools:

```C
/* doc2 shares memory pools with doc1 */
lxb_dom_document_t *doc2 = lxb_dom_document_create(doc1);
```

This is used internally for fragment parsing — the fragment document shares pools with the main document, so nodes can be moved between them without copying.

You can check whether a document owns its own pools:

```C
bool is_original = lxb_dom_document_is_original(document);
```

## Node Callbacks

The Document supports callbacks that are triggered when nodes are modified. This is used internally for CSS integration, but you can install your own callbacks:

```C
typedef struct {
    lxb_dom_node_cb_insert_f    insert;    /* Called when a node is inserted */
    lxb_dom_node_cb_remove_f    remove;    /* Called when a node is removed */
    lxb_dom_node_cb_destroy_f   destroy;   /* Called when a node is destroyed */
    lxb_dom_node_cb_set_value_f set_value; /* Called when an attribute value changes */
} lxb_dom_document_node_cb_t;
```

These callbacks are stored in `document->node_cb`. The `set_value` callback is only triggered for attribute value changes, while `insert`, `remove`, and `destroy` are called for all node types.

**Note:** The `_wo_events` variants of tree manipulation functions bypass these callbacks entirely.
