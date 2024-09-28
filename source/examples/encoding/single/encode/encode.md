# UTF-8 Encoding Example

The source file under discussion is `lexbor/encoding/single/encode/encode.c`. This example demonstrates how to encode a sequence of Unicode code points into a UTF-8 byte string using the `lexbor` library. The example covers the initialization of the encoding process, the encoding of individual Unicode code points, and the final assembly of the encoded string.

## Key Code Sections

### Initialization of Buffer and Encoding Setup

First, the code initializes the buffer and sets up the encoding structure.

```c
lxb_char_t buffer[1024];
lxb_char_t *data = buffer;
const lxb_char_t *end = data + sizeof(buffer);

// Unicode code points for encoding
lxb_codepoint_t cps[] = {0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442, 0x002C,
                         0x0020, 0x043C, 0x0438, 0x0440, 0x0021, 0};

encoding = lxb_encoding_data(LXB_ENCODING_UTF_8);

status = lxb_encoding_encode_init_single(&encode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to init encoder");
}
```
The buffer array serves as a container for the resulting UTF-8 byte string. The Unicode code points for "Привет, мир!" are specified in the `cps` array. The `lxb_encoding_data` function retrieves the encoding data for UTF-8, and `lxb_encoding_encode_init_single` initializes the `encode` structure for single character encoding.

### Encoding Loop

The next portion of the code encodes each Unicode code point and prints the results.

```c
printf("Encode code points to UTF-8 byte string:\n");

for (size_t i = 0; cps[i] != 0; i++) {
    pos = data;

    len = encoding->encode_single(&encode, &data, end, cps[i]);
    if (len < LXB_ENCODING_ENCODE_OK) {
        continue;
    }

    printf("0x%04X: %.*s\n", cps[i], len, pos);
}
```
Within the loop, `pos` stores the current position of `data`. The `encode_single` method encodes each code point into the buffer. `len` will be the number of bytes written, and the encoded representation of each code point is printed in hexadecimal.

### Finalizing the Encoded String

Finally, the code terminates the string and prints the result.

```c
*data = 0x00;

printf("\nResult: %s\n", (char *) buffer);
```
Adding a null terminator `0x00` to the buffer ensures it is a well-formed C string. The full UTF-8 encoded result is then printed.

## Notes

1. **Buffer Initialization**: The buffer's size ensures that it can contain the encoded string, preventing overflow.
2. **Encoder Initialization**: The `lxb_encoding_encode_init_single` function is essential for setting up the encoding process.
3. **Error Handling**: The code handles potential encoding errors, although they are not expected in this specific example.
4. **String Termination**: Proper string termination is necessary for safe string operations in C.

## Summary

This example showcases how to encode Unicode code points into a UTF-8 byte string using the `lexbor` library. It highlights buffer management, the encoding process, and error handling. This is a useful reference for developers needing to perform character encoding tasks with lexbor, demonstrating critical library functions and proper C programming practices.