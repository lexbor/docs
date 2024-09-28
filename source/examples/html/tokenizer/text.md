# HTML Tokenizer Example

This article describes the functionality of the example code provided in the file `lexbor/html/tokenizer/text.c`. The code implements an HTML tokenizer using the Lexbor library, focusing on extracting and printing text tokens from HTML input.

## Overview of the Code

The main thrust of this code is to parse HTML data, identify text tokens within it, and print those tokens to the standard output. The code utilizes functions provided by the Lexbor library, a lightweight and efficient HTML and XML processing library.

## Key Sections of the Code

### Header and Macros

The code begins with the inclusion of the `lexbor/html/tokenizer.h` header file, which contains the necessary declarations for using the tokenizer functionality of the Lexbor library. Following this, a macro named `FAILED` is defined. This macro can be used throughout the code to simplify error handling:

```c
#define FAILED(...)                                                            \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

It takes a format string and arguments to generate error messages. When invoked, it prints the message to standard error and terminates the program.

### Token Callback Function

Next, there is the `token_callback` function that manages the processing of tokens emitted by the tokenizer:

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

The function checks whether the token is a text token (identified by `LXB_TAG__TEXT`). If it is not, it simply returns the token without further processing. For text tokens, it prints the text content to standard output using the `printf` function. This content is extracted from the token's `text_start` and `text_end` fields, which indicate the starting and ending positions of the text within the HTML data.

### Main Function

Finally, the `main` function orchestrates the tokenizer's operation:

```c
int main(int argc, const char *argv[])
{
    ...
    const lxb_char_t data[] = "<div>Hi<span> my </span>friend</div>! "
                              "&#x54;&#x72;&#x79;&#x20;&#x65;&#x6e;&#x74;"
                              "&#x69;&#x74;&#x69;&#x65;&#x73;&excl;";
    
    ...
    
    tkz = lxb_html_tokenizer_create();
    status = lxb_html_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to create tokenizer object");
    }
    ...
    
    status = lxb_html_tokenizer_chunk(tkz, data, (sizeof(data) - 1));
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to parse the html data");
    }
    
    ...
    
    lxb_html_tokenizer_destroy(tkz);
    
    return 0;
}
```

The HTML input is defined as a character array that includes HTML elements and character references. The code creates a tokenizer instance using `lxb_html_tokenizer_create()` and initializes it with `lxb_html_tokenizer_init()`. If these operations fail, the `FAILED` macro is called to report the issue and exit.

The tokenizer callback is set through `lxb_html_tokenizer_callback_token_done_set()`, linking the `token_callback` function to handle tokens once they are fully parsed. The main parsing operations occur through `lxb_html_tokenizer_begin()` and `lxb_html_tokenizer_chunk()`, processing the data until the end of the input with `lxb_html_tokenizer_end()`.

Finally, the tokenizer instance is destroyed with `lxb_html_tokenizer_destroy(tkz)`, which frees up resources allocated during the process.

## Conclusion

This example provides a clear illustration of how to utilize the Lexbor library to parse HTML and process text tokens. By focusing on text tokens, and employing proper error handling mechanics, the code demonstrates a concise yet effective approach to basic HTML tokenization.