# Understanding Fast CSS Selector Parsing with `lexbor`: Example

This article provides a detailed explanation of the `lexbor/css/selectors/list_fast_way.c`
example from the `lexbor` library, focusing on its intermediate-to-advanced
aspects. The example demonstrates how to efficiently parse and process CSS selectors
using `lexbor`. We will look into the key sections, including initialization,
parsing, and serialization of selectors, highlighting the intent and logic behind
these implementations.

## Key Code Sections

### Initialization of Memory and Parser

The example starts with the initialization of memory and parser objects. Here are the
relevant portions of the code:

```c
lxb_css_memory_t *memory;
lxb_css_parser_t *parser;

/* Memory for all parsed structures. */
memory = lxb_css_memory_create();
status = lxb_css_memory_init(memory, 128);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}

/* Create parser. */
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

The `lxb_css_memory_create` and `lxb_css_memory_init` functions are used to create and
initialize a memory pool that will be used for storing parsed structures. The parser is
created with `lxb_css_parser_create` and initialized with `lxb_css_parser_init`. These
steps ensure that memory management is handled efficiently.

### Memory Binding to Parser

One crucial aspect is binding the memory pool to the parser, preventing redundant memory
allocations. The following lines achieve this:

```c
/* Bind memory to parser */
lxb_css_parser_memory_set(parser, memory);
```

By binding the memory object to the parser using `lxb_css_parser_memory_set`, the example
ensures that all parsed structures share the same memory pool, promoting efficiency and
preventing memory fragmentation.

### Creating and Binding Selectors

Selectors are created and bound to the parser, ensuring streamlined parsing operations:

```c
lxb_css_selectors_t *selectors;
selectors = lxb_css_selectors_create();
status = lxb_css_selectors_init(selectors);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
lxb_css_parser_selectors_set(parser, selectors);
```

The selectors object is created and initialized through `lxb_css_selectors_create` and
`lxb_css_selectors_init`. Binding the selectors to the parser with 
`lxb_css_parser_selectors_set` prevents the creation of new selectors objects on each
parsing operation.

### Parsing Selectors

The central part of the example involves parsing the CSS selectors provided in an array:

```c
const char *slctrs[] = { ":not()", "div #hash [refs=i]", "div.class", ... };

for (i = 0; slctrs[i] != NULL; i++) {
    lists[i] = lxb_css_selectors_parse(parser, (const lxb_char_t *) slctrs[i],
                                       strlen(slctrs[i]));
    if (parser->status != LXB_STATUS_OK) {
        /* Handle parse error */
    } else {
        /* Handle parse success */
    }
}
```

The array `slctrs` contains various CSS selectors to parse. The `lxb_css_selectors_parse`
function is called for each selector, and its result is stored in the `lists` array. The
parser's status is checked to determine if the parsing was successful.

### Log Serialization

In case of errors or warnings during parsing, the logs are serialized and printed:

```c
(void) lxb_css_log_serialize(parser->log, callback, NULL, indent, indent_length);
```

The `lxb_css_log_serialize` function serializes the log information, using a `callback`
to output the serialized data. This helps in diagnosing issues during the parsing process.

### Cleanup Resources

Once parsing is complete, the resources associated with the parser and selectors are
destroyed:

```c
(void) lxb_css_selectors_destroy(selectors, true);
(void) lxb_css_parser_destroy(parser, true);
```

Destroying these resources ensures that any allocated memory is properly freed, preventing
memory leaks.

### Outputting Results

The parsed selector lists are then serialized and outputted:

```c
for (i = 0; slctrs[i] != NULL; i++) {
    if (lists[i] != NULL) {
        (void) lxb_css_selector_serialize_list(lists[i], callback, NULL);
    }
}
```

Each parsed selector list is serialized using `lxb_css_selector_serialize_list`, and the
results are printed. This demonstrates the outcomes of the parsing operations.

## Notes

- Binding memory and selectors to the parser improves efficiency and prevents
  redundant memory allocations.
- Proper error handling and log serialization provide insights into parsing issues.
- Resource cleanup is essential to prevent memory leaks.

## Summary

This example illustrates efficient parsing of CSS selectors using the `lexbor` library by
binding memory and selectors to the parser, parsing various selectors, handling errors,
and serializing the results. Understanding these techniques is valuable for developers
looking to leverage `lexbor` for high-performance CSS parsing in their applications.