# Unicode Normalization Example

This article explains the example code found in the file [lexbor/unicode/normalization_form.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/unicode/normalization_form.c). The program demonstrates how to perform Unicode normalization using the Lexbor library, specifically focusing on four normalization forms: NFC, NFD, NFKC, and NFKD. 

## Introduction

The code begins by including the necessary headers for Unicode functionality and encoding. It defines a Unicode string, `"ẛ̣"`, which consists of the code points `U+1E9B` (LATIN SMALL LETTER S WITH DOT ABOVE) and `U+0323` (COMBINING DOT BELOW). The program aims to normalize this string and print the results of each normalization form.

## Main Function

The `main` function is the entry point of the program. Here, a `lxb_unicode_normalizer_t` object is created with the function `lxb_unicode_normalizer_create()`. This object will be used to perform the normalization forms. The initialization of this object specifies the normalization form to use, starting with NFC (Normalization Form C).

### Initialization

After the Unicode normalizer object is successfully created, it is initialized with NFC:

```c
status = lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);
```

If the initialization fails (`status != LXB_STATUS_OK`), an error message is printed, and the program exits with a failure status. Similar checks are made after each normalization operation to handle potential errors.

## Normalization Operations

The code proceeds through each normalization form: NFC, NFD, NFKC, and NFKD. In each case, the following steps are performed:

1. Set the desired normalization form using `lxb_unicode_normalization_form_set(uc, ...)`.
2. Call `lxb_unicode_normalize(...)` to perform the normalization, passing the source string, its length, a callback function to handle the result, the name of the normalization form, and a boolean indicating whether the function should show its results.

For instance, the NFC normalization is conducted as follows:

```c
status = lxb_unicode_normalize(uc, source, sizeof(source) - 1, callback, "NFC", true);
```

Each normalization form will produce a different output, reflecting how the Unicode string is represented under various normalization rules. The callback function processes the normalized output.

## Callback Function

The `callback` function accepts the normalized data, its length, and a context string (the name of the normalization form). Inside this function, the received data is processed to decode valid UTF-8 sequences. It utilizes the Lexbor function `lxb_encoding_decode_valid_utf_8_single()` to decode each character code point and print it in hexadecimal format.

### Printing the Results

Here's how the function handles output:

1. It prints the name of the normalization being processed.
2. It enters a loop to decode and print each code point in hexadecimal format until all data is processed.
3. Finally, it prints the original data in a string format for reference.

## Conclusion

After performing all normalization forms, the program cleans up by calling `lxb_unicode_normalizer_destroy(uc, true)` to free the allocated resources. It returns a success status, indicating that all operations were completed without errors.

This example provides a practical approach to understanding how Unicode normalization works in the Lexbor library and demonstrates how to handle Unicode strings effectively.