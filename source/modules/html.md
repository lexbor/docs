# HTML Module

* **Version:** 2.8.0
* **Path:** `source/lexbor/html`
* **Base Includes:** `lexbor/html/html.h`
* **Examples:** `examples/lexbor/html`
* **Specification:** [WHATWG HTML Living Standard](https://html.spec.whatwg.org/)

## Overview

The HTML module implements [WHATWG HTML Living Standard](https://html.spec.whatwg.org/) for parsing and serializing HTML documents.
The HTML module provides a complete, specification-compliant HTML parser. Yes, it's HTML5, but the current standard is called "Living Standard" — and this module adheres to it.

## Key Features

- **Specification Compliant** — passes all HTML5 tree construction tests
- **Extremely Fast** — optimized for performance
- **Streaming Support** — parse HTML by chunks for large documents
- **Fragment Parsing** — supports parsing HTML fragments (innerHTML)
- **Error Recovery** — handles malformed HTML gracefully following the spec
- **Production Tested** — tested with ASAN on 200+ million real-world pages
- **Two Parsing Modes**:
  - **Document mode** — simple high-level API for complete document parsing
  - **Parser mode** — direct parser control for advanced use cases

## What's Inside

- **[Parser](#parsing)** — high-level API combining tokenizer and tree builder
- **[Fragment Parser](#parsing-html-fragment)** — parses HTML fragments with context element (innerHTML)
- **[Serialization](#serialization)** — converts DOM tree back to HTML text with formatting options
- **[HTML Interfaces](#element-interfaces)** — 90+ HTML element interfaces (HTMLDivElement, HTMLInputElement, etc.)
- **[Tokenizer](#tokenizer)** — converts HTML text into tokens according to WHATWG spec
- **[Tree Builder](#tree-builder)** — constructs a DOM tree from tokens with proper error handling
- **[Encoding Detection](#encoding-detection)** — determines character encoding from byte stream

## Quick Start

### Basic Document Parsing

```C
#include <lexbor/html/html.h>

int main(void)
{
    const lxb_char_t html[] = "<div>Hello, World!</div>";

    /* Create document */
    lxb_html_document_t *document = lxb_html_document_create();
    if (document == NULL) {
        return EXIT_FAILURE;
    }

    /* Parse HTML */
    lxb_status_t status = lxb_html_document_parse(document, html,
                                                  sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_html_document_destroy(document);
        return EXIT_FAILURE;
    }

    /* Access parsed elements */
    lxb_dom_element_t *body = lxb_dom_interface_element(document->body);
    lxb_dom_node_t *div = lxb_dom_node_first_child(lxb_dom_interface_node(body));

    /* Get text content */
    size_t text_len;
    const lxb_char_t *text = lxb_dom_node_text_content(div, &text_len);

    printf("Text: %.*s\n", (int) text_len, text);

    /* Free all allocated resources */
    lxb_html_document_destroy(document);

    return 0;
}
```

## Parsing

The HTML module provides two distinct approaches for parsing HTML documents, each optimized for different use cases: **Document Parser** and **Parser**. Both approaches are fully spec-compliant and produce identical DOM trees, but differ in their level of control and API design.

### Parsing Approaches Overview

| Aspect | Document Parser | Parser |
|--------|----------------|--------|
| **API Style** | Simple, high-level | Low-level, explicit control |
| **Typical Use Case** | Standard HTML parsing | Advanced scenarios, custom processing |
| **Control Level** | Automatic | Manual |
| **Object Creation** | Document creates parser internally | You create parser explicitly |
| **Memory Management** | Document owns all resources | You manage parser lifecycle |
| **Best For** | Most applications | Custom tokenizer/tree callbacks, parser reuse |

### Location

All parsing functions are declared in `source/lexbor/html/parser.h` and `source/lexbor/html/interfaces/document.h`.

### Document Parser (Recommended for Most Use Cases)

The **Document Parser** is a high-level API that provides the simplest way to parse HTML. The document object internally manages the parser, tokenizer, and tree builder.

#### Key Features

- **Simple API** — one function call to parse entire HTML
- **Automatic resource management** — document owns and cleans up parser
- **Streaming support** — parse HTML in chunks for large documents
- **Fragment parsing** — parse HTML fragments (innerHTML)
- **Most common use case** — covers 95% of parsing scenarios

#### Basic Document Parsing

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div>Hello, World!</div>";

    /* Simple one-call parsing */
    lxb_html_document_t *doc = lxb_html_document_create();
    if (doc == NULL) {
        return EXIT_FAILURE;
    }

    /* Parse HTML document */
    lxb_status_t status = lxb_html_document_parse(doc, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_html_document_destroy(doc);
        return EXIT_FAILURE;
    }

    /* Clean up - also destroys internal parser */
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

#### Chunk Parsing (Streaming)

For large HTML documents or network streams, you can parse HTML incrementally:

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html_1[] = "<div>Hello, ";
    const lxb_char_t html_2[] = "World!</div>";

    /* Simple one-call parsing */
    lxb_html_document_t *doc = lxb_html_document_create();
    if (doc == NULL) {
        return EXIT_FAILURE;
    }

    /* For simplicity, we will omit checking the return values. */

    /* Begin chunk parsing */
    lxb_html_document_parse_chunk_begin(doc);

    /* Feed HTML chunks as they arrive */
    lxb_html_document_parse_chunk(doc, html_1, sizeof(html_1) - 1);
    lxb_html_document_parse_chunk(doc, html_1, sizeof(html_2) - 1);

    /* Finalize parsing */
    lxb_html_document_parse_chunk_end(doc);

    /* Clean up - also destroys internal parser */
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

#### Fragment Parsing (innerHTML)

Parse HTML fragments with a context element:

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div>Hello, World!</div>";

    /* Simple one-call parsing */
    lxb_html_document_t *doc = lxb_html_document_create();
    if (doc == NULL) {
        return EXIT_FAILURE;
    }

    /* Parse HTML document */
    lxb_status_t status = lxb_html_document_parse(doc, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_html_document_destroy(doc);
        return EXIT_FAILURE;
    }

    /* Parse a fragment */
    const lxb_char_t fragment[] = "<p>Paragraph</p><span>Text</span>";
    lxb_dom_element_t *context = lxb_dom_interface_element(doc->body);

    lxb_dom_node_t *frag_root = lxb_html_document_parse_fragment(doc, context, fragment,
                                                                 sizeof(fragment) - 1);

    /* Work with frag_root... */

    /* Clean up - also destroys internal parser */
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

### Parser (Advanced Control)

The **Parser** approach gives you explicit control over the parser object. This is useful when you need to:

- Reuse the same parser for multiple documents
- Install custom tokenizer or tree builder callbacks
- Access parser internals during parsing
- Manage parser lifecycle independently

**Note:** The documents created are not linked to the parser in any way, i.e. after creating a document (lxb_html_parse()), the parser can be destroyed and you can continue working with the document.

#### Key Features

- **Explicit control** — you create and manage the parser
- **Parser reuse** — parse multiple documents with one parser
- **Custom callbacks** — hook into tokenizer and tree builder
- **Direct access** — access tokenizer and tree objects
- **Advanced scenarios** — custom parsing logic

#### Basic Parser Usage

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div>Hello, World!</div>";

    /* Create parser explicitly */
    lxb_html_parser_t *parser = lxb_html_parser_create();
    lxb_status_t status = lxb_html_parser_init(parser);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Parse HTML - returns a new document */
    lxb_html_document_t *doc = lxb_html_parse(parser, html, sizeof(html) - 1);
    if (doc == NULL) {
        goto failed;
    }

    /* Use the document */
    lxb_dom_element_t *body = lxb_dom_interface_element(doc->body);

    /* Cleanup - parser and document are independent */
    lxb_html_document_destroy(doc);
    lxb_html_parser_destroy(parser);

    return EXIT_SUCCESS;

failed:

    lxb_html_parser_destroy(parser);
    return EXIT_FAILURE;
}
```

#### Parser Reuse

The parser can be reused for multiple documents:

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t first_html[] = "<div>Hello</div>";
    const lxb_char_t second_html[] = "<div>World!</div>";

    /* Create parser explicitly */
    lxb_html_parser_t *parser = lxb_html_parser_create();
    lxb_status_t status = lxb_html_parser_init(parser);
    if (status != LXB_STATUS_OK) {
        lxb_html_parser_destroy(parser);
        return EXIT_FAILURE;
    }

    /* Parse first document */
    lxb_html_document_t *doc_first = lxb_html_parse(parser, first_html,
                                                    sizeof(first_html) - 1);

    /* Reset parser state */
    lxb_html_parser_clean(parser);

    /* Parse second document */
    lxb_html_document_t *doc_second = lxb_html_parse(parser, second_html,
                                                     sizeof(second_html) - 1);

    /* Cleanup - parser and document are independent */
    lxb_html_document_destroy(doc_first);
    lxb_html_document_destroy(doc_second);
    lxb_html_parser_destroy(parser);

    return EXIT_SUCCESS;
}
```

#### Chunk Parsing (Streaming)

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html_1[] = "<div>Hello, ";
    const lxb_char_t html_2[] = "World!</div>";

    /* Create parser explicitly */
    lxb_html_parser_t *parser = lxb_html_parser_create();
    lxb_status_t status = lxb_html_parser_init(parser);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* For simplicity, we will omit checking the return values. */

    /* Begin chunk parsing */
    lxb_html_document_t *doc = lxb_html_parse_chunk_begin(parser);

    /* Feed chunks */
    lxb_html_parse_chunk_process(parser, html_1, sizeof(html_1) - 1);
    lxb_html_parse_chunk_process(parser, html_2, sizeof(html_2) - 1);

    /* End parsing */
    lxb_html_parse_chunk_end(parser);

    /* Cleanup - parser and document are independent */
    lxb_html_document_destroy(doc);
    lxb_html_parser_destroy(parser);

    return EXIT_SUCCESS;

failed:

    lxb_html_parser_destroy(parser);
    return EXIT_FAILURE;
}
```

#### Fragment Parsing (innerHTML)

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div>Hello, World!</div>";

    /* Create parser explicitly */
    lxb_html_parser_t *parser = lxb_html_parser_create();
    lxb_status_t status = lxb_html_parser_init(parser);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Parse HTML - returns a new document */
    lxb_html_document_t *doc = lxb_html_parse(parser, html, sizeof(html) - 1);
    if (doc == NULL) {
        goto failed;
    }

    /* Use the document */
    lxb_dom_element_t *body = lxb_dom_interface_element(doc->body);

    /* Parse fragment by tag ID */
    const lxb_char_t fragment[] = "<li>Item 1</li><li>Item 2</li>";

    lxb_dom_node_t *frag_root = lxb_html_parse_fragment_by_tag_id(parser, doc,
                                                                  LXB_TAG_UL, LXB_NS_HTML,
                                                                  fragment, sizeof(fragment) - 1);
    /* Work with frag_root... */

    /* Cleanup - parser and document are independent */
    lxb_html_document_destroy(doc);
    lxb_html_parser_destroy(parser);

    return EXIT_SUCCESS;

failed:

    lxb_html_parser_destroy(parser);
    return EXIT_FAILURE;
}
```

### Memory and Performance

**Document Parser:**
- Creates internal parser once per document
- Parser destroyed with document
- Slightly more overhead per parse (negligible for most uses)

**Parser:**
- Single parser allocation for multiple parses
- Must manage parser lifecycle manually
- Better for parsing many small documents
- Reduces allocation overhead

**Performance Note:** The difference is typically negligible unless you're parsing thousands of small documents. For most applications, the Document Parser's simplicity outweighs any performance difference.

## Parsing HTML Fragment

The HTML module supports parsing HTML fragments using a context element. This functionality is essential for operations like setting `innerHTML` on an element or parsing partial HTML snippets.

Fragment parsing differs from document parsing in several key ways:

- **Context Element** — fragments are parsed relative to a context element (e.g., parsing as if inside a `<div>` or `<ul>`)
- **No Document Structure** — fragments don't create `<html>`, `<head>`, or `<body>` elements
- **Return Value** — always returns a special HTML node in the HTML namespace, with parsed fragment nodes as children
- **Spec Compliance** — follows WHATWG HTML fragment parsing algorithm

### Location

All fragment parsing functions are declared in `source/lexbor/html/parser.h` and `source/lexbor/html/interfaces/document.h`.

### Fragment Parsing Functions

The HTML module provides multiple functions for parsing fragments:

#### Document-Based Fragment Parsing

```C
/* Parse fragment with an element as context */
lxb_dom_node_t *
lxb_html_document_parse_fragment(lxb_html_document_t *document,
                                 lxb_dom_element_t *element,
                                 const lxb_char_t *html, size_t size);

/* Chunk-based fragment parsing */
lxb_status_t
lxb_html_document_parse_fragment_chunk_begin(lxb_html_document_t *document,
                                             lxb_dom_element_t *element);

lxb_status_t
lxb_html_document_parse_fragment_chunk(lxb_html_document_t *document,
                                       const lxb_char_t *html, size_t size);

lxb_dom_node_t *
lxb_html_document_parse_fragment_chunk_end(lxb_html_document_t *document);
```

#### Parser-Based Fragment Parsing

```C
/* Parse fragment with an element as context */
lxb_dom_node_t *
lxb_html_parse_fragment(lxb_html_parser_t *parser,
                        lxb_html_element_t *element,
                        const lxb_char_t *html, size_t size);

/* Parse fragment by tag ID (without creating context element) */
lxb_dom_node_t *
lxb_html_parse_fragment_by_tag_id(lxb_html_parser_t *parser,
                                  lxb_html_document_t *document,
                                  lxb_tag_id_t tag_id, lxb_ns_id_t ns,
                                  const lxb_char_t *html, size_t size);

/* Chunk-based fragment parsing */
lxb_status_t
lxb_html_parse_fragment_chunk_begin(lxb_html_parser_t *parser,
                                    lxb_html_document_t *document,
                                    lxb_tag_id_t tag_id, lxb_ns_id_t ns);

lxb_status_t
lxb_html_parse_fragment_chunk_process(lxb_html_parser_t *parser,
                                      const lxb_char_t *html, size_t size);

lxb_dom_node_t *
lxb_html_parse_fragment_chunk_end(lxb_html_parser_t *parser);
```

### Return Value Structure

**Important:** Fragment parsing always returns a special container node:

- **Node Type:** `LXB_DOM_NODE_TYPE_ELEMENT`
- **Tag ID:** `LXB_TAG_HTML` (HTML element)
- **Namespace:** `LXB_NS_HTML` (HTML namespace)
- **Children:** The actual parsed fragment nodes

The returned node acts as a container for the parsed fragment. To access the parsed content, iterate through its children:

```C
lxb_dom_node_t *fragment_root = lxb_html_document_parse_fragment(doc, context, html, html_size);

/* The fragment_root itself is just a container */
/* Real parsed nodes are in its children */
lxb_dom_node_t *child = lxb_dom_node_first_child(fragment_root);

while (child != NULL) {
    /* Process each parsed node from the fragment */
    child = lxb_dom_node_next(child);
}
```

### Context Element

The context element determines how the fragment is parsed:

- Parsing `<li>Item</li>` with context `<ul>` → valid list item
- Parsing `<td>Cell</td>` with context `<table>` → creates intermediate `<tbody>` and `<tr>`
- Parsing `<option>Choice</option>` with context `<select>` → valid option

The context affects:
- Which tags are allowed
- How parsing states transition
- Whether implicit tags are created
- How the fragment is inserted into the tree

## Serialization

The HTML module provides comprehensive serialization functionality to convert DOM trees (or parts of them) back into HTML text.

### Features

- **Multiple output modes** — serialize to string or use callbacks for streaming
- **Flexible scope** — serialize single node, node with children, or entire subtree
- **Pretty printing** — format output with indentation for readability
- **Customizable options** — skip whitespace, comments, control formatting

### Functions

The module provides three main serialization modes, each with string and callback variants:

### Location

All functions are declared in `source/lexbor/html/serialize.h` and implemented in `source/lexbor/html/serialize.c`.

#### Basic Serialization Functions

The functions output valid HTML as required by the specification.

| Function | Description |
|----------|-------------|
| `lxb_html_serialize_str()` | Serialize single node to string (no children) |
| `lxb_html_serialize_cb()` | Serialize single node via callback (no children) |
| `lxb_html_serialize_tree_str()` | Serialize node with direct children to string |
| `lxb_html_serialize_tree_cb()` | Serialize node with direct children via callback |
| `lxb_html_serialize_deep_str()` | Serialize direct children (without node) to string |
| `lxb_html_serialize_deep_cb()` | Serialize direct children (without node) via callback |

#### Pretty Print Functions

The functions generate “pretty” HTML that is not valid; for easy to read and understand structure.

| Function | Description |
|----------|-------------|
| `lxb_html_serialize_pretty_str()` | Pretty print single node to string |
| `lxb_html_serialize_pretty_cb()` | Pretty print single node via callback |
| `lxb_html_serialize_pretty_tree_str()` | Pretty print node with children to string |
| `lxb_html_serialize_pretty_tree_cb()` | Pretty print node with children via callback |
| `lxb_html_serialize_pretty_deep_str()` | Pretty print direct children (without node) to string |
| `lxb_html_serialize_pretty_deep_cb()` | Pretty print direct children (without node) via callback |

### String vs Callback Output

#### String Output

Serializes to a `lexbor_str_t` structure (dynamic string):

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div><a>x</x><!-- Comment --></div>";

    /* Parse HTML document */
    lxb_html_document_t *doc = lxb_html_document_create();
    lxb_status_t status = lxb_html_document_parse(doc, html, sizeof(html) - 1);
    /* Check doc for NULL and status */

    lxb_dom_node_t *node = lxb_dom_interface_node(doc->body);

    /* Serialization */
    lexbor_str_t str = {0};
    status = lxb_html_serialize_deep_str(node, &str);
    /* Check status */

    printf("Serialized Output:\n%s\n", str.data);

    /* No need if we call lxb_html_document_destroy() */
    lexbor_str_destroy(&str, doc->dom_document.text, false);
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

**Example Output:**

```html
Serialized Output:
<div><a>x<!-- Comment --></a></div>
```

String output always null-terminates the data if returned status is `LXB_STATUS_OK`.
**Important:** Always initialize `lexbor_str_t` to `{0}` and destroy it using the document's text allocator (`doc->dom_document.text`).

#### Callback Output

Uses a callback function for streaming output (useful for large documents or writing directly to files/network):

```C
#include <lexbor/html/html.h>

lxb_status_t
my_callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}

int main(void) {
    const lxb_char_t html[] = "<div><a>x</x><!-- Comment --></div>";

    /* Parse HTML document */
    lxb_html_document_t *doc = lxb_html_document_create();
    lxb_status_t status = lxb_html_document_parse(doc, html, sizeof(html) - 1);
    /* Check doc for NULL and status */

    lxb_dom_node_t *node = lxb_dom_interface_node(doc->body);

    /* Serialization */
    printf("Serialized Output:\n");

    status = lxb_html_serialize_deep_cb(node, my_callback, NULL);
    /* Check status */

    printf("\n");

    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

**Example Output:**

```html
Serialized Output:
<div><a>x<!-- Comment --></a></div>
```

### Pretty Printing

Pretty print functions format HTML with indentation for readability:

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div><a>x</x><!-- Comment --></div>";

    /* Parse HTML document */
    lxb_html_document_t *doc = lxb_html_document_create();
    lxb_html_document_parse(doc, html, sizeof(html) - 1);

    lxb_dom_node_t *root = lxb_dom_interface_node(doc->body);

    /* Pretty print with default options and 4-space indentation */
    lexbor_str_t str = {0};
    lxb_html_serialize_pretty_deep_str(root, LXB_HTML_SERIALIZE_OPT_UNDEF, 4, &str);

    printf("%s\n", str.data);

    /* Cleanup */
    /* No need if we call lxb_html_document_destroy() */
    lexbor_str_destroy(&str, doc->dom_document.text, false);
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

**Example Output:**

```html
<div>
  <a>
    "x"
    <!--  Comment  -->
  </a>
</div>
```

### Serialization Options

The `lxb_html_serialize_opt_t` is a **bitfield** that controls serialization behavior.
Multiple options can be combined using bitwise OR (`|`):

| Option | Description |
|--------|-------------|
| `LXB_HTML_SERIALIZE_OPT_UNDEF` | Default behavior (no options set) |
| `LXB_HTML_SERIALIZE_OPT_SKIP_WS_NODES` | Skip whitespace-only text nodes |
| `LXB_HTML_SERIALIZE_OPT_SKIP_COMMENT` | Skip comment nodes |
| `LXB_HTML_SERIALIZE_OPT_RAW` | Serialize raw content (no escaping) |
| `LXB_HTML_SERIALIZE_OPT_WITHOUT_CLOSING` | Don't serialize closing tags |
| `LXB_HTML_SERIALIZE_OPT_TAG_WITH_NS` | Include namespace prefixes |
| `LXB_HTML_SERIALIZE_OPT_WITHOUT_TEXT_INDENT` | Don't indent text content |
| `LXB_HTML_SERIALIZE_OPT_FULL_DOCTYPE` | Serialize full DOCTYPE declaration |

**Example - combining options:**

```C
#include <lexbor/html/html.h>

int main(void) {
    const lxb_char_t html[] = "<div><a>x</x><!-- Comment --></div>";

    /* Parse HTML document */
    lxb_html_document_t *doc = lxb_html_document_create();
    lxb_status_t status = lxb_html_document_parse(doc, html, sizeof(html) - 1);
    /* Check doc for NULL and status */

    lxb_dom_node_t *node = lxb_dom_interface_node(doc->body);

    /* Skip comments and without closing tags */
    lxb_html_serialize_opt_t opts = LXB_HTML_SERIALIZE_OPT_SKIP_COMMENT
                                    | LXB_HTML_SERIALIZE_OPT_WITHOUT_CLOSING;

    lexbor_str_t str = {0};
    status = lxb_html_serialize_pretty_deep_str(node, opts, 2, &str);
    /* Check status */

    printf("Serialized Output:\n%s\n", str.data);

    /* No need if we call lxb_html_document_destroy() */
    lexbor_str_destroy(&str, doc->dom_document.text, false);
    lxb_html_document_destroy(doc);

    return EXIT_SUCCESS;
}
```

### Memory Management

**String Output:**

- Always initialize `lexbor_str_t` to `{0}` before use.
- Destroy the string using the document's text allocator after use.

```C
/* Always initialize to {0} */
lexbor_str_t str = {0};

/* Serialize */
lxb_html_serialize_deep_str(node, &str);

/* Use the string */
printf("%s\n", str.data);

/* IMPORTANT: Destroy using document's allocator */
lexbor_str_destroy(&str, doc->dom_document.text, false);
```

### Error Handling

All serialization functions return `lxb_status_t`:

```C
lxb_status_t status = lxb_html_serialize_deep_str(node, &str);

if (status != LXB_STATUS_OK) {
    fprintf(stderr, "Serialization failed with status: %d\n", status);
    return EXIT_FAILURE;
}
```

## Element Interfaces

The HTML module implements over 90 element interfaces (like `lxb_html_div_element_t`, `lxb_html_input_element_t`, etc.) that correspond to HTML elements. These interfaces use a "poor man's inheritance" pattern — a technique for simulating object-oriented inheritance in C through struct composition.

### Location

All interfaces are defined in `source/lexbor/html/interface.h` and `source/lexbor/html/interfaces/`.

### How Interface Inheritance Works

In lexbor, interfaces form an inheritance chain using struct embedding. Each specialized interface contains its parent interface as the **first field**, allowing safe type casting between parent and child types.

**Inheritance Chain Example:**

```C
lxb_dom_event_target_t (base)
    ↓ (first field in lxb_dom_node_t)
lxb_dom_node_t
    ↓ (first field in lxb_dom_element_t)
lxb_dom_element_t
    ↓ (first field in lxb_html_element_t)
lxb_html_element_t
    ↓ (first field in lxb_html_div_element_t)
lxb_html_div_element_t
```

**Actual Struct Definitions:**

```C
/* Base: Event Target */
struct lxb_dom_event_target {
    /* event target fields */
};

/* Level 1: Node (contains Event Target as first field) */
struct lxb_dom_node {
    lxb_dom_event_target_t event_target;  // First field!

    uintptr_t              local_name;
    uintptr_t              ns;
    /* ... more node fields ... */
};

/* Level 2: Element (contains Node as first field) */
struct lxb_dom_element {
    lxb_dom_node_t    node;  // First field!

    lxb_dom_attr_id_t upper_name;
    lxb_dom_attr_id_t qualified_name;
    lxb_dom_attr_t    *first_attr;
    /* ... more element fields ... */
};

/* Level 3: HTML Element (contains DOM Element as first field) */
struct lxb_html_element {
    lxb_dom_element_t element;  // First field!
};

/* Level 4: Specialized HTML Element (contains HTML Element as first field) */
struct lxb_html_div_element {
    lxb_html_element_t element;  // First field!
    /* Div-specific fields would go here */
};
```

### Why the First Field Position Matters

By placing the parent struct as the **first field**, the memory address of the child struct is identical to the address of its parent field. This allows zero-cost casting:

```C
lxb_html_div_element_t *div = /* ... */;

/* These all point to THE SAME memory address: */
lxb_html_div_element_t *div_ptr      = div;                            // 0x1000
lxb_html_element_t     *html_elem    = &div->element;                  // 0x1000
lxb_dom_element_t      *dom_elem     = &div->element.element;          // 0x1000
lxb_dom_node_t         *node         = &div->element.element.node;     // 0x1000
lxb_dom_event_target_t *event_target = &div->element.element.node.event_target; // 0x1000
```

### Safe Casting with Helper Macros

Lexbor provides type-casting macros for converting between interface types:

```C
/* DOM interface casting macros (from dom/interface.h) */
#define lxb_dom_interface_node(obj)    ((lxb_dom_node_t *) (obj))
#define lxb_dom_interface_element(obj) ((lxb_dom_element_t *) (obj))

/* HTML interface casting macros (from html/interface.h) */
#define lxb_html_interface_element(obj) ((lxb_html_element_t *) (obj))
#define lxb_html_interface_div(obj)     ((lxb_html_div_element_t *) (obj))
#define lxb_html_interface_input(obj)   ((lxb_html_input_element_t *) (obj))
/* ... and 90+ more element types ... */
```

You can find all casting macros in the header files `source/lexbor/dom/interface.h` and `source/lexbor/html/interface.h`.

**Usage Example:**

```C
const lxb_char_t html[] = "<div>Hello, World!</div>";

/* Parse HTML and get a div element */
lxb_html_document_t *doc = lxb_html_document_create();
lxb_html_document_parse(doc, html, sizeof(html) - 1);

lxb_dom_element_t *body = lxb_dom_interface_element(doc->body);
lxb_dom_node_t *child = lxb_dom_node_first_child(lxb_dom_interface_node(body));

/* Cast to specialized div element if needed */
lxb_html_div_element_t *div = lxb_html_interface_div(child);

/* Access parent interface methods via casting */
lxb_dom_node_t *next = lxb_dom_node_next(lxb_dom_interface_node(div));

/* Get node properties */
lxb_tag_id_t tag_id = lxb_dom_node_tag_id(lxb_dom_interface_node(div));
```

### How to Determine the Element/Node Type

Before casting a node to a specialized interface type (like `lxb_html_input_element_t *`), you must verify that the cast is safe. This requires checking three key properties:

1. **Node Type** — determines the general category (Element, Text, Comment, etc.)
2. **Namespace** — identifies the XML/HTML namespace (HTML, SVG, MathML, etc.)
3. **Tag ID** — identifies the specific element tag (DIV, INPUT, SPAN, etc.)

#### Step 1: Check Node Type

The `node->type` field indicates the fundamental node category:

```C
typedef enum {
    LXB_DOM_NODE_TYPE_ELEMENT                = 0x01,  // <div>, <input>, etc.
    LXB_DOM_NODE_TYPE_ATTRIBUTE              = 0x02,  // class="foo"
    LXB_DOM_NODE_TYPE_TEXT                   = 0x03,  // Text content
    LXB_DOM_NODE_TYPE_CDATA_SECTION          = 0x04,  // <![CDATA[...]]>
    /* ... */
}
lxb_dom_node_type_t;
```

You can find all node types in `source/lexbor/dom/interfaces/node.h`.

**Usage:**

```C
lxb_dom_node_t *node = /* ... */;

/* Get node type */
lxb_dom_node_type_t type = lxb_dom_node_type(node);

if (type == LXB_DOM_NODE_TYPE_ELEMENT) {
    /* Safe to cast to lxb_dom_element_t* */
    lxb_dom_element_t *element = lxb_dom_interface_element(node);
}
else if (type == LXB_DOM_NODE_TYPE_TEXT) {
    /* This is a text node, not an element */
    lxb_dom_text_t *text = lxb_dom_interface_text(node);
}
```

#### Step 2: Check Namespace

The `node->ns` field identifies the namespace. HTML elements must have the HTML namespace:

```C
typedef enum {
    /* ... other namespaces ... */
    LXB_NS_HTML   = 0x02,  // HTML namespace
    LXB_NS_MATH   = 0x03,  // MathML namespace
    LXB_NS_SVG    = 0x04,  // SVG namespace
    /* ... other namespaces ... */
}
lxb_ns_id_enum_t;
```

You can find all namespace IDs in `source/lexbor/ns/const.h`.
For more details, see the Namespaces Modul (`ns`).

**Usage:**

```C
lxb_dom_node_t *node = /* ... */;
lxb_ns_id_t ns = node->ns;

if (ns == LXB_NS_HTML) {
    /* This is an HTML element */
}
else if (ns == LXB_NS_SVG) {
    /* This is an SVG element */
}
```

#### Step 3: Check Tag ID

The `node->local_name` field stores the tag identifier. Each HTML/SVG/MathML tag has a unique ID:

```C
typedef enum {
    LXB_TAG__UNDEF       = 0x0000,  // Undefined
    LXB_TAG__TEXT        = 0x0002,  // Text node
    /* ... HTML tags ... */
    LXB_TAG_DIV          = 0x0033,  // <div>
    LXB_TAG_INPUT        = 0x006a,  // <input>
    LXB_TAG_SPAN         = 0x00c0,  // <span>
    LXB_TAG_BODY         = 0x001f,  // <body>
    LXB_TAG_A            = 0x0006,  // <a>
    /* ... 90+ more tags ... */
} lxb_tag_id_enum_t;
```

**Usage:**

```C
lxb_dom_node_t *node = /* ... */;
lxb_tag_id_t tag_id = lxb_dom_node_tag_id(node);

if (tag_id == LXB_TAG_INPUT) {
    /* Safe to cast to lxb_html_input_element_t * */
}
else if (tag_id == LXB_TAG_DIV) {
    /* Safe to cast to lxb_html_div_element_t * */
}
```

You can find all tag IDs in `source/lexbor/tag/const.h`.
For more details, see the Tag Module (`tag`).

### Complete Type Checking Example

Here's a comprehensive example showing safe type checking before casting:

```C
void process_element(lxb_dom_node_t *node)
{
    /* Step 1: Check if it's an element node */
    if (lxb_dom_node_type(node) != LXB_DOM_NODE_TYPE_ELEMENT) {
        printf("Not an element node\n");
        return;
    }

    /* Step 2: Check if it's in the HTML namespace */
    if (node->ns != LXB_NS_HTML) {
        printf("Not an HTML element (might be SVG or MathML)\n");
        return;
    }

    /* Step 3: Check the specific tag */
    lxb_tag_id_t tag_id = lxb_dom_node_tag_id(node);

    switch (tag_id) {
        case LXB_TAG_INPUT: {
            /* Safe to cast to input element */
            lxb_html_input_element_t *input = lxb_html_interface_input(node);
            printf("Found <input> element\n");
            /* Access input-specific fields here */
            break;
        }

        case LXB_TAG_DIV: {
            /* Safe to cast to div element */
            lxb_html_div_element_t *div = lxb_html_interface_div(node);
            printf("Found <div> element\n");
            break;
        }

        default: {
            /* Generic HTML element - use base interface */
            lxb_html_element_t *element = lxb_html_interface_element(node);
            printf("Generic HTML element\n");
            break;
        }
    }
}
```

### Practical Safe Casting Pattern

**Pattern 1: Full Check (Most Verbose)**

```C
lxb_dom_node_t *node = /* ... */;

/* Only cast to specialized type after verification */
if (lxb_dom_node_type(node) == LXB_DOM_NODE_TYPE_ELEMENT &&
    node->ns == LXB_NS_HTML &&
    lxb_dom_node_tag_id(node) == LXB_TAG_INPUT)
{
    lxb_html_input_element_t *input = lxb_html_interface_input(node);
    /* Now safe to use input-specific features */
}
```

### Optimization: Skip Redundant Checks

Not all three checks are always necessary. You can optimize based on what information you already have:

**Optimization 1: Tag ID Implies Node Type**

Certain tag IDs can only belong to specific node types, so checking the tag ID is sufficient:

```C
lxb_dom_node_t *node = /* ... */;
lxb_tag_id_t tag_id = lxb_dom_node_tag_id(node);

/* Special non-element tag IDs - no need to check node type */
if (tag_id == LXB_TAG__TEXT) {
    /* This is ALWAYS a text node */
    lxb_dom_text_t *text = lxb_dom_interface_text(node);
}
else if (tag_id == LXB_TAG__EM_COMMENT) {
    /* This is ALWAYS a comment node */
    lxb_dom_comment_t *comment = lxb_dom_interface_comment(node);
}
else if (tag_id == LXB_TAG__EM_DOCTYPE) {
    /* This is ALWAYS a DOCTYPE node */
    lxb_dom_document_type_t *doctype = lxb_dom_interface_document_type(node);
}
else if (tag_id == LXB_TAG__DOCUMENT) {
    /* This is ALWAYS a document node */
    lxb_dom_document_t *doc = lxb_dom_interface_document(node);
}
```

**Optimization 2: Element Tag ID + Namespace Check**

If you check a specific element tag ID (like `LXB_TAG_INPUT`, `LXB_TAG_DIV`), you already know it's an element — no need to check node type:

```C
lxb_dom_node_t *node = /* ... */;
lxb_tag_id_t tag_id = lxb_dom_node_tag_id(node);

/* LXB_TAG_INPUT can ONLY be an element, so skip type check */
if (tag_id == LXB_TAG_INPUT && node->ns == LXB_NS_HTML) {
    /* Safe - INPUT tag implies it's an element */
    lxb_html_input_element_t *input = lxb_html_interface_input(node);
}

/* Same for DIV, SPAN, and all other element tags */
if (tag_id == LXB_TAG_DIV && node->ns == LXB_NS_HTML) {
    lxb_html_div_element_t *div = lxb_html_interface_div(node);
}
```

**Why this works:** Element tag IDs (like `LXB_TAG_INPUT`, `LXB_TAG_DIV`) can only be assigned to element nodes. Text nodes always have `LXB_TAG__TEXT`, comments have `LXB_TAG__EM_COMMENT`, etc.

**Optimization 3: Namespace + Type Check for Generic Elements**

If you only need to verify it's an HTML element (without checking specific tag):

```C
lxb_dom_node_t *node = /* ... */;

/* Check it's an HTML element (skip tag check) */
if (lxb_dom_node_type(node) == LXB_DOM_NODE_TYPE_ELEMENT &&
    node->ns == LXB_NS_HTML) {
    /* Safe to use as generic HTML element */
    lxb_html_element_t *element = lxb_html_interface_element(node);
}
```

### Recommended Checking Strategy

**When to use each pattern:**

| Scenario | Checks Needed | Example |
|----------|---------------|---------|
| **Known special tag** (text, comment, doctype) | Tag ID only | `tag_id == LXB_TAG__TEXT` |
| **Known element tag** (div, input, span) | Tag ID + Namespace | `tag_id == LXB_TAG_INPUT && ns == LXB_NS_HTML` |
| **Generic HTML element** | Node Type + Namespace | `type == ELEMENT && ns == HTML` |
| **Unknown node** | All three checks | `type == ELEMENT && ns == HTML && tag_id == ...` |

**Practical Example with Optimizations:**

```C
void process_node_optimized(lxb_dom_node_t *node)
{
    lxb_tag_id_t tag_id = lxb_dom_node_tag_id(node);

    /* Optimization: Check tag ID first */
    switch (tag_id) {
        case LXB_TAG__TEXT:
            /* No type check needed - tag ID implies it's text */
            printf("Text node\n");
            break;

        case LXB_TAG__EM_COMMENT:
            /* No type check needed - tag ID implies it's comment */
            printf("Comment node\n");
            break;

        case LXB_TAG_INPUT:
            /* No type check needed - INPUT tag can only be an element */
            if (node->ns == LXB_NS_HTML) {
                lxb_html_input_element_t *input = lxb_html_interface_input(node);
                printf("HTML <input> element\n");
            }
            break;

        case LXB_TAG_DIV:
            /* No type check needed - DIV tag can only be an element */
            if (node->ns == LXB_NS_HTML) {
                lxb_html_div_element_t *div = lxb_html_interface_div(node);
                printf("HTML <div> element\n");
            }
            break;

        default:
            /* Unknown tag - need full check */
            if (lxb_dom_node_type(node) == LXB_DOM_NODE_TYPE_ELEMENT &&
                node->ns == LXB_NS_HTML) {
                lxb_html_element_t *element = lxb_html_interface_element(node);
                printf("Generic HTML element\n");
            }
            break;
    }
}
```

**Best Practice:** Check tag ID first when possible, as it often eliminates the need for other checks.

## Tokenizer

The tokenizer processes HTML input and produces tokens according to the WHATWG HTML specification. Each token represents a unit of HTML markup or content.

### Location

Tokenizer functions and structures are declared in `source/lexbor/html/tokenizer.h`, `source/lexbor/html/token.h`, `source/lexbor/html/token_attr.h`.

### Structure Overview

The tokenizer consists of several key structures:
- `lxb_html_tokenizer_t` — main tokenizer structure managing state and input
- `lxb_html_token_t` — represents individual tokens produced by the tokenizer
- `lxb_html_token_attr_t` — represents attributes associated with tags
- `lxb_html_token_type_t` — enumeration of token types and flags

### Token Structure

The `lxb_html_token_t` structure contains all information about a parsed token:

| Field | Type | Description |
|-------|------|-------------|
| `begin` | `const lxb_char_t *` | Token start position in input buffer |
| `end` | `const lxb_char_t *` | Token end position in input buffer |
| `text_start` | `const lxb_char_t *` | Text content start (for text, comment, DOCTYPE tokens) |
| `text_end` | `const lxb_char_t *` | Text content end |
| `attr_first` | `lxb_html_token_attr_t *` | Pointer to first attribute in linked list (NULL if no attributes) |
| `attr_last` | `lxb_html_token_attr_t *` | Pointer to last attribute in linked list |
| `base_element` | `void *` | Associated DOM element (internal use) |
| `null_count` | `size_t` | Number of NULL (`\0`) characters found in token (for error recovery) |
| `tag_id` | `lxb_tag_id_t` | Token type identifier (e.g., `LXB_TAG_DIV`, `LXB_TAG__TEXT`) |
| `type` | `lxb_html_token_type_t` | Bitfield flags (e.g., `LXB_HTML_TOKEN_TYPE_OPEN`, `LXB_HTML_TOKEN_TYPE_CLOSE_SELF`) |

### Token Type Flags (Bitfield)

The `type` field in `lxb_html_token_t` is a **bitfield** that holds flags describing token properties. Multiple flags can be combined using bitwise OR (`|`):

| Flag | Value | Description | Usage |
|------|-----------|-------------|-------|
| `LXB_HTML_TOKEN_TYPE_OPEN` | `0x0000` | Default state (no flags set) | Start tag: `<div>` |
| `LXB_HTML_TOKEN_TYPE_CLOSE` | `0x0001` | Token is a closing tag | End tag: `</div>` |
| `LXB_HTML_TOKEN_TYPE_CLOSE_SELF` | `0x0002` | Self-closing tag (void element) | `<br />`, `<img />` |
| `LXB_HTML_TOKEN_TYPE_FORCE_QUIRKS` | `0x0004` | DOCTYPE forces quirks mode | Malformed DOCTYPE |
| `LXB_HTML_TOKEN_TYPE_DONE` | `0x0008` | Token processing complete | Internal tokenizer state |

You can find all token type flags in `source/lexbor/html/token.h`.

### Example Usage

Here's a complete example showing how to use the tokenizer with a callback:

```C
#include <lexbor/html/html.h>

/* Token callback function */
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    /* Process the token */
    switch (token->tag_id) {
        case LXB_TAG_DIV:
            printf("Found <div> tag\n");
            break;

        case LXB_TAG__TEXT:
            printf("Found text node: %.*s\n",
                   (int) (token->text_end - token->text_start),
                   token->text_start);
            break;

        case LXB_TAG__EM_COMMENT:
            printf("Found comment\n");
            break;

        default:
            break;
    }

    /* Return token to continue processing */
    return token;
}
int main(void)
{
    lxb_status_t status;
    const lxb_char_t html[] = "<div>Hello</div><!-- comment -->";

    /* Create tokenizer */
    lxb_html_tokenizer_t *tkz = lxb_html_tokenizer_create();
    if (tkz == NULL) {
        return EXIT_FAILURE;
    }

    /* Initialize tokenizer */
    status = lxb_html_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Set token callback */
    lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);

    /* Begin tokenization */
    status = lxb_html_tokenizer_begin(tkz);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Process HTML chunk */
    status = lxb_html_tokenizer_chunk(tkz, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* End tokenization */
    status = lxb_html_tokenizer_end(tkz);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Clean up */
    lxb_html_tokenizer_destroy(tkz);

    return EXIT_SUCCESS;

failed:

    lxb_html_tokenizer_destroy(tkz);

    return EXIT_FAILURE;
}
```

**Example Output:**
```
Found <div> tag
Found text node: Hello
Found <div> tag
Found comment
```

#### CRITICAL: Token Memory Management and Return Value

**The tokenizer will use the token you return from the callback for the next token!**

The return value of your callback determines which token object the tokenizer will reuse for the next token:

- **If you return the same token** that was passed to you → the tokenizer reuses that token (single token approach, memory efficient)
- **If you return a new token** created with `lxb_html_token_create()` → the tokenizer uses the new token for the next iteration (accumulation approach)

This design allows you to choose between two strategies:

### Strategy 1: Single Token (Recommended - Memory Efficient)

Return the same token that was passed to you. The tokenizer will reuse this one token object for all subsequent tokens.

```C
static lxb_html_token_t *
single_token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    /* Process token immediately */
    printf("Tag ID: %zu\n", token->tag_id);

    /* Return the same token - tokenizer will reuse it */
    return token;
}
```

**Result:** Only one token object exists in memory throughout the entire tokenization process. Very fast and memory efficient.

### Strategy 2: Token Accumulation (Use When Necessary)

Return a newly created token. This allows you to store the current token and let the tokenizer use a fresh token for the next iteration.

```C
static lxb_html_token_t *stored_tokens[100];
static size_t token_count = 0;

static lxb_html_token_t *
accumulation_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    /* Store the current token */
    stored_tokens[token_count++] = token;

    /* Create a NEW token for the tokenizer to use next */
    lxb_html_token_t *new_token = lxb_html_token_create(tkz->dobj_token);
    if (new_token == NULL) {
        /* Handle error */
        return NULL;
    }

    /* Return the new token - tokenizer will use it for the next token */
    return new_token;
}

/* Don't forget to clean up stored tokens later! */
void cleanup_tokens(lxb_html_tokenizer_t *tkz)
{
    for (size_t i = 0; i < token_count; i++) {
        lxb_html_token_destroy(tkz->dobj_token, stored_tokens[i]);
    }
    token_count = 0;
}
```

**Result:** Each token is a separate object in memory. You can store and access all tokens, but this uses more memory.

### Why This Design?

This callback design gives you control over memory allocation:

1. **Performance**: If you only need to process tokens sequentially, use Strategy 1 (single token) for maximum performance
2. **Flexibility**: If you need to build a token list or AST, use Strategy 2 (accumulation) to keep all tokens in memory

### Important Notes

- **Always check for NULL**: If `lxb_html_token_create()` returns NULL, return NULL from your callback to signal an error
- **Memory management**: If you accumulate tokens, you are responsible for destroying them with `lxb_html_token_destroy()`
- **Don't mix strategies**: Choose one approach and stick with it throughout the tokenization
- **Attributes are separate**: Token attributes have their own memory management and may need deep copying with `lxb_html_token_deep_copy()`

### Complete Accumulation Example

```C
#include <lexbor/html/html.h>

typedef struct {
    lxb_html_token_t **tokens;
    size_t count;
    size_t capacity;
} token_storage_t;

static lxb_html_token_t *
store_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    token_storage_t *storage = (token_storage_t *) ctx;

    /* Store current token */
    if (storage->count < storage->capacity) {
        storage->tokens[storage->count++] = token;
    }

    /* Create new token for tokenizer */
    lxb_html_token_t *new_token = lxb_html_token_create(tkz->dobj_token);
    if (new_token == NULL) {
        return NULL;
    }

    return new_token;
}

int main(void)
{
    const lxb_char_t html[] = "<div>Hello</div><span>World</span>";

    /* Prepare storage */
    token_storage_t storage = {0};
    storage.capacity = 100;
    storage.tokens = malloc(storage.capacity * sizeof(lxb_html_token_t *));

    /* Create and setup tokenizer */
    lxb_html_tokenizer_t *tkz = lxb_html_tokenizer_create();
    lxb_html_tokenizer_init(tkz);
    lxb_html_tokenizer_tags_make(tkz, 128);
    lxb_html_tokenizer_callback_token_done_set(tkz, store_callback, &storage);

    /* Tokenize */
    lxb_html_tokenizer_begin(tkz);
    lxb_html_tokenizer_chunk(tkz, html, sizeof(html) - 1);
    lxb_html_tokenizer_end(tkz);

    /* Now you have all tokens stored */
    printf("Collected %zu tokens\n", storage.count);
    for (size_t i = 0; i < storage.count; i++) {
        printf("Token %zu: tag_id = %zu\n", i, storage.tokens[i]->tag_id);
    }

    /* Clean up stored tokens */
    for (size_t i = 0; i < storage.count; i++) {
        lxb_html_token_destroy(tkz->dobj_token, storage.tokens[i]);
    }
    free(storage.tokens);

    /* Clean up tokenizer */
    lxb_html_tokenizer_destroy(tkz);

    return 0;
}
```

**Key takeaway:** Return the same token for efficiency, or return a new token to accumulate them. The choice is yours!


## Tree Builder

The tree builder constructs the DOM tree from tokens produced by the tokenizer, following the WHATWG HTML parsing algorithm. It manages insertion modes, stack of open elements, and handles special cases like foreign content (SVG, MathML).

This is more of an internal set of functions that is of little use to third-party developers.
Tree construction functions can only be useful if the developer wants to build their tree using a tokenizer.

### Location

All tree builder functions and structures are declared in `source/lexbor/html/tree.h` and implemented in `source/lexbor/html/tree.c`, `source/lexbor/html/tree/`.

## Encoding Detection

The encoding detection functionality allows you to extract character encoding information from raw HTML byte streams. This is particularly useful when you need to determine the encoding before parsing the document, as HTML can declare its encoding in `<meta>` tags.

To convert one encoding to another, or a non-UTF-8 encoding (which the parser works with) to UTF-8, use the Encoding module.
Full work with encodings is available in `source/lexbor/engine/engine.c` in the `lxb_engine_parse()` function.

### Location

All encoding detection functions are declared in `source/lexbor/html/encoding.h`.

### What It Searches For

The encoding detector scans raw HTML for encoding declarations in the following places:

1. **`<meta charset="...">`** — HTML5 style charset declaration
   ```html
   <meta charset="UTF-8">
   ```

2. **`<meta http-equiv="Content-Type" content="...">`** — Legacy style with content attribute
   ```html
   <meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
   ```

The detector scans only the beginning of the HTML document (typically the first 1024 bytes) where meta tags are expected to appear according to the specification.
But how many bytes to scan is specified by the user, even if it's the entire HTML document.

### How It Works

The encoding detector implements a simplified HTML tokenizer that:

1. Searches for `<meta>` tags in the byte stream
2. Parses tag attributes without full HTML parsing
3. Extracts encoding names from `charset` or `content` attributes
4. Handles duplicate declarations correctly (first valid encoding wins)
5. Validates that `http-equiv="Content-Type"` is present when using the `content` attribute

The implementation follows the [WHATWG HTML Standard](https://html.spec.whatwg.org/#determining-the-character-encoding) for encoding detection.

### Functions

#### lxb_html_encoding_determine

Scans raw HTML data and extracts all encoding declarations.

```C
lxb_status_t
lxb_html_encoding_determine(lxb_html_encoding_t *em,
                            const lxb_char_t *data,
                            const lxb_char_t *end);
```

**Parameters:**
- `em` — encoding detector object
- `data` — pointer to raw HTML byte stream
- `end` — pointer to end of data

**Returns:** `LXB_STATUS_OK` on success, error status otherwise

**What it does:**
- Scans for `<meta>` tags in the HTML
- Extracts encoding from `charset` or `content` attributes
- Stores found encodings in the result array
- Can find multiple encoding declarations (though only first is typically used)

#### lxb_html_encoding_content

Extracts encoding name from a `content` attribute value.

```C
const lxb_char_t *
lxb_html_encoding_content(const lxb_char_t *data,
                          const lxb_char_t *end,
                          const lxb_char_t **name_end);
```

**Parameters:**
- `data` — pointer to content attribute value
- `end` — pointer to end of value
- `name_end` — output: pointer to end of encoding name

**Returns:** Pointer to encoding name, or `NULL` if not found

**What it does:**
- Searches for `charset=` pattern in the content string
- Handles quoted and unquoted values
- Extracts encoding name (e.g., "UTF-8", "windows-1251")

### Data Structures

```C
typedef struct {
    const lxb_char_t *name;  /* Pointer to encoding name */
    const lxb_char_t *end;   /* Pointer to end of name */
} lxb_html_encoding_entry_t;

typedef struct {
    lexbor_array_obj_t cache;   /* Internal cache for attribute deduplication */
    lexbor_array_obj_t result;  /* Array of found encoding entries */
} lxb_html_encoding_t;
```

### Usage Example

```C
#include <lexbor/html/encoding.h>

int main(void)
{
    const lxb_char_t html[] =
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        "  <meta charset=\"UTF-8\">"
        "  <title>Test</title>"
        "</head>"
        "<body>Content</body>"
        "</html>";

    /* Create and initialize encoding detector */
    lxb_html_encoding_t *enc = lxb_html_encoding_create();
    if (enc == NULL) {
        return EXIT_FAILURE;
    }

    lxb_status_t status = lxb_html_encoding_init(enc);
    if (status != LXB_STATUS_OK) {
        lxb_html_encoding_destroy(enc, true);
        return EXIT_FAILURE;
    }

    /* Detect encoding in raw HTML */
    status = lxb_html_encoding_determine(enc, html, html + sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_html_encoding_destroy(enc, true);
        return EXIT_FAILURE;
    }

    /* Get detected encodings */
    size_t count = lxb_html_encoding_meta_length(enc);

    for (size_t i = 0; i < count; i++) {
        lxb_html_encoding_entry_t *entry = lxb_html_encoding_meta_entry(enc, i);
        size_t name_len = entry->end - entry->name;

        printf("Found encoding: %.*s\n", (int) name_len, entry->name);
    }

    /* Clean up */
    lxb_html_encoding_destroy(enc, true);

    return 0;
}
```

**Output:**
```
Found encoding: UTF-8
```

### Reusing Encoding Detector

You can reuse the encoding detector object for multiple documents:

```C
lxb_html_encoding_t *enc = lxb_html_encoding_create();
lxb_html_encoding_init(enc);

/* First document */
lxb_html_encoding_determine(enc, html1, html1_end);
/* Process results... */

/* Clean for reuse */
lxb_html_encoding_clean(enc);

/* Second document */
lxb_html_encoding_determine(enc, html2, html2_end);
/* Process results... */

/* Destroy when done */
lxb_html_encoding_destroy(enc, true);
```

### Helper Functions

```C
/* Access results */
lxb_html_encoding_entry_t *lxb_html_encoding_meta_entry(lxb_html_encoding_t *em, size_t idx);
size_t lxb_html_encoding_meta_length(lxb_html_encoding_t *em);
lexbor_array_obj_t *lxb_html_encoding_meta_result(lxb_html_encoding_t *em);

/* Lifecycle */
lxb_html_encoding_t *lxb_html_encoding_create(void);
lxb_status_t lxb_html_encoding_init(lxb_html_encoding_t *em);
void lxb_html_encoding_clean(lxb_html_encoding_t *em);
lxb_html_encoding_t *lxb_html_encoding_destroy(lxb_html_encoding_t *em, bool self_destroy);
```

### Important Notes

1. **First Wins**: When multiple encoding declarations are found, only the first valid one should be used (though the detector returns all found declarations).
2. **Not Full Parsing**: This is a lightweight scanner, not a full HTML parser. It's designed specifically for quick encoding detection.
3. **BOM Not Handled**: This detector only searches for `<meta>` tag declarations. Byte Order Mark (BOM) detection should be handled separately if needed.
4. **Case Insensitive**: Tag names and attribute names are matched case-insensitively, following HTML parsing rules.
