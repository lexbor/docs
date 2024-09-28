# Unicode Normalization: Example

This article explores an example from the `lexbor` library located in the source
file `lexbor/unicode/normalization_form_stdin.c`. The purpose of this example is
to normalize Unicode text read from standard input (stdin) using a chosen
normalization form. It demonstrates how to initialize and use the Unicode
normalization functions provided by `lexbor`. We will dissect the key portions
of the code to understand how the library is used and its underlying logic.

## Key Code Sections

### Initialization and Argument Parsing

The code starts by initializing variables and checking command-line arguments.
The normalization form is expected as the first argument.

```c
lxb_unicode_form_t form;
if (strlen(argv[1]) == 3) {
    if (memcmp(argv[1], "NFC", 3) == 0) {
        form = LXB_UNICODE_NFC;
    }
    else if (memcmp(argv[1], "NFD", 3) == 0) {
        form = LXB_UNICODE_NFD;
    }
    else {
        goto usage;
    }
}
else if (strlen(argv[1]) == 4) {
    if (memcmp(argv[1], "NFKC", 4) == 0) {
        form = LXB_UNICODE_NFKC;
    }
    else if (memcmp(argv[1], "NFKD", 4) == 0) {
        form = LXB_UNICODE_NFKD;
    }
    else {
        goto usage;
    }
}
else {
    goto usage;
}
```

Here, the code checks if the provided normalization form is valid (`NFC`, `NFD`,
`NFKC`, or `NFKD`). Based on the input, it sets the variable `form` to the
corresponding `lexbor` constant.

### Normalizer Creation and Initialization

After validating the input, the code proceeds to create and initialize the 
Unicode normalizer.

```c
lxb_unicode_normalizer_t *uc;
uc = lxb_unicode_normalizer_create();
status = lxb_unicode_normalizer_init(uc, form);
if (status != LXB_STATUS_OK) {
    return EXIT_FAILURE;
}
```

The function `lxb_unicode_normalizer_create` allocates memory for the Unicode 
normalizer. Then, `lxb_unicode_normalizer_init` initializes the normalizer with 
the specified form. If initialization fails, the program exits with a failure 
status.

### Reading and Normalizing Input

The code then enters a loop to read from stdin and normalize the input text.

```c
char inbuf[4096];
size_t size;
bool loop = true;

do {
    size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        }
        else {
            return EXIT_FAILURE;
        }
    }

    status = lxb_unicode_normalize(uc, (const lxb_char_t *) inbuf, size,
                                   callback, NULL, !loop);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }
}
while (loop);
```

The `fread` function reads up to 4096 bytes from stdin into `inbuf`. The loop
continues until the end of file (EOF) is reached. The function 
`lxb_unicode_normalize` processes the input data, calling a callback function
to handle the normalized output.

### The Callback Function

The callback function is responsible for handling each chunk of normalized data.

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

This function simply prints the normalized data to stdout. The use of `printf`
with a length specifier ensures that only the appropriate number of bytes are
printed.

## Notes

- The example demonstrates proper handling of UTF-8 encoded Unicode data with
  different normalization forms (`NFC`, `NFD`, `NFKC`, and `NFKD`).
- The use of the callback mechanism allows for flexible handling of the
  normalized data, suitable for various outputs or further processing.
- It showcases important functions within `lexbor` for creating, initializing,
  and destroying a Unicode normalizer, as well as performing normalization.

## Summary

This example highlights how to use the `lexbor` library to normalize Unicode
text from stdin based on a specified normalization form. Key functions such as
`lxb_unicode_normalizer_create`, `lxb_unicode_normalizer_init`, and
`lxb_unicode_normalize` are utilized. The callback function mechanism ensures
flexible data handling, making this example a practical demonstration for
typical usage scenarios of Unicode normalization in `lexbor`.