# Selectors

* **Includes:** `lexbor/css/css.h`
* **API Reference:** `lexbor/css/selectors/selectors.h`, `lexbor/css/selectors/selector.h`
* **Specification:** [CSS Selectors Level 4](https://drafts.csswg.org/selectors-4/)

## Overview

The CSS module includes a full CSS Selectors Level 4 parser. It parses selector strings into a structured `lxb_css_selector_list_t` tree that represents the selector's components, combinators, and specificity.

**Note:** This is only **parsing** — converting a selector string into a data structure. To **search HTML nodes** using parsed selectors, see the [Selectors](/modules/selectors/) module.

## Quick Start

```C
#include <lexbor/css/css.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    const lxb_char_t slctrs[] = "div.my-class > p:first-child, #main a:hover, :has(#id, $bu)";

    /* Create and initialize parser */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    lxb_css_parser_init(parser, NULL);

    /* Parse selectors */
    lxb_css_selector_list_t *list = lxb_css_selectors_parse(parser,
                                                             slctrs,
                                                             sizeof(slctrs) - 1);
    if (parser->status != LXB_STATUS_OK) {
        /* Handle error */
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Serialize back to text */
    lxb_css_selector_serialize_list_chain(list, callback, NULL);
    printf("\n");

    /* Check for parse warnings/errors */
    if (lxb_css_log_length(lxb_css_parser_log(parser)) > 0) {
        printf("Parse log:\n");
        lxb_css_log_serialize(parser->log, callback, NULL,
                              (lxb_char_t *) "  ", 2);
    }

    /* Clean up */
    lxb_css_selector_list_destroy_memory(list);
    lxb_css_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```

Output:
```
div.my-class > p:first-child, #main a:hover, :has(#id)
Parse log:
  Syntax error. Selectors. Unexpected token: $
```

## Data Structure

The parser converts a selector string into two linked structures: `lxb_css_selector_list_t` and `lxb_css_selector_t`.

### Two levels of linked lists

**Selector List** (`lxb_css_selector_list_t`) — represents one group in a comma-separated selector. Lists are linked to each other via `next`/`prev` pointers. Each list points to its chain of selectors via `first`/`last`.

**Selector** (`lxb_css_selector_t`) — represents one simple selector (a tag name, class, id, attribute, pseudo-class, etc.). Selectors within a list are linked via `next`/`prev` pointers. Each selector has a `type` and a `combinator` that describes how it connects to the **previous** selector in the chain.

### Example

For the string `div.class > p, #main a`:

```
lxb_css_selector_list_t chain (comma-separated groups):

  List 1                          List 2
  +------------------+   next    +------------------+
  | first --> div    | --------> | first --> #main  |
  | last  --> p      |           | last  --> a      |
  +------------------+   <-----  +------------------+
                          prev

Selector chains inside each list (next/prev):

  List 1:  div --> .class --> p --> NULL
  List 2:  #main --> a --> NULL
```

Each selector stores a `combinator` field that says how it relates to the selector **before** it:

| Selector | `type` | `combinator` | Meaning |
|----------|--------|--------------|---------|
| `div` | `ELEMENT` | `DESCENDANT` | First in chain, no predecessor |
| `.class` | `CLASS` | `CLOSE` | Directly attached to `div` (no space) |
| `p` | `ELEMENT` | `CHILD` | Child of `div.class` (the `>`) |
| `#main` | `ID` | `DESCENDANT` | First in chain |
| `a` | `ELEMENT` | `DESCENDANT` | Descendant of `#main` (the space) |

The `CLOSE` combinator means "glued together" — no separator between selectors. This is how compound selectors like `div.class#id` are represented: each part is a separate selector node with `CLOSE` combinator.

### Nested selectors

Pseudo-class functions like `:has()`, `:is()`, `:not()` contain their own selector lists. The inner list's `parent` field points back to the selector that contains it.

### Traversal

Walking the full structure:

```C
/* Walk all comma-separated groups */
lxb_css_selector_list_t *list = /* parsed result */;

while (list != NULL) {
    /* Walk all selectors in this group */
    lxb_css_selector_t *sel = list->first;

    while (sel != NULL) {
        /* sel->type       — what kind of selector (element, class, id, ...) */
        /* sel->combinator — how it connects to the previous selector        */
        /* sel->name       — the name (tag name, class name, etc.)           */

        sel = sel->next;
    }

    list = list->next;
}
```

### Specificity

Each `lxb_css_selector_list_t` stores a `specificity` field (`uint32_t`) that encodes the (a, b, c) specificity values as bit fields. Use the macros to extract components:

```C
lxb_css_selector_sp_a(list->specificity)  /* ID selectors count */
lxb_css_selector_sp_b(list->specificity)  /* class/attribute/pseudo-class count */
lxb_css_selector_sp_c(list->specificity)  /* element/pseudo-element count */
```

## Parsing Levels

The selector parser supports different parsing levels depending on what you need:

| Function | Parses |
|----------|--------|
| `lxb_css_selectors_parse()` | Full selector list (`div, .class, #id`) |
| `lxb_css_selectors_parse_complex_list()` | Complex selector list |
| `lxb_css_selectors_parse_compound_list()` | Compound selector list |
| `lxb_css_selectors_parse_simple_list()` | Simple selector list |
| `lxb_css_selectors_parse_relative_list()` | Relative selector list |
| `lxb_css_selectors_parse_complex()` | Single complex selector |
| `lxb_css_selectors_parse_compound()` | Single compound selector |
| `lxb_css_selectors_parse_simple()` | Single simple selector |
| `lxb_css_selectors_parse_relative()` | Single relative selector |

For more information on parsing levels, see specification [Grammar](https://drafts.csswg.org/selectors-4/#grammar).

## Selector Types

Each parsed selector has a type that identifies what kind of selector it is:

| Type | Constant | Example |
|------|----------|---------|
| Universal | `LXB_CSS_SELECTOR_TYPE_ANY` | `*` |
| Element | `LXB_CSS_SELECTOR_TYPE_ELEMENT` | `div` |
| ID | `LXB_CSS_SELECTOR_TYPE_ID` | `#main` |
| Class | `LXB_CSS_SELECTOR_TYPE_CLASS` | `.active` |
| Attribute | `LXB_CSS_SELECTOR_TYPE_ATTRIBUTE` | `[href]` |
| Pseudo-Class | `LXB_CSS_SELECTOR_TYPE_PSEUDO_CLASS` | `:hover` |
| Pseudo-Class Function | `LXB_CSS_SELECTOR_TYPE_PSEUDO_CLASS_FUNCTION` | `:nth-child(2n)` |
| Pseudo-Element | `LXB_CSS_SELECTOR_TYPE_PSEUDO_ELEMENT` | `::before` |
| Pseudo-Element Function | `LXB_CSS_SELECTOR_TYPE_PSEUDO_ELEMENT_FUNCTION` | `::highlight(name)` |

## Combinators

Selectors within a complex selector are connected by combinators:

| Combinator | Constant | Example |
|------------|----------|---------|
| Descendant | `LXB_CSS_SELECTOR_COMBINATOR_DESCENDANT` | `div p` (space) |
| Close | `LXB_CSS_SELECTOR_COMBINATOR_CLOSE` | `div.class` (no separator) |
| Child | `LXB_CSS_SELECTOR_COMBINATOR_CHILD` | `div > p` |
| Next Sibling | `LXB_CSS_SELECTOR_COMBINATOR_SIBLING` | `div + p` |
| Subsequent Sibling | `LXB_CSS_SELECTOR_COMBINATOR_FOLLOWING` | `div ~ p` |
| Column | `LXB_CSS_SELECTOR_COMBINATOR_CELL` | `col \|\| td` (not supported now) |

## Attribute Matching

Attribute selectors support these matching modes:

| Match | Constant | Syntax |
|-------|----------|--------|
| Equals | `LXB_CSS_SELECTOR_MATCH_EQUAL` | `[attr=value]` |
| Includes | `LXB_CSS_SELECTOR_MATCH_INCLUDE` | `[attr~=value]` |
| Dash | `LXB_CSS_SELECTOR_MATCH_DASH` | `[attr\|=value]` |
| Prefix | `LXB_CSS_SELECTOR_MATCH_PREFIX` | `[attr^=value]` |
| Suffix | `LXB_CSS_SELECTOR_MATCH_SUFFIX` | `[attr$=value]` |
| Substring | `LXB_CSS_SELECTOR_MATCH_SUBSTRING` | `[attr*=value]` |
