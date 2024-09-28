# UTF-8 Encoding Example

This article explains the purpose and functionality of the UTF-8 encoding example provided in the file [lexbor/encoding/single/encode/encode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/encoding/single/encode/encode.c). The code demonstrates how to encode a series of Unicode code points into a UTF-8 byte string using the Lexbor encoding library. 

## Code Overview

The program begins by including the necessary header file for the Lexbor encoding library. It defines a macro for error handling named `FAILED`, which simplifies printing error messages and terminating the program if initialization or execution fails.

### Main Function Structure

The `main` function serves as the entry point of the program. It declares several variables needed for encoding, including a buffer for the output and an encoder instance. The following key steps are involved in the encoding process:

1. **Buffer Preparation**:
   A buffer of 1024 bytes is allocated to hold the UTF-8 encoded string. The variables `data` and `end` are set to track the start and the end of the buffer.

2. **Unicode Code Points**:
   An array of Unicode code points is defined and terminated with a zero. These code points (e.g., Cyrillic characters for "Привет, мир!") are the values that will be encoded.

3. **Encoding Initialization**:
   The function `lxb_encoding_data` retrieves the encoding data for UTF-8, which is passed to `lxb_encoding_encode_init_single` to initialize the encoder. If the initialization fails, the `FAILED` macro is invoked to handle the error.

4. **Encoding Loop**:
   The program enters a loop where each code point is processed for encoding:
   - The current position in the buffer (`pos`) is saved.
   - The encoder's `encode_single` function is called to perform the encoding. The length of the encoded output is returned.
   - If the encoding operation is successful, the resulting UTF-8 bytes are printed alongside their corresponding Unicode code point in hexadecimal format.

5. **String Termination**:
   After processing all code points, the buffer is null-terminated to ensure it is properly formatted as a C string.

6. **Output Display**:
   Finally, the UTF-8 encoded string is printed to the console, demonstrating the successful encoding of the provided Unicode code points.

## Conclusion

Upon reaching the end of the program, it exits gracefully, indicating successful execution. This example illustrates how to use the Lexbor encoding library for converting Unicode code points to a UTF-8 encoded string, providing a clear and practical implementation of encoding functionality in C using Lexbor.