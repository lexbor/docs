# URL Parsing Example

This article examines a code example from the
[lexbor/url/parse.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/url/parse.c)
file, focusing on URL parsing using the `lexbor` library. The intent of this code
is to demonstrate how to initialize the URL parser, parse a URL string, and
subsequently serialize different components of the parsed URL, such as the
scheme, username, password, host, and more. Each section of the code plays a
critical role in handling URL data.

## Code Breakdown

### Initialization

The code begins by including the necessary header for the `lexbor` URL library and
defining a static callback function. In the `main` function, several variables
are declared, including a pointer to `lxb_url_t`, an instance of
`lxb_url_parser_t`, and `lxb_unicode_idna_t`. 

```c
lxb_url_parser_t parser;
lxb_unicode_idna_t idna;
```

Here, `parser` is used to handle the URL parsing logic, while `idna` is utilized
for Internationalized Domain Name (IDN) handling.

### Parsing the URL

A static constant `url_str` initializes with a URL string containing various
components, including a scheme (`https`), credentials (`panda:pass`), a domain
name with Unicode characters, a port number (`2030`), a path, a query parameter,
and a fragment. 

```c
static const lexbor_str_t url_str = lexbor_str("https://panda:pass@тест.com:2030/path/to/hell?id=54321#comments");
```

Next, the parser is initialized using the `lxb_url_parser_init` function. It is
crucial to check the returned status to ensure that the parser was initialized
successfully.

```c
status = lxb_url_parser_init(&parser, NULL);
if (status != LXB_STATUS_OK) {
    printf("Failed to init URL parser.\n");
    return EXIT_FAILURE;
}
```

If the parser fails to initialize, an error message is printed, and the program
exits.

### Executing the Parse

The URL is parsed through `lxb_url_parse`, which processes the URL string into
its various components. Again, it is crucial to validate that the parsing was
successful by checking if `url` is `NULL`.

```c
url = lxb_url_parse(&parser, NULL, url_str.data, url_str.length);
if (url == NULL) {
    printf("Failed to parse URL.\n");
    return EXIT_FAILURE;
}
```

### Serializing URL Components

After successful parsing, the next step involves destroying the parser to clean
up resources. The code then initializes the IDNA handler, which is necessary for
the following serialization of Unicode hostnames.

```c
status = lxb_unicode_idna_init(&idna);
if (status != LXB_STATUS_OK) {
    printf("Failed to init IDNA.\n");
    return EXIT_FAILURE;
}
```

The program outputs the original URL string and proceeds to serialize various
parts of the URL. Each serialization function is linked to the previously
defined `callback`, which handles the output for each component.

- **Serialized URL**: Outputs the entire URL.
- **Scheme**: Extracts and displays only the scheme portion.
- **Username and Password**: Collects and shows the relevant sections.
- **Host**: Contains both ASCII and Unicode serialization capabilities.
- **Port, Path, Query, and Fragment**: Serializes these components in turn,
  showcasing all aspects of the URL.

```c
(void) lxb_url_serialize(url, callback, NULL, false);
```

Each of these print statements utilizes the callback function to handle the
printing of serialized data.

### Cleanup

Finally, the program cleans up by destroying the IDNA handler and the allocated
URL memory, ensuring that no resources are leaked.

```c
(void) lxb_unicode_idna_destroy(&idna, false);
(void) lxb_url_memory_destroy(url);
```

### Conclusion

The example succinctly demonstrates the capabilities of the `lexbor` URL parsing
library, showcasing how to initialize the parser, handle a complex URL with
Unicode characters, and serialize its components. Each part of the code works
harmoniously to show how flexible and powerful URL handling can be in modern C
programming with the `lexbor` library. The proper initialization, error handling,
and cleanup are crucial for robust application development.