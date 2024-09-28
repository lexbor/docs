# Determining HTML Encoding

The example code in `lexbor/html/encoding.c` demonstrates how to determine the encoding of an HTML file using the `lexbor` library. This example is particularly useful for understanding how to initialize the encoding mechanism and extract the encoding information from the HTML content.

In this example, the code performs several tasks to determine the HTML encoding. It initializes the HTML encoding detection system, reads the HTML file, and then identifies the encoding used in that file. This process is useful for web scraping, data extraction, and ensuring proper text rendering. The file in question is `lexbor/html/encoding.c`.

## Key Code Sections

### Main Function and Input Handling

The program starts with the `main` function, which handles user input and delegates file reading and encoding detection.

```c
int
main(int argc, const char *argv[])
{
    size_t len;
    lxb_char_t *html;
    lxb_status_t status;
    lxb_html_encoding_t em;
    lxb_html_encoding_entry_t *entry;

    if (argc != 2) {
        usage();
        exit(EXIT_SUCCESS);
    }

    html = lexbor_fs_file_easy_read((lxb_char_t *) argv[1], &len);
    if (html == NULL) {
        FAILED(true, "Failed to read file: %s", argv[1]);
    }
    // ... rest of code ...
}
```

Here, the program expects a single argument: the path to the HTML file. It reads the file content using `lexbor_fs_file_easy_read`, which returns the file's content and length.

### Encoding Initialization

Next, the program initializes the encoding detection mechanism.

```c
status = lxb_html_encoding_init(&em);
if (status != LXB_STATUS_OK) {
    FAILED(false, "Failed to init html encoding");
}
```

This part initializes the `lxb_html_encoding_t` structure. If initialization fails, the program exits with an error message.

### Encoding Determination

The core logic for determining the encoding follows.

```c
status = lxb_html_encoding_determine(&em, html, (html + len));
if (status != LXB_STATUS_OK) {
    goto failed;
}

entry = lxb_html_encoding_meta_entry(&em, 0);
if (entry != NULL) {
    printf("%.*s\n", (int) (entry->end - entry->name), entry->name);
}
else {
    printf("Encoding not found\n");
}
```

The function `lxb_html_encoding_determine` scans the HTML content to find any encoding declarations. If an encoding is found, it retrieves the encoding entry using `lxb_html_encoding_meta_entry` and prints the encoding name.

### Error Handling and Cleanup

In case of errors, the program provides error messages and performs necessary cleanups.

```c
lexbor_free(html);
lxb_html_encoding_destroy(&em, false);

return 0;

failed:

lexbor_free(html);
lxb_html_encoding_destroy(&em, false);

FAILED(false, "Failed to determine encoding");
```

Here, `lexbor_free` releases the allocated memory for the HTML content, and `lxb_html_encoding_destroy` cleans up the encoding structure.

## Notes

- The example limits the bytes read to the first 1024 to save time, as encoding declarations are typically found early in the HTML.
- It uses `lexbor_fs_file_easy_read` for easy file reading, which abstracts away low-level file operations.
- Proper initialization and cleanup are crucial to avoid memory leaks.

## Summary

This example provides a clear, practical demonstration of how to determine the encoding of an HTML file using the `lexbor` library. It covers essential tasks such as initialization, reading file content, detecting encoding, and handling errors. Understanding this example is invaluable for developers needing to ensure correct text processing and rendering in various web-related applications.