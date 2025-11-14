# Validating and Replacing Invalid UTF-8 Encodings

This article explains the example file [lexbor/encoding/buffer/decode/validate.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/decode/validate.c)
which demonstrates how to decode a UTF-8 encoded string and handle invalid byte
sequences by replacing them with a specific replacement sequence using the `lexbor` library.

The purpose of the example is to
show how to initialize a decoder, set replacement sequences for invalid byte
sequences, and decode a UTF-8 string, handling errors gracefully. This example
is useful to those needing to ensure robust UTF-8 decoding in their applications.

## Key Code Sections

### Initialization of Encoding Data

In the first significant part of the code, we initialize the `lexbor` encoding
data for UTF-8:

```c
const lxb_encoding_data_t *encoding;

/* Initialize for UTF-8 encoding */
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);
```

This uses the `lxb_encoding_data` function to obtain a pointer to the encoding
data for UTF-8, as specified by the constant `LXB_ENCODING_UTF_8`.

### Decoder Initialization

We then proceed with initializing the decoder by using `lxb_encoding_decode_init`:

```c
lxb_status_t status;
lxb_codepoint_t cp[32];
lxb_encoding_decode_t decode;

status = lxb_encoding_decode_init(&decode, encoding, cp,
                                  sizeof(cp) / sizeof(lxb_codepoint_t));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialization decoder");
}
```

Here, `lxb_encoding_decode_init` initializes the `decode` structure for the given
encoding and prepares it to store code points in the `cp` buffer. If this operation
fails, an error message is printed and the program exits.

### Setting Replacement Code Points

Invalid byte sequences are handled by setting a replacement sequence with
`lxb_encoding_decode_replace_set`:

```c
status = lxb_encoding_decode_replace_set(&decode, LXB_ENCODING_REPLACEMENT_BUFFER,
                                         LXB_ENCODING_REPLACEMENT_BUFFER_LEN);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to set replacement code points for decoder");
}
```

By using the `LXB_ENCODING_REPLACEMENT_BUFFER` and associated length macro,
we configure the decoder to substitute invalid sequences with a predefined replacement.

### Decoding the UTF-8 String

The core decoding process is performed with:

```c
const lxb_char_t *data = (const lxb_char_t *) "Привет,\x80 мир!";
const lxb_char_t *end = data + strlen((char *) data);

status = encoding->decode(&decode, &data, end);
if (status != LXB_STATUS_OK) {
    /* In this example, this cannot happen. */
}
```

Here, `data` contains the UTF-8 string to be decoded, including an invalid byte
sequence (`\x80`). We call the `encoding->decode` function to process the string
and handle any invalid sequences using the previously set replacement.

### Printing the Result

Finally, the decoded code points are printed:

```c
size_t buf_length = lxb_encoding_decode_buf_used(&decode);

for (size_t i = 0; i < buf_length; i++) {
    printf("0x%04X\n", cp[i]);
}
```

The `lxb_encoding_decode_buf_used` function returns the number of code points
stored in the buffer, which we then iterate over, printing each as a hexadecimal value.

## Notes

1. The `FAILED` macro is used for error handling by printing a message and exiting.
2. The invalid byte sequence, `\x80`, is replaced using the specified replacement sequence.
3. The example demonstrates how to handle both initialization and runtime errors
   gracefully.

## Summary

This example showcases the proper use of the `lexbor` library for decoding UTF-8
strings while managing invalid byte sequences. It covers data initialization,
decoder setup, and configurable error handling using replacement sequences.
Understanding this example is essential for developers needing robust UTF-8
decoding in their lexbor-based applications.