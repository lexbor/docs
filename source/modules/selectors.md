# Selectors Module

* **Version:** 0.5.0
* **Path:** `source/lexbor/selectors`
* **Base Includes:** `lexbor/selectors/selectors.h`
* **Examples:** `examples/lexbor/selectors`
* **Specification:** [CSS Selectors Level 4](https://drafts.csswg.org/selectors-4/)

## Overview

The Selectors module implements DOM node search by selectors. In other words, it combines three modules: DOM, HTML, and CSS selectors.
This module, which forms the basis for `querySelector` and `querySelectorAll`.

For parsing HTML documents, use the [HTML module](html.md).
For CSS selector parsing, use the [CSS module](css.md).

## What's Inside

- **Selector Matching Engine** — efficiently matches elements against compiled selectors
- **Attribute Selectors** — all 9 attribute matching modes with case sensitivity flags
- **Nth Selectors** — :nth-child(), :nth-of-type() and their variants with An+B notation
- **Pseudo-class Support** — 30+ pseudo-classes including :is(), :where(), :not(), :has()
- **Combinators** — descendant (` `), child (`>`), adjacent sibling (`+`), general sibling (`~`), column (`||`)

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
input[type = "text"]        /* exact match */
[class ~= "active"]         /* class contains "active" */
[lang |= "en"]              /* language is en or en-* */
a[href^="https"]            /* links starting with https */
img[src$=".png"]            /* images ending with .png */
[title*="hello"]            /* title contains "hello" */
[data-value="Test" i]       /* case-insensitive */
```

### Pseudo-classes

#### User Action Pseudo-classes
- `:hover` — element is being hovered
- `:active` — element is being activated (e.g., mouse button pressed)
- `:focus` — element has focus
- `:focus-visible` — element has focus and should show focus indicator
- `:focus-within` — element or any descendant has focus

#### Location Pseudo-classes
- `:link` — unvisited link
- `:visited` — visited link
- `:any-link` — matches both :link and :visited
- `:local-link` — link to same page
- `:target` — element targeted by fragment identifier (URL hash)
- `:target-within` — element or descendant is targeted
- `:scope` — reference point for relative selectors

#### Input Pseudo-classes
- `:enabled` — form control is enabled
- `:disabled` — form control is disabled
- `:read-only` — element is not editable
- `:read-write` — element is editable
- `:placeholder-shown` — input shows placeholder text
- `:default` — default form control in a group
- `:checked` — checkbox or radio button is checked
- `:indeterminate` — checkbox is in indeterminate state

#### Input Validation Pseudo-classes
- `:valid` — form control passes validation
- `:invalid` — form control fails validation
- `:in-range` — value is within min/max range
- `:out-of-range` — value is outside min/max range
- `:required` — form control is required
- `:optional` — form control is optional
- `:user-invalid` — invalid after user interaction

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
- `:nth-col(An+B)` — selects nth column
- `:nth-last-col(An+B)` — selects nth column from end

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
- `:lang(language)` — matches elements in specified language
  - Example: `:lang(en)`, `:lang(fr)`
- `:dir(ltr|rtl)` — matches by text direction
  - `:dir(ltr)` — left-to-right
  - `:dir(rtl)` — right-to-left
- `:current(selector-list)` — time-dimensional pseudo-class for media

#### Display State Pseudo-classes
- `:fullscreen` — element is in fullscreen mode

#### Other Pseudo-classes
- `:blank` — input is blank
- `:warning` — element has warning state
- `:past` — time-dimensional, element represents past
- `:future` — time-dimensional, element represents future

#### Custom Lexbor Pseudo-class
- `:-lexbor-contains(text)` — **non-standard**, matches elements containing specific text content
  - Useful for web scraping and testing

### Pseudo-elements

Pseudo-elements create abstraction about the document tree beyond those specified by the document language.

- `::before` — generated content before element
- `::after` — generated content after element
- `::first-line` — first formatted line of element
- `::first-letter` — first letter of first line
- `::selection` — portion selected by user
- `::inactive-selection` — selection when element is not active
- `::placeholder` — placeholder text in input
- `::marker` — list item marker
- `::backdrop` — backdrop behind fullscreen element
- `::spelling-error` — text with spelling error
- `::grammar-error` — text with grammar error
- `::target-text` — text targeted by scroll-to-text fragment

### Combinators

Combinators combine multiple selectors to create relationships:

- **Descendant** (` `) — `div p` (any p inside div)
- **Child** (`>`) — `div > p` (direct child p of div)
- **Next sibling** (`+`) — `h1 + p` (p immediately after h1)
- **Subsequent sibling** (`~`) — `h1 ~ p` (any p after h1 at same level)
- **Column** (`||`) — `col || td` (td in column represented by col)

## Basic Usage

```c
#include <lexbor/html/html.h>
#include <lexbor/selectors/selectors.h>

/* Parse HTML */
lxb_html_document_t *document = lxb_html_document_create();
lxb_html_document_parse(document, html, html_len);

/* Create selector */
lxb_selectors_t *selectors = lxb_selectors_create();
lxb_selectors_init(selectors);

/* Compile selector */
const lxb_char_t selector_str[] = "div.container > p:first-child";
lxb_css_selector_list_t *list;
list = lxb_selectors_parse(selectors, selector_str, sizeof(selector_str) - 1);

if (list == NULL) {
    /* Parsing error */
    lxb_selectors_destroy(selectors, true);
    lxb_html_document_destroy(document);
    return EXIT_FAILURE;
}

/* Find matching elements */
lxb_dom_collection_t *collection = lxb_dom_collection_make(&document->dom_document, 128);

lxb_selectors_find(selectors,
                   lxb_dom_interface_node(document->body),
                   list,
                   collection);

/* Process results */
for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
    lxb_dom_element_t *element = lxb_dom_collection_element(collection, i);
    /* Process element */
    const lxb_char_t *tag_name = lxb_dom_element_local_name(element, NULL);
    printf("Found: %s\n", tag_name);
}

/* Cleanup */
lxb_dom_collection_destroy(collection, true);
lxb_selectors_destroy(selectors, true);
lxb_html_document_destroy(document);
```

## Test Single Element

Check if a specific element matches a selector:

```c
/* Check if element matches selector */
bool matches = lxb_selectors_match(selectors,
                                    lxb_dom_interface_node(element),
                                    list);

if (matches) {
    printf("Element matches the selector\n");
}
```

## Advanced Examples

### Complex Selectors with Pseudo-classes

```c
/* Find all checked checkboxes in a form */
const lxb_char_t selector1[] = "form input[type='checkbox']:checked";

/* Find all even rows in a table */
const lxb_char_t selector2[] = "table tr:nth-child(even)";

/* Find all invalid, required inputs */
const lxb_char_t selector3[] = "input:required:invalid";

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
/* Find all required, invalid email inputs in an enabled form */
const lxb_char_t selector1[] = "form:not(:disabled) input[type='email']:required:invalid";

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

## Performance Considerations

### Selector Compilation

Selectors are compiled once and can be reused multiple times:

```c
/* Compile once */
lxb_css_selector_list_t *list = lxb_selectors_parse(selectors, selector_str, selector_len);

/* Use multiple times */
lxb_selectors_find(selectors, root1, list, collection1);
lxb_selectors_find(selectors, root2, list, collection2);
lxb_selectors_find(selectors, root3, list, collection3);

/* Cleanup only once */
lxb_css_selector_list_destroy_memory(list);
```

### Efficient Selector Strategies

**Fast selectors:**
- ID selectors: `#id`
- Class selectors: `.class`
- Type selectors: `div`
- Direct child: `parent > child`

**Slower selectors:**
- Descendant combinator: `ancestor descendant` (must traverse entire subtree)
- `:has()` pseudo-class (requires searching descendants)
- Attribute contains: `[attr*='value']`

**Optimization tips:**
1. Be as specific as possible on the rightmost part (key selector)
2. Use child combinator (`>`) instead of descendant when possible
3. Avoid overly complex `:has()` selectors
4. Compile selectors once, reuse many times

## Error Handling

```c
lxb_css_selector_list_t *list;
list = lxb_selectors_parse(selectors, selector_str, selector_len);

if (list == NULL) {
    /* Parse error - invalid selector syntax */
    printf("Invalid selector syntax\n");

    /* You can get error information if needed */
    lxb_selectors_destroy(selectors, true);
    return EXIT_FAILURE;
}

/* Selector is valid, proceed with matching */
```

## Examples in Repository

See the [examples/lexbor/selectors/](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/selectors) directory for complete working examples:

- Basic selector usage
- Complex selectors
- Pseudo-classes
- Attribute matching
- Performance testing

## Related Articles

- [CSS Selectors, the Easy Way](../articles/example-CSS-selectors-easy-way.md) — practical guide with examples

## API Reference

### Main Functions

```c
/* Create and initialize selector engine */
lxb_selectors_t *lxb_selectors_create(void);
lxb_status_t lxb_selectors_init(lxb_selectors_t *selectors);

/* Parse selector string */
lxb_css_selector_list_t *
lxb_selectors_parse(lxb_selectors_t *selectors,
                    const lxb_char_t *data, size_t length);

/* Find all matching elements */
lxb_status_t
lxb_selectors_find(lxb_selectors_t *selectors, lxb_dom_node_t *root,
                   lxb_css_selector_list_t *list,
                   lxb_dom_collection_t *collection);

/* Check if single element matches */
bool
lxb_selectors_match(lxb_selectors_t *selectors, lxb_dom_node_t *node,
                    lxb_css_selector_list_t *list);

/* Cleanup */
void lxb_selectors_destroy(lxb_selectors_t *selectors, bool self_destroy);
void lxb_css_selector_list_destroy_memory(lxb_css_selector_list_t *list);
```

## Specification Conformance

The Selectors module implements [CSS Selectors Level 4](https://drafts.csswg.org/selectors-4/) specification with the following status:

- All simple selectors
- All combinators
- All attribute selectors
- All pseudo-classes
- Specificity calculation
- Selector list (`,` separator)

The module passes extensive test suites and is used in production by major projects like PHP, SerpApi, and various language bindings.
