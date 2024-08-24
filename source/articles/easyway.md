# Lexbor HTML Parser Library Example Explanation

Let's start with the easy example of using `lexbor` for parsing and serializing
CSS selectors, breaking down the major steps and elements of the example,
explaining the overall purpose, requirements, and assumptions at each step.

## Overall Purpose:

The example demonstrates the usage of `lexbor` to parse a CSS selector string,
create a selector list, and then serialize the selector list. It also shows how
to handle parser logs and properly destroy allocated resources.

It serves as a guide for utilizing `lexbor` to parse and serialize CSS
selectors, with an emphasis on error handling and resource cleanup.

It's important to note straight away that this is a basic (or *naive*) approach;
a faster, real-life example will be provided further.

## Major Steps and Elements:

### 1. Library Inclusion and Callback Function:

The code includes the necessary header files and defines a callback function
(`callback`) that prints the parsed data.

```c
#include <lexbor/css/css.h>

lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

### 2. Main Function:

The `main` function initializes the CSS parser, parses a CSS selector string,
and then serializes the resulting selector list.

```c
int main(int argc, const char *argv[])
{
    // ... (variable declarations)

    // Create parser.
    parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);
    
    // Check if parser initialization was successful.
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    // Parse and get the log.
    // ...

    // Selector List Serialization.
    // ...

    // Destroy resources for Parser.
    // ...

    // Destroy all Selector List memory.
    // ...

    return EXIT_SUCCESS;
}
```

### 3. CSS Selector String and Parser Initialization:

The code defines a CSS selector string (`slctrs`) and initializes the CSS
parser.

```c
static const lxb_char_t slctrs[] = ":has(div, :not(as, 1%, .class), #hash)";

parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
```

### 4. Parsing CSS Selector and Handling Errors:

The code then parses the CSS selector string, checks for parsing errors, and
prints the result.

```c
list = lxb_css_selectors_parse(parser, slctrs,
                               sizeof(slctrs) / sizeof(lxb_char_t) - 1);

if (parser->status != LXB_STATUS_OK) {
    printf("Something went wrong\n");
    return EXIT_FAILURE;
}
```

### 5. Selector List Serialization and Handling Logs:

The example serializes the parsed selector list and prints any parser logs.

```c
printf("Result: ");
(void) lxb_css_selector_serialize_list(list, callback, NULL);
printf("\n");

// Check if there are any parser logs.
if (lxb_css_log_length(lxb_css_parser_log(parser)) != 0) {
    printf("Log:\n");
    // Serialize parser logs with proper indentation.
    (void) lxb_css_log_serialize(parser->log, callback, NULL,
                                 indent, indent_length);
    printf("\n");
}
```

### 6. Resource Cleanup:

Finally, the code destroys resources for the parser and frees memory allocated
for the selector list.

```c
(void) lxb_css_parser_destroy(parser, true);
lxb_css_selector_list_destroy_memory(list);
```

## Requirements and Assumptions:

Some things may have gone unnoticed:

- The CSS selector string (`slctrs`) is predefined and used for parsing.
- We assume the parser initialization and selector list creation are successful.
- Proper error handling is demonstrated by checking the parser's status,
  but can be improved.
- The cleanup section ensures proper destruction of parser resources and memory.
