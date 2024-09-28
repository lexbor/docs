# Encoding Unicode Code Points to UTF-8 Example

This article explains the encoding of Unicode code points to a UTF-8 byte string using the Lexbor library. The source code is located in `lexbor/encoding/buffer/encode/encode.c`. This example demonstrates how to initialize the encoder, encode Unicode code points, and handle the output appropriately.

## Overview

The primary purpose of this code is to convert an array of Unicode code points into a UTF-8 encoded string. The code includes error handling, memory allocation for the output buffer, and final output printing. 

## Code Explanation

### Includes and Macros

The code begins with the inclusion of the `lexbor/encoding/encoding.h` header file, which provides necessary functions and definitions for encoding operations. A macro called `FAILED` is defined to handle error reporting:

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

This macro simplifies the error handling by printing an error message to `stderr` and exiting the program if there is a failure during initialization.

### Main Function

The `main` function initializes several variables and prepares to encode the Unicode code points:

```c
int main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_encoding_encode_t encode;
    const lxb_codepoint_t *cps_ref, *cps_end;
    const lxb_encoding_data_t *encoding;

    /* Prepare buffer */
    lxb_char_t buffer[1024];
```

In this section, a buffer of 1024 characters is created to hold the encoded byte string. The `lxb_codepoint_t` array contains several predefined Unicode code points.

### Unicode Code Points

The code points initialized in the `cps` array represent Cyrillic characters and symbols:

```c
lxb_codepoint_t cps[] = {0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442,
                         0x002C, 0x0020, 0x043C, 0x0438, 0x0440, 0x0021};
```

### Encoder Initialization

The encoding data for UTF-8 is retrieved and the encoder is initialized with:

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);
status = lxb_encoding_encode_init(&encode, encoding, buffer, sizeof(buffer));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization encoder");
}
```

Here, `lxb_encoding_data` retrieves encoding information for UTF-8, and `lxb_encoding_encode_init` initializes the encoding context. If the initialization fails, the `FAILED` macro is invoked.

### Encoding Process

Next, the code encodes the Unicode code points:

```c
status = encoding->encode(&encode, &cps_ref, cps_end);
if (status != LXB_STATUS_OK) {
    /* In this example, this cannot happen. */
}
```

This line calls the `encode` function from the `encoding` structure, which encodes the code points from `cps_ref` to `cps_end`.

### Output Preparation

After encoding, the buffer is terminated with a null character:

```c
buffer[ lxb_encoding_encode_buf_used(&encode) ] = 0x00;
```

### Printing Results

Finally, the result is displayed:

```c
printf("\nResult: %s\n", (char *) buffer);
```

This prints the encoded UTF-8 string to standard output along with the original Unicode values shown in hexadecimal format.

## Conclusion

This code example effectively demonstrates the usage of the Lexbor encoding library for converting Unicode code points to a UTF-8 encoded string. It emphasizes proper initialization, error handling, and output formatting, which are essential for working with character encoding in C programming.