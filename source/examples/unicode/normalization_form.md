# Unicode Normalization

This article explains the code from the file [lexbor/unicode/normalization_form.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/unicode/normalization_form.c). The example demonstrates how to use the `lexbor` library to normalize a Unicode string using different Unicode normalization forms. We will walk through the essential sections of the code, explaining the rationale and intent behind each part.

The example showcases how to normalize a given Unicode string using four different normalization forms: NFC, NFD, NFKC, and NFKD. The purpose of this example is to illustrate how to initialize the Unicode normalizer, perform normalization with different forms, and handle the results via a callback function.

## Key Code Sections

### Initialization of the Unicode Normalizer

The code first creates and initializes the Unicode normalizer:

```c
uc = lxb_unicode_normalizer_create();
status = lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);
if (status != LXB_STATUS_OK) {
    printf("Failed to init unicode object.\n");
    return EXIT_FAILURE;
}
```

Here, the function `lxb_unicode_normalizer_create()` allocates memory for the normalizer object. The `lxb_unicode_normalizer_init()` function initializes the normalizer for NFC (Normalization Form C). If initialization fails, an error message is printed, and the program exits.

### Normalizing with Different Unicode Forms

#### NFC Normalization

The code snippet below demonstrates NFC normalization:

```c
status = lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                               callback, "NFC", true);
if (status != LXB_STATUS_OK) {
    printf("Failed to normalize NFC.\n");
    return EXIT_FAILURE;
}
```

The `lxb_unicode_normalize()` function normalizes the `source` string according to the NFC form. It uses the callback function `callback`, passes "NFC" as context, and prints an error message if normalization fails.

#### NFD Normalization

To switch to the NFD form and normalize, the code uses:

```c
(void) lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFD);
status = lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                               callback, "NFD", true);
if (status != LXB_STATUS_OK) {
    printf("Failed to normalize NFD.\n");
    return EXIT_FAILURE;
}
```

The `lxb_unicode_normalization_form_set()` function changes the normalization form to NFD. The subsequent call to `lxb_unicode_normalize()` processes the string in NFD form, utilizing the same callback for displaying the result.

#### NFKC and NFKD Normalization

The normalization forms NFKC and NFKD follow similar patterns:

```c
(void) lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFKC);
status = lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                               callback, "NFKC", true);
if (status != LXB_STATUS_OK) {
    printf("Failed to normalize NFKC.\n");
    return EXIT_FAILURE;
}

(void) lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFKD);
status = lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                               callback, "NFKD", true);
if (status != LXB_STATUS_OK) {
    printf("Failed to normalize NFKD.\n");
    return EXIT_FAILURE;
}
```

The code changes the normalization form using `lxb_unicode_normalization_form_set()` to NFKC and NFKD, respectively, and normalizes the `source` string with each form.

### Callback Function

The callback function handles the normalized data and prints it:

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    lxb_codepoint_t cp;
    const lxb_char_t *p, *end;
    const char *name = ctx;

    p = data;
    end = data + len;

    printf("%s: ", name);

    while (p < end) {
        cp = lxb_encoding_decode_valid_utf_8_single(&p, end);
        printf("%04x ", cp);
    }

    printf("(%.*s)\n", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}
```

This function decodes the normalized UTF-8 data, printing each Unicode code point in hexadecimal form along with the normalization form name and the string itself. The parameter `ctx` provides the normalization form name.

## Notes

- Different normalization forms have specific usages and implications for string comparison, search, and storage.
- The `lxb_unicode_normalizer_create()` and `lxb_unicode_normalizer_destroy()` manage memory efficiently, preventing leaks.
- Error handling is essential to ensure that normalization processes are executed correctly and any issues are appropriately reported.

## Summary

The example demonstrates initializing a Unicode normalizer, switching between various normalization forms, and processing the normalized data using a callback function. This detailed understanding of the `lexbor` normalization API enables users to implement Unicode normalization effectively in their projects. Understanding these processes is crucial for managing and comparing Unicode strings accurately.