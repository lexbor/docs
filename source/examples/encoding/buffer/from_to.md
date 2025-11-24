# Character Encoding Conversion

This document explains the [lexbor/encoding/buffer/from_to.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/buffer/from_to.c) file in the `lexbor` library, which demonstrates how to read input data, decode it using one encoding, and then encode it with another encoding. This example highlights core functionalities of lexbor's encoding module.

## Key Code Sections

### Encoding Data Initialization

The program starts by verifying the command-line arguments and retrieving the corresponding encoding data for the given `from` and `to` encodings. The `lxb_encoding_data_by_pre_name` function retrieves the encoding data by its name.

```c
if (argc != 3) {
    usage();
    exit(EXIT_SUCCESS);
}

/* Get encoding data for 'from' */
from = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1],
                                     strlen(argv[1]));
if (from == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n", argv[1]);
}

/* Get encoding data for 'to' */
to = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[2],
                                   strlen(argv[2]));
if (to == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n", argv[2]);
}
```

The `from` and `to` variables store the encoding data retrieved based on the user's input. If the encoding names provided are invalid, the program exits with an error message.

### Decoder and Encoder Initialization

Next, the code initializes the decode and encode contexts using the retrieved encoding data.

```c
/* Initialization decode */
status = lxb_encoding_decode_init(&decode, from, cp,
                                  sizeof(cp) / sizeof(lxb_codepoint_t));
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to initialization decoder");
}

status = lxb_encoding_decode_replace_set(&decode,
      LXB_ENCODING_REPLACEMENT_BUFFER, LXB_ENCODING_REPLACEMENT_BUFFER_LEN);
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to set replacement code point for decoder");
}

/* Initialization encode */
status = lxb_encoding_encode_init(&encode, to, outbuf, sizeof(outbuf));
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to initialization encoder");
}

if (to->encoding == LXB_ENCODING_UTF_8) {
    status = lxb_encoding_encode_replace_set(&encode,
             LXB_ENCODING_REPLACEMENT_BYTES, LXB_ENCODING_REPLACEMENT_SIZE);
}
else {
    status = lxb_encoding_encode_replace_set(&encode, (lxb_char_t *) "?", 1);
}

if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to set replacement bytes for encoder");
}
```

The `lxb_encoding_decode_init` and `lxb_encoding_encode_init` functions initialize the decoder and encoder contexts, respectively. The replacements are set to handle invalid sequences during decoding and encoding.

### Data Decoding and Encoding Loop

The core of the program reads data from standard input, decodes it, and then encodes the resulting code points using the specified encoding.

```c
do {
    /* Read standard input */
    size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        }
        else {
            FAILED(false, "Failed to read stdin");
        }
    }

    /* Decode incoming data */
    data = (const lxb_char_t *) inbuf;
    end = data + size;

    do {
        /* Decode */
        decode_status = from->decode(&decode, &data, end);

        cp_ref = cp;
        cp_end = cp + lxb_encoding_decode_buf_used(&decode);

        do {
            encode_status = to->encode(&encode, &cp_ref, cp_end);
            if (encode_status == LXB_STATUS_ERROR) {
                cp_ref++;
                encode_status = LXB_STATUS_SMALL_BUFFER;
            }

            size = lxb_encoding_encode_buf_used(&encode);

            /* The printf function cannot print \x00, it can be in UTF-16 */
            if (fwrite(outbuf, 1, size, stdout) != size) {
                FAILED(false, "Failed to write data to stdout");
            }

            lxb_encoding_encode_buf_used_set(&encode, 0);
        }
        while (encode_status == LXB_STATUS_SMALL_BUFFER);

        lxb_encoding_decode_buf_used_set(&decode, 0);
    }
    while (decode_status == LXB_STATUS_SMALL_BUFFER);
}
while (loop);
```

This segment reads the input in chunks, decodes each chunk, and encodes the result. The loop handles the possibility that the buffers might be too small to hold the decoded or encoded data entirely at once.

### Finalization of Decoding and Encoding

After the input is fully processed, the program finalizes the decoding and encoding operations to ensure all data is correctly handled.

```c
/* End of file */
/* In this moment encoder and decoder out buffer is empty */

/* First: finish decoding */
(void) lxb_encoding_decode_finish(&decode);

if (lxb_encoding_decode_buf_used(&decode)) {
    cp_ref = cp;
    cp_end = cp + lxb_encoding_decode_buf_used(&decode);

    (void) to->encode(&encode, &cp_ref, cp_end);
    size = lxb_encoding_encode_buf_used(&encode);

    if (fwrite(outbuf, 1, size, stdout) != size) {
        FAILED(false, "Failed to write data to stdout");
    }
}

/* Second: finish encoding */
(void) lxb_encoding_encode_finish(&encode);
size = lxb_encoding_encode_buf_used(&encode);

if (size != 0) {
    if (fwrite(outbuf, 1, size, stdout) != size) {
        FAILED(false, "Failed to write data to stdout");
    }
}
```

The `lxb_encoding_decode_finish` and `lxb_encoding_encode_finish` functions ensure that any remaining data in the buffers is processed and outputted.

## Notes

- It is crucial to handle buffer sizes and potential overflows carefully to avoid data loss.
- Setting replacement characters or byte sequences helps manage invalid encoding sequences gracefully.
- Properly finalizing decoding and encoding processes ensures that all input data is correctly processed.

## Summary

This example illustrates how to use the `lexbor` library to convert data between different character encodings. It handles reading from standard input, decoding using one encoding, and then encoding to another, while managing buffer sizes and invalid sequences. Understanding this code helps users leverage lexbor's powerful encoding functionalities in their own applications.