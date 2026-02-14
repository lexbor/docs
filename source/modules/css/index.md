# CSS

* **Version:** 1.4.0
* **Path:** `source/lexbor/css`
* **Base Includes:** `lexbor/css/css.h`
* **Examples:** `examples/lexbor/css`
* **Specification:** [CSS](https://www.w3.org/Style/CSS/)

```{toctree}
:hidden:
:maxdepth: 2

/modules/css/parser
/modules/css/stylesheet
/modules/css/selectors
/modules/css/syntax
```

## Overview

CSS itself is a modular system. Unlike a single monolithic specification, [CSS is defined as a collection of independent modules](https://www.w3.org/Style/CSS/), each covering a specific aspect of styling: syntax, selectors, colors, layout, fonts, text, and many others. Each CSS module has its own specification, its own level (version), and evolves at its own pace. The W3C actively develops and extends these modules, so the CSS landscape is constantly growing.

The lexbor CSS module mirrors this modular approach. It is a CSS parser that processes CSS text — stylesheets, individual rules, declarations, selectors, and values — and builds corresponding in-memory data structures. Support for CSS specification modules is being actively developed; new modules and properties are added regularly.

**Important:** This module handles **parsing** only. It builds CSS data structures (rule trees, selector lists, declaration lists) from CSS text. If you need to **find HTML elements matching CSS selectors**, see the [Selectors](/modules/selectors/) module documentation.

## Key Features

- **Specification Compliant** — implements CSS Syntax Module Level 3
- **CSS Selectors Level 4** — full parsing support for CSS Selectors
- **Modular Design** — parser, selectors, properties, and at-rules are separate subsystems
- **Stylesheet Parsing** — parses complete CSS stylesheets into a rule tree (CSSOM)
- **Property Parsing** — parses 100+ CSS properties with typed values
- **Serialization** — serialize any CSS structure back to text
- **Error Logging** — detailed parse error reporting
- **Memory Efficient** — shared memory pools, parser reuse

## Quick Start

### Parse a Stylesheet

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
    const lxb_char_t css[] = "div { color: red; font-size: 16px; }";

    /* Create and initialize the parser */
    lxb_css_parser_t *parser = lxb_css_parser_create();
    lxb_status_t status = lxb_css_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Create a stylesheet object */
    lxb_css_stylesheet_t *sst = lxb_css_stylesheet_create(NULL);
    if (sst == NULL) {
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Parse CSS into the stylesheet */
    status = lxb_css_stylesheet_parse(sst, parser, css, sizeof(css) - 1);
    if (status != LXB_STATUS_OK) {
        lxb_css_stylesheet_destroy(sst, true);
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Serialize the rule tree back to text */
    lxb_css_rule_serialize(sst->root, callback, NULL);
    printf("\n");

    /* Clean up */
    lxb_css_stylesheet_destroy(sst, true);
    lxb_css_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```

Output:
```CSS
div {color: red; font-size: 16px}
```

## CSS Specification Modules

The table below lists CSS specification modules and their support status in lexbor. The modules marked as supported have full or near-complete parsing implementation. Work on adding support for new modules is ongoing.

### Supported

| CSS Module | Specification | What It Covers |
|------------|---------------|----------------|
| CSS Syntax | [Level 3](https://drafts.csswg.org/css-syntax-3/) | Tokenization and grammar rules — the foundation for all other modules |
| CSS Selectors | [Level 4](https://drafts.csswg.org/selectors-4/) | Selector parsing: type, class, ID, attribute, pseudo-classes, pseudo-elements, combinators |
| CSS Cascading and Inheritance | [Level 3–4](https://drafts.csswg.org/css-cascade-4/) | Keywords `initial`, `inherit`, `unset`, `revert` |
| CSS Color | [Level 4](https://drafts.csswg.org/css-color-4/) | Color values: named colors, hex, `rgb()`, `hsl()`, `hwb()`, `lab()`, `lch()` |
| CSS Values and Units | [Level 4](https://drafts.csswg.org/css-values-4/) | Lengths, angles, durations, frequencies, resolutions, percentages |
| CSS Box Model | [Level 3](https://drafts.csswg.org/css-box-3/) | `width`, `height`, `margin`, `padding`, `box-sizing` |
| CSS Flexible Box Layout | [Level 1](https://drafts.csswg.org/css-flexbox-1/) | `display: flex`, `flex-direction`, `flex-wrap`, `justify-content`, `align-items`, etc. |
| CSS Positioned Layout | [Level 3](https://drafts.csswg.org/css-position-3/) | `position`, `top`, `right`, `bottom`, `left`, `z-index` |
| CSS Fonts | [Level 4](https://drafts.csswg.org/css-fonts-4/) | `font-family`, `font-size`, `font-weight`, `font-style`, `font-stretch` |
| CSS Text | [Level 4](https://drafts.csswg.org/css-text-4/) | `text-align`, `text-indent`, `white-space`, `word-break`, `letter-spacing`, `line-height`, etc. |
| CSS Text Decoration | [Level 3](https://drafts.csswg.org/css-text-decor-3/) | `text-decoration`, `text-decoration-line`, `text-decoration-color`, `text-decoration-style` |
| CSS Writing Modes | [Level 4](https://drafts.csswg.org/css-writing-modes-4/) | `writing-mode`, `text-orientation`, `direction`, `unicode-bidi` |
| CSS Overflow | [Level 3](https://drafts.csswg.org/css-overflow-3/) | `overflow-x`, `overflow-y`, `text-overflow` |
| CSS Inline Layout | [Level 3](https://drafts.csswg.org/css-inline-3/) | `vertical-align`, `dominant-baseline`, `alignment-baseline` |
| CSS Display | [Level 3](https://drafts.csswg.org/css-display-3/) | `display`, `visibility`, `order` |

### Not Yet Supported

These modules are not yet implemented but may be added in the future:

| CSS Module | Specification |
|------------|---------------|
| CSS Grid Layout | [Level 2](https://drafts.csswg.org/css-grid-2/) |
| CSS Multi-column Layout | [Level 1](https://drafts.csswg.org/css-multicol-1/) |
| CSS Transitions | [Level 1](https://drafts.csswg.org/css-transitions-1/) |
| CSS Animations | [Level 1](https://drafts.csswg.org/css-animations-1/) |
| CSS Transforms | [Level 2](https://drafts.csswg.org/css-transforms-2/) |
| CSS Backgrounds and Borders | [Level 3](https://drafts.csswg.org/css-backgrounds-3/) |
| CSS Images | [Level 4](https://drafts.csswg.org/css-images-4/) |
| CSS Shapes | [Level 1](https://drafts.csswg.org/css-shapes-1/) |
| CSS Containment | [Level 2](https://drafts.csswg.org/css-contain-2/) |
| CSS Custom Properties | [Level 1](https://drafts.csswg.org/css-variables-1/) |
| CSS Scroll Snap | [Level 1](https://drafts.csswg.org/css-scroll-snap-1/) |
| CSS Conditional Rules - @media | [Level 3](https://drafts.csswg.org/css-conditional-3/) |
| CSS Fonts — @font-face | [Level 4](https://drafts.csswg.org/css-fonts-4/#font-face-rule) |
| CSS Namespaces — @namespace | [Level 3](https://drafts.csswg.org/css-namespaces-3/) |
