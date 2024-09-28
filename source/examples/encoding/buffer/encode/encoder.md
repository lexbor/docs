# Encoding Data with Escaped Sequences: Example

In this example, found in the file `lexbor/encoding/buffer/encode/encoder.c`, we delve into an implementation that reads input data, processes any escaped sequences, and encodes the data using the specified character encoding. The purpose of this code is to demonstrate how the `lexbor` library can be used to handle textual data with escaped sequences and convert it to various encodings. This write-up explains key parts of the program, focusing on the logic and usage of `lexbor` functions.

## Key Code Sections

### Command Line Arguments Handling

The program starts with a basic check for command line arguments, where it expects exactly one argument specifying the desired encoding.

```c
if (argc != 2) {
    usage();
    exit(EXIT_SUCCESS);
}
```

This section ensures that the user provides an encoding name, and if not, it shows usage instructions and exits.

### Fetching and Initializing Encoding

The encoding is determined from the user-provided argument, and the encoder is initialized accordingly.

```c
encoding = lxb_encoding_data_by_pre_name((const lxb_char_t *) argv[1], strlen(argv[1]));
if (encoding == NULL) {
    FAILED(true, "Failed to get encoding from name: %s\n", argv[1]);
}

status = lxb_encoding_encode_init(&encode, encoding, outbuf, sizeof(outbuf));
if (status != Lxb_STATUS_OK) {
    FAILED(false, "Failed to initialize encoder");
}
```

Here, `lxb_encoding_data_by_pre_name` retrieves the encoding data, and `lxb_encoding_encode_init` initializes the encoding context.

### Setting Replacement Bytes for Encoder

Depending on the encoding specified, replacement bytes are set. This is crucial for handling invalid or unencodable sequences.

```c
if (encoding->encoding == Lxb_ENCODING_UTF_8) {
    status = lxb_encoding_encode_replace_set(&encode, LXB_ENCODING_REPLACEMENT_BYTES, LXB_ENCODING_REPLACEMENT_SIZE);
}
else {
    status = lxb_encoding_encode_replace_set(&encode, (lxb_char_t *) "?", 1);
}

if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to set replacement bytes for encoder");
}
```

UTF-8 has specific replacement bytes, while other encodings use a generic question mark.

### Processing Input Data

The program reads data from standard input in chunks of 4096 bytes, processes each chunk, and converts it into code points.

```c
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
cp_end = escaped_to_codepoint(data, end, cp, &state, &cp_rep, loop == false);
```

This part handles reading input, processes potential partial reads due to end-of-file, and calls the `escaped_to_codepoint` function to process the escaped sequences into code points.

### Encoding and Output

After converting to code points, the data is encoded and written to standard output.

```c
do {
    status = encoding->encode(&encode, &cp_ref, cp_end);
    read_size = lxb_encoding_encode_buf_used(&encode);

    if (fwrite(outbuf, 1, read_size, stdout) != read_size) {
        FAILED(false, "Failed to write data to stdout");
    }

    lxb_encoding_encode_buf_used_set(&encode, 0);
}
while (status == LXB_STATUS_SMALL_BUFFER);
```

This loop ensures that all data is properly encoded and outputted, even handling cases where the buffer might be too small on the first pass.

### Finalizing Encoding

At the end of processing, the encoder is finalized to flush any remaining data.

```c
(void) lxb_encoding_encode_finish(&encode);

read_size = lxb_encoding_encode_buf_used(&encode);
if (read_size != 0) {
    if (fwrite(outbuf, 1, read_size, stdout) != read_size) {
        FAILED(false, "Failed to write data to stdout");
    }
}
```

This ensures that any leftover data in the encoder’s internal buffer is written out.

## Notes

1. **Error Handling**: The macro `FAILED` helps in providing consistent error messages and exits on failure.
2. **Escaped Sequence Processing**: The function `escaped_to_codepoint` is crucial for converting escaped sequences like `\xNN` and `\uNNNN` into code points.
3. **Buffer Management**: Proper buffer management ensures that encoding processes can handle partial reads and writes effectively.

## Summary

This example demonstrates how to use the `lexbor` library to handle input data with escaped sequences, converting it to the specified encoding. It showcases the critical steps for initializing encoders, processing input data, handling partial reads, and finalizing output. Understanding this example is essential for those looking to leverage `lexbor` for complex text encoding tasks in their applications.