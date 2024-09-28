# UTF-8 Decoding and Replacement Example

This article will explain a C code example that demonstrates UTF-8 decoding and
the handling of invalid byte sequences using the `lexbor` library. The source file
for the example is
[lexbor/encoding/buffer/decode/validate.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/decode/validate.c).

## Overview

The provided code illustrates how to initialize a decoder for UTF-8 encoded
strings and replace any invalid byte sequences with specified replacement code
points. This is accomplished utilizing the lexbor encoding API.

## Code Breakdown

### Including Necessary Headers

At the start of the code, the relevant header file from the `lexbor` library is
included:

```c
#include <lexbor/encoding/encoding.h>
```

This inclusion is necessary as it provides the required declarations and
definitions for encoding operations performed later in the code.

### Defining a Macro for Error Handling

A macro named `FAILED` is defined to handle errors gracefully:

```c
#define FAILED(...)                                                            \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
                                                                               \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

This macro uses `fprintf` to print error messages to standard error and then
exits the program with `EXIT_FAILURE`. It helps streamline error reporting
throughout the code.

### Main Function and Buffer Preparation

The main function initializes several variables, including a buffer for decoded
code points and an instance of the decoder:

```c
int main(int argc, const char *argv[]) {
    size_t buf_length;
    lxb_status_t status;
    lxb_codepoint_t cp[32];
    lxb_encoding_decode_t decode;
    const lxb_encoding_data_t *encoding;

    const lxb_char_t *data = (const lxb_char_t *) "Привет,\x80 мир!";
    const lxb_char_t *end = data + strlen((char *) data);
```

In this segment, a buffer `cp` is defined to hold up to 32 decoded code points.
The `data` variable contains a UTF-8 string that includes an invalid byte
(`\x80`). The `end` variable calculates the pointer to the end of the `data`.

### Initializing the Decoder

The code initializes the decoder for UTF-8 using:

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);
status = lxb_encoding_decode_init(&decode, encoding, cp,
                                  sizeof(cp) / sizeof(lxb_codepoint_t));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization decoder");
}
```

Here, `lxb_encoding_data` retrieves the encoding data for UTF-8. The
`lxb_encoding_decode_init` function sets up the decoder with the encoding
information and the previously defined buffer for decoded code points. If
initialization fails, the `FAILED` macro is invoked.

### Configuring Replacement Settings

Next, the code sets up settings for replacing invalid byte sequences:

```c
status = lxb_encoding_decode_replace_set(&decode, LXB_ENCODING_REPLACEMENT_BUFFER,
                                         LXB_ENCODING_REPLACEMENT_BUFFER_LEN);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to set replacement code points for decoder");
}
```

This step allows the decoder to specify how to handle invalid sequences by using
the replacement character defined in lexbor. Again, the error handling is
consistent throughout.

### Decoding the Input String

The actual decoding is performed with the following:

```c
status = encoding->decode(&decode, &data, end);
if (status != LXB_STATUS_OK) {
    /* In this example, this cannot happen. */
}
```

This line invokes the decoding process, moving through the input string from
`data` to `end`. The decoder attempts to handle any valid sequences and replaces
any invalid sequences as configured earlier.

### Outputting the Decoded Values

Finally, the decoded code points are printed:

```c
buf_length = lxb_encoding_decode_buf_used(&decode);

for (size_t i = 0; i < buf_length; i++) {
    printf("0x%04X\n", cp[i]);
}
```

Here, `lxb_encoding_decode_buf_used` retrieves the number of valid code points
decoded. Then, a loop iterates over each code point in the buffer, printing the
hexadecimal representation.

## Conclusion

This example effectively showcases the use of the `lexbor` library for decoding
UTF-8 strings while managing potentially invalid byte sequences. By initializing
the decoder, setting up replacement strategies, and decoding the input string,
the program demonstrates a robust method for handling encoding issues in C.