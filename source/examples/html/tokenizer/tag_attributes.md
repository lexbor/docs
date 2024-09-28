# Tokenization and Attribute Extraction Example

This article explains the code found in the `tag_attributes.c` file of the
lexbor project, which focuses on the tokenization of HTML content and the
extraction of attributes from tokens. The primary purpose of this code is to
parse a small fragment of HTML and output the attributes associated with each
token.

## Overview

The `tag_attributes.c` file implements a simple HTML tokenizer. It initializes a
tokenizer instance, feeds it some HTML data, and uses a callback function to
process and display the attributes of parsed tokens. The tokenizer effectively
handles different HTML tags and their attributes while logging any potential
errors that may occur during the process.

## Code Breakdown

### Includes and Macros

The file begins with including necessary header files:

```c
#include "lexbor/html/tokenizer.h"
#include "lexbor/html/token_attr.h"
```

These headers provide definitions and functionalities related to HTML
tokenization and attribute handling.

The `FAILED` macro is defined to streamline error handling throughout the code.
This macro takes a format string and variable arguments, prints the error
message to standard error, and exits the program if an issue arises.

### Token Callback Function

The core of the token processing logic is in the `token_callback` function:

```c
static lxb_html_token_t *
token_callback(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
```

This function is called whenever a token is completed. It first checks if the
token is a text node or has no attributes:

```c
if (token->tag_id == LXB_TAG__TEXT || attr == NULL) {
    return token;
}
```

If the token is a text node or has no attributes, the function returns
immediately without further processing. Otherwise, it retrieves the name of the
tag associated with the token using `lxb_tag_name_by_id`. A failure at this
point will invoke the `FAILED` macro:

```c
tag = lxb_tag_name_by_id(token->tag_id, NULL);
if (tag == NULL) {
    FAILED("Failed to get token name");
}
```

Assuming the tag name retrieval is successful, it prints out the tag's
attributes. The `while` loop iterates through the list of attributes associated
with the token:

```c
while (attr != NULL) {
    name = lxb_html_token_attr_name(attr, NULL);
```

For each attribute found, it checks if the name is valid; if not, it
acknowledges the situation by noting that the name is not set, particularly
handling tokens like `DOCTYPE`. The associated values of the attributes are
likewise printed if they exist.

### Main Function

The `main` function orchestrates the entire process:

```c
int main(int argc, const char *argv[])
```

This function initializes the tokenizer and sets up the HTML string for parsing.
The HTML fragment being parsed includes a `div` tag with several attributes and
nested `option` tags. It first prints the HTML string to the console:

```c
const lxb_char_t data[] = "<div id=one-id class=silent ref='some &copy; a'>"
                          "<option-one enabled>"
                          "<option-two enabled='&#81'>";
```

Next, it creates and initializes the tokenizer:

```c
tkz = lxb_html_tokenizer_create();
status = lxb_html_tokenizer_init(tkz);
```

In case of an error during the tokenizer's creation or initialization, it
utilizes the `FAILED` macro to handle the error appropriately.

The callback function for token completion is set, and the tokenizer begins
processing the HTML data. It processes the input by calling
`lxb_html_tokenizer_chunk`, and if any issues arise during these stages, the
`FAILED` macro is utilized once more to identify failures in parsing.

Finally, the tokenizer is destroyed, freeing any resources it allocated during
its execution, and the program returns 0, indicating a successful run.

## Conclusion

This example illustrates the process of HTML tokenization using the lexbor
library. By implementing a callback to handle parsed tokens, the code
effectively extracts and displays attribute names and values from the given HTML
fragment. It showcases the ability to manage errors gracefully while providing
informative output for attribute processing within tokens.