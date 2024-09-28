# Tokenizing Text Nodes in HTML: Example

In this example, found in `lexbor/html/tokenizer/text.c`, we explore how to 
use the `lexbor` library to tokenize HTML content and selectively process 
text nodes (`#text` nodes). The example shows how to set up a tokenizer, 
manage the parsing process, and handle tokens using callback functions 
provided by `lexbor`.

## Key Code Sections

### Defining the Error Handling Macro

Before diving into the core functionality, the example defines an error 
handling macro, `FAILED`. This macro ensures that any critical error 
terminates the program with an appropriate error message.

```c
#define FAILED(...)                                                            \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

### The Token Callback Function

The `token_callback` function processes tokens produced by the tokenizer. 
Its purpose is to skip all tokens that are not text nodes and print 
the content of the text nodes.

```c
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    /* Skip all not #text tokens */
    if (token->tag_id != LXB_TAG__TEXT) {
        return token;
    }

    printf("%.*s", (int) (token->text_end - token->text_start),
           token->text_start);

    return token;
}
```

Here, we check the `tag_id` of the token. If it is not `LXB_TAG__TEXT`, the 
function returns the token unchanged. Otherwise, it calculates the token's 
text length and prints it.

### Main Function and Initialization

The `main` function sets up the tokenizer, registers the callback function, 
and processes a chunk of HTML data.

```c
int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_html_tokenizer_t *tkz;

    const lxb_char_t data[] = "<div>Hi<span> my </span>friend</div>! "
                              "&#x54;&#x72;&#x79;&#x20;&#x65;&#x6e;&#x74;"
                              "&#x69;&#x74;&#x69;&#x65;&#x73;&excl;";

    printf("HTML:\n%s\n\n", (char *) data);
    printf("Result:\n");

    tkz = lxb_html_tokenizer_create();
    status = lxb_html_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to create tokenizer object");
    }
```

This portion of the code initializes a new tokenizer and checks for 
successful creation. If initialization fails, the program exits.

### Setting the Callback and Processing HTML

Next, we set the token callback function, begin tokenization, feed the HTML 
data chunk, and finalize the parsing.

```c
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

    printf("\n");

    lxb_html_tokenizer_destroy(tkz);

    return 0;
}
```

Here, the critical steps include:
- Setting the callback function with `lxb_html_tokenizer_callback_token_done_set`.
- Starting tokenization with `lxb_html_tokenizer_begin`.
- Feeding the HTML data with `lxb_html_tokenizer_chunk`.
- Completing the parsing with `lxb_html_tokenizer_end`.
- Cleaning up resources with `lxb_html_tokenizer_destroy`.

## Notes

- The example uses a custom callback function to handle specific tokens 
  (only text nodes in this case).
- The macro `FAILED` provides a simple and effective way to handle errors.
- Understanding the use of callbacks in tokenization processes is crucial 
  for advanced HTML parsing tasks.

## Summary

This example demonstrates how to use the `lexbor` library to tokenize and 
process HTML content, focusing on text nodes. By setting up a tokenizer, 
defining a callback function, and managing the parsing process, users gain 
insights into effectively handling HTML content in C with `lexbor`. This 
example is particularly instructive for developers looking to perform 
fine-grained HTML parsing and extraction tasks.