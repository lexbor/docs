# Token Callback in HTML Tokenizer

This article explains an example in the [lexbor/html/tokenizer/callback.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/tokenizer/callback.c) file. This code demonstrates how to use the `lexbor` library to create an HTML tokenizer, set a callback function for processing tokens, and parse a chunk of HTML data. Each important part of the code will be analyzed to understand its intent and behavior.

## Key Code Sections

### Token Callback Definition

The `token_callback` function is defined to process each HTML token that the tokenizer produces.

```c
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    bool is_close;
    const lxb_char_t *name;

    name = lxb_tag_name_by_id(token->tag_id, NULL);
    if (name == NULL) {
        FAILED("Failed to get token name");
    }

    is_close = token->type & LXB_HTML_TOKEN_TYPE_CLOSE;

    printf("Tag name: %s; Tag id: %" PRIxPTR "; Is close: %s\n", name,
           token->tag_id, (is_close ? "true" : "false"));

    return token;
}
```

Here’s what this function does:
- It retrieves the tag name using `lxb_tag_name_by_id`.
- It checks if the token is a closing tag.
- It prints the tag name, tag ID, and whether it is a closing tag.

### Initializing and Configuring the Tokenizer

Next, the code initializes and configures the tokenizer object.

```c
tkz = lxb_html_tokenizer_create();
status = lxb_html_tokenizer_init(tkz);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to create tokenizer object");
}

/* Set callback for token */
lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);
```

- `lxb_html_tokenizer_create` allocates memory for the tokenizer.
- `lxb_html_tokenizer_init` initializes the tokenizer.
- `lxb_html_tokenizer_callback_token_done_set` sets the `token_callback` function to be called for each processed token.

### Starting and Feeding Data to the Tokenizer

The tokenizer is then prepared for parsing, and the HTML data is processed.

```c
status = lxb_html_tokenizer_begin(tkz);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to prepare tokenizer object for parsing");
}

status = lxb_html_tokenizer_chunk(tkz, data, (sizeof(data) - 1));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse the html data");
}

status = lxb_html_tokenizer_end(tkz);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to ending of parsing the html data");
}
```

- `lxb_html_tokenizer_begin` prepares the tokenizer to start processing.
- `lxb_html_tokenizer_chunk` processes the chunk of HTML data.
- `lxb_html_tokenizer_end` signifies the end of the data chunk for the tokenizer.

## Notes

- The `FAILED` macro is used for error handling, providing a concise and consistent way to handle errors.
- The `token_callback` function is crucial for customizing the processing of each token.
- `lxb_html_tokenizer_create`, `init`, `begin`, `chunk`, and `end` are key tokenizer functions that manage the lifecycle of the tokenizer.

## Summary

This example shows how to set up and use a tokenizer with the `lexbor` library. By defining a custom token callback, it demonstrates the flexible processing of HTML tokens. Understanding these steps and functions allows for creating more complex and tailored HTML processing workflows using `lexbor`. This example is instrumental for developers looking to implement custom HTML parsing solutions.