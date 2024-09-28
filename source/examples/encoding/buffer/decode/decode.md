# Decoding UTF-8 Strings to Code Points with `lexbor`
The code example in [lexbor/encoding/buffer/decode/decode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/decode/decode.c) demonstrates how to decode a UTF-8 encoded string into individual Unicode code points using the `lexbor` library. The example illustrates initialization, decoding, and extracting code points using various `lexbor` functions and data types.

## Key Code Sections

### Initialization and Buffer Preparation

```c
const lxb_char_t *data = (const lxb_char_t *) "Привет, мир!";
const lxb_char_t *end = data + strlen((char *) data);
```

Here, a UTF-8 encoded string `"Привет, мир!"` is defined and its length is calculated. These will be utilized later during the decoding process.

### Initializing the Decoder

```c
const lxb_encoding_data_t *encoding;
lxb_status_t status;
lxb_codepoint_t cp[32];
lxb_encoding_decode_t decode;

encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

status  = lxb_encoding_decode_init(&decode, encoding, cp,
                                   sizeof(cp) / sizeof(lxb_codepoint_t));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization decoder");
}
```

In this section, the UTF-8 encoding data structure is obtained with `lxb_encoding_data(LXB_ENCODING_UTF_8)`. The decoder is then initialized via `lxb_encoding_decode_init`, where `decode` is the decoder context, `encoding` provides encoding information, and `cp` is an array to store the decoded code points. The size of this array is specified in terms of the number of `lxb_codepoint_t` elements it can hold.

### Performing the Decoding

```c
status = encoding->decode(&decode, &data, end);
if (status != LXB_STATUS_OK) {
    // In this example, this cannot happen.
}
```

The actual decoding process occurs with `encoding->decode(&decode, &data, end)`, taking the initialized decoder and the data buffer into account. The `data` pointer is updated during the procedure and moves towards `end`. It’s worth noting that usual error handling is omitted here, under the assumption that decoding will succeed.

### Printing the Decoded Code Points

```c
size_t buf_length = lxb_encoding_decode_buf_used(&decode);

for (size_t i = 0; i < buf_length; i++) {
    printf("0x%04X\n", cp[i]);
}
```

Finally, the number of used buffer entries (`buf_length`) is obtained using `lxb_encoding_decode_buf_used(&decode)`. A loop then iterates through the decoded code points within `cp[]`, printing each as a hexadecimal value (`0x%04X`), conforms to the Unicode code points of the original UTF-8 string.

## Notes

- **Error Handling**: The macro `FAILED(...)` is used for error handling, terminating the program with a corresponding message and `EXIT_FAILURE`. This ensures immediate notification of initialization failures.
- **Buffer Management**: The `cp[]` array size is set to 32, meant for handling individual code points and providing enough space for decoding without buffer overflow.
- **Assumptions**: The example assumes a successful decoding process, omitting error handling for the decoding step itself.

## Summary
This example illustrates a foundational aspect of working with `lexbor`: converting a UTF-8 encoded string to Unicode code points. By understanding how to initialize the decoder, handle buffer management, and perform the decoding process, developers can leverage `lexbor` for advanced text processing tasks. This underscores `lexbor`’s utility in dealing with various encodings efficiently and robustly.