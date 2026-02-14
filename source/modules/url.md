# URL Module

* **Version:** 0.4.0
* **Path:** `source/lexbor/url`
* **Base Includes:** `lexbor/url/url.h`
* **Examples:** `examples/lexbor/url`
* **Specification:** [WHATWG URL Living Standard](https://url.spec.whatwg.org/)

## Overview

The URL module implements [WHATWG URL Living Standard](https://url.spec.whatwg.org/) for parsing, manipulating, and serializing URLs.

Browsers use this exact algorithm to process every URL you type in the address bar, click in a link, or set in JavaScript. This module gives you the same behavior in C — byte-for-byte compatible with how browsers parse URLs.

Why does this matter? Because URLs are surprisingly tricky. The WHATWG specification defines a complex state machine with many edge cases to handle all the weird and wonderful URLs that exist in the wild. By following this spec, lexbor's URL module ensures that you get the same results as browsers do.

## Key Features

- **Specification Compliant** — follows WHATWG URL Living Standard
- **Unicode Support** — handles international domain names with IDNA/Punycode
- **Relative URL Resolution** — parse relative URLs against a base URL
- **Component Access** — extract and modify individual URL components
- **Serialization** — convert URL objects to strings (callback or string output)
- **URLSearchParams** — parse and manipulate query parameters
- **URL API** — modify individual URL components after parsing (href, host, port, path, etc.)

## What's Inside

- **[Quick Start](#quick-start)** — minimal working example to get started
- **[URL Structure](#url-structure)** — what a parsed URL looks like
- **[Parsing URLs](#parsing-urls)** — parse absolute and relative URLs
- **[Relative URL Resolution](#relative-url-resolution)** — resolve relative URLs against a base
- **[Serialization](#serialization)** — convert URL objects back to strings
- **[Accessing URL Components](#accessing-url-components)** — read individual parts of a URL
- **[Modifying URLs (URL API)](#modifying-urls-url-api)** — change URL components after parsing
- **[URLSearchParams](#urlsearchparams)** — work with query string parameters
- **[Special Schemes](#special-schemes)** — how http, https, ftp, file, ws, wss are handled differently
- **[Memory Management](#memory-management)** — how memory works for URL objects
- **[Error Handling](#error-handling)** — validation errors and logging

## Quick Start

### Basic URL Parsing

```C
#include <lexbor/url/url.h>

int main(void)
{
    lxb_url_t *url;
    lxb_status_t status;
    lxb_url_parser_t parser;

    static const lxb_char_t url_str[]
        = "https://example.com:8080/path?query=value#fragment";

    /* Initialize parser (on the stack) */
    status = lxb_url_parser_init(&parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Parse URL */
    url = lxb_url_parse(&parser, NULL, url_str, sizeof(url_str) - 1);
    if (url == NULL) {
        lxb_url_parser_destroy(&parser, false);
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
    lxb_url_parser_destroy(&parser, false);
    lxb_url_memory_destroy(url);

    return EXIT_SUCCESS;
}
```

Output:
```
Scheme: https
Port: 8080
Path: /path
```

## URL Structure

A URL has the following structure according to the WHATWG specification:

```
  https://user:password@example.com:8080/path/to/page?key=value#section
  \___/   \__/ \______/ \_________/ \__/\___________/\________/\______/
    |       |      |         |        |       |           |        |
  scheme  user  password   host     port    path       query   fragment
```

After parsing, a URL is represented by the `lxb_url_t` structure. Each component can be accessed through inline functions:

| Component | Accessor | Returns |
|-----------|----------|---------|
| Scheme | `lxb_url_scheme(url)` | `const lexbor_str_t *` — e.g. `"https"` |
| Username | `lxb_url_username(url)` | `const lexbor_str_t *` |
| Password | `lxb_url_password(url)` | `const lexbor_str_t *` |
| Host | `lxb_url_host(url)` | `const lxb_url_host_t *` |
| Port | `lxb_url_port(url)` | `uint16_t` |
| Has Port | `lxb_url_has_port(url)` | `bool` — true if port was explicitly set |
| Path | `lxb_url_path(url)` | `const lxb_url_path_t *` |
| Path (string) | `lxb_url_path_str(url)` | `const lexbor_str_t *` — e.g. `"/path/to/page"` |
| Query | `lxb_url_query(url)` | `const lexbor_str_t *` — e.g. `"key=value"` (without `?`) |
| Fragment | `lxb_url_fragment(url)` | `const lexbor_str_t *` — e.g. `"section"` (without `#`) |

**Note about `lexbor_str_t`:** This is lexbor's string type with `data` (pointer to characters) and `length` fields. If a component is absent, `data` will be `NULL` and `length` will be `0`.

## Parsing URLs

### Parser Lifecycle

The URL parser has the standard create/init/clean/destroy lifecycle:

```C
/* Option 1: Stack allocation (recommended for simple use) */
lxb_url_parser_t parser;
lxb_url_parser_init(&parser, NULL);
/* ... use parser ... */
lxb_url_parser_destroy(&parser, false);  /* false = don't free the struct */

/* Option 2: Heap allocation */
lxb_url_parser_t *parser = lxb_url_parser_create();
lxb_url_parser_init(parser, NULL);
/* ... use parser ... */
lxb_url_parser_destroy(parser, true);  /* true = free the struct too */
```

**Important:** The parser is not bound to the URLs it creates. After parsing, you can destroy the parser and continue working with the parsed URL objects. Each URL stores a pointer to its own memory allocator.

### Parsing an Absolute URL

```C
lxb_url_t *url = lxb_url_parse(&parser, NULL, url_str, url_str_length);
if (url == NULL) {
    /* Parsing failed — invalid URL */
}
```

The second argument (`NULL` here) is the base URL. Pass `NULL` when parsing absolute URLs.

### Reusing the Parser

To parse multiple URLs with the same parser, call `lxb_url_parser_clean()` between parses:

```C
lxb_url_parser_t parser;
lxb_url_parser_init(&parser, NULL);

lxb_url_t *url1 = lxb_url_parse(&parser, NULL, str1, len1);

/* Clean parser state before next parse */
lxb_url_parser_clean(&parser);

lxb_url_t *url2 = lxb_url_parse(&parser, NULL, str2, len2);

/* Both url1 and url2 are valid and independent */

lxb_url_parser_destroy(&parser, false);

/* URLs are still alive — parser doesn't own them */
lxb_url_destroy(url1);
lxb_url_destroy(url2);
```

### Basic URL Parser

For advanced use cases, `lxb_url_parse_basic()` gives more control:

```C
lxb_status_t status = lxb_url_parse_basic(
    &parser,
    NULL,               /* existing URL to update, or NULL to create new */
    NULL,               /* base URL */
    data, length,       /* input string */
    LXB_URL_STATE__UNDEF,  /* override state (UNDEF = default) */
    LXB_ENCODING_UTF_8    /* input encoding */
);
```

After `lxb_url_parse_basic()` succeeds, retrieve the URL with `lxb_url_get(&parser)`.

This function allows you to:
- Start parsing from a specific state (e.g., `LXB_URL_STATE_HOST_STATE` to parse only the host part)
- Specify input encoding other than UTF-8
- Update an existing URL object instead of creating a new one

## Relative URL Resolution

Relative URLs are resolved against a base URL. This is exactly what browsers do when they encounter a relative link on a page.

```C
#include <lexbor/url/url.h>

int main(void)
{
    lxb_url_t *url, *base_url;
    lxb_status_t status;
    lxb_url_parser_t parser;

    static const lxb_char_t base_str[] = "https://example.com:2030/";
    static const lxb_char_t rel_str[] = "/path/to/page?id=123#comments";

    status = lxb_url_parser_init(&parser, NULL);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* First, parse the base URL */
    base_url = lxb_url_parse(&parser, NULL,
                              base_str, sizeof(base_str) - 1);
    if (base_url == NULL) {
        return EXIT_FAILURE;
    }

    lxb_url_parser_clean(&parser);

    /* Parse relative URL against the base */
    url = lxb_url_parse(&parser, base_url,
                         rel_str, sizeof(rel_str) - 1);
    if (url == NULL) {
        return EXIT_FAILURE;
    }

    /* url is now: https://example.com:2030/path/to/page?id=123#comments */

    lxb_url_parser_destroy(&parser, false);
    lxb_url_memory_destroy(url);

    return EXIT_SUCCESS;
}
```

The resolution follows the WHATWG algorithm:
- `"/path"` with base `"https://example.com/"` -> `"https://example.com/path"`
- `"../other"` with base `"https://example.com/a/b/"` -> `"https://example.com/a/other"`
- `"?q=1"` with base `"https://example.com/page"` -> `"https://example.com/page?q=1"`
- `"#frag"` with base `"https://example.com/page?q=1"` -> `"https://example.com/page?q=1#frag"`
- `"https://other.com"` with any base -> `"https://other.com"` (absolute URL ignores base)

## Serialization

Serialization converts a parsed URL object back into a string. The module provides callback-based serialization for all URL components.

### Full URL Serialization

```C
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

/* Serialize full URL */
lxb_url_serialize(url, callback, NULL, false);
/* false = include fragment; true = exclude fragment */
```

**Note:** The callback may be called multiple times for a single URL. For example, serializing `https://example.com/path` will call the callback separately for `https`, `://`, `example.com`, and `/path`.

### Unicode Domain Serialization

By default, international domain names are stored in their ASCII (Punycode) form. To serialize them back to Unicode, use `lxb_url_serialize_idna()`:

```C
lxb_unicode_idna_t idna;

lxb_unicode_idna_init(&idna);

/* Serialize with Unicode domain names */
lxb_url_serialize_idna(&idna, url, callback, NULL, false);

lxb_unicode_idna_destroy(&idna, false);
```

For a URL like `https://тест.com/`, `lxb_url_serialize()` outputs `https://xn--e1afmapc.com/`, while `lxb_url_serialize_idna()` outputs `https://тест.com/`.

### Component Serialization

Each URL component can be serialized individually:

```C
lxb_url_serialize_scheme(url, callback, ctx);      /* "https"       */
lxb_url_serialize_username(url, callback, ctx);    /* "user"        */
lxb_url_serialize_password(url, callback, ctx);    /* "pass"        */
lxb_url_serialize_host(host, callback, ctx);       /* "example.com" */
lxb_url_serialize_port(url, callback, ctx);        /* "8080"        */
lxb_url_serialize_path(path, callback, ctx);       /* "/path"       */
lxb_url_serialize_query(url, callback, ctx);       /* "key=value"   */
lxb_url_serialize_fragment(url, callback, ctx);    /* "section"     */
```

Note that `lxb_url_serialize_host()` takes `const lxb_url_host_t *` (use `lxb_url_host(url)`) and `lxb_url_serialize_path()` takes `const lxb_url_path_t *` (use `lxb_url_path(url)`).

For Unicode domain serialization:

```C
lxb_url_serialize_host_unicode(&idna, lxb_url_host(url), callback, ctx);
```

There are also specialized host serialization functions:

```C
lxb_url_serialize_host_ipv4(ipv4_value, callback, ctx);   /* "192.168.0.1"    */
lxb_url_serialize_host_ipv6(ipv6_array, callback, ctx);   /* "[::1]"          */
```

## Accessing URL Components

After parsing, use inline accessor functions to read URL components:

```C
lxb_url_t *url = lxb_url_parse(&parser, NULL, str, len);

/* Scheme: always present after successful parse */
const lexbor_str_t *scheme = lxb_url_scheme(url);
printf("Scheme: %.*s\n", (int) scheme->length, scheme->data);

/* Host: check type before accessing */
const lxb_url_host_t *host = lxb_url_host(url);

if (host->type == LXB_URL_HOST_TYPE_DOMAIN) {
    printf("Domain: %.*s\n",
           (int) host->u.domain.length, host->u.domain.data);
}
else if (host->type == LXB_URL_HOST_TYPE_IPV4) {
    printf("IPv4: %u\n", host->u.ipv4);
}

/* Port: check if explicitly present */
if (lxb_url_has_port(url)) {
    printf("Port: %u\n", lxb_url_port(url));
}

/* Path */
const lexbor_str_t *path = lxb_url_path_str(url);
if (path->data != NULL) {
    printf("Path: %.*s\n", (int) path->length, path->data);
}

/* Query */
const lexbor_str_t *query = lxb_url_query(url);
if (query->data != NULL) {
    printf("Query: %.*s\n", (int) query->length, query->data);
}

/* Fragment */
const lexbor_str_t *fragment = lxb_url_fragment(url);
if (fragment->data != NULL) {
    printf("Fragment: %.*s\n", (int) fragment->length, fragment->data);
}

/* Credentials */
const lexbor_str_t *user = lxb_url_username(url);
const lexbor_str_t *pass = lxb_url_password(url);
if (user->length > 0) {
    printf("User: %.*s\n", (int) user->length, user->data);
}
```

## Modifying URLs (URL API)

After parsing a URL, you can modify individual components using the URL API functions. These follow the [WHATWG URL API](https://url.spec.whatwg.org/#api) specification — the same interface that JavaScript's `URL` object provides.

All API functions accept `NULL` as the data pointer, which is treated as an empty string.

```C
lxb_url_t *url = lxb_url_parse(&parser, NULL, str, len);

/* Change the protocol (scheme) */
lxb_url_api_protocol_set(url, &parser,
                          (lxb_char_t *) "http:", 5);

/* Change the host */
lxb_url_api_host_set(url, &parser,
                      (lxb_char_t *) "other.com:9090", 14);

/* Change just the hostname (without port) */
lxb_url_api_hostname_set(url, &parser,
                          (lxb_char_t *) "new.com", 7);

/* Change the port */
lxb_url_api_port_set(url, &parser,
                      (lxb_char_t *) "3000", 4);

/* Change the path */
lxb_url_api_pathname_set(url, &parser,
                          (lxb_char_t *) "/new/path", 9);

/* Change the query */
lxb_url_api_search_set(url, &parser,
                        (lxb_char_t *) "?newkey=newval", 13);

/* Change the fragment */
lxb_url_api_hash_set(url, &parser,
                      (lxb_char_t *) "#new-section", 12);

/* Change credentials */
lxb_url_api_username_set(url, (lxb_char_t *) "admin", 5);
lxb_url_api_password_set(url, (lxb_char_t *) "secret", 6);

/* Replace the entire URL */
lxb_url_api_href_set(url, &parser,
                      (lxb_char_t *) "https://completely.new/url", 26);
```

**Note:** The `parser` parameter is optional for some API functions. If you pass `NULL`, parsing still works but no validation logs will be generated. The `lxb_url_api_username_set()` and `lxb_url_api_password_set()` functions don't need a parser at all.

## URLSearchParams

URLSearchParams provides a convenient way to work with URL query string parameters. It implements the [URLSearchParams](https://url.spec.whatwg.org/#interface-urlsearchparams) interface from the WHATWG specification — the same API available in JavaScript.

### Creating from a Query String

```C
#include <lexbor/url/url.h>

/* URLSearchParams needs a memory allocator */
lexbor_mraw_t *mraw = lexbor_mraw_create();
lexbor_mraw_init(mraw, 256);

/* Parse query parameters */
static const lxb_char_t query[] = "name=Alice&age=30&color=blue&color=red";

lxb_url_search_params_t *sp = lxb_url_search_params_init(
    mraw, query, sizeof(query) - 1
);

/* sp now contains 4 entries: name=Alice, age=30, color=blue, color=red */
```

You can also use the memory allocator from a parsed URL:

```C
lxb_url_t *url = lxb_url_parse(&parser, NULL, str, len);

/* Use the URL's own memory allocator */
lxb_url_search_params_t *sp = lxb_url_search_params_init(
    url->mraw, lxb_url_query(url)->data, lxb_url_query(url)->length
);
```

### Getting Values

```C
/* Get the first value for a parameter name */
lexbor_str_t *value = lxb_url_search_params_get(sp,
    (lxb_char_t *) "name", 4);

if (value != NULL) {
    printf("name = %.*s\n", (int) value->length, value->data);
}

/* Get the entry object (has both name and value) */
lxb_url_search_entry_t *entry = lxb_url_search_params_get_entry(sp,
    (lxb_char_t *) "name", 4);

/* Get count of values for a parameter name */
size_t count = lxb_url_search_params_get_count(sp,
    (lxb_char_t *) "color", 5);
/* count = 2 (blue, red) */

/* Get all values for a parameter name */
lexbor_str_t *buf[10];
size_t found = lxb_url_search_params_get_all(sp,
    (lxb_char_t *) "color", 5, buf, 10);
/* found = 2, buf[0] = "blue", buf[1] = "red" */
```

### Checking Existence

```C
/* Check if parameter name exists */
bool exists = lxb_url_search_params_has(sp,
    (lxb_char_t *) "name", 4, NULL, 0);

/* Check if specific name=value pair exists */
bool exact = lxb_url_search_params_has(sp,
    (lxb_char_t *) "color", 5,
    (lxb_char_t *) "blue", 4);
```

### Adding and Modifying

```C
/* Append a new parameter (duplicates allowed) */
lxb_url_search_params_append(sp,
    (lxb_char_t *) "lang", 4,
    (lxb_char_t *) "en", 2);

/* Set a parameter (removes all existing with this name, creates one) */
lxb_url_search_params_set(sp,
    (lxb_char_t *) "color", 5,
    (lxb_char_t *) "green", 5);
/* Now there is only one color=green (blue and red were removed) */
```

### Deleting

```C
/* Delete all parameters with a given name */
lxb_url_search_params_delete(sp,
    (lxb_char_t *) "age", 3, NULL, 0);

/* Delete only a specific name=value pair */
lxb_url_search_params_delete(sp,
    (lxb_char_t *) "color", 5,
    (lxb_char_t *) "blue", 4);
```

### Sorting

```C
/* Sort parameters alphabetically by name */
lxb_url_search_params_sort(sp);
```

### Serialization

```C
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

/* Serialize to application/x-www-form-urlencoded format */
lxb_url_search_params_serialize(sp, callback, NULL);
/* Outputs: "name=Alice&color=green&lang=en" */
```

The callback is called exactly once with the fully prepared string.

### Iteration

You can iterate through matching entries using a callback:

```C
static lexbor_action_t
match_cb(lxb_url_search_params_t *sp,
         lxb_url_search_entry_t *entry, void *ctx)
{
    printf("%.*s = %.*s\n",
           (int) entry->name.length, entry->name.data,
           (int) entry->value.length, entry->value.data);

    return LEXBOR_ACTION_OK;  /* continue iteration */
    /* return LEXBOR_ACTION_STOP to stop early */
}

/* Iterate all entries with name "color" */
lxb_url_search_params_match(sp,
    (lxb_char_t *) "color", 5, NULL, 0,
    match_cb, NULL);
```

Or iterate manually using `lxb_url_search_params_match_entry()`:

```C
lxb_url_search_entry_t *entry = NULL;

while ((entry = lxb_url_search_params_match_entry(sp,
    (lxb_char_t *) "color", 5, NULL, 0, entry)) != NULL)
{
    printf("color = %.*s\n",
           (int) entry->value.length, entry->value.data);
}
```

### Cleanup

```C
lxb_url_search_params_destroy(sp);
lexbor_mraw_destroy(mraw, true);
```

## Special Schemes

The URL specification defines a set of "special" schemes with default ports and specific parsing rules:

| Scheme | Default Port | Notes |
|--------|-------------|-------|
| `http` | 80 | |
| `https` | 443 | |
| `ws` | 80 | WebSocket |
| `wss` | 443 | Secure WebSocket |
| `ftp` | 21 | |
| `file` | — | No port, no credentials |

Special schemes have the following behavior differences:
- **Default ports are implicit.** Parsing `https://example.com:443/` will not store port 443 — `lxb_url_has_port()` returns `false`, because 443 is the default for HTTPS.
- **Host is required.** `http:path` is invalid. Non-special schemes like `foo:path` are valid.
- **Backslash `\` is treated as `/`** in the authority and path. `https://example.com\path` is parsed as `https://example.com/path`.
- **Two slashes `//` are expected** after the scheme. `http://host` is the normal form.

Non-special schemes (like `data:`, `mailto:`, `blob:`, or any custom scheme) have more relaxed rules: they can have opaque paths, don't require a host, and don't have default ports.

### International Domain Names

Domain names with non-ASCII characters (like `тест.com` or `münchen.de`) are automatically converted to their ASCII (Punycode) representation during parsing. So `тест.com` becomes `xn--e1afmapc.com` in the parsed URL.

To display the domain back in Unicode form, use `lxb_url_serialize_host_unicode()` with an IDNA object (see [Serialization](#serialization)).

## Memory Management

The URL module uses `lexbor_mraw_t` as its memory allocator.

### How It Works

1. When you call `lxb_url_parser_init(&parser, NULL)`, the parser creates its own `lexbor_mraw_t` object internally.
2. Every URL created by `lxb_url_parse()` gets its memory from this allocator and stores a pointer to it (`url->mraw`).
3. The parser and URLs are **independent** — destroying the parser does NOT destroy the URLs.

### Destroying a Single URL

```C
lxb_url_t *url = lxb_url_parse(&parser, NULL, str, len);
/* ... use url ... */
lxb_url_destroy(url);  /* Frees this URL's memory */
```

### Destroying All URLs at Once

If you created multiple URLs from the same parser, you can destroy all of them at once by destroying the memory allocator:

```C
lxb_url_t *url1 = lxb_url_parse(&parser, NULL, str1, len1);
lxb_url_parser_clean(&parser);
lxb_url_t *url2 = lxb_url_parse(&parser, NULL, str2, len2);

/* Destroy all URLs created by this parser's allocator */
lxb_url_memory_destroy(url1);
/* Both url1 and url2 are now invalid — they shared the same allocator */
```

You can also destroy all URLs via the parser:

```C
lxb_url_parser_memory_destroy(&parser);
/* All URLs created by this parser are now invalid */
```

### Using a Custom Memory Allocator

You can pass your own `lexbor_mraw_t` to the parser:

```C
lexbor_mraw_t *mraw = lexbor_mraw_create();
lexbor_mraw_init(mraw, 4096);

lxb_url_parser_init(&parser, mraw);

/* URLs will use your allocator */
lxb_url_t *url = lxb_url_parse(&parser, NULL, str, len);

/* You manage the allocator's lifecycle */
lexbor_mraw_destroy(mraw, true);  /* Destroys all URLs too */
```

### Replacing the Allocator

After calling `lxb_url_parser_memory_destroy()`, you need to assign a new allocator before parsing again:

```C
lxb_url_parser_memory_destroy(&parser);
/* parser->mraw is now garbage */

lexbor_mraw_t *new_mraw = lexbor_mraw_create();
lexbor_mraw_init(new_mraw, 4096);

lxb_url_mraw_set(&parser, new_mraw);
/* Parser is ready to create new URLs */
```

### Cloning a URL

You can clone a URL, optionally into a different memory allocator:

```C
/* Clone into the same allocator */
lxb_url_t *copy = lxb_url_clone(url->mraw, url);

/* Clone into a different allocator */
lexbor_mraw_t *other_mraw = lexbor_mraw_create();
lexbor_mraw_init(other_mraw, 4096);

lxb_url_t *independent_copy = lxb_url_clone(other_mraw, url);
/* independent_copy has its own memory — original can be destroyed */
```

## Error Handling

### Parse Errors

`lxb_url_parse()` returns `NULL` if the URL is invalid. `lxb_url_parse_basic()` returns a status code.

The parser generates validation errors for various issues during parsing. These correspond to the validation errors defined in the WHATWG specification:

| Error Type | Description |
|-----------|-------------|
| `LXB_URL_ERROR_TYPE_DOMAIN_TO_ASCII` | IDNA encoding failed |
| `LXB_URL_ERROR_TYPE_DOMAIN_INVALID_CODE_POINT` | Invalid character in domain |
| `LXB_URL_ERROR_TYPE_HOST_INVALID_CODE_POINT` | Invalid character in host |
| `LXB_URL_ERROR_TYPE_IPV4_TOO_MANY_PARTS` | IPv4 address has more than 4 parts |
| `LXB_URL_ERROR_TYPE_IPV4_OUT_OF_RANGE_PART` | IPv4 part exceeds 255 |
| `LXB_URL_ERROR_TYPE_IPV6_UNCLOSED` | Missing closing `]` in IPv6 |
| `LXB_URL_ERROR_TYPE_IPV6_TOO_MANY_PIECES` | IPv6 has more than 8 groups |
| `LXB_URL_ERROR_TYPE_INVALID_URL_UNIT` | Invalid character in URL |
| `LXB_URL_ERROR_TYPE_MISSING_SCHEME_NON_RELATIVE_URL` | No scheme and no base URL |
| `LXB_URL_ERROR_TYPE_HOST_MISSING` | Special scheme requires a host |
| `LXB_URL_ERROR_TYPE_PORT_OUT_OF_RANGE` | Port number exceeds 65535 |
| `LXB_URL_ERROR_TYPE_PORT_INVALID` | Port contains non-numeric characters |
| `LXB_URL_ERROR_TYPE_INVALID_CREDENTIALS` | Credentials in URL where not allowed |

All error types are defined in the `lxb_url_error_type_t` enum.
