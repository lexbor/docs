# CSS Module

* **Version:** 1.4.0
* **Path:** `source/lexbor/css`
* **Base Includes:** `lexbor/css/css.h`
* **Examples:** `examples/lexbor/css`
* **Specification:** [CSS Syntax Level 3](https://www.w3.org/TR/css-syntax-3/), [Selectors Level 4](https://www.w3.org/TR/selectors-4/), [CSSOM](https://www.w3.org/TR/cssom-1/)

## Overview

The CSS module provides a complete CSS parser implementing CSS Syntax Module Level 3. It can parse stylesheets, individual style rules, and declarations, building a rule tree that can be serialized back to CSS text.

The module includes:

- **Syntax Tokenizer** — converts CSS text into tokens per CSS Syntax Level 3
- **Parser** — builds a CSS rule tree from tokens
- **Stylesheet** — parses and holds a complete stylesheet's rule tree
- **Rule Tree** — CSSOM-style representation of style rules, at-rules, and declarations
- **Property Parsing** — parses CSS property values into typed structures
- **Selectors** — CSS Selectors Level 4 (documented separately in the [Selectors module](selectors.md))
- **Log** — collects warnings and errors during parsing

## Key Features

- **CSS Syntax Level 3** — complete tokenizer and parser implementation
- **CSS Selectors Level 4** — full selector parsing (see [Selectors module](selectors.md))
- **CSS Namespaces Level 3** — complete namespace support
- **CSSOM** — CSS Object Model (in progress)
- **Property Value Parsing** — typed parsing for display, position, color, opacity, dimensions, margin, padding, border, background, font, text, flexbox, and more

## What's Inside

- **[Quick Start](#quick-start)** — minimal working example to parse and serialize CSS
- **[Parser](#parser-lxb_css_parser_t)** — core CSS parser entry point
- **[Stylesheet](#stylesheet-lxb_css_stylesheet_t)** — parsed stylesheet representation
- **[Rule Tree](#rule-tree)** — CSSOM-style rule node hierarchy
- **[Serialization](#serialization)** — callback-based CSS text output
- **[Log](#log-lxb_css_log_t)** — parser warnings and errors
- **[Memory Management](#memory-management-lxb_css_memory_t)** — shared memory pool
- **[Examples](#examples)** — complete working programs

## Quick Start

### Parsing and Serializing CSS

```C
#include <lexbor/css/css.h>

static lxb_status_t
serializer_callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, data);
    return LXB_STATUS_OK;
}

int main(void)
{
    lxb_status_t status;

    static const lxb_char_t css[] = "div { color: red; display: flex; }";

    /* Create and initialize the parser */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Create a stylesheet and parse CSS into it */
    lxb_css_stylesheet_t *sst = lxb_css_stylesheet_create(NULL);
    status = lxb_css_stylesheet_parse(sst, parser, css, sizeof(css) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_css_stylesheet_destroy(sst, true);
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Serialize back to CSS text */
    lxb_css_rule_serialize(sst->root, serializer_callback, NULL);
    printf("\n");

    lxb_css_stylesheet_destroy(sst, true);
    lxb_css_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```


## Parser (`lxb_css_parser_t`)

The CSS parser is the core entry point. Defined in `source/lexbor/css/parser.h`.

### Location

Declared in `source/lexbor/css/parser.h`.

### Lifecycle

```C
lxb_css_parser_t *
lxb_css_parser_create(void);

lxb_status_t
lxb_css_parser_init(lxb_css_parser_t *parser, lxb_css_syntax_tokenizer_t *tkz);

void
lxb_css_parser_clean(lxb_css_parser_t *parser);

void
lxb_css_parser_erase(lxb_css_parser_t *parser);

lxb_css_parser_t *
lxb_css_parser_destroy(lxb_css_parser_t *parser, bool self_destroy);
```

- `lxb_css_parser_init()`: If `tkz` is `NULL`, the parser creates and manages its own tokenizer.
- `lxb_css_parser_clean()`: Resets state but keeps allocated memory for reuse.
- `lxb_css_parser_erase()`: Resets state and releases internal allocations.
- `lxb_css_parser_destroy()`: If `self_destroy` is `true`, frees the parser object itself.

### Selectors Integration

To parse CSS that contains selectors (which is most CSS), initialize the selectors module:

```C
lxb_status_t
lxb_css_parser_selectors_init(lxb_css_parser_t *parser);

void
lxb_css_parser_selectors_destroy(lxb_css_parser_t *parser);
```

If the selectors module is not initialized when parsing a stylesheet, one is created temporarily for each parse call. For better performance when parsing multiple stylesheets, initialize it once.

### Status

```C
lxb_status_t
lxb_css_parser_status(lxb_css_parser_t *parser);

lxb_css_log_t *
lxb_css_parser_log(lxb_css_parser_t *parser);
```


## Stylesheet (`lxb_css_stylesheet_t`)

Represents a parsed CSS stylesheet. Defined in `source/lexbor/css/stylesheet.h`.

### Location

Declared in `source/lexbor/css/stylesheet.h`.

### Lifecycle

```C
lxb_css_stylesheet_t *
lxb_css_stylesheet_create(lxb_css_memory_t *memory);

lxb_css_stylesheet_t *
lxb_css_stylesheet_destroy(lxb_css_stylesheet_t *sst, bool destroy_memory);
```

- `lxb_css_stylesheet_create()`: If `memory` is `NULL`, the stylesheet creates its own memory pool.
- `lxb_css_stylesheet_destroy()`: If `destroy_memory` is `true`, also destroys the associated memory pool.

### Parsing

```C
lxb_status_t
lxb_css_stylesheet_parse(lxb_css_stylesheet_t *sst, lxb_css_parser_t *parser,
                         const lxb_char_t *data, size_t length);
```

Parses CSS text into the stylesheet's rule tree. Only returns errors for severe failures (e.g., out of memory). Invalid CSS is handled gracefully — broken rules are recorded as `lxb_css_rule_bad_style_t`.

After parsing, the rule tree is available at `sst->root`.


## Rule Tree

The parsed CSS is represented as a tree of rule nodes. All rule types share a common base `lxb_css_rule_t`. Defined in `source/lexbor/css/rule.h`.

### Location

Defined in `source/lexbor/css/rule.h`.

### Rule Types

```C
typedef enum {
    LXB_CSS_RULE_UNDEF = 0,
    LXB_CSS_RULE_STYLESHEET,
    LXB_CSS_RULE_LIST,
    LXB_CSS_RULE_AT_RULE,
    LXB_CSS_RULE_STYLE,
    LXB_CSS_RULE_BAD_STYLE,
    LXB_CSS_RULE_DECLARATION_LIST,
    LXB_CSS_RULE_DECLARATION
} lxb_css_rule_type_t;
```

### Key Rule Structures

**`lxb_css_rule_style_t`** — A CSS style rule (selector + declarations):

```C
struct lxb_css_rule_style {
    lxb_css_rule_t                  rule;
    lxb_css_selector_list_t         *selector;
    lxb_css_rule_declaration_list_t *declarations;
    /* ... */
};
```

**`lxb_css_rule_declaration_t`** — A single CSS declaration (property: value):

```C
struct lxb_css_rule_declaration {
    lxb_css_rule_t rule;
    uintptr_t      type;      /* property ID from LXB_CSS_PROPERTY_* */
    union { /* typed property value */ } u;
    bool           important;
};
```

The `type` field holds the property ID (e.g., `LXB_CSS_PROPERTY_DISPLAY`), and the union `u` holds the parsed value in a type-safe structure.

**`lxb_css_rule_at_t`** — An at-rule (@media, @font-face, @namespace):

```C
struct lxb_css_rule_at {
    lxb_css_rule_t rule;
    uintptr_t      type;      /* at-rule ID from LXB_CSS_AT_RULE_* */
    union { /* typed at-rule data */ } u;
};
```

**`lxb_css_rule_bad_style_t`** — A style rule whose selector failed to parse:

```C
struct lxb_css_rule_bad_style {
    lxb_css_rule_t                  rule;
    lexbor_str_t                    selectors;  /* raw selector text */
    lxb_css_rule_declaration_list_t *declarations;
};
```

### Casting Macros

```C
lxb_css_rule(obj)               /* cast to lxb_css_rule_t *               */
lxb_css_rule_style(obj)         /* cast to lxb_css_rule_style_t *         */
lxb_css_rule_at(obj)            /* cast to lxb_css_rule_at_t *            */
lxb_css_rule_declaration(obj)   /* cast to lxb_css_rule_declaration_t *   */
lxb_css_rule_declaration_list(obj) /* cast to lxb_css_rule_declaration_list_t * */
```

### Traversal

Rules form a linked list via `next`/`prev` pointers. List containers (`lxb_css_rule_list_t`, `lxb_css_rule_declaration_list_t`) have `first`/`last` pointers.

```C
/* Iterate over rules in a list */
lxb_css_rule_t *rule = list->first;
while (rule != NULL) {
    /* process rule */
    rule = rule->next;
}
```


## Serialization

All rule types support callback-based serialization back to CSS text.

### Location

Serialization functions are declared in `source/lexbor/css/rule.h`.

```C
lxb_status_t
lxb_css_rule_serialize(const lxb_css_rule_t *rule,
                       lexbor_serialize_cb_f cb, void *ctx);

lxb_status_t
lxb_css_rule_serialize_chain(const lxb_css_rule_t *rule,
                             lexbor_serialize_cb_f cb, void *ctx);
```

- `lxb_css_rule_serialize()`: Serializes a single rule.
- `lxb_css_rule_serialize_chain()`: Serializes a rule and all its `next` siblings.

Type-specific serialization functions:

```C
lxb_css_rule_style_serialize(style, cb, ctx);
lxb_css_rule_at_serialize(at, cb, ctx);
lxb_css_rule_declaration_serialize(decl, cb, ctx);
lxb_css_rule_declaration_list_serialize(list, cb, ctx);
```

The callback signature is `lexbor_serialize_cb_f`:

```C
typedef lxb_status_t
(*lexbor_serialize_cb_f)(const lxb_char_t *data, size_t len, void *ctx);
```


## Log (`lxb_css_log_t`)

The CSS parser log collects messages generated during parsing. Defined in `source/lexbor/css/log.h`.

### Location

Declared in `source/lexbor/css/log.h`.

### Message Types

```C
typedef enum {
    LXB_CSS_LOG_INFO = 0,
    LXB_CSS_LOG_WARNING,
    LXB_CSS_LOG_ERROR,
    LXB_CSS_LOG_SYNTAX_ERROR
} lxb_css_log_type_t;
```

### Lifecycle

```C
lxb_css_log_t *
lxb_css_log_create(void);

lxb_status_t
lxb_css_log_init(lxb_css_log_t *log, lexbor_mraw_t *mraw);

void
lxb_css_log_clean(lxb_css_log_t *log);

lxb_css_log_t *
lxb_css_log_destroy(lxb_css_log_t *log, bool self_destroy);
```

### Usage

```C
/* Get the number of log messages */
size_t
lxb_css_log_length(lxb_css_log_t *log);

/* Serialize all log messages */
lxb_status_t
lxb_css_log_serialize(lxb_css_log_t *log, lexbor_serialize_cb_f cb, void *ctx,
                      const lxb_char_t *indent, size_t indent_length);

/* Serialize to a string (caller must free with lexbor_free) */
lxb_char_t *
lxb_css_log_serialize_char(lxb_css_log_t *log, size_t *out_length,
                           const lxb_char_t *indent, size_t indent_length);
```


## Memory Management (`lxb_css_memory_t`)

The CSS module uses a shared memory pool for all allocations. Defined in `source/lexbor/css/base.h`.

### Location

Declared in `source/lexbor/css/base.h`.

```C
lxb_css_memory_t *
lxb_css_memory_create(void);

lxb_status_t
lxb_css_memory_init(lxb_css_memory_t *memory, size_t prepare_count);

void
lxb_css_memory_clean(lxb_css_memory_t *memory);

lxb_css_memory_t *
lxb_css_memory_destroy(lxb_css_memory_t *memory, bool self_destroy);
```

The memory pool uses reference counting:

```C
lxb_css_memory_t *
lxb_css_memory_ref_inc(lxb_css_memory_t *memory);

void
lxb_css_memory_ref_dec(lxb_css_memory_t *memory);

lxb_css_memory_t *
lxb_css_memory_ref_dec_destroy(lxb_css_memory_t *memory);
```


## Examples

### Parsing and Serializing a Stylesheet

```C
#include <lexbor/css/css.h>

static lxb_status_t
serializer_callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, data);
    return LXB_STATUS_OK;
}

int
main(void)
{
    lxb_status_t status;
    lxb_css_parser_t *parser;
    lxb_css_stylesheet_t *sst;

    static const lxb_char_t css[] =
        "div { color: red; display: flex; }"
        "p.intro { font-size: 16px; margin: 10px; }";

    /* Create and initialize the parser */
    parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Create a stylesheet and parse CSS into it */
    sst = lxb_css_stylesheet_create(NULL);
    status = lxb_css_stylesheet_parse(sst, parser, css, sizeof(css) - 1);

    lxb_css_parser_destroy(parser, true);

    if (status != LXB_STATUS_OK) {
        lxb_css_stylesheet_destroy(sst, true);
        return EXIT_FAILURE;
    }

    /* Serialize the parsed stylesheet back to CSS text */
    lxb_css_rule_serialize(sst->root, serializer_callback, NULL);
    printf("\n");

    lxb_css_stylesheet_destroy(sst, true);
    return EXIT_SUCCESS;

failed:
    lxb_css_parser_destroy(parser, true);
    return EXIT_FAILURE;
}
```

### Walking the Rule Tree

```C
#include <lexbor/css/css.h>

static lxb_status_t
print_cb(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, data);
    return LXB_STATUS_OK;
}

int
main(void)
{
    lxb_status_t status;
    lxb_css_parser_t *parser;
    lxb_css_stylesheet_t *sst;
    lxb_css_rule_t *rule;

    static const lxb_char_t css[] =
        ".header { color: blue; } .footer { margin: 0; }";

    parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    sst = lxb_css_stylesheet_create(NULL);
    status = lxb_css_stylesheet_parse(sst, parser, css, sizeof(css) - 1);
    lxb_css_parser_destroy(parser, true);

    if (status != LXB_STATUS_OK) {
        lxb_css_stylesheet_destroy(sst, true);
        return EXIT_FAILURE;
    }

    /* Walk the rule list */
    lxb_css_rule_list_t *list = lxb_css_rule_list(sst->root);
    rule = list->first;

    while (rule != NULL) {
        printf("Rule type: %d\n", rule->type);

        if (rule->type == LXB_CSS_RULE_STYLE) {
            printf("  Style rule: ");
            lxb_css_rule_style_serialize(lxb_css_rule_style(rule),
                                         print_cb, NULL);
            printf("\n");
        }

        rule = rule->next;
    }

    lxb_css_stylesheet_destroy(sst, true);
    return EXIT_SUCCESS;
}
```
