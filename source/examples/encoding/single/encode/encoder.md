# Encoding Input Data Example

This article explains the purpose and functionality of the `encoder.c` source file located in the `lexbor/encoding/single/encode` directory. The code provides a utility for encoding text input based on a specified character encoding scheme. It reads data from standard input (stdin), decodes any escaped code points in the input, and encodes the results according to the selected encoding. 

## Key Components

### Header and Macros

The file begins with some header information including copyright and the author's details. Following this, necessary includes and definitions are placed. The macro `FAILED` is defined to handle error reporting and exit when a critical failure occurs. This block of code succinctly prints an error message, displays usage instructions if required, and terminates the program:

```c
#define FAILED(with_usage, ...)                                                \
    do {                                                                       \
        fprintf(stderr, __VA_ARGS__);                                          \
        fprintf(stderr, "\n");                                                 \
        if (with_usage) {                                                      \
            usage();                                                           \
        }                                                                      \
        exit(EXIT_FAILURE);                                                    \
    }                                                                          \
    while (0)
```

### Usage Function

The `usage` function outputs the required command-line usage for the program, listing all of the available encodings such as `UTF-8`, `ISO-8859-1`, and `SHIFT-JIS`. This function is invoked if the user does not supply the required arguments.

```c
static void usage(void) {
    printf("Usage: encoder <encoding name>\n\n");
    // List of available encodings...
}
```

### Escaped Code Point Conversion

The function `escaped_to_codepoint` is responsible for converting escaped Unicode sequences to their corresponding code points. The function processes the input data character by character, identifying whether the sequence starts with a backslash, and checking for either hexadecimal (`\x`) or Unicode (`\u`) formats. If an incorrectly formatted escape sequence is detected, an error state is triggered prompting the program to exit:

```c
static const lxb_char_t *escaped_to_codepoint(const lxb_char_t *data, const lxb_char_t *end,
                     lxb_codepoint_t *cp, int8_t *state)
{
    // Processing logic...
    if (*data != '\\') {
        goto failed;  // Handle invalid start of escape sequence
    }
    // More processing...
}
```

### Main Functionality

The `main` function orchestrates the entire encoding process:

1. **Argument Handling**: It requires one argument indicating the desired encoding.
2. **Encoding Setup**: It retrieves the encoding configuration using the provided argument and initializes the encoder.
3. **Input Loop**: The program enters a loop where it reads input data from stdin, processes it into code points, and then encodes these points:
   
   ```c
   while (data < end) {
       data = escaped_to_codepoint(data, end, &cp, &state);
       // Encoding logic...
   }
   ```

4. **Output Handling**: The encoded output is written to stdout. If the encoding is `UTF-8`, replacement bytes are used as necessary.

Overall, the program is designed to robustly handle input encoding, managing possible errors during reading and writing, and validating formats. The use of the `lexbor` library enables effective encoding management, providing a variety of supported character encodings.

In conclusion, the `encoder.c` file serves as a practical example of encoding conversion using a command-line utility, highlighting important coding principles, such as error handling, input/output operations, and state management within the context of encoding mechanisms.