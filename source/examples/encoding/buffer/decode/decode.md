# UTF-8 Decoding Example

In this article, we will explore a code example from the file
[lexbor/encoding/buffer/decode/decode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/decode/decode.c)
that demonstrates how to decode a UTF-8 encoded string into code points using
the `lexbor` library. This example specifically highlights the usage of `lexbor`'s
encoding functionalities, providing insights into how to leverage these features
for character decoding in C.

## Code Explanation

The code begins by including the necessary header files. It specifically
includes `lexbor/encoding/encoding.h`, which contains the declarations needed
for encoding and decoding operations. The definition of the `FAILED` macro is
also provided, which facilitates error handling by printing an error message to
`stderr` and terminating the program if an error occurs.

### Main Function

The `main` function serves as the entry point of our program, where we will set
up the decoding of a UTF-8 encoded string.

#### Variable Declarations

Within the `main` function, several important variables are declared:

- `buf_length`: To store the length of the decoded buffer.
- `status`: To hold the status of operations, indicated by the `lxb_status_t`
  type.
- `cp`: An array of `lxb_codepoint_t` to hold the decoded code points.
- `decode`: An instance of `lxb_encoding_decode_t`, which manages the decoding
  process.
- `encoding`: A pointer to the encoding data.

Next, we prepare the buffer that contains the UTF-8 string "Привет, мир!" (which
translates to "Hello, World!"). The buffer is defined as `data`, and `end` is
set to point to the end of the string using `strlen`.

#### Initialization

The initialization process is crucial for setting up the decoder. We call
`lxb_encoding_data(LXB_ENCODING_UTF_8)` to get the encoding data for UTF-8.
Then, we initialize the decoder using `lxb_encoding_decode_init`, passing the
decoder instance, encoding, the code point array, and its capacity.

If this initialization fails, the `FAILED` macro is triggered, notifying us with
an error message and stopping the program.

#### Decoding Process

After successful initialization, we print the original UTF-8 string to the
console. The actual decoding is carried out by calling the `decode` function
through the `encoding` pointer. The function decodes the string pointed to by
`data` up to its `end`, storing the results in the `cp` array.

In this context, an error during decoding is not expected. Therefore, the code
contains a comment indicating that such a situation cannot occur in this
example, underlining the robustness of the decoding function for the given
input.

#### Output and Conclusion

Finally, we calculate the length of the buffer used in the decoding process with
`lxb_encoding_decode_buf_used(&decode)` and print each decoded code point in
hexadecimal format.

The program concludes with a return statement indicating successful execution.

## Summary

This example effectively illustrates how to decode a UTF-8 string into
individual code points using the `lexbor` library. It emphasizes the
initialization of the decoding context, error handling strategies, and the
process of translating encoded UTF-8 data into usable character representations.
Through careful management of buffers and decoding functions, developers can
build robust applications that accurately handle multi-byte character sets.