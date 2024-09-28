# URL Parsing Example

This article provides an explanation of the URL parsing example found in the
source file
[lexbor/url/relative.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/url/relative.c).
The example demonstrates the parsing of a relative URL based on a provided base
URL using the lexbor library. It outlines the setup of the URL parser, handling
of input strings, and the serialization of various components of the parsed URL.

## Code Breakdown

### Initial Setup

The program begins by including necessary headers and defining the callback
function. The callback function serves the purpose of printing parsed URL
components. The main function contains the core logic where URL parsing occurs.

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx);
```

### URL Initialization

In `main`, variables are defined for the base URL and the URL to parse. The
lexbor string structures are initialized with `url_str` and `base_url_str`. The
`lxb_url_parser_t parser` is initialized to set up the parser for processing the
URLs.

```c
lxb_url_parser_t parser;
status = lxb_url_parser_init(&parser, NULL);
```

This initializes the parser and checks for successful initialization. If it
fails, the program outputs an error message and exits.

### Parsing Base URL

The `base_url` is then parsed using `lxb_url_parse`, which takes the initialized
parser, a null pointer (for context), the data of the base URL string, and its
length.

```c
base_url = lxb_url_parse(&parser, NULL, base_url_str.data, base_url_str.length);
```

If parsing the base URL fails, an error message is printed.

### Cleaning Up and Parsing Relative URL

Subsequently, the parser is cleaned up, and the relative URL is parsed in a
similar manner using the base URL as a reference.

```c
lxb_url_parser_clean(&parser);
url = lxb_url_parse(&parser, base_url, url_str.data, url_str.length);
```

Again, if the parsing fails, an appropriate error message is printed. After the
relative URL is successfully parsed, the parser must be cleaned up using
`lxb_url_parser_destroy`.

### Serializing URL Components

The main focus of this example is the serialization of various components of the
parsed URL. Using callbacks, the program outputs the base URL, relative URL, and
several segments of the parsed URL:

- Scheme
- Username
- Password
- Host (both ASCII and Unicode)
- Port
- Path
- Query
- Fragment

Each of these components is printed by invoking serialization functions, such as
`lxb_url_serialize_scheme` for the scheme, and so forth.

```c
(void) lxb_url_serialize(url, callback, NULL, false);
```

The callback function defined earlier is utilized here to display each component
by printing its representation.

### Final Cleanup

After displaying all URL components, the program cleans up the IDNA context and
the memory associated with the parsed URL. This ensures that any resources
utilized during the parsing are properly released.

```c
(void) lxb_unicode_idna_destroy(&idna, false);
(void) lxb_url_memory_destroy(url);
```

### Conclusion

The provided example illustrates the process of relative URL parsing using the
lexbor library. From initializing the parser to serializing specific components
of the URL, each step is crucial for accurate URL handling in applications. The
careful management of memory and resources also highlights best practices in
programming with C.