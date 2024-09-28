# Encode and Validate Unicode Code Points

This article explains the code from the `lexbor` library in the file `lexbor/encoding/single/encode/validate.c`. The example demonstrates how to encode a sequence of Unicode code points into a UTF-8 byte string and handle validation of those points, especially focusing on dealing with invalid Unicode code points.

The example code shows how to use the `lexbor` library to encode an array of Unicode code points into UTF-8. It includes the crucial steps of initializing the encoder, iterating through the Unicode code points, encoding each point, handling errors, replacing invalid code points, and finally, outputting the encoded string.

## Key Code Sections

### Buffer Preparation

The code prepares the buffer that will hold the encoded UTF-8 byte string:

```c
/* Prepare buffer */
lxb_char_t buffer[1024];
lxb_char_t *data = buffer;
const lxb_char_t *end = data + sizeof(buffer);
```

Here, `buffer` is a fixed-size array where the encoded UTF-8 data will be stored. `data` is a pointer that will be adjusted as data is written into the buffer, and `end` marks the endpoint of the buffer to prevent overflow.

### Defining Unicode Code Points

A set of Unicode code points, including an invalid one, is defined for encoding:

```c
/* Unicode code points for encoding */
lxb_codepoint_t cps[] = {0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442,
                         0x002C, 
                         0x110000, /* <-- bad code point */
                         0x0020, 0x043C, 0x0438, 0x0440, 0x0021, 0};
```

This array includes a mix of valid Unicode code points and an intentionally invalid code point (`0x110000`). The `0` at the end signifies the end of the array.

### Initialize Encoder

An encoder for the UTF-8 encoding is initialized:

```c
encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

status = lxb_encoding_encode_init_single(&encode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to init encoder");
}
```

The `lxb_encoding_data` function fetches the encoding data structure for UTF-8, and `lxb_encoding_encode_init_single` initializes the single-byte encoder context. An error check ensures that the encoder was initialized successfully.

### Encoding and Validation

The code iterates over the Unicode code points array to validate and encode each point:

```c
for (size_t i = 0; cps[i] != 0; i++) {
    pos = data;

    len = encoding->encode_single(&encode, &data, end, cps[i]);

    if (len < LXB_ENCODING_ENCODE_OK) {
        if (len == LXB_ENCODING_ENCODE_SMALL_BUFFER) {
            break;
        }

        printf("Bad code point: 0x%04X; Replaced to: %s (0x%04X)\n",
               cps[i], LXB_ENCODING_REPLACEMENT_BYTES,
               LXB_ENCODING_REPLACEMENT_CODEPOINT);

        memcpy(data, LXB_ENCODING_REPLACEMENT_BYTES,
               LXB_ENCODING_REPLACEMENT_SIZE);

        data += LXB_ENCODING_REPLACEMENT_SIZE;

        continue;
    }

    printf("0x%04X: %.*s\n", cps[i], len, pos);
}
```

For each code point:

1. `pos` marks the initial position in the buffer.
2. `encoding->encode_single` attempts to encode the current code point.
3. If the return value `len` indicates an error:
    - It checks if the buffer is too small (the code handles it theoretically, though it never occurs here due to enough buffer space).
    - For invalid code points, it replaces them with a predefined replacement character (commonly `0xFFFD` in UTF-8).
4. If the encoding is successful, `len` specifies the number of bytes written.

### Final Output

The result is terminated with a null character and printed:

```c
/* Terminate string */
*data = 0x00;

printf("\nResult: %s\n", (char *) buffer);
```

This step ensures the buffer is a valid C string and outputs the final encoded string.

## Notes

- The example uses `lexbor`'s encoding library for UTF-8 encoding.
- Error handling is implemented to manage invalid Unicode code points.
- The buffer is large enough to handle the encoded output, avoiding buffer overflow concerns in this context.

## Summary

This example demonstrates the usage of the `lexbor` library for encoding Unicode code points into UTF-8, handling errors gracefully, and replacing invalid code points. It highlights lexbor's flexibility and robustness in dealing with text encoding tasks, proving indispensable for applications needing precise control over encoding processes. By understanding this example, developers can leverage lexbor's capabilities for their encoding needs, ensuring correct handling and encoding of text data.