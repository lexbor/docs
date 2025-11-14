# Decoding UTF-8 to Code Points

The example provided in [lexbor/encoding/single/decode/decode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/decode/decode.c) demonstrates
how to use the `lexbor` library to decode a UTF-8 string into its respective Unicode
code points. This process involves initializing a decoder, processing each character
in the string, and handling the decoding results.

## Key Code Sections

### Buffer Preparation

The example starts by defining the input string in UTF-8 and preparing pointers to
iterate through this string:

```c
const lxb_char_t *data = (const lxb_char_t *) "Привет, мир!";
const lxb_char_t *end = data + strlen((char *) data);
```

Here, `data` points to the start of the UTF-8 encoded string, and `end` points to
the address just after the last character of the string. This setup is essential
for the following decoding process.

### Initializing the Decoder

Next, the example code initializes the decoder for UTF-8:

```c
const lxb_encoding_data_t *encoding;
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

lxb_status_t status = lxb_encoding_decode_init_single(&decode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to init decoder");
}
```

Here, `lxb_encoding_data` retrieves the data structure for the specified encoding.
Then, `lxb_encoding_decode_init_single` initializes the decoding process using
this encoding. The function checks for successful initialization and exits if it
fails.

### Decoding the String

The core decoding loop processes each character in the input string:

```c
while (data < end) {
    pos = data;

    cp = encoding->decode_single(&decode, &data, end);
    if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
        continue;
    }

    printf("%.*s: 0x%04X\n", (int) (data - pos), pos, cp);
}
```

In each iteration of the loop:
- `pos` captures the current pointer position in the string.
- `decode_single` processes the next character, updating `data` to point to the
  next position.
- If `cp` (code point) is valid, it prints the UTF-8 character and its
  corresponding code point.

The loop continues until `data` reaches the `end` of the string, effectively
decoding and printing every character.

## Notes

- The example is hardcoded to decode a specific UTF-8 string (`"Привет, мир!"`).
- The `decode_single` function is used for simplicity, suitable for decoding one
  character at a time.
- Error handling is minimal, assuming that code points will always be valid for
  the given string.

## Summary

This example from [lexbor/encoding/single/decode/decode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/decode/decode.c) demonstrates the basic
process of decoding a UTF-8 encoded string into Unicode code points using the lexbor
library. It initializes the decoder for UTF-8, iterates through the string, and
prints each character with its corresponding Unicode code point. This showcases
the practicality and ease of using the `lexbor` library for encoding-related tasks,
highlighting essential steps like buffer preparation, decoder initialization,
and the decoding process itself.