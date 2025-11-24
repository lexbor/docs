# CSS Tokenizer Printing

This article explains the source code example found in [lexbor/css/syntax/tokenizer/print_raw.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/css/syntax/tokenizer/print_raw.c). This example demonstrates how to utilize the `lexbor` library to parse a CSS file and print the raw tokens produced by the tokenizer. We'll delve into the key code sections to better understand the parsing process and token management with `lexbor`.

## Key Code Sections

### Usage Function

The `usage` function provides a simple command-line usage description. It's designed to inform the user about the proper way to run the program.

```c
static void
usage(void)
{
    fprintf(stderr, "print_raw <file>\n");
}
```

This function prints the correct command-line format to `stderr`. It's invoked when the user provides incorrect arguments.

### Colorize Callback

The `colorize_cb` function prints tokens to the standard output. It differentiates special cases, such as dimension tokens, and handles them appropriately.

```c
void
colorize_cb(lxb_css_syntax_token_t *token)
{
    int length;
    lxb_css_syntax_token_base_t *base;
    lxb_css_syntax_token_string_t *str;

    base = lxb_css_syntax_token_base(token);
    length = (int) base->length;

    printf("%.*s", length, base->begin);

    if (token->type == LXB_CSS_SYNTAX_TOKEN_DIMENSION) {
        str = lxb_css_syntax_token_dimension_string(token);

        /* Ident */
        length = (int) str->base.length;

        printf("%.*s", length, str->base.begin);
    }
}
```

This function extracts the base token details and prints them. If the token is of type `LXB_CSS_SYNTAX_TOKEN_DIMENSION`, it also prints the dimension string. 

### Main Function

The `main` function orchestrates the overall process of reading the file, initializing the tokenizer, and processing CSS tokens.

```c
int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_css_syntax_token_t *token;
    lxb_css_syntax_tokenizer_t *tkz;
    lxb_css_syntax_token_type_t type;
    lxb_char_t *css;
    size_t css_len;

    if (argc != 2) {
        usage();
        FAILED("Invalid number of arguments");
    }

    css = lexbor_fs_file_easy_read((const lxb_char_t *) argv[1], &css_len);
    if (css == NULL) {
        FAILED("Failed to read CSS file");
    }

    tkz = lxb_css_syntax_tokenizer_create();
    status = lxb_css_syntax_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        PRINT("Failed to create CSS:Syntax parser");
        goto failed;
    }
```

This block checks the command-line arguments and reads the content of the specified CSS file. If successful, it creates and initializes the CSS tokenizer.

```c
tkz->with_comment = true;
lxb_css_syntax_tokenizer_buffer_set(tkz, css, css_len);

do {
    token = lxb_css_syntax_token(tkz);
    if (token == NULL) {
        PRINT("Failed to parse CSS");
        goto failed;
    }

    colorize_cb(token);

    type = lxb_css_syntax_token_type(token);

    lxb_css_syntax_token_consume(tkz);
} while (type != LXB_CSS_SYNTAX_TOKEN__EOF);

lxb_css_syntax_tokenizer_destroy(tkz);
lexbor_free(css);

printf("\n");

return EXIT_SUCCESS;
```

The tokenizing loop handles each token produced by the tokenizer. Each token is processed by the `colorize_cb` function and then consumed. The loop continues until an EOF token is encountered.

### Clean-Up and Error Handling

If any step in the process fails, the resources are properly released, and an error code is returned.

```c
failed:

lxb_css_syntax_tokenizer_destroy(tkz);
lexbor_free(css);

return EXIT_FAILURE;
```

This block ensures that the tokenizer and memory allocated for the CSS content are freed even if an error occurs.

## Notes

1. **Token Consumption**: The `lxb_css_syntax_token_consume` function advances the tokenizer to the next token.
2. **Dimension Tokens**: The example specially handles `LXB_CSS_SYNTAX_TOKEN_DIMENSION`, indicating the handling of composite tokens.
3. **Error Handling**: Proper clean-up routines ensure that resources are freed in both success and failure cases.

## Summary

This example effectively demonstrates how to use `lexbor` to tokenize and print CSS tokens. It highlights crucial aspects such as correct tokenizer initialization, token handling, and the importance of resource management. Understanding this pattern is essential for developers dealing with CSS parsing or similar tasks using the `lexbor` library.