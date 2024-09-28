# Encoding Decoder Example

In this article, we will explore the encoding decoder example found in the file `lexbor/encoding/single/decode/decoder.c`. This code demonstrates how to decode input data from standard input according to a specified character encoding. It provides a useful utility for developers needing to handle various text encodings in their applications.

## Code Overview

The main function of this code is to read data from standard input, decode it according to the specified encoding, and print the corresponding Unicode values. It uses the Lexbor library to facilitate this process.

### Header and Includes

At the beginning of the file, we find the licensing information and the inclusion of the Lexbor encoding header:

```c
#include <lexbor/encoding/encoding.h>
```

This inclusion allows access to functions and definitions related to text encoding and decoding.

### Error Handling Macro

A macro named `FAILED` is defined to streamline error management:

```c
#define FAILED(with_usage, ...)                                                \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
                                                                               \
        if (with_usage) {                                                      \
            usage();                                                           \
        }                                                                      \
                                                                               \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

This macro takes a condition (`with_usage`) and, upon failure, prints an error message to standard error, optionally displays usage instructions, and exits the program with a failure status. This convenient encapsulation enhances code readability and maintainability.

### Usage Function

Next, the `usage` function is defined:

```c
static void usage(void)
{
    printf("Usage: decoder <encoding name>\n\n");
    printf("Available encodings:\n");
    ...
}
```

This function provides users with information about how to use the decoder program and lists the available character encodings that can be specified as command-line arguments.

### Main Function Structure

The `main` function begins with some variable declarations:

```c
int main(int argc, const char *argv[])
{
    size_t read_size;
    lxb_status_t status;
    lxb_codepoint_t cp = 0x0000;
    lxb_encoding_decode_t decode;
    const lxb_encoding_data_t *encoding;
```

**Variable Description:**
- `read_size`: To store the number of bytes read from standard input.
- `status`: To capture the success or failure of encoding operations.
- `cp`: A variable representing the code point being processed.
- `decode`: A structure for managing the decoding state.
- `encoding`: A pointer to the encoding data determined by user input.

#### Input Validation

The program first checks for the correct number of command-line arguments:

```c
if (argc != 2) {
    usage();
    exit(EXIT_SUCCESS);
}
```

If no encoding is specified, it invokes the `usage` function and exits gracefully.

#### Encoding Detection

Next, the program attempts to identify the desired encoding based on the provided name:

```c
encoding = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1],
                                         strlen(argv[1]));
if (encoding == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n\n", argv[1]);
}
```

If the specified encoding is not recognized, it triggers the `FAILED` macro, providing feedback to the user.

#### Decoder Initialization

The decoder is then initialized:

```c
status = lxb_encoding_decode_init_single(&decode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to init decoder");
}
```

This step configures the decoder to use the chosen encoding. If the initialization fails, the program prints an error and exits.

### Data Reading and Decoding Loop

The program enters a loop to read from standard input:

```c
do {
    read_size = fread(inbuf, 1, sizeof(inbuf), stdin);
    ...
    while (data < end) {
        cp = encoding->decode_single(&decode, &data, end);
        ...
    }
} while (loop);
```

Within this loop:
- Data is read into a buffer (`inbuf`).
- Each code point is decoded using the `decode_single` method.
- Based on the value of `cp`, different output formats are printed for Unicode and ASCII characters.

### Output and Continuation

Finally, the program checks if the decoding process requires continuation, outputting a replacement character where necessary:

```c
if (cp == LXB_ENCODING_DECODE_CONTINUE) {
    printf("\\u%04X", LXB_ENCODING_REPLACEMENT_CODEPOINT);
}
```

### Conclusion

By effectively using the Lexbor library's encoding functionalities, this code provides a flexible and powerful example of how to decode various text encodings from standard input. Developers can adapt this example for their applications, thereby enhancing their ability to handle encoded text data efficiently.