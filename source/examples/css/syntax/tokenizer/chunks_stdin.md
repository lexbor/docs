# Tokenizing CSS from Standard Input

The file `lexbor/css/syntax/tokenizer/chunks_stdin.c` demonstrates how to tokenize CSS data read from standard input using the `lexbor` library. This article will delve into the key parts of this example, explaining the purpose and workings of each section.

## Key Code Sections

### Callback for Token Serialization

The function `callback` is used to handle the serialized tokens. It simply prints the token data to the standard output.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%s", (const char *) data);

    return LXB_STATUS_OK;
}
```

This demonstrates a basic usage of `lxb_css_syntax_token_serialize`, indicating how tokens will be rendered and processed.

### Handling Input in Chunks

The function `chunk_cb` reads data from standard input into a buffer, allowing the tokenizer to process it in chunks. This is particularly useful for handling large inputs gracefully.

```c
lxb_status_t
chunk_cb(lxb_css_syntax_tokenizer_t *tkz, const lxb_char_t **data,
         const lxb_char_t **end, void *ctx)
{
    size_t size;
    lxb_char_t *buff = ctx;

    size = fread((char *) buff, 1, BUFFER_SIZE, stdin);
    if (size != BUFFER_SIZE) {
        if (feof(stdin)) {
            tkz->eof = true;
        }
        else {
            return EXIT_FAILURE;
        }
    }

    *data = buff;
    *end = buff + size;

    return LXB_STATUS_OK;
}
```

This function fills a buffer with a fixed size (`BUFFER_SIZE`) from `stdin`, managing the end-of-file condition by setting `tkz->eof` when necessary. This function returns `LXB_STATUS_OK` if reading proceeds without errors.

### Tokenizing the Input

The `main` function initializes the CSS tokenizer, sets the chunk callback, and processes tokens in a loop until the end-of-file token is encountered. 

```c
int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_css_syntax_token_t *token;
    lxb_css_syntax_tokenizer_t *tkz;
    lxb_css_syntax_token_type_t type;
    const lxb_char_t *name;
    char inbuf[BUFFER_SIZE];

    tkz = lxb_css_syntax_tokenizer_create();
    status = lxb_css_syntax_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        PRINT("Failed to create CSS:Syntax parser");
        goto failed;
    }

    lxb_css_syntax_tokenizer_chunk_cb_set(tkz, chunk_cb, inbuf);

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

    lxb_css_syntax_tokenizer_destroy(tkz);

    return EXIT_SUCCESS;

failed:

    lxb_css_syntax_tokenizer_destroy(tkz);

    return EXIT_FAILURE;
}
```

Here, the tokenizer is created and initialized, and the chunk callback is set with a buffer for data. The loop continues to fetch tokens, prints their names and serialized content, and consumes each token until the end-of-file token is reached.

## Notes

- **Buffer Size**: The buffer size (`BUFFER_SIZE`) is set to 32 to demonstrate handling small chunks of data. This size can be adjusted based on specific needs.
- **Error Handling**: The example includes basic error handling, with appropriate messages and clean-up.
- **EOF Management**: The end-of-file is managed using `tkz->eof`, ensuring the tokenizer knows when no more data is available.

## Summary

This example illustrates how to tokenize CSS data read from standard input, demonstrating key aspects of using the `lexbor` library. It covers initialization, setting up a chunk callback function, handling tokens, and managing end-of-file conditions. Understanding these steps is crucial for effectively working with `lexbor` to tokenize CSS or other similar structured data inputs.