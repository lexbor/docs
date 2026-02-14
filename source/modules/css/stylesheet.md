# Stylesheet

* **Path:** `source/lexbor/css/stylesheet.h`, `source/lexbor/css/stylesheet.c`
* **Includes:** `lexbor/css/stylesheet.h`

## Overview

Stylesheet parsing converts a complete CSS text into a rule tree — the CSS Object Model (CSSOM). The result is a tree of `lxb_css_rule_t` nodes representing style rules, at-rules, and declarations.

## Rule Tree Structure

A parsed stylesheet produces a tree of rules:

```
Stylesheet (lxb_css_rule_t, type = STYLESHEET)
+-- Rule List (lxb_css_rule_list_t)
    |-- Style Rule (lxb_css_rule_style_t)
    |   |-- Selectors (lxb_css_selector_list_t)
    |   +-- Declaration List (lxb_css_rule_declaration_list_t)
    |       |-- Declaration (lxb_css_rule_declaration_t)  /* e.g. color: red */
    |       +-- Declaration (lxb_css_rule_declaration_t)  /* e.g. font-size: 16px */
    |-- At-Rule (lxb_css_rule_at_t)                       /* e.g. @media */
    |   +-- Rule List (nested rules)
    +-- Style Rule (lxb_css_rule_style_t)
        +-- ...
```

## Rule Types

| Type | Constant | Description |
|------|----------|-------------|
| Stylesheet | `LXB_CSS_RULE_STYLESHEET` | Root of the rule tree |
| Rule List | `LXB_CSS_RULE_LIST` | Container for rules (first/last) |
| Style Rule | `LXB_CSS_RULE_STYLE` | Selector + declarations (`div { color: red }`) |
| Bad Style Rule | `LXB_CSS_RULE_BAD_STYLE` | Malformed style rule (error recovery) |
| At-Rule | `LXB_CSS_RULE_AT_RULE` | @-rule (`@media`, `@font-face`, etc.) |
| Declaration List | `LXB_CSS_RULE_DECLARATION_LIST` | List of declarations inside a rule |
| Declaration | `LXB_CSS_RULE_DECLARATION` | Single property-value pair |

## Structure

### lxb_css_stylesheet_t

```C
struct lxb_css_stylesheet {
    lxb_css_rule_t   *root;    /* Root rule node */
    lxb_css_memory_t *memory;  /* Memory pool */
};
```

### lxb_css_rule_t

Base rule type. All rule types embed this structure:

```C
struct lxb_css_rule {
    lxb_css_rule_type_t type;     /* Rule type */
    lxb_css_rule_t      *next;    /* Next sibling rule */
    lxb_css_rule_t      *prev;    /* Previous sibling rule */
    lxb_css_rule_t      *parent;  /* Parent rule */
    lxb_css_memory_t    *memory;  /* Memory pool */
    size_t              ref_count;
};
```

### lxb_css_rule_style_t

```C
struct lxb_css_rule_style {
    lxb_css_rule_t                  rule;         /* Base rule */
    lxb_css_selector_list_t         *selector;    /* Parsed selectors */
    lxb_css_rule_declaration_list_t *declarations; /* Declarations */
    lxb_css_rule_list_t             *child;       /* Nested rules */
};
```

### lxb_css_rule_at_t

```C
struct lxb_css_rule_at {
    lxb_css_rule_t rule;       /* Base rule */
    uintptr_t      type;       /* At-rule type ID */

    union {
        lxb_css_at_rule__undef_t    *undef;
        lxb_css_at_rule__custom_t   *custom;
        lxb_css_at_rule_font_face_t *font_face;
        lxb_css_at_rule_media_t     *media;
        lxb_css_at_rule_namespace_t *ns;
        void                        *user;
    } u;
};
```

## API

### lxb_css_stylesheet_create

```C
lxb_css_stylesheet_t *
lxb_css_stylesheet_create(lxb_css_memory_t *memory);
```

Create a new stylesheet object. If `memory` is `NULL`, a new internal memory pool is created.

### lxb_css_stylesheet_destroy

```C
lxb_css_stylesheet_t *
lxb_css_stylesheet_destroy(lxb_css_stylesheet_t *sst, bool destroy_memory);
```

Destroy a stylesheet object. If `destroy_memory` is `true`, also destroys the attached memory pool.

### lxb_css_stylesheet_parse

```C
lxb_status_t
lxb_css_stylesheet_parse(lxb_css_stylesheet_t *sst, lxb_css_parser_t *parser,
                         const lxb_char_t *data, size_t length);
```

Parse CSS text and build the rule tree in the stylesheet.

Returns an error only in extremely unforeseen circumstances (e.g., memory allocation failure). Any broken CSS will not cause an error — it will be handled via error recovery.

If the parser does not have an initialized selectors module, one is created temporarily. For better performance when parsing multiple stylesheets, initialize selectors once:

```C
lxb_css_parser_t *parser = lxb_css_parser_create();
lxb_css_parser_init(parser, NULL);
lxb_css_parser_selectors_init(parser);
```

## Parsing Example

```C
#include <lexbor/css/css.h>

int main(void)
{
    const lxb_char_t css[] =
        "div { color: red; }"
        "@media (min-width: 768px) { .container { width: 100%; } }"
        "p.intro { font-size: 18px; }";

    /* Create parser */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    lxb_css_parser_init(parser, NULL);

    /* Create stylesheet (NULL = create its own memory pool) */
    lxb_css_stylesheet_t *sst = lxb_css_stylesheet_create(NULL);

    /* Parse CSS */
    lxb_status_t status = lxb_css_stylesheet_parse(sst, parser, css,
                                                    sizeof(css) - 1);
    if (status != LXB_STATUS_OK) {
        /* Handle error */
    }

    /* The rule tree is now in sst->root */
    /* Serialize, traverse, or inspect it... */

    /* Clean up */
    lxb_css_stylesheet_destroy(sst, true);
    lxb_css_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```

## Traversing the Rule Tree

Rules form a linked list. Each rule has `next` and `prev` pointers. A rule list has `first` and `last` pointers.

```C
/* After parsing... */
lxb_css_rule_t *root = sst->root;

/* Root is a stylesheet rule with a child rule list */
/* Iterate through all top-level rules */
lxb_css_rule_list_t *list = lxb_css_rule_list(root);

lxb_css_rule_t *rule = list->first;

while (rule != NULL) {
    switch (rule->type) {
        case LXB_CSS_RULE_STYLE: {
            lxb_css_rule_style_t *style = lxb_css_rule_style(rule);
            /* Access style->selector and style->declarations */
            break;
        }

        case LXB_CSS_RULE_AT_RULE: {
            lxb_css_rule_at_t *at = lxb_css_rule_at(rule);
            /* Access at-rule data */
            break;
        }

        default:
            break;
    }

    rule = rule->next;
}
```

## Serialization

### lxb_css_rule_serialize

```C
lxb_status_t
lxb_css_rule_serialize(const lxb_css_rule_t *rule,
                       lexbor_serialize_cb_f cb, void *ctx);
```

Serialize a single rule node.

### lxb_css_rule_serialize_chain

```C
lxb_status_t
lxb_css_rule_serialize_chain(const lxb_css_rule_t *rule,
                             lexbor_serialize_cb_f cb, void *ctx);
```

Serialize a rule and all its siblings.

### lxb_css_rule_list_serialize

```C
lxb_status_t
lxb_css_rule_list_serialize(const lxb_css_rule_list_t *list,
                            lexbor_serialize_cb_f cb, void *ctx);
```

Serialize all rules in a rule list.

## Cast Macros

Convenience macros for casting rule pointers:

| Macro | Target Type |
|-------|-------------|
| `lxb_css_rule(ptr)` | `lxb_css_rule_t *` |
| `lxb_css_rule_list(ptr)` | `lxb_css_rule_list_t *` |
| `lxb_css_rule_at(ptr)` | `lxb_css_rule_at_t *` |
| `lxb_css_rule_style(ptr)` | `lxb_css_rule_style_t *` |
| `lxb_css_rule_bad_style(ptr)` | `lxb_css_rule_bad_style_t *` |
| `lxb_css_rule_declaration_list(ptr)` | `lxb_css_rule_declaration_list_t *` |
| `lxb_css_rule_declaration(ptr)` | `lxb_css_rule_declaration_t *` |

## Reference Counting

Rules use reference counting for lifetime management:

| Function | Description |
|----------|-------------|
| `lxb_css_rule_ref_count(rule)` | Get current reference count |
| `lxb_css_rule_ref_inc(rule)` | Increment reference count |
| `lxb_css_rule_ref_dec(rule)` | Decrement reference count |
| `lxb_css_rule_ref_dec_destroy(rule)` | Decrement and destroy if count reaches 0 |
