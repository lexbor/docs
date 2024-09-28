# Encoding Data Retrieval Example

This article provides an explanation of an example from the file [lexbor/encoding/data_by_name.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/data_by_name.c). The purpose of this code is to demonstrate how to retrieve encoding data by its name using the Lexbor encoding library. The code illustrated here highlights the procedure for accessing character encoding information, specifically focusing on UTF-8.

## Code Explanation

The program starts with the necessary `#include` directive, which includes the Lexbor encoding library header file. This library provides the functionality needed to work with different character encodings.

### Main Function

The `main` function serves as the entry point of the program:

```c
int main(int argc, const char *argv[])
```

Here, it accepts two parameters: the argument count `argc` and an array of argument strings `argv`. Although the parameters are not utilized in this example, they are typically included for potential command-line functionality.

### Retrieving Encoding Data

The key operation occurs in the following block:

```c
const lxb_encoding_data_t *enc_data;
enc_data = lxb_encoding_data_by_name((lxb_char_t *) "uTf-8", 5);
```

In this segment, the variable `enc_data` is declared as a pointer to `lxb_encoding_data_t`, which represents the encoding data structure in Lexbor. The function `lxb_encoding_data_by_name` is called with two arguments: the string "uTf-8" (with a deliberate mixed case) and the length of the string, which is `5`.

This function attempts to retrieve encoding data corresponding to the specified name. If the name provided does not match any available encoding in the library, the function will return `NULL`.

### Error Handling

The next block of code provides basic error handling:

```c
if (enc_data == NULL) {
    return EXIT_FAILURE;
}
```

If `enc_data` is `NULL`, the program terminates with a failure status. This is an important check to ensure that the encoding has been found before attempting to access any of its properties, thus preventing potential runtime errors.

### Output Encoding Name

Upon successful retrieval of the encoding data, the program proceeds to print the name of the encoding:

```c
printf("%s\n", enc_data->name);
```

This line outputs the name of the encoding that has been retrieved, which in this case would be "UTF-8", assuming the spelling was correct in the function call.

### Exit Status

Finally, the program completes its execution successfully:

```c
return EXIT_SUCCESS;
```

This line returns a success status to the operating system, indicating that the program has run without any issues.

## Conclusion

The example presented in [lexbor/encoding/data_by_name.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/data_by_name.c) effectively demonstrates how to access encoding data using the Lexbor encoding library. It showcases the importance of error handling and provides a simple way to retrieve and display the name of a character encoding, using UTF-8 as a practical example. This code can serve as a foundational component for applications that require encoding information for text processing.