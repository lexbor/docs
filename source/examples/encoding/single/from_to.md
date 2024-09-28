# Encoding Conversion Example

This article explains the encoding conversion functionality provided in the
source file
[lexbor/encoding/single/from_to.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/from_to.c).
The code allows users to convert text from one character encoding to another via
command-line input. It demonstrates how to utilize the `lexbor` encoding library
for encoding and decoding different formats of character sets.

## Overview

The main function in this code receives two command-line arguments representing
the source (`from`) and target (`to`) encodings. It reads input data from
standard input, decodes it from the specified `from` encoding to Unicode code
points, and then encodes those code points into the specified `to` encoding
before writing the output to standard output.

## Code Breakdown

### Definitions and Includes

At the beginning of the file, we include the necessary header for the `lexbor`
encoding module:

```c
#include <lexbor/encoding/encoding.h>
```

This allows us access to various functions and types defined in the library,
which facilitate character encoding tasks.

### Failure Handling Macro

The `FAILED` macro is defined for error handling throughout the code:

```c
#define FAILED(with_usage, ...) ...
```

This macro simplifies error reporting by printing error messages to standard
error and conditionally calling the `usage` function to display usage
instructions before terminating the program. Adopting this macro ensures a
consistent approach to error handling across the code.

### Usage Function

The `usage` function provides instructions on how to use the encoding conversion
tool:

```c
static void usage(void) { ... }
```

It lists the accepted input encodings that users can specify when executing the
program. This function is crucial for user guidance, ensuring that they know the
correct format for command inputs.

### Main Function

The `main` function orchestrates the overall process:

```c
int main(int argc, const char *argv[]) { ... }
```

1. **Argument Count Check**: The function starts by checking if the user
   provided exactly two arguments (the source and target encodings). If not, the
   `usage` function is called, and the program exits.

2. **Encoding Data Retrieval**: The code fetches the encoding information for
   both the source and target encodings using the
   `lxb_encoding_data_by_pre_name` function:

   ```c
   from = lxb_encoding_data_by_pre_name(...);
   to = lxb_encoding_data_by_pre_name(...);
   ```

   If either retrieval fails, the `FAILED` macro is triggered, stopping
   execution.

3. **Initialization of Encoder and Decoder**: The encoder and decoder are
   initialized with the retrieved encoding data:

   ```c
   status = lxb_encoding_encode_init_single(&encode, to);
   status = lxb_encoding_decode_init_single(&decode, from);
   ```

   These initializations set up the necessary state for encoding and decoding
   operations.

### Input Reading and Processing Loop

The program enters a loop where it continuously reads from standard input until
EOF (End Of File) is reached:

```c
do {
    read_size = fread(inbuf, 1, sizeof(inbuf), stdin);
    ...
} while (loop);
```

Within the loop:

- The fetched data is decoded using the `from` encoder to obtain Unicode code
  points.

- For each code point decoded, it is then encoded with the `to` encoder and
  written to standard output.

### Finalization

After processing all input data, the code finalizes the decoder and encoder:

```c
status = lxb_encoding_decode_finish_single(&decode);
len = lxb_encoding_encode_finish_single(&encode, &out, out_end);
```

These finalization steps ensure that any remaining data is processed and that
resources are cleaned up properly before the program exits.

## Conclusion

The `from_to.c` example illustrates a practical approach to character encoding
conversion using the `lexbor` encoding library. It showcases error handling, user
guidance, and processing loops, making it a valuable reference for developers
needing to handle various text encodings in their applications. This example
emphasizes the importance of robust input handling and clean output generation
within character encoding operations.