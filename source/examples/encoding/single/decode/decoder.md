# Encoding Text Data with `lexbor`

The example source file [lexbor/encoding/single/decode/decoder.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/decode/decoder.c) provides an in-depth look at using the `lexbor` library to decode text data from various character encodings. The primary intent of this example is to demonstrate how to initialize a decoding context, read data from standard input, and correctly handle the decoding process using the `lexbor` library. This example targets developers aiming to understand the library's capabilities for text decoding and error handling.

## Key Code Sections

### Command-Line Argument Parsing and Usage

The program begins by checking if the correct number of command-line arguments is provided. If not, it displays the usage information and exits.

```c
if (argc != 2) {
    usage();
    exit(EXIT_SUCCESS);
}
```

The `usage` function prints the expected usage of the program, including the list of supported encodings. This helps users understand how to properly invoke the decoder and which encodings are available.

### Encoding Initialization

The encoding provided by the user as a command-line argument is determined using the `lxb_encoding_data_by_pre_name` function.

```c
encoding = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1], strlen(argv[1]));
if (encoding == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n\n", argv[1]);
}

status = lxb_encoding_decode_init_single(&decode, encoding);
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to init decoder");
}
```

Here, the program retrieves the encoding data associated with the user-provided name. If the encoding is invalid, the program exits with an error message. Once the encoding data is obtained, it initializes the decoder object with `lxb_encoding_decode_init_single`. Proper initialization is crucial for subsequently processing the incoming data.

### Reading from Standard Input

The main decoding loop reads data from standard input in blocks and decodes them using the initialized decoder.

```c
do {
    read_size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (read_size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        }
        else {
            FAILED(false, "Failed to read stdin");
        }
    }
     
    data = (const lxb_char_t *) inbuf;
    end = data + read_size;
    
    // Decoding happens here
} while (loop);
```

The input data is read in chunks and processed in a loop. The `fread()` function reads up to `sizeof(inbuf)` bytes from the standard input. If the read size is different (and the end of the file is not reached), it indicates an error.

### Decoding Loop

Inside the decoding loop, the program calls the decoder's `decode_single` method to decode individual characters.

```c
while (data < end) {
    cp = encoding->decode_single(&decode, &data, end);
    if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
        if (cp == LXB_ENCODING_DECODE_CONTINUE) {
            break;
        }
        printf("\\u%04X", LXB_ENCODING_REPLACEMENT_CODEPOINT);
        continue;
    }

    if (cp >= 0x00A0) {
        printf("\\u%04X", cp);
    }
    else {
        printf("\\x%02X", cp);
    }
}
```

Here, `decode_single` decodes characters from the input buffer and manages input pointer `data`. Special handling is implemented for cases when the code point indicates a continuation (`LXB_ENCODING_DECODE_CONTINUE`) or an invalid character. Valid Unicode characters are printed in `\u` format, while ASCII characters are printed in `\x` format.

### Handling Remaining Unfinished Decodings

After the loop, if there's an indication that decoding was incomplete (i.e., if `cp` equals `LXB_ENCODING_DECODE_CONTINUE`), the program outputs a Unicode replacement character.

```c
if (cp == LXB_ENCODING_DECODE_CONTINUE) {
    printf("\\u%04X", LXB_ENCODING_REPLACEMENT_CODEPOINT);
}
```

This ensures that any unfinished multi-byte sequences are handled gracefully.

## Notes

1. **Error Handling**: The macro `FAILED` is used extensively to simplify error messages and includes conditional usage guidance.
2. **Buffer Management**: The program efficiently manages input data using a fixed-size buffer, ensuring that large input streams are handled correctly.
3. **Decoding Logic**: The implementation highlights robust decoding logic that appropriately handles different character encoding cases, including Unicode and ASCII conversions.

## Summary

This decoding example from the `lexbor` library demonstrates essential techniques for initializing encoding contexts, reading and decoding text data, and handling various edge cases. Being equipped with such knowledge allows developers to leverage `lexbor` for efficient and accurate character encoding transformation tasks across different applications.