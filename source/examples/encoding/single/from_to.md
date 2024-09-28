# Text Conversion Through Custom Encodings

This article will provide an in-depth explanation of the `lexbor/encoding/single/from_to.c`
example file. The intent of this example is to demonstrate how the `lexbor` library can be
used to read input text in one character encoding, decode it, and then encode it to another
character encoding before writing it out. The article will break down the important sections
of the code, explain the functionality provided by the `lexbor` library, and present
key insights for potential users.

The example code uses the `lexbor` library to
create a program that reads text input in one encoding, decodes it to a universal codepoint
representation, and re-encodes it to a different encoding before outputting it. This process
involves setting up encoding and decoding specifications, handling I/O efficiently, and
managing edge cases in encoding conversion.

## Key Code Sections

### Command-Line Argument Processing

The program begins by checking if the correct number of command-line arguments are provided,
which represent the 'from' and 'to' encodings.

```c
if (argc != 3) {
    usage();
    exit(EXIT_SUCCESS);
}

/* Get encoding data for 'from' */
from = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1], strlen(argv[1]));
if (from == NULL) {
    FAILED(true, "Failed to get encoding from name: %s", argv[1]);
}

/* Get encoding data for 'to' */
to = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[2], strlen(argv[2]));
if (to == NULL) {
    FAILED(true, "Failed to get encoding from name: %s", argv[2]);
}
```

Here, the `lxb_encoding_data_by_pre_name` function retrieves the encoding data based on the
provided name. If the encoding data cannot be found, the program exits with an error.

#### Initializing Encoders and Decoders

The code initializes the encoding and decoding structures provided by the `lexbor` library.

```c
status = lxb_encoding_encode_init_single(&encode, to);
if (status != LXB_STATUS_OK) {
    FAILED(true, "Failed to init encoder");
}

status = lxb_encoding_decode_init_single(&decode, from);
if (status != LXB_STATUS_OK) {
    FAILED(true, "Failed to init decoder");
}
```

The `lxb_encoding_encode_init_single` and `lxb_encoding_decode_init_single` functions prepare
the encoder and decoder for the specified encodings. Handling their status ensures proper
resource initialization before processing input.

### Reading and Processing Input Data

The core logic of reading input data, decoding it, transforming it to a codepoint and re-encoding
is encapsulated in a loop that handles data in chunks.

```c
do {
    /* Read standard input */
    read_size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (read_size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        }
        else {
            FAILED(false, "Failed to read stdin");
        }
    }

    /* Decode incoming data */
    data = (const lxb_char_t *) inbuf;
    end = data + read_size;

    while (data < end) {
        /* Decode */
        cp = from->decode_single(&decode, &data, end);
        if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
            if (cp == LXB_ENCODING_DECODE_CONTINUE && loop) {
                break;
            }
            cp = LXB_ENCODING_REPLACEMENT_CODEPOINT;
        }

        /* Encode */
        out = outbuf;
        len = to->encode_single(&encode, &out, out_end, cp);
        if (len < LXB_ENCODING_ENCODE_OK) {
            printf("?");
            continue;
        }
        
        if (fwrite(outbuf, 1, len, stdout) != len) {
            FAILED(false, "Failed to write data to stdout");
        }
    }
}
while (loop);
```

The input is read in chunks of 4096 bytes, decoded character by character to codepoints, and
then re-encoded using the target encoding. Any decoding errors result in a replacement codepoint
being used, while encoding errors default to printing a question mark (`?`).

### Finalizing Encoding and Decoding

Finally, the program ensures that any remaining buffer data is handled by finalizing the
decoding and encoding processes.

```c
status = lxb_encoding_decode_finish_single(&decode);
if (status != LXB_STATUS_OK) {
    printf("?");
}

out = outbuf;
len = lxb_encoding_encode_finish_single(&encode, &out, out_end);
if (len != 0) {
    if (fwrite(outbuf, 1, len, stdout) != len) {
        FAILED(false, "Failed to write data to stdout");
    }
}
```

These steps ensure that any buffered data is properly flushed out before program termination.

## Notes

1. The program supports a wide range of encodings, making it a versatile tool for encoding conversion.
2. Error handling and edge cases are managed to ensure the program does not crash on unexpected input.
3. The `lexbor` library provides comprehensive functions for encoding and decoding, making such
   conversions straightforward.

## Summary

This example highlights how the `lexbor` library can be used to build a robust encoding conversion
tool. The key takeaways include understanding how to initialize encoding and decoding structures,
process input data efficiently, handle error cases gracefully, and ensure that conversions
are completed correctly before program exit. Such an understanding can facilitate building
more sophisticated text processing tools using the `lexbor` library.