# CSS Syntax Tokenizer Example

This article explains the implementation of a CSS syntax tokenizer in the file [lexbor/css/syntax/tokenizer/chunks_stdin.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/css/syntax/tokenizer/chunks_stdin.c). The code demonstrates how to read CSS data from standard input, tokenize it, and output the identified token types along with their serialized representations.

## Overview

The main purpose of this example is to showcase the mechanics of the `lxb_css_syntax_tokenizer`, a component provided by the Lexbor library for parsing CSS syntax. The example leverages standard input (stdin) to read CSS input, processes the tokens through the tokenizer, and outputs details about each token to the console.

## Code Breakdown

### Includes and Definitions

At the beginning of the file, necessary headers are included, such as `lexbor/css/css.h`, which contains the definitions and interfaces for the CSS parser. A small buffer size of 32 bytes is defined with `#define BUFFER_SIZE 32`, which limits the amount of data read from stdin at one time, making it suitable for demonstration purposes.

### Callback Function

The `callback` function is defined to handle the serialized output of the tokens:

```c
lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx) {
    printf("%s", (const char *) data);
    return LXB_STATUS_OK;
}
```

This function prints the serialized token data to the console and returns a status indicating success. It serves as a simple mechanism to display token information during parsing.

### Chunk Callback Function

The `chunk_cb` function reads chunks of CSS data into a buffer and sets up the tokenizer to consume these chunks:

```c
lxb_status_t chunk_cb(lxb_css_syntax_tokenizer_t *tkz, const lxb_char_t **data, const lxb_char_t **end, void *ctx) {
    size_t size;
    lxb_char_t *buff = ctx;

    size = fread((char *) buff, 1, BUFFER_SIZE, stdin);
    if (size != BUFFER_SIZE) {
        if (feof(stdin)) {
            tkz->eof = true;
        } else {
            return EXIT_FAILURE;
        }
    }

    *data = buff;
    *end = buff + size;

    return LXB_STATUS_OK;
}
```

The function first attempts to read a buffer full of CSS data from stdin. If the end of input is reached, it marks the tokenizer's end-of-file (EOF) state. If an error occurs during reading, it returns a failure status. The function effectively prepares the data for the tokenizer by updating the pointed `data` and `end` pointers.

### Main Function

The `main` function orchestrates the initialization and the execution of the CSS syntax tokenizer:

```c
int main(int argc, const char *argv[]) {
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
```

This section starts by creating and initializing a tokenizer instance. If initialization fails, it gracefully exits the process. Notably, it sets the chunk callback function, associating it with the previously defined `chunk_cb` and the input buffer `inbuf`.

#### Token Processing Loop

The main loop processes tokens until the EOF is reached:

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
} while (type != LXB_CSS_SYNTAX_TOKEN__EOF);
```

In this loop, it retrieves the next token from the tokenizer and checks for parsing errors. If a token is successfully obtained, it retrieves and prints the token's type name, serializes the token using the earlier defined `callback`, and then consumes the token to prepare for the next cycle. This loop continues until an EOF token is encountered.

### Cleanup

At the end of the function, the tokenizer is destroyed to free up allocated resources:

```c
lxb_css_syntax_tokenizer_destroy(tkz);
```

If any failures occur at various stages, the code ensures proper cleanup to avoid memory leaks.

## Conclusion

This example illustrates how to implement a simple CSS syntax tokenizer using the Lexbor library, allowing for parsing CSS input from stdin and outputting token information. Anyone looking to understand or extend CSS parsing functionality can use this code as a foundation for further development.