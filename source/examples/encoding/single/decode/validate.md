# UTF-8 String Decoding and Validation

This article explains a demonstrative code file [lexbor/encoding/single/decode/validate.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/decode/validate.c) that 
decodes and validates a UTF-8 encoded string to code points using the `lexbor` library. The example 
focuses on initializing the decoder, processing each byte sequence in the input string to validate 
and decode it, and handling invalid byte sequences.

## Key Code Sections

### Initialization and Setup

The main function initializes the necessary variables and prepares the input buffer. This part 
includes selecting the UTF-8 encoding type and initializing the decoder struct:

```c
int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_codepoint_t cp;
    lxb_encoding_decode_t decode;
    const lxb_encoding_data_t *encoding;
    const lxb_char_t *pos;

    /* Prepare buffer */
    const lxb_char_t *data = (const lxb_char_t *) "Привет,\x80 мир!";
    const lxb_char_t *end = data + strlen((char *) data);

    encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

    status = lxb_encoding_decode_init_single(&decode, encoding);
    if (status != LXB_STATUS_OK) {
        FAILED("Failed to init decoder");
    }
```

Key points:
- `lxb_encoding_data(LXB_ENCODING_UTF_8)` retrieves data for the UTF-8 encoding.
- `lxb_encoding_decode_init_single(&decode, encoding)` initializes the decoder structure for that encoding.

### Decoding the Input String

The core of the decoding process involves a loop to read each byte sequence of the input string and 
convert it to Unicode code points:

```c
    printf("Decode and validate UTF-8 string \"%s\" to code points:\n", (char *) data);

    while (data < end) {
        pos = data;

        cp = encoding->decode_single(&decode, &data, end);
        if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
            printf("Bad byte sequences: 0x%04X; Replaced to: 0x%04X ('%s')\n", 
                   *pos, LXB_ENCODING_REPLACEMENT_CODEPOINT,
                   LXB_ENCODING_REPLACEMENT_BYTES);

            continue;
        }

        printf("%.*s: 0x%04X\n", (int) (data - pos), pos, cp);
    }
```

Key points:
- The loop runs while `data` is less than `end` to process each byte sequence.
- `encoding->decode_single(&decode, &data, end)` performs the core decoding of the current byte sequence.
- If the decoded code point `cp` exceeds `LXB_ENCODING_DECODE_MAX_CODEPOINT`, it handles this invalid 
  byte sequence by replacing it with a predefined replacement code point and bytes.

### Handling Invalid Byte Sequences

When encountering invalid byte sequences, the code prints out an error message and continues:

```c
        if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
            printf("Bad byte sequences: 0x%04X; Replaced to: 0x%04X ('%s')\n", 
                   *pos, LXB_ENCODING_REPLACEMENT_CODEPOINT,
                   LXB_ENCODING_REPLACEMENT_BYTES);

            continue;
        }
```

Key points:
- The check `cp > LXB_ENCODING_DECODE_MAX_CODEPOINT` determines if the decoded value is valid.
- Invalid input sequences are substituted with `LXB_ENCODING_REPLACEMENT_CODEPOINT`, and an error message 
  is printed using the original byte.

## Notes

- The `lexbor` library's decoding functions must be initialized with the specific encoding data.
- Each byte sequence in the input string is validated and can be replaced if found invalid.
- The code uses a custom macro `FAILED` to handle initialization errors and terminate execution.

## Summary

This example demonstrates how to decode and validate a UTF-8 encoded string using the `lexbor` 
library. By initializing the decoder with UTF-8 encoding, processing each byte sequence, and 
handling invalid sequences, it showcases essential functionality for anyone working with text 
processing and encoding validation using `lexbor`. This provides a practical foundation for 
handling encoded text robustness in applications.