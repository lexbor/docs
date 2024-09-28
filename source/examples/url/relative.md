# URL Parsing and Serialization: Example

This example comes from the `lexbor/url/relative.c` file and demonstrates how
to parse and serialize URLs using the `lexbor` library. The following
explanation will dive into crucial parts of the code, illustrate its core
functions, and provide detailed reasoning about the various `lexbor` elements 
used.

The example illustrates parsing a relative URL against a base URL, initializing
necessary parsers, and then serializing different components of the URL,
showcasing the ability of `lexbor` to handle URL manipulation and IDNA
(internationalized domain name) conversion.

## Key Code Sections

### URL Parser Initialization
The first key part involves initializing the URL parser.

```c
    status = lxb_url_parser_init(&parser, NULL);
    if (status != LXB_STATUS_OK) {
        printf("Failed to init URL parser.\n");
        return EXIT_FAILURE;
    }
```
In this section, `lxb_url_parser_init` initializes the `parser` object.
Initialization is essential as it sets up the internal state for subsequent URL
parsing.

### Parsing the Base URL
Once the parser is initialized, the next task is to parse the base URL.

```c
    base_url = lxb_url_parse(&parser, NULL, base_url_str.data,
                             base_url_str.length);
    if (base_url == NULL) {
        printf("Failed to parse Base URL.\n");
        return EXIT_FAILURE;
    }
    lxb_url_parser_clean(&parser);
```
Here, `lxb_url_parse` is called with the `parser` object, parsing the provided
`base_url_str`. If successful, it returns a pointer to a `lxb_url_t` structure
representing the parsed URL. The parser is then cleaned to reset its state.

### Parsing the Relative URL
Next, the relative URL is parsed using the previously parsed base URL as the
reference.

```c
    url = lxb_url_parse(&parser, base_url, url_str.data, url_str.length);
    if (url == NULL) {
        printf("Failed to parse URL.\n");
        return EXIT_FAILURE;
    }

    lxb_url_parser_destroy(&parser, false);
```
Again, `lxb_url_parse` is used, this time passing the `base_url` to provide context 
for the relative URL. The resulting URL structure is stored in `url`.

### Initializing IDNA
To serialize Unicode hostnames, IDNA initialization is necessary.

```c
    status = lxb_unicode_idna_init(&idna);
    if (status != LXB_STATUS_OK) {
        printf("Failed to init IDNA.\n");
        return EXIT_FAILURE;
    }
```
`lxb_unicode_idna_init` prepares the `idna` structure for handling
internationalized domain names, facilitating transformation between Unicode and
ASCII representations.

### Serializing URL Components
Finally, different parts of the parsed URL are serialized and printed out.

```c
    printf("Parsed URL: ");
    (void) lxb_url_serialize(url, callback, NULL, false);
    printf("\n");

    printf("Scheme: ");
    (void) lxb_url_serialize_scheme(url, callback, NULL);
    printf("\n");

    printf("Username: ");
    (void) lxb_url_serialize_username(url, callback, NULL);
    printf("\n");
```
Each `lxb_url_serialize_*` function takes the parsed URL and the `callback`
function to print each part of the URL string. For the host, both ASCII and
Unicode formats are printed:

```c
    printf("Host (ASCII): ");
    (void) lxb_url_serialize_host(lxb_url_host(url), callback, NULL);
    printf("\n");

    printf("Host (Unicode): ");
    (void) lxb_url_serialize_host_unicode(&idna, lxb_url_host(url),
                                          callback, NULL);
    printf("\n");
```
Using `lxb_url_serialize_host_unicode` alongside `idna` converts and prints the
Unicode hostname.

### Callback Function
The `callback` function is a utility to print the individual URL components:

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}
```
This `callback` is vital for the standard `lexbor` serialization pattern,
outputting each URL component.

## Notes
- Initialization and cleanup functions (`init`, `clean`, `destroy`) are crucial
  to managing `lexbor` objects.
- Parsing relative URLs against base URLs showcases `lexbor`'s robustness.
- IDNA transformation emphasizes handling internationalized domain names.

## Summary
The example from `lexbor/url/relative.c` demonstrates parsing relative URLs
using a base URL, initializing necessary `lexbor` objects, and serializing the
URL components. This process highlights `lexbor`'s capabilities in handling
URL parsing and internationalization, which is crucial for applications dealing
with diverse web addresses. Understanding these routines is essential for
anyone looking to manipulate URLs effectively using `lexbor`.