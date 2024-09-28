# HTML Tokenizer Callback Example

This article describes the implementation of an HTML Tokenizer Callback found in
the
[lexbor/html/tokenizer/callback.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/tokenizer/callback.c)
source file. The purpose of this code is to demonstrate how to parse an HTML
string and handle tokens as they are generated. It establishes a callback
mechanism that is invoked after each token is processed, allowing for custom
processing or logging of token data.

## Overview

The code begins by including necessary headers and defining a macro to handle
error reporting. It then implements a token callback function, `token_callback`,
which retrieves the tag name from a token, determines if the token represents a
closing tag, and prints relevant details. The main function orchestrates the
creation, initialization, and execution of the tokenizer.

## Error Handling Macro

The code defines a macro, `FAILED`, which simplifies error reporting and exits
the program when an error occurs. This macro takes a format string and variadic
arguments, prints the error message to standard error, and terminates the
program with `EXIT_FAILURE`. This approach centralizes error handling and
ensures that the program stops execution on critical failures.

## Token Callback Function

The function `token_callback` is critical as it processes each token generated
by the tokenizer. It accepts three parameters: a pointer to the tokenizer, a
pointer to the current token, and a context pointer (which is unused in this
case).

Within `token_callback`, the tag name is obtained using `lxb_tag_name_by_id`. If
the tag name cannot be retrieved, the macro `FAILED` is invoked to log the error
and exit. The token's type is checked to see if it indicates a closing tag. The
results, including the tag name, ID, and whether it is a closing tag, are
printed to standard output.

## Main Function Execution Flow

The `main` function contains several key operations:

1. **Creating and Initializing the Tokenizer**: The tokenizer is created using
   `lxb_html_tokenizer_create` and initialized with `lxb_html_tokenizer_init`.
   If any of these operations fail, the `FAILED` macro is invoked.

2. **Setting the Token Callback**: The tokenizer's callback function is set
   using `lxb_html_tokenizer_callback_token_done_set`, linking the tokenizer to
   the `token_callback` function defined earlier.

3. **Beginning the Tokenization Process**: The tokenization process is initiated
   with `lxb_html_tokenizer_begin`. This prepares the tokenizer for consuming
   HTML data.

4. **Processing HTML Data**: The provided HTML string
   (`"<div><span>test</span></div>"`) is processed by calling
   `lxb_html_tokenizer_chunk`, which reads a chunk of HTML to tokenize. After
   processing, the tokenizer is signaled to end its operation with
   `lxb_html_tokenizer_end`.

5. **Cleanup**: Finally, the tokenizer is destroyed using
   `lxb_html_tokenizer_destroy`, freeing up any resources allocated during its
   operation.

## Summary

This example illustrates the use of a callback function within a tokenizer to
process HTML tokens sequentially. By gracefully handling errors and providing
hooks for further processing, the code affords flexibility and clarity in
parsing HTML inputs using the `lexbor` library. It exemplifies best practices in
resource management, modular function design, and effective error handling in C.