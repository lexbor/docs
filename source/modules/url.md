# URL Module

* **Version:** 0.4.0
* **Path:** `source/lexbor/url`
* **Base Includes:** `lexbor/url/url.h`
* **Examples:** `examples/lexbor/url`
* **Specification:** [WHATWG URL Living Standard](https://url.spec.whatwg.org/)

## Overview

The URL module implements [WHATWG URL Living Standard](https://url.spec.whatwg.org/) for parsing, manipulating, and serializing URLs with full Unicode and internationalization support.
The module provides complete, specification-compliant URL parsing with IDNA (Internationalized Domain Names in Applications) and Punycode support.

## Key Features

- **Specification Compliant** — follows WHATWG URL Living Standard
- **Unicode Support** — handles international domain names with IDNA/Punycode
- **Relative URL Resolution** — parse relative URLs against a base URL
- **Component Access** — extract and modify individual URL components
- **Flexible Serialization** — convert URLs back to strings with callback or string output
- **URLSearchParams** — parse and manipulate query parameters

## What's Inside

- **URL Parser** — parse absolute and relative URLs with base URL support
- **URL Serialization** — convert URL objects to strings
- **URL Components** — access scheme, host, port, path, query, fragment
- **URL API** — modify URL
- **URLSearchParams** — parse and manipulate query strings
- **IDNA Support** — international domain names with Punycode encoding
- **Host Types** — domain, opaque, IPv4, IPv6, empty host types
- **Memory Management** — efficient memory allocation and cleanup

## Quick Start

### Basic URL Parsing

```C
#include <lexbor/url/url.h>

int main(void)
{
    const lxb_char_t url_str[] = "https://example.com:8080/path?query=value#fragment";

    /* Create and initialize parser */
    lxb_url_parser_t *parser = lxb_url_parser_create();
    if (parser == NULL) {
        return EXIT_FAILURE;
    }

    lxb_status_t status = lxb_url_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Parse URL */
    lxb_url_t *url = lxb_url_parse(parser, NULL, url_str, sizeof(url_str) - 1);
    if (url == NULL) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Access components */
    printf("Scheme: %.*s\n",
           (int) lxb_url_scheme(url)->length,
           lxb_url_scheme(url)->data);

    printf("Port: %u\n", lxb_url_port(url));

    printf("Path: %.*s\n",
           (int) lxb_url_path_str(url)->length,
           lxb_url_path_str(url)->data);

    /* Cleanup */
    lxb_url_memory_destroy(url);
    lxb_url_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```


*(Documentation is currently being developed, details will be available here soon.)*
