# Parsing and Serializing a URL: Example

This article will delve into a code example from the `lexbor` library, specifically found in `lexbor/url/parse.c`. The example demonstrates parsing a URL and serializing its components using the `lexbor` URL parser. The context is to take an input URL, parse it into its components, and then serialize and display these components.

## Key Code Sections

### Initialization

The first important part of the code initializes several structures:

```c
lxb_url_t *url;
lxb_status_t status;
lxb_url_parser_t parser;
lxb_unicode_idna_t idna;

static const lexbor_str_t url_str = lexbor_str("https://panda:pass@тест.com:2030/path/to/hell?id=54321#comments");
```

Here, we declare pointers and status variables needed for URL manipulation. The `url_str` is a constant string that contains the URL to be parsed.

### URL Parser Initialization

Next, the code initializes the URL parser:

```c
status = lxb_url_parser_init(&parser, NULL);
if (status != LXB_STATUS_OK) {
    printf("Failed to init URL parser.\n");
    return EXIT_FAILURE;
}

url = lxb_url_parse(&parser, NULL, url_str.data, url_str.length);
if (url == NULL) {
    printf("Failed to parse URL.\n");
    return EXIT_FAILURE;
}
```

- `lxb_url_parser_init` initializes the URL parser structure. This setup ensures that the parser is ready to operate.
- `lxb_url_parse` parses the input URL string into a structured format. The function returns a pointer to an `lxb_url_t` structure if successful.

### Cleanup After Parsing

After parsing, the parser structure is destroyed:
  
```c
lxb_url_parser_destroy(&parser, false);
```

This line frees any resources allocated for the parser, preventing memory leaks.

### Serializing URL Components

To output the parsed URL components, several serialization functions are used. Each function serializes a specific part of the URL:

```c
printf("Source URL: %s\n", (const char *) url_str.data);

printf("Parsed URL: ");
(void) lxb_url_serialize(url, callback, NULL, false);
printf("\n");

printf("Scheme: ");
(void) lxb_url_serialize_scheme(url, callback, NULL);
printf("\n");
```

- `lxb_url_serialize` serializes the entire URL.
- `lxb_url_serialize_scheme` serializes only the scheme (e.g., "https").

The code continues similarly for other components: username, password, host, port, path, query, and fragment, each time calling the appropriate serialization function.

### Unicode Handling for Host

Special handling is required for the host part of the URL if it contains Unicode characters:

```c
status = lxb_unicode_idna_init(&idna);
if (status != LXB_STATUS_OK) {
    printf("Failed to init IDNA.\n");
    return EXIT_FAILURE;
}

printf("Host (Unicode): ");
(void) lxb_url_serialize_host_unicode(&idna, lxb_url_host(url), callback, NULL);
printf("\n");
```

- `lxb_unicode_idna_init` initializes a structure to handle Internationalized Domain Names (IDN).
- `lxb_url_serialize_host_unicode` serializes the host in Unicode form after conversion using IDNA.

### Callback Function

The example uses a callback function to handle data chunks during serialization:

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}
```

The callback function outputs the serialized data chunk by chunk. This approach allows handling large strings or specific formatting as needed.

### Resource Cleanup

Finally, the code ensures all resources are properly freed:

```c
(void) lxb_unicode_idna_destroy(&idna, false);
(void) lxb_url_memory_destroy(url);
```

- `lxb_unicode_idna_destroy` and `lxb_url_memory_destroy` free resources allocated for IDNA handling and URL parsing, respectively.

## Notes

- Always ensure resources are freed to prevent memory leaks.
- Proper initialization and error checking are crucial for stable and robust parsing.
- Callbacks are useful for handling serialized data flexibly.

## Summary

This example from `lexbor` demonstrates the initialization, parsing, serialization, and cleanup processes for URL handling. It highlights the library's capabilities in managing URLs, including those with Unicode components. Understanding this process is essential for developers working with URLs in various applications.