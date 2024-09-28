# Encoding Unicode Code Points to UTF-8 Example

This example demonstrates how to validate and encode Unicode code points into a
UTF-8 byte string using the lexbor library. The functionality is encapsulated
within a C program located in the
[lexbor/encoding/single/encode/validate.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/encode/validate.c)
file. The purpose of this code is to illustrate the encoding of a set of given
code points, handling exceptions for those that are invalid by replacing them
with a predefined replacement character.

## Overview of the Code

The code begins by including the necessary header files from the lexbor library,
specifically targeting encoding functionality. It subsequently defines a macro
for error handling, which outputs an error message to `stderr` and exits the
program with a failure status.

### Variable Declarations

The `main` function sets up various variables needed for the encoding process:

- `len`: This variable stores the length of the encoded string.
- `status`: Utilized for capturing the status of encoding operations.
- `encode`: An instance of `lxb_encoding_encode_t`, used to manage encoding
  context.
- `encoding`: A pointer to the appropriate encoding data.
- `pos`: A pointer that tracks the current position in the output buffer.

### Buffer Preparation

A buffer (`buffer`) of 1024 `lxb_char_t` elements is defined to hold the
resulting UTF-8 byte string. Pointers are initialized to manage the writing
process into this buffer safely.

### Unicode Code Points

An array of Unicode code points is declared, which includes both valid and an
intentionally invalid code point (`0x110000`). This is to illustrate how the
code handles bad input during encoding.

### Encoding Initialization

The code retrieves the UTF-8 encoding data using
`lxb_encoding_data(LXB_ENCODING_UTF_8)` and initializes the encoding context
with `lxb_encoding_encode_init_single(&encode, encoding)`. If this
initialization fails, an error message is reported, and the program exits.

### Encoding Loop

The core functionality is encapsulated in a loop that processes each code point
from the `cps` array:

1. **Position Tracking**: The position pointer `pos` is reset to the current
   data pointer at the start of the loop iteration.
2. **Encoding**: Each code point is encoded using the `encode_single` method.
   The returned `len` represents the number of bytes written to the buffer.
3. **Error Handling**: If `len` indicates a problem (less than
   `LXB_ENCODING_ENCODE_OK`), the code checks for buffer size issues (though
   this example does not expect to encounter this). If the code point is
   invalid, it prints an error message along with a replacement character
   output, handling the invalid code point scenario gracefully.
4. **Output**: For valid code points, the program prints the code point and its
   corresponding UTF-8 representation.

### Finalization

After processing all code points, the program terminates the string by setting
the last byte of the buffer to `0x00`. It then prints the final UTF-8 result.

## Conclusion

The program effectively showcases how to handle Unicode encoding with proper
error management for invalid inputs. This example is particularly useful for
developers using the lexbor library to manage character encodings, providing
insight on validating and encoding procedures in C.