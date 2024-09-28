# Retrieve Encoding Data by Name: Example

This example demonstrates how to retrieve encoding data by name using the `lexbor`
library, as shown in the file `lexbor/encoding/data_by_name.c`. This code 
illustrates the utilization of `lexbor` functions and data types to find specific 
character encoding details based on a given encoding name.

The purpose of the example is to demonstrate 
how to use the `lexbor` library to query character encoding information by 
providing an encoding name. This example is helpful for understanding how to 
interact with the encoding module of `lexbor`, which is crucial for various 
tasks such as text processing, web scraping, or any application requiring 
character set conversions.

## Key Code Sections

### Finding Encoding Data by Name

The main functionality of this example is encapsulated in the following lines:

```c
enc_data = lxb_encoding_data_by_name((lxb_char_t *) "uTf-8", 5);
if (enc_data == NULL) {
    return EXIT_FAILURE;
}
```

Here, `lxb_encoding_data_by_name` is called with the encoding name "uTf-8" 
and its length (5). This function is designed to return a pointer to
`lxb_encoding_data_t` which contains information about the encoding. 

- **Function Call**: `lxb_encoding_data_by_name` converts the provided name 
  to a canonical form and searches for its associated encoding data.
- **Parameters**:
  - `(lxb_char_t *) "uTf-8"`: The encoding name, cast to `lxb_char_t *`.
  - `5`: The length of the encoding name.
- **Return Value**: The function returns a pointer to `lxb_encoding_data_t`
  if the encoding is found. If not, `NULL` is returned.

### Error Handling

After the encoding data is retrieved, the code checks if the returned pointer 
is `NULL`:

```c
if (enc_data == NULL) {
    return EXIT_FAILURE;
}
```

This ensures that the program handles the case where the encoding is not found 
appropriately by exiting with `EXIT_FAILURE`.

### Printing Encoding Name

If the encoding is found, the name of the encoding is printed out:

```c
printf("%s\n", enc_data->name);
```

`enc_data->name` holds the canonical encoding name. This line demonstrates 
how to access and use the information within the `lxb_encoding_data_t` structure.

## Notes

- **Case Insensitivity**: The function `lxb_encoding_data_by_name` is 
  case-insensitive, as evidenced by the mixed-case input "uTf-8".
- **Canonical Form**: The returned encoding name is ensured to be in 
  a standard canonical form.
- **Static Data**: The encoding names and their data are typically 
  static and predefined within `lexbor`.

## Summary

This example highlights how to use the `lexbor` library to look up encoding 
data by name. By invoking `lxb_encoding_data_by_name`, users can retrieve 
information about specific encodings efficiently. Understanding this process 
is vital for applications that handle diverse text encodings, ensuring proper 
text interpretation and conversion.

For `lexbor` users, this example provides a clear and practical method to 
interact with the library’s encoding functionalities, facilitating smooth 
integration into larger projects requiring robust encoding support.