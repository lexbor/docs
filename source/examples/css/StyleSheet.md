# Parsing and Serializing CSS Stylesheet

This article explains an intermediate-to-advanced example code that demonstrates 
how to parse and serialize a CSS stylesheet using the `lexbor` library. The 
example can be found in the file `lexbor/css/StyleSheet.c`.

The provided code example demonstrates how to read a CSS file, parse it using 
the `lexbor` library, and then serialize the parsed CSS back to a string. This 
example is valuable for developers looking to understand how to interact with 
CSS data programmatically using `lexbor`.

## Key Code Sections

### Reading the CSS File

The first significant operation in the code is reading the contents of a CSS 
file. This is done using the `lexbor_fs_file_easy_read` function which reads the 
contents into memory.

```c
fl = (const lxb_char_t *) argv[1];

css = lexbor_fs_file_easy_read(fl, &css_len);
if (css == NULL) {
    FAILED("Failed to read CSS file");
}
```

Here, `argv[1]` is expected to contain the path to the CSS file. The function 
`lexbor_fs_file_easy_read` reads the file into a dynamically allocated buffer, 
with `css_len` capturing the length of the data. If the file read fails, the 
program exits with an error.

### Initializing the Parser

Next, the code initializes a `lexbor` CSS parser. This involves creating a 
parser instance and initializing it.

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to create CSS Parser");
}
```

First, a new parser instance is created using `lxb_css_parser_create()`. The 
`lxb_css_parser_init` function initializes this parser. If the initialization 
fails, an error is reported and the program exits.

### Parsing the Stylesheet

Once the parser is ready, the next task is to parse the contents of the CSS 
file.

```c
sst = lxb_css_stylesheet_parse(parser, css, css_len);

(void) lexbor_free(css);
(void) lxb_css_parser_destroy(parser, true);

if (sst == NULL) {
    FAILED("Failed to parse CSS");
}
```

The function `lxb_css_stylesheet_parse` parses the CSS data stored in the buffer 
`css` with length `css_len`. After parsing, the buffer is freed and the parser 
is destroyed. If parsing fails, the program reports an error and exits.

### Serializing the Stylesheet

After parsing the stylesheet, the example serializes it back to a string using a 
callback function.

```c
status = lxb_css_rule_serialize(sst->root, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize StyleSheet");
}
```

The function `lxb_css_rule_serialize` walks through the stylesheet rules, 
serializing each one. The `callback` function is called for each chunk of data 
during serialization. If an error occurs during serialization, the program 
reports it and exits.

### The Callback Function

The callback function is straightforward but crucial for outputting the 
serialized data.

```c
lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, data);
    return LXB_STATUS_OK;
}
```

This function simply prints each chunk of serialized data to the standard 
output. The `printf` function uses the precision field to handle the length of 
data correctly.

## Notes

- Ensure that the CSS file exists and is accessible.
- Error handling is fundamental when dealing with file operations and parsing.
- The example provides a clear pathway from reading a file to parsing and 
  serializing CSS.

## Summary

This example demonstrates effectively how to use the `lexbor` library to handle 
CSS files. It highlights reading a file, parsing the CSS content, and 
serializing the parsed content back to a string. Understanding this example 
enables developers to manage CSS data programmatically with `lexbor`, which can 
be extended and integrated into larger projects dealing with CSS manipulation.