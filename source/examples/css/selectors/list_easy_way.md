# Parsing and Serializing CSS Selectors with lexbor

This article discusses a C code example from the `lexbor` library, specifically focusing on the file [lexbor/css/selectors/list_easy_way.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/css/selectors/list_easy_way.c). The example demonstrates how to parse CSS selectors and serialize them using the capabilities provided by `lexbor`.

In this example, we'll cover the process of creating a CSS parser using `lexbor`, parsing a complex selector string, and then serializing it back to a readable form. The workflow includes initialization of the parser, parsing the selector, error handling, and cleanup of resources.

## Key Code Sections

### Initialization of the CSS Parser

First, we need to create and initialize a CSS parser.

```c
lxb_css_parser_t *parser;
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

Here, `lxb_css_parser_create` allocates memory for the parser, while `lxb_css_parser_init` initializes the parser. If initialization fails (`status != LXB_STATUS_OK`), the program exits with `EXIT_FAILURE`.

### Parsing CSS Selectors

Next, we define our CSS selectors string and parse it.

```c
static const lxb_char_t slctrs[] = ":has(div, :not(as, 1%, .class), #hash)";
list = lxb_css_selectors_parse(parser, slctrs,
                               sizeof(slctrs) / sizeof(lxb_char_t) - 1);
if (parser->status != LXB_STATUS_OK) {
    printf("Something went wrong\n");
    return EXIT_FAILURE;
}
```

The function `lxb_css_selectors_parse` accepts the parser, the CSS selector string, and its length. It returns a pointer to `lxb_css_selector_list_t`, which represents the parsed selector list. Error handling confirms if the parsing was successful by checking `parser->status`.

### Callback Function for Serialization

We use a callback function to process the serialized data.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

The callback simply prints the serialized data to the standard output.

### Serializing the Selector List

We serialize the list of selectors to a readable form.

```c
printf("Result: ");
(void) lxb_css_selector_serialize_list(list, callback, NULL);
printf("\n");
```

The `lxb_css_selector_serialize_list` function processes each selector in the list, calling the `callback` for each. 

### Logging and Error Messages

If there are any log messages, we serialize and print them.

```c
if (lxb_css_log_length(lxb_css_parser_log(parser)) != 0) {
    static const lxb_char_t indent[] = "    ";
    static const size_t indent_length = sizeof(indent) / sizeof(lxb_char_t) - 1;
    
    printf("Log:\n");
    (void) lxb_css_log_serialize(parser->log, callback, NULL, indent, indent_length);
    printf("\n");
}
```

Here, `lxb_css_log_serialize` formats any log messages using the provided indentation and then calls the callback for each log entry.

### Cleanup Resources

Finally, we must clean up allocated resources.

```c
(void) lxb_css_parser_destroy(parser, true);
lxb_css_selector_list_destroy_memory(list);
```

`lxb_css_parser_destroy` and `lxb_css_selector_list_destroy_memory` ensure that all memory allocated for the parser and selector list is properly freed.

## Notes

- The example demonstrates robust error handling tied with each crucial step.
- Serialization is handled via callback functions, which offers flexibility for different output handling needs.
- Proper memory management is critical, underscored by the cleanup section.

## Summary

This example from `lexbor` showcases a complete cycle from parsing a complex CSS selector string to its serialization and error logging. For users looking to leverage the `lexbor` library, understanding this example is fundamental as it highlights key functionalities: parser creation, selector parsing, serialization, and resource management. By mastering these steps, developers can efficiently integrate CSS parsing capabilities into their applications.