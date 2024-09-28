# UTF-8 Decoding and Validation Example

This article explains an example of decoding and validating a UTF-8 string, using the Lexbor library. The source file for this code example is `lexbor/encoding/single/decode/validate.c`. The primary objective of this code is to demonstrate how to properly decode a UTF-8 encoded string, handle decoding errors, and output both valid code points and error information for invalid byte sequences.

## Code Breakdown

The example begins with necessary includes and macro definitions. It imports the required header file for Lexbor encoding and defines a macro `FAILED` that handles error reporting and terminates the program if an error occurs.

### Setting Up the Main Function

The `main` function initializes variables needed for decoding. Here, `lxb_status_t status`, `lxb_codepoint_t cp`, and `lxb_encoding_decode_t decode` are declared. Additionally, a pointer to encoding data will be initialized as the UTF-8 encoding.

```c
lxb_status_t status;
lxb_codepoint_t cp;
lxb_encoding_decode_t decode;
const lxb_encoding_data_t *encoding;
```

### Preparing the Data Buffer

The code prepares a buffer containing the string "Привет,\x80 мир!". The string contains a valid UTF-8 sequence followed by an invalid byte sequence (0x80). The end of the buffer is determined using `strlen` to ensure the decoding process will iterate through the entire string.

```c
const lxb_char_t *data = (const lxb_char_t *) "Привет,\x80 мир!";
const lxb_char_t *end = data + strlen((char *) data);
```

### Initializing the Decoder

The encoding is initialized with `lxb_encoding_data(LXB_ENCODING_UTF_8)`, and the decoder is set up using the function `lxb_encoding_decode_init_single`. If initialization fails, the `FAILED` macro reports the error and exits the program.

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);
status = lxb_encoding_decode_init_single(&decode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to init decoder");
}
```

### Decoding Process

The core loop of the example begins, where the program continuously decodes until the end of the data buffer is reached. Each iteration decodes a single code point from the UTF-8 data.

```c
while (data < end) {
    pos = data;
    cp = encoding->decode_single(&decode, &data, end);
}
```

If a valid code point is within the acceptable range defined by `LXB_ENCODING_DECODE_MAX_CODEPOINT`, it gets printed together with the decoded UTF-8 sequence. If an invalid byte sequence is encountered that exceeds the maximum code point, it prints an error message indicating the bad byte sequences.

```c
if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
    printf("Bad byte sequences: 0x%04X; Replaced to: 0x%04X ('%s')\n", 
           *pos, LXB_ENCODING_REPLACEMENT_CODEPOINT,
           LXB_ENCODING_REPLACEMENT_BYTES);
    continue;
}
```

### Conclusion

The program concludes by returning a success status if all decoding operations complete without errors. In summary, this code serves as an illustrative example of how to utilize the Lexbor encoding library to decode and validate UTF-8 encoded strings effectively, while properly handling potential errors in byte sequences. By implementing this method, developers can ensure their applications correctly interpret and display UTF-8 content.