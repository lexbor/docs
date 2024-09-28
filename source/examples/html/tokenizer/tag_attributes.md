# Parsing HTML Tag Attributes

The example code found in `lexbor/html/tokenizer/tag_attributes.c` demonstrates how to use the `lexbor` library to tokenize an HTML string and retrieve the attributes of HTML tags. This will help to understand how to parse HTML data using the `lexbor` library and handle token attributes. Below, I will break down the important sections of the code and explain them in detail.

## Key Code Sections

### Token Callback Function

The `token_callback` function is registered as a callback to process tokens as they are parsed. Here's the function:

```c
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    const lxb_char_t *tag, *name;
    lxb_html_token_attr_t *attr;

    attr = token->attr_first;

    /* Skip all #text or without attributes tokens */
    if (token->tag_id == LXB_TAG__TEXT || attr == NULL) {
        return token;
    }

    tag = lxb_tag_name_by_id(token->tag_id, NULL);
    if (tag == NULL) {
        FAILED("Failed to get token name");
    }

    printf("\"%s\" attributes:\n", tag);

    while (attr != NULL) {
        name = lxb_html_token_attr_name(attr, NULL);

        if (name != NULL) {
            printf("    Name: %s; ", name);
        }
        else {
            /* This can only happen for the DOCTYPE token. */
            printf("    Name: <NOT SET>; \n");
        }

        if (attr->value != NULL) {
            printf("Value: %.*s\n", (int) attr->value_size, attr->value);
        }
        else {
            printf("Value: <NOT SET>\n");
        }

        attr = attr->next;
    }

    return token;
}
```

The function retrieves and prints the attributes of each token:
- **Checking Token Type and Attributes**: It first checks if the token is a text node (`LXB_TAG__TEXT`) or if it has no attributes (`attr == NULL`) and skips processing if so.
- **Getting Tag Name**: Uses `lxb_tag_name_by_id` to get the tag's name.
- **Iterating Attributes**: Loops through the token's attributes, printing their names and values.
- **Handling Null Values**: If an attribute name or value is not set, it handles this case gracefully.

### Main Function

The `main` function initializes the tokenizer, sets up the callback, and processes the HTML string.

```c
int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_html_tokenizer_t *tkz;

    const lxb_char_t data[] = "<div id=one-id class=silent ref='some &copy; a'>"
                              "<option-one enabled>"
                              "<option-two enabled='&#81'>"
                              "</div>";

    printf("HTML:\n%s\n\n", (char *) data);
    printf("Result:\n");

    tkz = lxb_html_tokenizer_create();
    status = lxb_html_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to create tokenizer object");
    }

    /* Set callback for token */
    lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);

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

    lxb_html_tokenizer_destroy(tkz);

    return 0;
}
```

### Setting Up the Tokenizer

```c
tkz = lxb_html_tokenizer_create();
status = lxb_html_tokenizer_init(tkz);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to create tokenizer object");
}
```

This section creates and initializes the tokenizer. Proper error handling ensures that the function exits if the tokenizer setup fails.

### Setting the Callback

```c
lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);
```

Here, the `token_callback` is set to be called whenever a token is fully parsed. This is central to processing each HTML token the tokenizer identifies.

### Processing the HTML

```c
status = lxb_html_tokenizer_chunk(tkz, data, (sizeof(data) - 1));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse the html data");
}

status = lxb_html_tokenizer_end(tkz);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to ending of parsing the html data");
}
```

These lines pass the HTML data to the tokenizer in chunks and signify the end of the data stream. Error checking ensures that any issues in those stages are caught.

### Destroying the Tokenizer

```c
lxb_html_tokenizer_destroy(tkz);
```

Finally, the tokenizer is destroyed to free resources.

## Notes

- **Error Handling**: The `FAILED` macro ensures that errors are caught and reported, and the application exits gracefully.
- **Callback Flexibility**: Using a callback function allows for custom processing of tokens.
- **Attribute Handling**: The tokenizer efficiently retrieves and iterates through token attributes.

## Summary

This example from the `lexbor` library showcases the process of tokenizing HTML and handling tag attributes. It highlights the efficient use of callback functions and robust error checking, demonstrating essential practices in HTML parsing. Understanding and using these techniques is fundamental for developers working with HTML parsing and manipulation using the `lexbor` library.