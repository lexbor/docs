# Extract All Links and Resolve URLs

In this tutorial, we will learn how to:

1. Parse an HTML document and find all `<a>` elements.
2. Extract `href` attribute values from each link.
3. Use the URL module to resolve relative URLs against a base URL, producing
   fully-qualified absolute URLs.

This is a common task when building web crawlers, scrapers, or any tool that
needs to collect and normalize links from HTML pages.


## Prerequisites

- `lexbor` library installed on your system. See the [Quick Start](../documentation.md)
  guide for installation instructions.
- Basic knowledge of C.


## The Complete Example

Here is the full source code. We will break it down step by step below.

```c
#include <lexbor/html/html.h>
#include <lexbor/url/url.h>


static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}

int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_html_document_t *document;
    lxb_dom_collection_t *collection;
    lxb_dom_element_t *element;
    lxb_url_parser_t url_parser;
    lxb_url_t *base_url, *url;
    const lxb_char_t *href;
    size_t href_len;

    static const lxb_char_t html[] =
        "<html><head><title>Example</title></head>"
        "<body>"
        "<a href=\"/about\">About</a>"
        "<a href=\"news/today.html\">Today's News</a>"
        "<a href=\"https://other.com/page\">Other Site</a>"
        "<a href=\"../archive/2024.html\">Archive</a>"
        "<a>No href</a>"
        "</body></html>";
    size_t html_len = sizeof(html) - 1;

    static const lxb_char_t base_url_str[] = "https://example.com/blog/index.html";
    size_t base_url_len = sizeof(base_url_str) - 1;

    /* Step 1: Parse the HTML document. */

    document = lxb_html_document_create();
    if (document == NULL) {
        goto failed;
    }

    status = lxb_html_document_parse(document, html, html_len);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Step 2: Find all <a> elements. */

    collection = lxb_dom_collection_make(&document->dom_document, 128);
    if (collection == NULL) {
        goto failed;
    }

    status = lxb_dom_elements_by_tag_name(
        lxb_dom_interface_element(document->body),
        collection, (const lxb_char_t *) "a", 1
    );
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    printf("Found %zu link(s).\n\n",
           lxb_dom_collection_length(collection));

    /* Step 3: Initialize the URL parser and parse the base URL. */

    status = lxb_url_parser_init(&url_parser, NULL);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    base_url = lxb_url_parse(&url_parser, NULL,
                             base_url_str, base_url_len);
    if (base_url == NULL) {
        goto failed;
    }

    /* Step 4: Iterate links, extract href, and resolve each URL. */

    for (size_t i = 0; i < lxb_dom_collection_length(collection); i++) {
        element = lxb_dom_collection_element(collection, i);

        href = lxb_dom_element_get_attribute(element,
                                             (const lxb_char_t *) "href", 4,
                                             &href_len);
        if (href == NULL) {
            printf("[%zu] <a> without href, skipping.\n", i);
            continue;
        }

        printf("[%zu] href: %.*s\n", i, (int) href_len, (const char *) href);

        /* Resolve the href against the base URL. */

        lxb_url_parser_clean(&url_parser);

        url = lxb_url_parse(&url_parser, base_url, href, href_len);
        if (url == NULL) {
            printf("     Failed to parse URL.\n");
            continue;
        }

        printf("     Resolved: ");
        (void) lxb_url_serialize(url, callback, NULL, false);
        printf("\n");
    }

    /* Cleanup. */

    lxb_dom_collection_destroy(collection, true);
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

We create an HTML document object and parse our HTML string into it. After
parsing, the document contains a complete DOM tree just like in a browser.

### Step 2: Find All `<a>` Elements

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);

status = lxb_dom_elements_by_tag_name(
    lxb_dom_interface_element(document->body),
    collection, (const lxb_char_t *) "a", 1
);
```

We create a collection to hold the found elements. The second argument (`128`)
is the initial preallocated capacity of the collection; it will grow
automatically if needed.

`lxb_dom_elements_by_tag_name()` searches the subtree starting from
`document->body` for all elements with the tag name `"a"` (length `1`). The
results are placed into `collection`.

### Step 3: Initialize the URL Parser and Parse the Base URL

```c
status = lxb_url_parser_init(&url_parser, NULL);

base_url = lxb_url_parse(&url_parser, NULL, base_url_str, base_url_len);
```

The URL parser is initialized on the stack (passing `NULL` for `lexbor_mraw_t`
lets the parser create its own internal memory allocator).

We parse the base URL string `"https://example.com/blog/index.html"` first. The
second argument to `lxb_url_parse()` is `NULL` because this is an absolute URL
and requires no base.

### Step 4: Iterate Links, Extract `href`, and Resolve URLs

```c
href = lxb_dom_element_get_attribute(element,
                                     (const lxb_char_t *) "href", 4,
                                     &href_len);
```

For each `<a>` element in the collection, we get the `href` attribute value.
The function returns `NULL` if the attribute does not exist.

```c
lxb_url_parser_clean(&url_parser);

url = lxb_url_parse(&url_parser, base_url, href, href_len);
```

Before reusing the URL parser, we must call `lxb_url_parser_clean()`. Then we
parse the `href` value with `base_url` as the base. The URL module
automatically resolves relative URLs according to the
[WHATWG URL Standard](https://url.spec.whatwg.org/):

- `/about` resolves to `https://example.com/about`
- `news/today.html` resolves to `https://example.com/blog/news/today.html`
- `https://other.com/page` stays as is (already absolute)
- `../archive/2024.html` resolves to `https://example.com/archive/2024.html`

```c
(void) lxb_url_serialize(url, callback, NULL, false);
```

Finally, we serialize the resolved URL. The serialization uses a callback
function that is called with chunks of data. The last argument (`false`) means
the fragment is included in the output.


## Expected Output

```
Found 5 link(s).

[0] href: /about
     Resolved: https://example.com/about
[1] href: news/today.html
     Resolved: https://example.com/blog/news/today.html
[2] href: https://other.com/page
     Resolved: https://other.com/page
[3] href: ../archive/2024.html
     Resolved: https://example.com/archive/2024.html
[4] <a> without href, skipping.
```


## Building

Compile the example and run:

```sh
gcc extract_links.c -llexbor -o extract_links
./extract_links
```


## Summary

In this tutorial, we learned how to:

- Parse HTML with `lxb_html_document_parse()`.
- Find elements by tag name with `lxb_dom_elements_by_tag_name()`.
- Read attribute values with `lxb_dom_element_get_attribute()`.
- Parse and resolve URLs with `lxb_url_parse()` using a base URL.
- Serialize a URL back to a string with `lxb_url_serialize()`.
