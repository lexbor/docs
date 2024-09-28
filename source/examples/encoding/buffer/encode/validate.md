# Validating Encoded Strings with `lexbor`

This article explains the functioning of a code example found in the file 
[lexbor/encoding/buffer/encode/validate.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/encode/validate.c). This code demonstrates how to use 
the `lexbor` library to encode a series of Unicode code points into a UTF-8 byte 
string, validating and handling invalid code points along the way.

The example showcases how to properly initialize an encoder with 
the `lexbor` library, encode a sequence of Unicode code points into a UTF-8 byte 
string, and manage any invalid code points encountered in the process. The 
example's intent is to demonstrate the practical use of the `lexbor` encoding 
library for encoding and validating Unicode sequences.

## Key Code Sections

### Initialization and Buffer Preparation

The first critical step is to initialize the encoder and prepare the buffer for 
the encoded output.

```c
lxb_encoding_encode_t encode;
const lxb_codepoint_t *cps_ref, *cps_end;
const lxb_encoding_data_t *encoding;

/* Prepare buffer */
lxb_char_t buffer[1024];
```

Here, the `encode` structure is declared to hold the encoder state. An array of 
Unicode code points (`cps`) is prepared, consisting of valid and one invalid 
code point (`0x110000`). Buffer size of 1024 bytes is allocated to hold the 
encoded string.

### Setting Up the Encoder

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

status = lxb_encoding_encode_init(&encode, encoding, buffer, sizeof(buffer));
if (status != LXB_STATUS_OK) {
    FAILED("Failed to initialize encoder");
}

status = lxb_encoding_encode_replace_set(&encode, LXB_ENCODING_REPLACEMENT_BYTES,
                                         LXB_ENCODING_REPLACEMENT_SIZE);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to set replacement bytes for encoder");
}
```

The encoder is initialized with the `UTF-8` encoding and the provided buffer. 
The function `lxb_encoding_encode_init` takes care of this initialization. 
Additionally, `lxb_encoding_encode_replace_set` sets the replacement bytes to 
handle invalid code points. This ensures that invalid entries are substituted 
with a predefined replacement sequence.

### Encoding the Unicode Code Points

```c
cps_ref = cps;
cps_end = cps_ref + (sizeof(cps) / sizeof(lxb_codepoint_t));

printf("Encode code points to UTF-8 byte string:\n");

/* Encode */
status = encoding->encode(&encode, &cps_ref, cps_end);
if (status != LXB_STATUS_OK) {
    /* In this example, this cannot happen. */
}
```

The encoder processes the Unicode code points with the `encode` function, 
transforming them into a UTF-8 byte string. The output buffer will contain the 
encoded byte string, and a bad code point is replaced by the replacement bytes 
set previously.

### Finalizing the Encoding and Printing the Result

```c
buffer[ lxb_encoding_encode_buf_used(&encode) ] = 0x00;

/* Print result */
cps_ref = cps;

for (; cps_ref < cps_end; cps_ref++) {
    printf("0x%04X", *cps_ref);
}

printf("\nResult: %s\n", (char *) buffer);
```

The encoded string is null-terminated using the `lxb_encoding_encode_buf_used` 
to get the actual length of the encoded content. The original code points and 
the resulting encoded string are printed to the stdout, showcasing how the 
encoder dealt with the input, including the invalid code point.

## Notes

- **Error Handling**: Proper error handling is demonstrated with the `FAILED` 
  macro, ensuring that the program exits if initialization or replacement 
  byte setup fails.
- **Invalid Code Points**: The example shows how to handle invalid Unicode code 
  points gracefully by setting replacement bytes.
- **Initialization and Finalization**: Correct encoder initialization, buffer 
  setup, and string termination are important for ensuring the accuracy and 
  safety of the encoding process.

## Summary

This example demonstrates fundamental techniques in using the `lexbor` encoding 
library for converting Unicode code points to a UTF-8 byte string. It emphasizes 
error handling, the importance of setting replacement bytes for invalid code 
points, and proper buffer management. Understanding these concepts is crucial 
for developers working with Unicode text processing and encoding using the 
`lexbor` library.