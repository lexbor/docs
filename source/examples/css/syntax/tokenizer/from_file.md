# Parsing a CSS File with `lexbor`: Example

This article focuses on the source file `lexbor/css/syntax/tokenizer/from_file.c` and explains how to parse a CSS file using the `lexbor` library. This explanation delves into the specific functions and methods employed to tokenize and handle CSS content, illustrating a practical approach to CSS parsing with `lexbor`.

The example code demonstrates how to read a CSS file, tokenize its content using `lexbor`'s CSS syntax tokenizer, and print each recognized token. Understanding this example provides insight into the fundamental use of `lexbor` for processing CSS files, which is critical for many web development and parsing applications that require robust CSS manipulation.

## Key Code Sections

### Reading the CSS File

The initial step in the code involves reading a CSS file. This is accomplished using `lexbor`'s file reading utility:

```c
css = lexbor_fs_file_easy_read((const lxb_char_t *) argv[1], &css_len);
if (css == NULL) {
    FAILED("Failed to read CSS file");
}
```

Here, `lexbor_fs_file_easy_read` takes the file path provided via command line arguments and reads its content into a dynamically allocated buffer. The length of the CSS content is stored in `css_len`. If the file reading fails, the program exits with an error.

### Initializing the Tokenizer

Once the CSS content is loaded, the next step is to initialize the tokenizer:

```c
tkz = lxb_css_syntax_tokenizer_create();
status = lxb_css_syntax_tokenizer_init(tkz);
if (status != LXB_STATUS_OK) {
    PRINT("Failed to create CSS:Syntax parser");
    goto failed;
}
```

The tokenizer is created with `lxb_css_syntax_tokenizer_create` and initialized with `lxb_css_syntax_tokenizer_init`. If the initialization fails, the code jumps to the `failed` label to clean up resources and exit.

### Setting the Buffer and Tokenizing

After initializing the tokenizer, the CSS content is set as the buffer for the tokenizer:

```c
lxb_css_syntax_tokenizer_buffer_set(tkz, css, css_len);
```

This function sets the internal buffer of the tokenizer to the CSS data, preparing it for tokenization.

### Processing Tokens

The core of the tokenization process involves a loop that retrieves and processes each token:

```c
do {
    token = lxb_css_syntax_token(tkz);
    if (token == NULL) {
        PRINT("Failed to parse CSS");
        goto failed;
    }

    name = lxb_css_syntax_token_type_name_by_id(token->type);
    printf("%s: ", (const char *) name);

    lxb_css_syntax_token_serialize(token, callback, NULL);
    printf("\n");

    type = lxb_css_syntax_token_type(token);

    lxb_css_syntax_token_consume(tkz);
}
while (type != LXB_CSS_SYNTAX_TOKEN__EOF);
```

In this loop:
- `lxb_css_syntax_token` retrieves the next token from the tokenizer.
- `lxb_css_syntax_token_type_name_by_id` gets the token's type name.
- `lxb_css_syntax_token_serialize` outputs the token's content using a callback function.
- `lxb_css_syntax_token_consume` advances the tokenizer to the next token.

The loop continues until the end-of-file (EOF) token is encountered.

### Cleaning Up

Finally, once all tokens are processed, resources are cleaned up:

```c
lxb_css_syntax_tokenizer_destroy(tkz);
lexbor_free(css);
```

This ensures that allocated memory is properly freed.

## Notes

- `lexbor_fs_file_easy_read` simplifies file reading but requires proper error handling.
- Proper initialization and cleanup of the tokenizer are crucial to avoid memory leaks.
- The tokenization loop processes each token and prints its type and content.

## Summary

This example illustrates how to use `lexbor` to read and tokenize CSS files. It covers essential functions for file reading, tokenizer initialization, and token processing. Understanding these steps is fundamental for developers looking to integrate CSS parsing capabilities into their applications using `lexbor`.