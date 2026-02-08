# Extract All Links Using CSS Selectors

In this tutorial, we will learn how to:

1. Parse an HTML document.
2. Use CSS selectors to find all `<a>` elements with an `href` attribute.
3. Extract `href` values and resolve them against a base URL.

This tutorial solves the same task as
[Extract All Links and Resolve URLs](extract-links.md), but uses CSS selectors
instead of `lxb_dom_elements_by_tag_name()`. CSS selectors are more flexible:
you can use any selector expression to precisely target the elements you need.


## Prerequisites

- `lexbor` library installed on your system. See the [Quick Start](../documentation.md)
  guide for installation instructions.
- Basic knowledge of C.


## The Complete Example

Here is the full source code. We will break it down step by step below.

```c
#include <lexbor/html/html.h>
#include <lexbor/css/css.h>
#include <lexbor/selectors/selectors.h>
#include <lexbor/url/url.h>


typedef struct {
    lxb_url_parser_t *url_parser;
    const lxb_url_t  *base_url;
    unsigned         count;
} find_ctx_t;

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}

static lxb_status_t
find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec,
              void *ctx)
{
    find_ctx_t *fctx = ctx;
    lxb_dom_element_t *element;
    const lxb_char_t *href;
    size_t href_len;
    lxb_url_t *url;

    fctx->count++;
    element = lxb_dom_interface_element(node);

    href = lxb_dom_element_get_attribute(element, (const lxb_char_t *) "href", 4,
                                         &href_len);
    if (href == NULL) {
        return LXB_STATUS_OK;
    }

    printf("[%u] href: %.*s\n", fctx->count,
           (int) href_len, (const char *) href);

    /* Resolve the href against the base URL. */

    lxb_url_parser_clean(fctx->url_parser);

    url = lxb_url_parse(fctx->url_parser, fctx->base_url,
                        href, href_len);
    if (url == NULL) {
        printf("     Failed to parse URL.\n");
        return LXB_STATUS_OK;
    }

    printf("     Resolved: ");
    (void) lxb_url_serialize(url, callback, NULL, false);
    printf("\n");

    return LXB_STATUS_OK;
}

int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_html_document_t *document;
    lxb_css_parser_t *css_parser;
    lxb_css_selector_list_t *list;
    lxb_selectors_t *selectors;
    lxb_url_parser_t url_parser;
    lxb_url_t *base_url;
    find_ctx_t fctx;

    static const lxb_char_t html[] =
        "<html><head><title>Example</title></head>"
        "<body>"
        "<nav>"
        "  <a href=\"/\">Home</a>"
        "  <a href=\"/about\">About</a>"
        "</nav>"
        "<article>"
        "  <a href=\"news/today.html\">Today's News</a>"
        "  <a href=\"https://other.com/page\">Other Site</a>"
        "  <a href=\"../archive/2024.html\">Archive</a>"
        "  <a name=\"anchor\">Anchor without href</a>"
        "</article>"
        "</body></html>";
    size_t html_len = sizeof(html) - 1;

    static const lxb_char_t base_url_str[] = "https://example.com/blog/index.html";
    size_t base_url_len = sizeof(base_url_str) - 1;

    /* The CSS selector: find all <a> elements that have an href attribute. */
    static const lxb_char_t slctrs[] = "a[href]";
    size_t slctrs_len = sizeof(slctrs) - 1;

    /* Step 1: Parse the HTML document. */

    document = lxb_html_document_create();
    if (document == NULL) {
        goto failed;
    }

    status = lxb_html_document_parse(document, html, html_len);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Step 2: Create CSS parser and parse the selector. */

    css_parser = lxb_css_parser_create();
    status = lxb_css_parser_init(css_parser, NULL);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    list = lxb_css_selectors_parse(css_parser, slctrs, slctrs_len);
    if (css_parser->status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Step 3: Create Selectors engine. */

    selectors = lxb_selectors_create();
    status = lxb_selectors_init(selectors);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Step 4: Initialize the URL parser and parse the base URL. */

    status = lxb_url_parser_init(&url_parser, NULL);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    base_url = lxb_url_parse(&url_parser, NULL,
                             base_url_str, base_url_len);
    if (base_url == NULL) {
        goto failed;
    }

    /* Step 5: Find all matching elements and resolve their URLs. */

    fctx.url_parser = &url_parser;
    fctx.base_url = base_url;
    fctx.count = 0;

    printf("Selector: %s\n\n", (const char *) slctrs);

    status = lxb_selectors_find(selectors,
                                lxb_dom_interface_node(document),
                                list, find_callback, &fctx);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    printf("\nTotal: %u link(s) found.\n", fctx.count);

    /* Cleanup. */

    (void) lxb_selectors_destroy(selectors, true);
    (void) lxb_css_parser_destroy(css_parser, true);
    lxb_css_selector_list_destroy_memory(list);
    lxb_url_parser_destroy(&url_parser, false);
    lxb_url_memory_destroy(base_url);
    lxb_html_document_destroy(document);

    return EXIT_SUCCESS;

failed:

    printf("Something went wrong.\n");

    return EXIT_FAILURE;
}
```


## Step-by-Step Explanation

### Step 1: Parse the HTML Document

```c
document = lxb_html_document_create();
status = lxb_html_document_parse(document, html, html_len);
```

Same as in the previous tutorial: we create a document and parse HTML into a
DOM tree.

### Step 2: Create CSS Parser and Parse the Selector

```c
css_parser = lxb_css_parser_create();
status = lxb_css_parser_init(css_parser, NULL);

list = lxb_css_selectors_parse(css_parser, slctrs, slctrs_len);
```

We create a CSS parser and use `lxb_css_selectors_parse()` to compile the
selector string `"a[href]"` into an internal selector list.

The selector `a[href]` matches all `<a>` elements that have an `href` attribute.
This is more precise than searching by tag name alone, because it automatically
skips `<a>` elements without `href` (such as named anchors).

You can use any valid CSS selector here. For example:

- `a` — all links, with or without `href`.
- `a[href^="https"]` — only links starting with `https`.
- `nav a[href]` — only links inside `<nav>` elements.
- `a[href]:not([href^="#"])` — links excluding fragment-only references.

### Step 3: Create the Selectors Engine

```c
selectors = lxb_selectors_create();
status = lxb_selectors_init(selectors);
```

The Selectors engine is a separate object that performs the actual matching of
CSS selectors against the DOM tree. It takes a parsed selector list and walks
the DOM to find matching nodes.

### Step 4: Initialize the URL Parser and Parse the Base URL

```c
status = lxb_url_parser_init(&url_parser, NULL);
base_url = lxb_url_parse(&url_parser, NULL, base_url_str, base_url_len);
```

Same as in the previous tutorial: we prepare the URL parser and parse the base
URL for later resolution.

### Step 5: Find Matching Elements and Resolve URLs

```c
status = lxb_selectors_find(selectors,
                            lxb_dom_interface_node(document),
                            list, find_callback, &fctx);
```

`lxb_selectors_find()` walks the DOM tree starting from the given root node and
calls `find_callback` for every node matching the selector. The arguments are:

1. `selectors` — the Selectors engine.
2. `lxb_dom_interface_node(document)` — the root node to search from.
3. `list` — the parsed CSS selector list.
4. `find_callback` — a callback function invoked for each match.
5. `&fctx` — user context passed to the callback.

Inside the callback, we extract the `href` attribute and resolve it against the
base URL, exactly as in the previous tutorial:

```c
static lxb_status_t
find_callback(lxb_dom_node_t *node, lxb_css_selector_specificity_t spec,
              void *ctx)
{
    /* ... */
    href = lxb_dom_element_get_attribute(element,
                                         (const lxb_char_t *) "href", 4,
                                         &href_len);
    lxb_url_parser_clean(fctx->url_parser);
    url = lxb_url_parse(fctx->url_parser, fctx->base_url, href, href_len);
    /* ... */
}
```

The callback receives `lxb_css_selector_specificity_t spec` — the specificity
of the matched selector. We don't use it here, but it can be useful when working
with multiple selectors of different priorities.


## Expected Output

```
Selector: a[href]

[1] href: /
     Resolved: https://example.com/
[2] href: /about
     Resolved: https://example.com/about
[3] href: news/today.html
     Resolved: https://example.com/blog/news/today.html
[4] href: https://other.com/page
     Resolved: https://other.com/page
[5] href: ../archive/2024.html
     Resolved: https://example.com/archive/2024.html

Total: 5 link(s) found.
```

Notice that the `<a name="anchor">` element is not included — the `a[href]`
selector automatically filters it out.


## Building

Compile the example and run:

```sh
gcc extract_links_css.c -llexbor -o extract_links_css
./extract_links_css
```

## Summary

In this tutorial, we learned how to:

- Parse a CSS selector string with `lxb_css_selectors_parse()`.
- Create a Selectors engine with `lxb_selectors_create()`.
- Find DOM nodes matching a selector with `lxb_selectors_find()`.
- Process matched nodes in a callback and resolve their URLs.
