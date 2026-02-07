# URL Module

* **Version:** 0.4.0
* **Path:** `source/lexbor/url`
* **Base Includes:** `lexbor/url/url.h`
* **Examples:** `examples/lexbor/url`
* **Specification:** [WHATWG URL Living Standard](https://url.spec.whatwg.org/)

## Overview

The URL module implements the [WHATWG URL Living Standard](https://url.spec.whatwg.org/) for parsing, manipulating, and serializing URLs. It provides full Unicode and internationalization support through IDNA (Internationalized Domain Names in Applications) and Punycode encoding via the [Unicode module](unicode.md).

## Supported Features

- Complete URL parsing per WHATWG specification
- Relative URL resolution against a base URL
- URL API for modifying individual components (scheme, host, port, path, query, fragment, credentials)
- Host parsing: domain names, opaque hosts, IPv4, IPv6
- Special scheme handling: `http`, `https`, `ws`, `wss`, `ftp`, `file`
- URLSearchParams for query string manipulation
- Callback-based and component-level serialization
- URL cloning
- IDNA/Punycode for international domain names


## URL Parser (`lxb_url_parser_t`)

The URL parser creates URL objects from string input. Defined in `lexbor/url/url.h`.

### Lifecycle

```c
lxb_url_parser_t *
lxb_url_parser_create(void);

lxb_status_t
lxb_url_parser_init(lxb_url_parser_t *parser, lexbor_mraw_t *mraw);

void
lxb_url_parser_clean(lxb_url_parser_t *parser);

lxb_url_parser_t *
lxb_url_parser_destroy(lxb_url_parser_t *parser, bool destroy_self);
```

- `lxb_url_parser_init()`: The `mraw` parameter is a memory allocator for created URLs. If `NULL`, the parser creates its own. All URLs created by this parser share this allocator — destroying the allocator destroys all associated URLs.
- `lxb_url_parser_clean()`: Resets parser state. **Must** be called between successive parse calls.
- `lxb_url_parser_destroy()`: Destroys the parser but **does not** destroy the memory allocator or any created URLs. If `destroy_self` is `true`, frees the parser object itself.

### Memory Management

The parser and URLs share a `lexbor_mraw_t` memory allocator. Understanding the ownership model is important:

```c
/* Destroy the parser's memory allocator and ALL associated URLs */
void
lxb_url_parser_memory_destroy(lxb_url_parser_t *parser);

/* Destroy a single URL */
lxb_url_t *
lxb_url_destroy(lxb_url_t *url);

/* Destroy the memory allocator referenced by this URL (and ALL URLs sharing it) */
void
lxb_url_memory_destroy(lxb_url_t *url);

/* Get/set the parser's memory allocator */
lexbor_mraw_t *
lxb_url_mraw(lxb_url_parser_t *parser);

void
lxb_url_mraw_set(lxb_url_parser_t *parser, lexbor_mraw_t *mraw);
```

- `lxb_url_destroy()`: Frees a single URL's internal data.
- `lxb_url_memory_destroy()`: Destroys the `lexbor_mraw_t` allocator associated with the URL, which destroys **all** URLs that share that allocator. If the parser still references this allocator, you must assign a new one with `lxb_url_mraw_set()` before parsing again.
- `lxb_url_parser_memory_destroy()`: Same as above, accessed through the parser.

### Parsing

```c
lxb_url_t *
lxb_url_parse(lxb_url_parser_t *parser, const lxb_url_t *base_url,
              const lxb_char_t *data, size_t length);

lxb_status_t
lxb_url_parse_basic(lxb_url_parser_t *parser, lxb_url_t *url,
                    const lxb_url_t *base_url,
                    const lxb_char_t *data, size_t length,
                    lxb_url_state_t override_state, lxb_encoding_t encoding);
```

- `lxb_url_parse()`: Parses a URL string and returns a new `lxb_url_t` object. Pass a `base_url` to resolve relative URLs, or `NULL` for absolute URLs. Returns `NULL` on failure.
- `lxb_url_parse_basic()`: Lower-level parser. Can parse into an existing `lxb_url_t` (pass `NULL` to create a new one). Supports overriding the start state and encoding. Use `LXB_URL_STATE__UNDEF` and `LXB_ENCODING_DEFAULT` for defaults. The resulting URL is retrieved with `lxb_url_get(parser)`.


## URL Structure (`lxb_url_t`)

A parsed URL. Defined in `lexbor/url/url.h`.

```c
typedef struct {
    lxb_url_scheme_t   scheme;
    lxb_url_host_t     host;
    lexbor_str_t       username;
    lexbor_str_t       password;
    uint16_t           port;
    bool               has_port;
    lxb_url_path_t     path;
    lexbor_str_t       query;
    lexbor_str_t       fragment;
    lexbor_mraw_t      *mraw;
} lxb_url_t;
```

### Component Accessors

Inline functions for reading URL components:

```c
const lexbor_str_t *   lxb_url_scheme(const lxb_url_t *url);
const lexbor_str_t *   lxb_url_username(const lxb_url_t *url);
const lexbor_str_t *   lxb_url_password(const lxb_url_t *url);
const lxb_url_host_t * lxb_url_host(const lxb_url_t *url);
uint16_t               lxb_url_port(const lxb_url_t *url);
bool                   lxb_url_has_port(const lxb_url_t *url);
const lxb_url_path_t * lxb_url_path(const lxb_url_t *url);
const lexbor_str_t *   lxb_url_path_str(const lxb_url_t *url);
const lexbor_str_t *   lxb_url_query(const lxb_url_t *url);
const lexbor_str_t *   lxb_url_fragment(const lxb_url_t *url);
```

String components (`lexbor_str_t`) have `data` and `length` fields. A component is absent when its `data` is `NULL`.

### Cloning

```c
lxb_url_t *
lxb_url_clone(lexbor_mraw_t *mraw, const lxb_url_t *url);
```

Creates a deep copy of a URL. Use `url->mraw` to clone into the same memory pool, or pass a different allocator.


## Scheme Types

```c
typedef enum {
    LXB_URL_SCHEMEL_TYPE__UNDEF   = 0x00,
    LXB_URL_SCHEMEL_TYPE__UNKNOWN = 0x01,
    LXB_URL_SCHEMEL_TYPE_HTTP     = 0x02,
    LXB_URL_SCHEMEL_TYPE_HTTPS    = 0x03,
    LXB_URL_SCHEMEL_TYPE_WS       = 0x04,
    LXB_URL_SCHEMEL_TYPE_WSS      = 0x05,
    LXB_URL_SCHEMEL_TYPE_FTP      = 0x06,
    LXB_URL_SCHEMEL_TYPE_FILE     = 0x07
} lxb_url_scheme_type_t;
```

The scheme is stored in `lxb_url_scheme_t` which contains both the string `name` and a `type` field for fast comparisons. Special schemes (`http`, `https`, `ws`, `wss`, `ftp`, `file`) have known types; all others are `_UNKNOWN`.


## Host Types

```c
typedef enum {
    LXB_URL_HOST_TYPE__UNDEF = 0x00,
    LXB_URL_HOST_TYPE_DOMAIN = 0x01,
    LXB_URL_HOST_TYPE_OPAQUE = 0x02,
    LXB_URL_HOST_TYPE_IPV4   = 0x03,
    LXB_URL_HOST_TYPE_IPV6   = 0x04,
    LXB_URL_HOST_TYPE_EMPTY  = 0x05
} lxb_url_host_type_t;
```

The host is stored in `lxb_url_host_t` with a tagged union:

```c
typedef struct {
    lxb_url_host_type_t type;
    union {
        uint16_t     ipv6[8];   /* 8 x 16-bit pieces */
        uint32_t     ipv4;      /* 32-bit address    */
        lexbor_str_t opaque;    /* opaque host string */
        lexbor_str_t domain;    /* domain string      */
    } u;
} lxb_url_host_t;
```

Check `host->type` before accessing the union.


## URL API (Setters)

Functions for modifying URL components per the [URL API specification](https://url.spec.whatwg.org/#api). The `parser` parameter is optional — pass it to collect parsing logs, or `NULL` to skip logging.

```c
lxb_status_t lxb_url_api_href_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                   const lxb_char_t *href, size_t length);

lxb_status_t lxb_url_api_protocol_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                       const lxb_char_t *protocol, size_t length);

lxb_status_t lxb_url_api_username_set(lxb_url_t *url,
                                       const lxb_char_t *username, size_t length);

lxb_status_t lxb_url_api_password_set(lxb_url_t *url,
                                       const lxb_char_t *password, size_t length);

lxb_status_t lxb_url_api_host_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                   const lxb_char_t *host, size_t length);

lxb_status_t lxb_url_api_hostname_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                       const lxb_char_t *hostname, size_t length);

lxb_status_t lxb_url_api_port_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                   const lxb_char_t *port, size_t length);

lxb_status_t lxb_url_api_pathname_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                       const lxb_char_t *pathname, size_t length);

lxb_status_t lxb_url_api_search_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                     const lxb_char_t *search, size_t length);

lxb_status_t lxb_url_api_hash_set(lxb_url_t *url, lxb_url_parser_t *parser,
                                   const lxb_char_t *hash, size_t length);
```

- `lxb_url_api_host_set()`: Sets both hostname and port (e.g., `"example.com:8080"`).
- `lxb_url_api_hostname_set()`: Sets hostname only.
- All functions accept `NULL` as the data pointer to clear the component.


## Serialization

Callback-based serialization for the full URL or individual components. The callback may be invoked multiple times per call.

```c
lxb_status_t
lxb_url_serialize(const lxb_url_t *url, lexbor_serialize_cb_f cb, void *ctx,
                  bool exclude_fragment);
```

Pass `exclude_fragment` as `true` to omit the fragment from output.

### Component Serialization

```c
lxb_status_t lxb_url_serialize_scheme(const lxb_url_t *url,
                                       lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_username(const lxb_url_t *url,
                                         lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_password(const lxb_url_t *url,
                                         lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_host(const lxb_url_host_t *host,
                                     lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_port(const lxb_url_t *url,
                                     lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_path(const lxb_url_path_t *path,
                                     lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_query(const lxb_url_t *url,
                                      lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_fragment(const lxb_url_t *url,
                                         lexbor_serialize_cb_f cb, void *ctx);
```

### Host Serialization Variants

```c
lxb_status_t lxb_url_serialize_host_unicode(lxb_unicode_idna_t *idna,
                                             const lxb_url_host_t *host,
                                             lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_host_ipv4(uint32_t ipv4,
                                          lexbor_serialize_cb_f cb, void *ctx);
lxb_status_t lxb_url_serialize_host_ipv6(const uint16_t *ipv6,
                                          lexbor_serialize_cb_f cb, void *ctx);
```

There is also `lxb_url_serialize_idna()` which serializes the full URL with Unicode domain display using an IDNA context.


## URLSearchParams (`lxb_url_search_params_t`)

Implements the [URLSearchParams](https://url.spec.whatwg.org/#interface-urlsearchparams) interface for parsing and manipulating query parameters.

### Structure

```c
typedef struct lxb_url_search_entry {
    lexbor_str_t           name;
    lexbor_str_t           value;
    lxb_url_search_entry_t *next;
    lxb_url_search_entry_t *prev;
} lxb_url_search_entry_t;

typedef struct {
    lxb_url_search_entry_t *first;
    lxb_url_search_entry_t *last;
    lexbor_mraw_t          *mraw;
    size_t                 length;
} lxb_url_search_params_t;
```

Parameters are stored as a doubly-linked list of name/value entries.

### Lifecycle

```c
lxb_url_search_params_t *
lxb_url_search_params_init(lexbor_mraw_t *mraw,
                           const lxb_char_t *params, size_t length);

lxb_url_search_params_t *
lxb_url_search_params_destroy(lxb_url_search_params_t *search_params);
```

- `lxb_url_search_params_init()`: Creates and initializes from a query string (e.g., `"key1=val1&key2=val2"`). The `mraw` parameter is required and can be taken from a URL's `mraw` field. Pass `NULL`/`0` for `params`/`length` to create an empty set.

### Operations

```c
/* Append a name/value pair (duplicates allowed) */
lxb_url_search_entry_t *
lxb_url_search_params_append(lxb_url_search_params_t *sp,
                             const lxb_char_t *name, size_t name_length,
                             const lxb_char_t *value, size_t value_length);

/* Delete entries by name; if value is non-NULL, only matching name+value pairs */
void
lxb_url_search_params_delete(lxb_url_search_params_t *sp,
                             const lxb_char_t *name, size_t name_length,
                             const lxb_char_t *value, size_t value_length);

/* Get the first value for a name */
lexbor_str_t *
lxb_url_search_params_get(lxb_url_search_params_t *sp,
                          const lxb_char_t *name, size_t length);

/* Get the first entry for a name */
lxb_url_search_entry_t *
lxb_url_search_params_get_entry(lxb_url_search_params_t *sp,
                                const lxb_char_t *name, size_t length);

/* Get all values for a name into a buffer; returns number found */
size_t
lxb_url_search_params_get_all(lxb_url_search_params_t *sp,
                              const lxb_char_t *name, size_t length,
                              lexbor_str_t **out_buf, size_t out_size);

/* Count values for a name (useful for sizing the buffer before get_all) */
size_t
lxb_url_search_params_get_count(lxb_url_search_params_t *sp,
                                const lxb_char_t *name, size_t length);

/* Check if a name (and optionally value) exists */
bool
lxb_url_search_params_has(lxb_url_search_params_t *sp,
                          const lxb_char_t *name, size_t name_length,
                          const lxb_char_t *value, size_t value_length);

/* Set a name to a single value (removes all existing entries with that name) */
lxb_url_search_entry_t *
lxb_url_search_params_set(lxb_url_search_params_t *sp,
                          const lxb_char_t *name, size_t name_length,
                          const lxb_char_t *value, size_t value_length);

/* Sort entries alphabetically by name */
void
lxb_url_search_params_sort(lxb_url_search_params_t *sp);

/* Serialize to application/x-www-form-urlencoded format */
lxb_status_t
lxb_url_search_params_serialize(lxb_url_search_params_t *sp,
                                lexbor_callback_f cb, void *ctx);
```

### Iteration

```c
/* Find matching entry starting from a given position */
lxb_url_search_entry_t *
lxb_url_search_params_match_entry(lxb_url_search_params_t *sp,
                                  const lxb_char_t *name, size_t name_length,
                                  const lxb_char_t *value, size_t value_length,
                                  lxb_url_search_entry_t *entry);

/* Iterate all matching entries with a callback */
void
lxb_url_search_params_match(lxb_url_search_params_t *sp,
                            const lxb_char_t *name, size_t name_length,
                            const lxb_char_t *value, size_t value_length,
                            lxb_url_search_params_match_f cb, void *ctx);
```

The callback type is:

```c
typedef lexbor_action_t
(*lxb_url_search_params_match_f)(lxb_url_search_params_t *sp,
                                 lxb_url_search_entry_t *entry, void *ctx);
```

Return `LEXBOR_ACTION_OK` to continue iteration, `LEXBOR_ACTION_STOP` to stop.


## Examples

### Parsing and Accessing Components

```c
#include <lexbor/url/url.h>

int
main(void)
{
    lxb_status_t status;
    lxb_url_parser_t *parser;
    lxb_url_t *url;

    static const lxb_char_t url_str[] =
        "https://user:pass@example.com:8080/path/to/page?q=test#section";

    /* Create and initialize parser */
    parser = lxb_url_parser_create();
    status = lxb_url_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Parse URL */
    url = lxb_url_parse(parser, NULL, url_str, sizeof(url_str) - 1);
    if (url == NULL) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Access components */
    const lexbor_str_t *scheme = lxb_url_scheme(url);
    printf("Scheme: %.*s\n", (int) scheme->length, scheme->data);

    const lexbor_str_t *user = lxb_url_username(url);
    printf("Username: %.*s\n", (int) user->length, user->data);

    if (lxb_url_has_port(url)) {
        printf("Port: %u\n", lxb_url_port(url));
    }

    const lexbor_str_t *path = lxb_url_path_str(url);
    printf("Path: %.*s\n", (int) path->length, path->data);

    const lexbor_str_t *query = lxb_url_query(url);
    if (query->data != NULL) {
        printf("Query: %.*s\n", (int) query->length, query->data);
    }

    const lexbor_str_t *fragment = lxb_url_fragment(url);
    if (fragment->data != NULL) {
        printf("Fragment: %.*s\n", (int) fragment->length, fragment->data);
    }

    /* Cleanup: destroy all URLs and the parser */
    lxb_url_memory_destroy(url);
    lxb_url_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```

### Relative URL Resolution

```c
#include <lexbor/url/url.h>

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
    lxb_url_parser_t *parser;
    lxb_url_t *base, *relative;

    static const lxb_char_t base_str[] = "https://example.com/docs/guide/";
    static const lxb_char_t rel_str[] = "../api/reference.html?v=2";

    parser = lxb_url_parser_create();
    status = lxb_url_parser_init(parser, NULL);
    if (status != LXB_STATUS_OK) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Parse the base URL */
    base = lxb_url_parse(parser, NULL, base_str, sizeof(base_str) - 1);
    if (base == NULL) {
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    lxb_url_parser_clean(parser);

    /* Parse relative URL against the base */
    relative = lxb_url_parse(parser, base, rel_str, sizeof(rel_str) - 1);
    if (relative == NULL) {
        lxb_url_memory_destroy(base);
        lxb_url_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Serialize the resolved URL */
    printf("Resolved: ");
    lxb_url_serialize(relative, print_cb, NULL, false);
    printf("\n");
    /* Output: Resolved: https://example.com/api/reference.html?v=2 */

    lxb_url_memory_destroy(base);
    lxb_url_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}
```

### URLSearchParams

```c
#include <lexbor/url/url.h>
#include <lexbor/core/mraw.h>

int
main(void)
{
    lexbor_mraw_t *mraw;
    lxb_url_search_params_t *sp;

    /* Create a memory allocator */
    mraw = lexbor_mraw_create();
    if (lexbor_mraw_init(mraw, 256) != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Initialize from a query string */
    static const lxb_char_t params[] = "lang=en&page=1&sort=name";
    sp = lxb_url_search_params_init(mraw, params, sizeof(params) - 1);
    if (sp == NULL) {
        lexbor_mraw_destroy(mraw, true);
        return EXIT_FAILURE;
    }

    /* Get a value */
    lexbor_str_t *val = lxb_url_search_params_get(sp,
        (const lxb_char_t *) "page", 4);
    if (val != NULL) {
        printf("page = %.*s\n", (int) val->length, val->data);
    }

    /* Set a value (replaces existing) */
    lxb_url_search_params_set(sp,
        (const lxb_char_t *) "page", 4,
        (const lxb_char_t *) "2", 1);

    /* Append a new parameter */
    lxb_url_search_params_append(sp,
        (const lxb_char_t *) "filter", 6,
        (const lxb_char_t *) "active", 6);

    /* Check existence */
    bool has = lxb_url_search_params_has(sp,
        (const lxb_char_t *) "filter", 6, NULL, 0);
    printf("has 'filter': %s\n", has ? "true" : "false");

    /* Delete a parameter */
    lxb_url_search_params_delete(sp,
        (const lxb_char_t *) "sort", 4, NULL, 0);

    /* Sort alphabetically */
    lxb_url_search_params_sort(sp);

    /* Cleanup */
    lxb_url_search_params_destroy(sp);
    lexbor_mraw_destroy(mraw, true);

    return EXIT_SUCCESS;
}
```
