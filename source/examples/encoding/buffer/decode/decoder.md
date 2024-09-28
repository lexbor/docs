# Lexbor Encoding Decoder

This article delves into the purpose and functionality of the code from the file [lexbor/encoding/buffer/decode/decoder.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/decode/decoder.c). The example demonstrates how to utilize the `lexbor` library to decode text from various encodings, converting it to Unicode code points. We'll explore key sections of the code to understand how it achieves this.

## Key Code Sections

### Initialization and Argument Handling

The code begins by checking command-line arguments to ensure an encoding name is provided and initializing necessary components.

```c
if (argc != 2) {
    usage();
    exit(EXIT_SUCCESS);
}

/* Determine encoding from first argument from command line */
encoding = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1], strlen(argv[1]));
if (encoding == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n\n", argv[1]);
}
```

Here, `argc` is checked to guarantee exactly one argument is provided. The `usage()` function outputs how to use the program if the condition isn't met. The `lxb_encoding_data_by_pre_name()` function fetches encoding data based on the provided encoding name. If the encoding cannot be found, `FAILED()` is called to print an error and exit.

### Decoder Initialization

Next, the decoder is initialized with the specified encoding and a buffer for storing code points:

```c
status = lxb_encoding_decode_init(&decode, encoding, cp, sizeof(cp) / sizeof(lxb_codepoint_t));
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to initialization decoder");
}

status = lxb_encoding_decode_replace_set(&decode, LXB_ENCODING_REPLACEMENT_BUFFER, LXB_ENCODING_REPLACEMENT_BUFFER_LEN);
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to set replacement code points for decoder");
}
```

The `lxb_encoding_decode_init()` function initializes the decoder, and `lxb_encoding_decode_replace_set()` sets replacement code points to handle invalid sequences during decoding. Both functions return a status code that must be checked to prevent further errors.

### Reading and Decoding Input

The core of the example is a loop that reads from `stdin` and decodes the data:

```c
do {
    /* Read standard input */
    read_size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (read_size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        } else {
            FAILED(false, "Failed to read stdin");
        }
    }

    /* Decode incoming data */
    data = (const lxb_char_t *) inbuf;
    end = data + read_size;

    do {
        status = encoding->decode(&decode, &data, end);

        buf_length = lxb_encoding_decode_buf_used(&decode);

        for (size_t i = 0; i < buf_length; i++) {
            if (cp[i] >= 0x00A0) {
                /* Code point is Unicode */
                printf("\\u%04X", cp[i]);
            } else {
                /* Code point is ASCII */
                printf("\\x%02X", cp[i]);
            }
        }

        lxb_encoding_decode_buf_used_set(&decode, 0);
    } while (status == LXB_STATUS_SMALL_BUFFER);
} while (loop);
```

This section reads input into `inbuf` and updates the decoder with `encoding->decode()`. It processes the buffer in chunks, printing converted code points as either Unicode or ASCII, depending on their values. The `lxb_encoding_decode_buf_used()` function returns the number of decoded code points, and this information is used to print the decoded values.

### Finishing the Decoding Process

Finally, after all input has been processed, the decoder flushes any remaining code points:

```c
(void) lxb_encoding_decode_finish(&decode);

/*
 * We need to check the out buffer after calling the finish function.
 * If there was not enough data to form a code point, then the finish
 * function will add the replacement character to the out buffer.
 */
buf_length = lxb_encoding_decode_buf_used(&decode);

if (buf_length != 0) {
    for (size_t i = 0; i < buf_length; i++) {
        if (cp[i] >= 0x00A0) {
            printf("\\u%04X", cp[i]);
        } else {
            printf("\\x%02X", cp[i]);
        }
    }
}
```

The `lxb_encoding_decode_finish()` function ensures all data is processed, adding replacement characters if necessary. The remaining code points are then printed similarly to the earlier steps.

## Notes

- **Error Handling**: The use of the `FAILED()` macro ensures graceful termination upon encountering errors.
- **Encoding Support**: The `usage()` function lists the supported encodings that the program can handle.
- **Buffer Management**: Adequate handling of input and decoding buffers is critical for managing memory and ensuring correct decoding.

## Summary

This example demonstrates how to use the `lexbor` library for decoding text from various encodings to Unicode code points. Key aspects include initializing the decoder, reading input in manageable chunks, handling errors gracefully, and ensuring all data is processed. Understanding this example is valuable for leveraging `lexbor` in applications requiring robust text encoding handling.