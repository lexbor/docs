# CSS Selector Parsing Example

This article provides an in-depth explanation of the code found in
`list_easy_way.c`, which demonstrates how to use the `lexbor` library for parsing
CSS selectors. The code illustrates the steps involved in initializing a parser,
parsing a CSS selector string, and handling the results and logs.

## Code Overview

The example begins by including the necessary header file from the lexbor CSS
library. The main purpose of this code is to showcase the parsing of a CSS
selector string, specifically `:has(div, :not(as, 1%, .class), #hash)`, using
the lexbor's CSS parser.

## Key Sections of the Code

### Callback Function

The `callback` function is defined to handle output during the serialization
process of the CSS selector list. It takes three parameters: a character pointer
to the data, the length of that data, and a context pointer. Inside the
function, the data is printed to the standard output using `printf`, formatted
to respect the length provided.

```c
lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx) {
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

### Main Function

The `main` function begins by declaring variables for the parser and the
selector list. It initializes the necessary constants for indentation used in
log formatting and specifies the CSS selector string to be parsed.

#### Parser Initialization

A parser is created with `lxb_css_parser_create()`, and its initialization is
performed with `lxb_css_parser_init()`. The code checks the return status of the
initialization and exits gracefully if there is an issue, preventing further
execution with an invalid parser instance.

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

#### Parsing the Selector

The parsing of the CSS selector occurs with the function
`lxb_css_selectors_parse()`, which takes the parser, the selector string, and
its length as arguments. The status of the parser is checked afterward to ensure
that the parsing was successful.

```c
list = lxb_css_selectors_parse(parser, slctrs,
                               sizeof(slctrs) / sizeof(lxb_char_t) - 1);
if (parser->status != LXB_STATUS_OK) {
    printf("Something went wrong\n");
    return EXIT_FAILURE;
}
```

#### Selector List Serialization

The parsed selector list is then serialized using
`lxb_css_selector_serialize_list()`, which invokes the previously defined
`callback` function. This outputs the result of the serialization to standard
output.

```c
(void) lxb_css_selector_serialize_list(list, callback, NULL);
```

### Handling Logs

If there are any logs generated during parsing, they are checked with
`lxb_css_log_length()`, and the log is serialized in a similar manner, making
use of the callback function and proper indentation for the displayed log.

### Cleanup

Finally, the example demonstrates proper resource management by destroying the
parser and the associated memory. This is crucial in C programming to prevent
memory leaks. The parser is destroyed first, followed by the cleanup of the
selector list's memory.

```c
(void) lxb_css_parser_destroy(parser, true);
lxb_css_selector_list_destroy_memory(list);
```

## Conclusion

This example effectively showcases the functionality of the lexbor CSS library
for parsing CSS selectors. From initializing the parser to handling logs and
cleaning up memory, each step is crucial for ensuring that the program runs
efficiently and correctly. The structured approach presented in the code
promotes good practices in C programming, particularly regarding memory
management and error handling.