# CSS Syntax Tokenizer Example

This article provides a detailed explanation of a CSS syntax tokenizer
implemented in the file
[lexbor/css/syntax/tokenizer/from_file.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/css/syntax/tokenizer/from_file.c).
The code serves the purpose of reading a CSS file, processing its contents to
extract tokens, and producing output that describes each token.

## Overview

The main function of the tokenizer is to parse CSS code from a file, generate
tokens for syntactic analysis, and then invoke a callback function to handle the
output of each token. The program efficiently handles input and organizes the
parsing process with the help of the lexbor library.

## Code Breakdown

### Includes and Utility Functions

At the beginning of the file, necessary libraries are included:

```c
#include <lexbor/css/css.h>
#include <lexbor/core/fs.h>
```

The first include provides access to CSS-related functionality within the lexbor
library, whereas the second includes core file system operations needed to read
the CSS file.

A utility function `usage` is defined to provide a simple usage instruction:

```c
static void usage(void)
{
    fprintf(stderr, "parse_file <file>\n");
}
```

This function prints an error message when the user does not provide the correct
number of arguments.

### Main Function Logic

The entry point of the program is the `main` function, which processes
command-line arguments and orchestrates the tokenization process:

```c
int main(int argc, const char *argv[])
```

#### Argument Validation

At the start of the main function, the program checks whether exactly one
command-line argument (the CSS file name) has been provided:

```c
if (argc != 2) {
    usage();
    FAILED("Invalid number of arguments");
}
```

If not, it calls the `usage` function and exits with an error.

#### File Reading

Next, the code attempts to read the specified CSS file:

```c
css = lexbor_fs_file_easy_read((const lxb_char_t *) argv[1], &css_len);
if (css == NULL) {
    FAILED("Failed to read CSS file");
}
```

The `lexbor_fs_file_easy_read` function reads the entire file into memory, and
if it fails, the program reports the error and exits.

#### Tokenizer Initialization

The tokenizer is created and initialized:

```c
tkz = lxb_css_syntax_tokenizer_create();
status = lxb_css_syntax_tokenizer_init(tkz);
```

These lines allocate memory for the tokenizer and perform any necessary setup.
If initialization fails, an error message is printed, and the program proceeds
to cleanup.

#### Setting Input Buffer

Next, the contents of the CSS file are set as the input buffer for the
tokenizer:

```c
lxb_css_syntax_tokenizer_buffer_set(tkz, css, css_len);
```

This prepares the tokenizer to begin processing the CSS data.

### Tokenization Loop

The program enters a loop to process the tokens extracted from the input buffer:

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

#### Token Extraction

Within the loop, the function `lxb_css_syntax_token` retrieves a token. If no
token is available, it reports a parsing failure. Upon successful token
retrieval, it prints the type name of the token followed by calling
`lxb_css_syntax_token_serialize`, which uses the provided `callback` function to
output the token data.

The type of the current token is acquired to determine if the end of the file
(EOF) has been reached. If the EOF is not reached, the loop continues to consume
tokens.

### Cleanup and Exit

When the entire CSS file has been processed, resources are cleaned up:

```c
lxb_css_syntax_tokenizer_destroy(tkz);
lexbor_free(css);
```

Finally, the program returns `EXIT_SUCCESS` if the execution was successful, or
`EXIT_FAILURE` in case of any errors during the process.

## Conclusion

The CSS syntax tokenizer effectively reads and parses a CSS file, extracting and
displaying token details by utilizing the lexbor library's API for CSS
processing. This example demonstrates not only the functionality of lexer-based
parsing but also highlights memory management and error handling within a
complex system.