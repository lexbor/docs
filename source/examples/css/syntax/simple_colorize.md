# CSS Lexer with Colorized Output: Example

This example demonstrates how to use the `lexbor` library to parse a CSS file and provide colorized output based on the different types of CSS tokens encountered. The code is found in the `lexbor/css/syntax/simple_colorize.c` file. The primary objective of this example is to showcase how to set up a CSS parser, process different CSS rules, and colorize the output dynamically to reflect the structure of CSS syntax.

## Key Code Sections

### Parsing Initialization

First, let's look at the initialization process for the CSS parser, file reading, and the initial call to the parsing function:

```c
if (argc != 2) {
    fprintf(stderr, "Usage:\n");
    fprintf(stderr, "\tcolorize <file>\n");
    FAILED("Invalid number of arguments");
}

fl = (const lxb_char_t *) argv[1];

css = lexbor_fs_file_easy_read(fl, &css_len);
if (css == NULL) {
    FAILED("Failed to read CSS file");
}

parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to create CSS Parser");
}

status = css_parse(parser, css, css_len);
```

This part checks for a single command-line argument, reads the CSS file, initializes the `lexbor` CSS parser, and starts the parsing process using `css_parse`.

### `css_parse` Function

The main parsing logic is within the `css_parse` function:

```c
static lxb_status_t
css_parse(lxb_css_parser_t *parser, const lxb_char_t *data, size_t length)
{
    css_ctx_t ctx;
    lxb_css_syntax_rule_t *stack;

    ctx.data = data;
    ctx.offset = 0;

    lxb_css_parser_buffer_set(parser, data, length);

    stack = lxb_css_syntax_parser_list_rules_push(parser, NULL, NULL,
                                                  &css_list_rules,
                                                  &ctx, true,
                                                  LXB_CSS_SYNTAX_TOKEN_UNDEF);
    if (stack == NULL) {
        return LXB_STATUS_ERROR;
    }

    printf("\n");

    return lxb_css_syntax_parser_run(parser);
}
```

This function sets up the parser buffer and pushes the initial parsing rules onto the stack using `lxb_css_syntax_parser_list_rules_push`. It then runs the parser by calling `lxb_css_syntax_parser_run`.

### Callback Structures

The following structures define callbacks for handling different CSS syntactic elements:

```c
static const lxb_css_syntax_cb_at_rule_t css_at_rule = {
    .state = css_at_rule_state,
    .block = css_at_rule_block,
    .failed = lxb_css_state_failed,
    .end = css_at_rule_end
};

static const lxb_css_syntax_cb_qualified_rule_t css_qualified_rule = {
    .state = css_qualified_rule_state,
    .block = css_qualified_rule_block,
    .failed = lxb_css_state_failed,
    .end = css_qualified_rule_end
};

static const lxb_css_syntax_cb_list_rules_t css_list_rules = {
    .cb.state = css_list_rules_state,
    .cb.failed = lxb_css_state_failed,
    .cb.end = css_list_rules_end,
    .next = css_list_rules_next,
    .at_rule = &css_at_rule,
    .qualified_rule = &css_qualified_rule
};
```

These structures define callbacks for handling different rules such as at-rules, qualified rules, and lists of rules. They point to specific functions that handle each part of the CSS token processing.

### Handling Rules with Color

Let's examine how specific rules are handled and colorized, starting with the at-rule state:

```c
static bool
css_at_rule_state(lxb_css_parser_t *parser,
                  const lxb_css_syntax_token_t *token, void *ctx)
{
    css_print_token_offset(token, ctx);

    printf("\033[35m");
    css_print_token(token, ctx);

    lxb_css_syntax_parser_consume(parser);
    token = lxb_css_syntax_parser_token(parser);

    printf("\033[33m");

    css_consule_tokens(parser, token, ctx);

    printf("\033[39m");

    return lxb_css_parser_success(parser);
}
```

Here, the at-rule state function sets the color (using ANSI escape codes) and prints the token while consuming and processing subsequent tokens within an at-rule block.

### Token Serialization

The function `css_consule_tokens` is used to serialize and print tokens:

```c
lxb_inline void
css_consule_tokens(lxb_css_parser_t *parser,
                   const lxb_css_syntax_token_t *token, void *ctx)
{
    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__END) {
        (void) lxb_css_syntax_token_serialize(token, token_cb_f, ctx);

        lxb_css_syntax_parser_consume(parser);
        token = lxb_css_syntax_parser_token(parser);
    }
}
```

It continuously consumes and prints each token until the end of the input or a terminating token is reached.

### Coloring Declaration Names and Values

The following functions handle the coloring of CSS property names and values:

```c
static bool
css_declarations_name(lxb_css_parser_t *parser,
                      const lxb_css_syntax_token_t *token, void *ctx)
{
    css_print_token_offset(token, ctx);

    printf("\033[31m");

    css_consule_tokens(parser, token, ctx);

    printf("\033[39m");

    return lxb_css_parser_success(parser);
}

static bool
css_declarations_value(lxb_css_parser_t *parser,
                       const lxb_css_syntax_token_t *token, void *ctx)
{
    css_print_token_offset(token, ctx);

    printf("\033[36m");

    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__END) {
        (void) lxb_css_syntax_token_serialize(token, token_cb_f, ctx);

        lxb_css_syntax_parser_consume(parser);
        token = lxb_css_syntax_parser_token(parser);
    }

    printf("\033[39m");

    return lxb_css_parser_success(parser);
}
```

These functions respectively color CSS property names in red and their values in cyan.

## Notes

- **Color Codes**: The example uses ANSI escape codes (e.g., `\033[31m`) to color the output, which may not be supported on all terminals.
- **Memory Management**: It is critical to properly destroy and free the parser and allocated memory to prevent leaks.
- **Error Handling**: The example includes fundamental error handling mechanisms but may require enhancements for robustness in production systems.

## Summary

This example illustrates how to use the `lexbor` library effectively for parsing and colorizing CSS. The key takeaways include setting up the parser, defining callback structures to handle different CSS rules, and utilizing token serialization and ANSI escape codes for colored output. Understanding these principles helps leverage the `lexbor` library for more complex CSS parsing and processing tasks.