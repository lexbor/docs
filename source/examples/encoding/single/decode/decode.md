# UTF-8 Decoding Example

This article explains a code example from [lexbor/encoding/single/decode/decode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/decode/decode.c), which demonstrates how to decode a UTF-8 string into its respective code points using the lexbor library.

## Introduction

The primary purpose of this code is to decode a UTF-8 encoded string, specifically the phrase "Привет, мир!" (which means "Hello, world!" in Russian), into individual Unicode code points. It showcases the initialization of the decoder, the processing of the input string, and outputting the results in a formatted manner.

## Code Explanation

### Include the Required Header

The necessary header file is included at the beginning of the code:

```c
#include <lexbor/encoding/encoding.h>
```

This header provides the necessary declarations for working with encoding functionalities offered by lexbor.

### Error Handling Macro

The code defines a macro for error handling:

```c
#define FAILED(...)                                                            \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

This macro outputs an error message to the standard error stream and exits the program if a failure condition is met. It streamlines error handling throughout the code.

### Main Function

The `main` function serves as the entry point of the program:

```c
int main(int argc, const char *argv[])
{
    ...
}
```

### Variable Declarations

Several variables are declared to handle the decoding process, including:

- `lxb_codepoint_t cp;`: Stores the current code point.
- `lxb_status_t status;`: Holds the status of operations.
- `lxb_encoding_decode_t decode;`: The decoder instance.
- `const lxb_encoding_data_t *encoding;`: Pointer to the encoding data.
- `const lxb_char_t *pos;`: Pointer to track the current position in the input data.

### Preparing the Input Buffer

The input UTF-8 string is initialized, along with a pointer to the end of the string:

```c
const lxb_char_t *data = (const lxb_char_t *) "Привет, мир!";
const lxb_char_t *end = data + strlen((char *) data);
```

The `strlen` function determines the length of the string to establish the end of the data.

### Setting Up the Encoding

The program retrieves UTF-8 encoding data with:

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);
```

This function sets up the necessary encoding data for subsequent decoding operations.

### Initializing the Decoder

The decoder is initialized with:

```c
status = lxb_encoding_decode_init_single(&decode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to init decoder");
}
```

If the initialization fails, the program invokes the `FAILED` macro to print the error and exit.

### Decoding Loop

Following initialization, the program enters a loop to decode each character in the input string:

```c
while (data < end) {
    ...
}
```

Inside the loop, the current position (`pos`) is recorded, and the decoding function is called:

```c
cp = encoding->decode_single(&decode, &data, end);
```

This line decodes a single UTF-8 character, advancing the input pointer `data` as needed. The result is checked against a maximum allowable code point value, although in this example, that condition is expected never to occur.

### Outputting the Results

For each decoded character, the code prints the results to the standard output:

```c
printf("%.*s: 0x%04X\n", (int) (data - pos), pos, cp);
```

This formatted output provides both the original UTF-8 character (as a substring) and its corresponding Unicode code point in hexadecimal format.

## Conclusion

The example demonstrates a straightforward approach to decoding a UTF-8 string into Unicode code points using the lexbor library. It effectively showcases initialization, error handling, and character decoding, providing a practical illustration of working with character encodings in C.