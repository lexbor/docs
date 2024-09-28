# HTML Tokenization with lexbor

In this article, we will walk through an example demonstrating the usage of the
`lexbor` HTML tokenizer, specifically focusing on the `simple.c` file located in
`lexbor/html/tokenizer/`. This sample illustrates how to tokenize HTML content,
process tokens, and utilize callback functions.

The code example demonstrates how
to use the `lexbor` library to tokenize HTML content. The intent of this example
is to process HTML data, extract tokens and their attributes, and print them to
standard output in a structured way. This involves setting up the tokenizer,
handling tokens through a callback, and managing tokenizer lifecycle.

## Key Code Sections

### Token Callback Function

In the code, the `token_callback` function is defined to handle tokens as they
are parsed. Here's how it works:

```c
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    // [token processing logic]
}
```

The function takes three arguments: a pointer to the tokenizer instance, the
current token, and a context pointer. It returns the current token to continue
processing.

The token processing logic inside the callback function is designed to handle
different types of tokens. For example:

```c
if (token->tag_id == LXB_TAG__END_OF_FILE) {
    return token;
}
```

This checks if the current token indicates the end of file, denoting the
completion of parsing.

### Tokenizing Text Tokens

The function also handles text tokens (i.e., content between tags):

```c
if (token->tag_id == LXB_TAG__TEXT) {
    printf("%.*s", (int) (token->end - token->begin), token->begin);
    return token;
}
```

Here, the text token content is printed directly by calculating the length of
the text and using its pointer values.

### Handling Element Tokens and Attributes

For element tokens, the function writes out the tag name and its attributes:

```c
if (token->type & LXB_HTML_TOKEN_TYPE_CLOSE) {
    printf("</%.*s", (int) (token->end - token->begin), token->begin);
}
else {
    printf("<%.*s", (int) (token->end - token->begin), token->begin);
}
```

Depending on whether the token is a closing tag, the appropriate tag format is
printed.

Attributes are handled in a loop to cater to multiple attributes within a single
tag:

```c
attr = token->attr_first;
while (attr != NULL) {
    printf(" %.*s", (int) (attr->name_end - attr->name_begin), attr->name_begin);
    if (attr->value_begin) {
        char qo = (char) *(attr->value_begin - 1);
        if (qo == '=') {
            printf("=%.*s", (int) (attr->value_end - attr->value_begin), attr->value_begin);
        } else {
            printf("=%c%.*s%c", qo, (int) (attr->value_end - attr->value_begin), attr->value_begin, qo);
        }
    }
    attr = attr->next;
}
```

### Main Function and Tokenizer Setup

The main function is responsible for setting up the tokenizer, initiating
parsing, and defining the HTML input data.

```c
int main(int argc, const char *argv[])
{
    lxb_html_tokenizer_t *tkz;
    const lxb_char_t data[] = "<div a='b' enabled> &copy; Hi<span c=\"d\" e=f> my </span>friend</div>";
    
    printf("HTML:\n%s\n\n", (char *) data);
    printf("Result:\n");

    tkz = lxb_html_tokenizer_create();
    lxb_html_tokenizer_init(tkz);
    lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);
    lxb_html_tokenizer_begin(tkz);
    lxb_html_tokenizer_chunk(tkz, data, (sizeof(data) - 1));
    lxb_html_tokenizer_end(tkz);
    lxb_html_tokenizer_destroy(tkz);

    return 0;
}
```

- The `data` array contains the HTML content to tokenize.
- The tokenizer is created and initialized.
- The callback function is set to handle tokens.
- The HTML content is processed in chunks, and parsing is finalized.

### Tokenizer Lifecycle Management

Proper management of the tokenizer's lifecycle is crucial:

```c
tkz = lxb_html_tokenizer_create();
lxb_html_tokenizer_init(tkz);
lxb_html_tokenizer_callback_token_done_set(tkz, token_callback, NULL);
lxb_html_tokenizer_begin(tkz);
lxb_html_tokenizer_chunk(tkz, data, (sizeof(data) - 1));
lxb_html_tokenizer_end(tkz);
lxb_html_tokenizer_destroy(tkz);
```

These calls are responsible for initializing the tokenizer, setting up the
callback, starting the tokenizer, processing data in chunks, finalizing the
parsing, and ultimately destroying the tokenizer object.

## Notes

- The example covers the handling of text and element tokens separately.
- Attributes are processed with consideration for quoted and unquoted values.
- Proper lifecycle management ensures resource cleanup and error handling.

## Summary

This example showcases the usage of the `lexbor` HTML tokenizer and how it can
be utilized to parse and process HTML content efficiently. It provides insights
into token processing and callback functions, making it valuable for developers
looking to work with the `lexbor` library for HTML parsing tasks. Understanding
the structure and flow of this example will aid in creating robust HTML parsers
using `lexbor`.