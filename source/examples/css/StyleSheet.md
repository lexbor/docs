# CSS Stylesheet Parsing Example

This article explains the example code within the file
[lexbor/css/StyleSheet.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/css/StyleSheet.c),
which demonstrates how to use the Lexbor library to read and parse a CSS
stylesheet. The code showcases the steps required to initialize the parser, read
the CSS data from a file, parse the stylesheet, and serialize the resulting
object.

## Code Breakdown

### Includes and Function Declaration

The code begins by including the necessary headers: `base.h` for foundational
functionalities and `lexbor/core/fs.h` and `lexbor/css/css.h` for file system
operations and CSS processing respectively.

### Callback Function

A callback function is defined that takes a pointer to character data, its
length, and a context pointer as parameters:

```c
lxb_status_t callback(const lxb_char_t *data, size_t len, void *ctx) {
    printf("%.*s", (int) len, data);
    return LXB_STATUS_OK;
}
```

This function will be used later to output the serialized CSS rules. It prints
the data passed to it, formatted to handle the length of the string, ensuring
that only the relevant part of the buffer is printed.

### Main Function

The `main` function initializes the program and takes one argument: the path to
a CSS file. It begins by checking if the number of arguments is correct and
printing usage instructions if not:

```c
if (argc != 2) {
    fprintf(stderr, "Usage:\n");
    fprintf(stderr, "\tStyleSheet <file>\n");
    FAILED("Invalid number of arguments");
}
```

### Reading the CSS File

Next, the code reads the contents of the specified CSS file into memory:

```c
fl = (const lxb_char_t *) argv[1];
css = lexbor_fs_file_easy_read(fl, &css_len);
if (css == NULL) {
    FAILED("Failed to read CSS file");
}
```

The `lexbor_fs_file_easy_read` function loads the file into the `css` buffer,
and the length of the data is stored in `css_len`. If reading the file fails, an
error message is displayed.

### Parsing the CSS

After successfully loading the CSS data, a CSS parser is created and
initialized:

```c
parser = lxb_css_parser_create();
status = lxb_css_parser_init(parser, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to create CSS Parser");
}
```

The parser initialization must succeed; otherwise, the program exits early with
an error message.

### StyleSheet Parsing

The actual parsing occurs with the following line:

```c
sst = lxb_css_stylesheet_parse(parser, css, css_len);
```

Here, `lxb_css_stylesheet_parse` processes the loaded CSS content and generates
a stylesheet object, `sst`. If parsing fails, the program will exit.

### Memory Management

Following the parsing step, memory for the CSS buffer is freed, and the parser
is destroyed:

```c
(void) lexbor_free(css);
(void) lxb_css_parser_destroy(parser, true);
```

This cleanup is essential to avoid memory leaks in the application.

### Serializing the Output

The code then serializes the stylesheet and outputs the rules using the
previously defined callback:

```c
status = lxb_css_rule_serialize(sst->root, callback, NULL);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to serialize StyleSheet");
}
```

This process invokes the callback for each rule in the stylesheet, allowing for
customizable output handling.

### Final Cleanup

Finally, the stylesheet object is destroyed to free up resources:

```c
(void) lxb_css_stylesheet_destroy(sst, true);
```

The program concludes successfully by returning `EXIT_SUCCESS`.

## Summary

In this example, a CSS file is read, parsed, and its contents serialized using
the Lexbor library. Each significant section of the code has been explained to
provide clarity on the parsing process and resource management. By following
these steps, developers can incorporate CSS parsing capabilities into their
applications using Lexbor.