# Selectors Module

* **Version:** 0.5.0
* **Path:** `source/lexbor/selectors`
* **Base Includes:** `lexbor/selectors/selectors.h`
* **Examples:** `examples/lexbor/selectors`
* **Specification:** [CSS Selectors Level 4](https://drafts.csswg.org/selectors-4/)

## Overview

The Selectors module implements DOM node search by selectors. In other words, it combines three modules: DOM, HTML, and CSS selectors.
This module, which forms the basis for `querySelector` and `querySelectorAll`.

For parsing HTML documents, use the [HTML module](/modules/html).
For CSS selector parsing, use the [CSS module](/modules/css/selectors).

## What's Inside

- [**Quick Start**](#quick-start) — minimal working example to get started quickly
- [**Supported Selectors**](#supported-selectors) — complete list of supported CSS selectors
- [**Advanced Examples**](#advanced-examples) — complex selector patterns and use cases
- [**Search Options**](#search-options) — customize search behavior with options
- [**Specificity**](#specificity) — how selector specificity is calculated and compared

## Quick Start

```c
#include <lexbor/html/html.h>
#include <lexbor/css/css.h>
#include <lexbor/selectors/selectors.h>

lxb_status_t
find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec, void *ctx)
{
    size_t text_len;
    const lxb_char_t *text = lxb_dom_node_text_content(node, &text_len);
    printf("%.*s\n", (int)text_len, text);

    /*
     * Here, there is no need to free the memory occupied by "text" because
     * after the document is destroyed, all memory will be freed.
     */

    return LXB_STATUS_OK;
}

int main(int argc, const char *argv[])
{
    lxb_status_t status;
    const lxb_char_t html[] = "<div class='container'><p>Hello</p><p>World</p></div>";
    const lxb_char_t selector[] = "div.container > p";

    /* Create HTML Document */
    lxb_html_document_t *document = lxb_html_document_create();
    status = lxb_html_document_parse(document, html, sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Create CSS parser */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Create and initialize selectors */
    lxb_selectors_t *selectors = lxb_selectors_create();
    status = lxb_selectors_init(selectors);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Parse selector */
    lxb_css_selector_list_t *list = lxb_css_selectors_parse(parser, selector,
                                                            sizeof(selector) - 1);
    if (parser->status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Find matching elements */
    status = lxb_selectors_find(selectors, lxb_dom_interface_node(document),
                                list, find_callback, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Cleanup */
    lxb_selectors_destroy(selectors, true);
    lxb_css_parser_destroy(parser, true);
    lxb_css_selector_list_destroy_memory(list);
    lxb_html_document_destroy(document);

    return EXIT_SUCCESS;
}
```

## Supported Selectors

### Basic Selectors

#### Type Selectors
- **Pattern:** `element-name`
- **Description:** Matches elements by their tag name
- **Examples:**
  - `div` — selects all `<div>` elements

#### Universal Selector
- **Pattern:** `*`
- **Description:** Matches any element of any type
- **Examples:**
  - `*` — selects all elements in the document
  - `div *` — selects all elements inside `<div>`
  - `*.warning` — selects any element with class "warning" (equivalent to `.warning`)

#### Class Selectors
- **Pattern:** `.classname`
- **Description:** Matches elements by their class attribute value
- **Examples:**
  - `.classname` — selects elements with `class="classname"`
  - `.class1.class2` — selects elements that have both "class1" AND "class2" classes `class="class1 class2"`
  - `div.container` — selects `<div>` elements with class "container"
  - `.nav .item` — selects elements with class "item" inside elements with class "nav"

#### ID Selectors
- **Pattern:** `#id-value`
- **Description:** Matches a single element by its unique ID attribute
- **Examples:**
  - `#header` — selects the element with `id="header"`
  - `div#main` — selects `<div>` element with `id="main"`
  - `#form input` — selects `<input>` elements inside element with `id="form"`

### Attribute Selectors

All 7 attribute matching modes are supported:

- `[attr]` — element has attribute
- `[attr = value]` — exact match
- `[attr ~= value]` — whitespace-separated list contains value (e.g., class names)
- `[attr |= value]` — exact match or starts with value followed by hyphen (for language codes)
- `[attr ^= value]` — attribute value starts with
- `[attr $= value]` — attribute value ends with
- `[attr *= value]` — attribute value contains substring

The attribute name is compared case-insensitively.
`[attr *= value]` == `[ATTR *= value]` == `[AtTr *= value]`

Each of the attribute selectors listed may contain an indicator of how to compare the value, whether case-sensitive or not:
- `[attr=value i]` — case-insensitive matching (add `i` flag)
- `[attr=value s]` — case-sensitive matching (add `s` flag)

You can use quotation marks (single or double) around the value, or omit them for simple values without spaces:
`[attr="value"]`, `[attr='value']`, `[attr=value]` are all valid.

**Examples:**
```css
input[type = "text"]          /* exact match */
[class ~= "active"]           /* class contains "active" */
[lang |= "en"]                /* language is en or en-* */
a[href ^= "https"]            /* links starting with https */
img[src $= ".png"]            /* images ending with .png */
[title *= "hello"]            /* title contains "hello" */
[data-value = "Test" i]       /* case-insensitive */
```

### Pseudo-classes

#### User Action Pseudo-classes
- `:hover` — element is being hovered
- `:active` — element is being activated (e.g., mouse button pressed)
- `:focus` — element has focus

#### Location Pseudo-classes
- `:link` — unvisited link
- `:any-link` — matches both :link and :visited

#### Input Pseudo-classes
- `:enabled` — form control is enabled
- `:disabled` — form control is disabled
- `:read-only` — element is not editable
- `:read-write` — element is editable
- `:placeholder-shown` — input shows placeholder text
- `:checked` — checkbox or radio button is checked

#### Input Validation Pseudo-classes
- `:required` — form control is required
- `:optional` — form control is optional

#### Tree-structural Pseudo-classes
- `:root` — root element of document (usually `<html>`)
- `:empty` — element has no children (including text nodes)
- `:first-child` — first child of parent
- `:last-child` — last child of parent
- `:only-child` — only child of parent
- `:first-of-type` — first sibling of its type
- `:last-of-type` — last sibling of its type
- `:only-of-type` — only sibling of its type

#### Functional Pseudo-classes

##### Nth-child Selectors
- `:nth-child(An+B)` — selects nth child
- `:nth-last-child(An+B)` — selects nth child from end
- `:nth-of-type(An+B)` — selects nth element of same type
- `:nth-last-of-type(An+B)` — selects nth element of same type from end

**An+B notation examples:**
```css
:nth-child(2n)         /* even children: 2, 4, 6, 8... */
:nth-child(2n+1)       /* odd children: 1, 3, 5, 7... */
:nth-child(3n)         /* every 3rd: 3, 6, 9, 12... */
:nth-child(3n+2)       /* 2, 5, 8, 11, 14... */
:nth-child(-n+5)       /* first 5 elements */
:nth-child(n+3)        /* 3rd element and after */
:nth-child(odd)        /* alias for 2n+1 */
:nth-child(even)       /* alias for 2n */
```

##### Relational Selectors
- `:is(selector-list)` — matches if any selector in list matches
  - Specificity = highest specificity in the list
- `:where(selector-list)` — matches if any selector in list matches
  - Specificity = 0 (useful for low-specificity patterns)
- `:not(selector-list)` — negation, matches if none of the selectors match
- `:has(selector-list)` — relational pseudo-class (parent/ancestor selector)
  - Matches if any relative selector matches

**Examples:**
```css
:is(h1, h2, h3, h4, h5, h6)        /* any heading */
:where(article, section) p         /* paragraphs in article or section, low specificity */
p:not(.exclude)                    /* paragraphs without class "exclude" */
article:has(img)                   /* articles containing images */
div:has(> p.important)             /* divs with direct child p.important */
```

##### Other Functional Pseudo-classes
- `:current(selector-list)` — time-dimensional pseudo-class for media

#### Other Pseudo-classes
- `:blank` — input is blank

#### Custom Lexbor Pseudo-class
- `:-lexbor-contains(text)` — **non-standard**, matches elements containing specific text content
  - Useful for web scraping and testing

### Combinators

Combinators combine multiple selectors to create relationships:

- **Descendant** (` `) — `div p` (any p inside div)
- **Child** (`>`) — `div > p` (direct child p of div)
- **Next sibling** (`+`) — `h1 + p` (p immediately after h1)
- **Subsequent sibling** (`~`) — `h1 ~ p` (any p after h1 at same level)
- **Column** (`||`) — `col || td` (td in column represented by col) (not supported yet)

## Advanced Examples

### Complex Selectors with Pseudo-classes

```c
/* Find all checked checkboxes in a form */
const lxb_char_t selector1[] = "form input[type='checkbox']:checked";

/* Find all even rows in a table */
const lxb_char_t selector2[] = "table tr:nth-child(even)";

/* Find first paragraph in each article */
const lxb_char_t selector4[] = "article > p:first-of-type";
```

### Using :is() and :where() for Grouping

```c
/* Match any heading */
const lxb_char_t selector1[] = ":is(h1, h2, h3, h4, h5, h6)";

/* Match links in header or footer (with 0 specificity) */
const lxb_char_t selector2[] = ":where(header, footer) a";

/* Match inputs that are text, email, or password */
const lxb_char_t selector3[] = "input:is([type='text'], [type='email'], [type='password'])";
```

### Using :not() for Exclusion

```c
/* All paragraphs except those with class 'exclude' */
const lxb_char_t selector1[] = "p:not(.exclude)";

/* All inputs that are not disabled or read-only */
const lxb_char_t selector2[] = "input:not(:disabled):not(:read-only)";

/* All elements except divs and spans */
const lxb_char_t selector3[] = ":not(div):not(span)";

/* All links except external ones */
const lxb_char_t selector4[] = "a:not([href^='http'])";
```

### Using :has() for Parent Selection

```c
/* Find articles that contain an image */
const lxb_char_t selector1[] = "article:has(img)";

/* Find divs that have a direct child p with class 'important' */
const lxb_char_t selector2[] = "div:has(> p.important)";

/* Find sections containing both a heading and a paragraph */
const lxb_char_t selector3[] = "section:has(h2):has(p)";

/* Find list items that don't contain links */
const lxb_char_t selector4[] = "li:not(:has(a))";
```

### Attribute Selectors with Case Sensitivity

```c
/* Case-insensitive attribute match */
const lxb_char_t selector1[] = "[title*='hello' i]";

/* Case-sensitive attribute match */
const lxb_char_t selector2[] = "[data-value^='ABC' s]";

/* Match any attribute value containing "test" (case-insensitive) */
const lxb_char_t selector3[] = "[class*='test' i]";
```

### Complex nth-child Patterns

```c
/* Every 3rd element starting from the 2nd: 2, 5, 8, 11... */
const lxb_char_t selector1[] = "li:nth-child(3n+2)";

/* First 5 elements */
const lxb_char_t selector2[] = "div:nth-child(-n+5)";

/* All but the first element */
const lxb_char_t selector3[] = "p:nth-child(n+2)";

/* Even rows in a table body */
const lxb_char_t selector4[] = "tbody tr:nth-child(even)";

/* Every 4th element starting from 1st: 1, 5, 9, 13... */
const lxb_char_t selector5[] = "div:nth-child(4n+1)";
```

### Combining Multiple Techniques

```c
/* Find divs with specific class that contain images but not links */
const lxb_char_t selector2[] = "div.gallery:has(img):not(:has(a))";

/* Find the first 3 paragraphs in articles that are not empty */
const lxb_char_t selector3[] = "article p:not(:empty):nth-child(-n+3)";

/* Find all headings (h1-h6) inside main that are followed by a paragraph */
const lxb_char_t selector4[] = "main :is(h1, h2, h3, h4, h5, h6):has(+ p)";
```

### Custom Lexbor Selector

```c
/* Find elements containing specific text (non-standard) */
const lxb_char_t selector1[] = "div:-lexbor-contains('search text')";

/* Find paragraphs containing "important" */
const lxb_char_t selector2[] = "p:-lexbor-contains('important')";

/* Combine with other selectors */
const lxb_char_t selector3[] = ".content p:-lexbor-contains('TODO'):not(.done)";
```

## Search Options

You can customize the search behavior by setting options using `lxb_selectors_opt_set()`. This allows you to control how the selector engine processes nodes and handles matches.

### Available Options

#### `LXB_SELECTORS_OPT_DEFAULT`
Default behavior:
- Root node does **not** participate in the search (only its children)
- If a node matches multiple selectors, callback is triggered for **each match**

```c
lxb_selectors_opt_set(selectors, LXB_SELECTORS_OPT_DEFAULT);
```

#### `LXB_SELECTORS_OPT_MATCH_ROOT`
Include the root node in the search.

By default, when you call `lxb_selectors_find(selectors, root, list, callback, ctx)`, the `root` node itself is not checked against the selectors — only its descendants are searched.

This option makes the root node participate in the search, which is useful when you want to check if the root node itself matches any selectors.

```c
lxb_selectors_opt_set(selectors, LXB_SELECTORS_OPT_MATCH_ROOT);
```

#### `LXB_SELECTORS_OPT_MATCH_FIRST`
Stop after the first match for each node.

By default, if a node matches multiple selectors in the list, the callback is triggered once for **each matching selector**. This can result in duplicate callbacks for the same node.

This option ensures the callback is called only **once per node**, even if it matches multiple selectors.

```c
lxb_selectors_opt_set(selectors, LXB_SELECTORS_OPT_MATCH_FIRST);
```

### Combining Options

You can combine options using the bitwise OR operator (`|`):

```c
/* Include root node AND stop after first match */
lxb_selectors_opt_set(selectors,
                      LXB_SELECTORS_OPT_MATCH_ROOT | LXB_SELECTORS_OPT_MATCH_FIRST);
```

### Complete Example

```c
#include <lexbor/html/html.h>
#include <lexbor/css/css.h>
#include <lexbor/selectors/selectors.h>

lxb_status_t
callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec, void *ctx)
{
    const lxb_char_t *name = lxb_dom_element_local_name(lxb_dom_interface_element(node), NULL);
    printf("Found: %s\n", name);
    return LXB_STATUS_OK;
}

int main(void)
{
    const lxb_char_t html[] = "<div id='main' class='container'><p>Text</p></div>";
    /* Here, three selectors that match the div element are specifically
     * indicated. In a typical case, the callback would be called three times
     * with the same div element. But with the MATCH_FIRST option, the callback
     * will be called only once.
     */
    const lxb_char_t selectors_str[] = "div, div.container, div#main";

    /* Create and parse HTML */
    lxb_html_document_t *document = lxb_html_document_create();
    lxb_html_document_parse(document, html, sizeof(html) - 1);

    /* Create CSS parser and selectors engine */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    lxb_css_parser_init(parser, NULL);

    lxb_selectors_t *selectors = lxb_selectors_create();
    lxb_selectors_init(selectors);

    /* Parse selectors */
    lxb_css_selector_list_t *list = lxb_css_selectors_parse(parser,
                                                            selectors_str,
                                                            sizeof(selectors_str) - 1);

    /* Set options: include root node, avoid duplicates */
    lxb_selectors_opt_set(selectors,
                          LXB_SELECTORS_OPT_MATCH_ROOT |
                          LXB_SELECTORS_OPT_MATCH_FIRST);

    /* Find matching elements */
    lxb_dom_node_t *body = lxb_dom_interface_node(document->body);
    lxb_selectors_find(selectors, body, list, callback, NULL);

    /* Cleanup */
    lxb_css_selector_list_destroy_memory(list);
    lxb_selectors_destroy(selectors, true);
    lxb_css_parser_destroy(parser, true);
    lxb_html_document_destroy(document);

    return 0;
}
```

Output:
```
Found: div
```

## Specificity

Specificity is a weight that determines which CSS rule is applied when multiple selectors match the same element. The selector with the highest specificity wins.

### How Specificity is Calculated

Specificity is calculated as a three-component value `(A, B, C)`:

- **A** — number of ID selectors (`#id`)
- **B** — number of class selectors (`.class`), attribute selectors (`[attr]`), and pseudo-classes (`:hover`)
- **C** — number of type selectors (`div`) and pseudo-elements (`::before`)

The universal selector (`*`), combinators (`>`, `+`, `~`, ` `), and negation pseudo-class (`:not()`) don't add to specificity.

### Specificity Comparison

Specificity is compared component by component from left to right. The selector with a higher value in the leftmost differing component wins:

```
(1, 0, 0) > (0, 5, 5)   // ID beats any number of classes
(0, 2, 1) > (0, 1, 5)   // More classes beat more types
(0, 1, 1) > (0, 1, 0)   // Same classes, more types wins
```

### Examples

| Selector | A | B | C | Specificity |
|----------|---|---|---|-------------|
| `*` | 0 | 0 | 0 | (0, 0, 0) |
| `div` | 0 | 0 | 1 | (0, 0, 1) |
| `.container` | 0 | 1 | 0 | (0, 1, 0) |
| `#header` | 1 | 0 | 0 | (1, 0, 0) |
| `div.container` | 0 | 1 | 1 | (0, 1, 1) |
| `div#main.container` | 1 | 1 | 1 | (1, 1, 1) |
| `ul li a.link` | 0 | 1 | 3 | (0, 1, 3) |
| `div > p:first-child` | 0 | 1 | 2 | (0, 1, 2) |
| `[type="text"]` | 0 | 1 | 0 | (0, 1, 0) |
| `a:hover` | 0 | 1 | 1 | (0, 1, 1) |
| `::before` | 0 | 0 | 1 | (0, 0, 1) |

### Special Cases

#### `:is()` and `:has()`
Take the specificity of the **most specific selector** in their argument list:
```c
/* Specificity of #header (1, 0, 0) */
const lxb_char_t sel1[] = ":is(#header, .main, div)";
```

#### `:where()`
Always has **zero specificity** (0, 0, 0), regardless of its arguments:
```c
/* Specificity is (0, 0, 1) - only 'a' counts */
const lxb_char_t sel[] = ":where(#header, .main) a";
```

#### `:not()`
The negation itself adds nothing, but its argument counts:
```c
/* Specificity is (0, 1, 1) - .exclude + p */
const lxb_char_t sel[] = "p:not(.exclude)";
```

### Getting Specificity in Code

The `lxb_selectors_find` callback receives specificity for each matched element:

```c
lxb_status_t
find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec, void *ctx)
{
    /* spec contains specificity components */
    printf("Specificity: A=%u, B=%u, C=%u\n",
           lxb_css_selector_sp_a(spec),
           lxb_css_selector_sp_b(spec),
           lxb_css_selector_sp_c(spec));

    return LXB_STATUS_OK;
}
```

For more information, see specification [Calculating a selector’s specificity](https://drafts.csswg.org/selectors-4/#specificity-rules).

### Practical Tips

1. **Avoid over-specific selectors** — they're harder to override later
2. **Use `:where()` for reusable patterns** — zero specificity makes them easy to override
3. **Use `:is()` when specificity matters** — inherits specificity from arguments
4. **ID selectors are very specific** — (1,0,0) beats any combination of classes and types

