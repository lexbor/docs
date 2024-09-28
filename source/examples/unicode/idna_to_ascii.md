# Converting Unicode to ASCII with IDNA

This article explains the use of the `lexbor` library to convert Unicode text to ASCII using Internationalized Domain Names in Applications (IDNA). We will analyze the code in [lexbor/unicode/idna_to_ascii.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/unicode/idna_to_ascii.c), providing a detailed explanation of how it works.

The example demonstrates how to use the `lexbor` library to convert Unicode text to ASCII, particularly in the context of internationalized domain names. The program initializes an IDNA object, reads input from stdin, processes it, and finally converts the read content to ASCII using a callback function. This article dissects the key sections of the code, explaining their functionality and rationale.

## Key Code Sections

### Initialization of the IDNA Object

The IDNA object is initialized using the `lxb_unicode_idna_init` function. This step is fundamental as it sets up the necessary state and resources for the IDNA operations.

```c
lxb_status_t status;
lxb_unicode_idna_t idna;

status = lxb_unicode_idna_init(&idna);
if (status != LXB_STATUS_OK) {
    printf("Failed to init IDNA object.\n");
    return EXIT_FAILURE;
}
```

Here, `lxb_unicode_idna_t idna` is a structure that holds the IDNA-related context. The initialization function returns `LXB_STATUS_OK` if successful. If initialization fails, the program exits with an error message.

### Reading Input Data

The program dynamically reads input data from stdin. The input data is stored in a buffer that is resized as needed to accommodate the read content.

```c
size_t size, nsize;
lxb_char_t *buf, *end, *p, *tmp;
char inbuf[4096];

buf = lexbor_malloc(sizeof(inbuf));
if (buf == NULL) {
    printf("Failed memory allocation.\n");

    lxb_unicode_idna_destroy(&idna, false);

    return EXIT_FAILURE;
}
p = buf;
end = buf + sizeof(inbuf);

do {
    size = fread(inbuf, 1, sizeof(inbuf), stdin);
    if (size != sizeof(inbuf)) {
        if (feof(stdin)) {
            loop = false;
        }
        else {
            printf("Failed read stdin.\n");
            goto failed;
        }
    }

    if (p + size > end) {
        nsize = (end - buf) * 3;

        tmp = lexbor_realloc(buf, nsize);
        if (tmp == NULL) {
            printf("Failed memory reallocation.\n");
            goto failed;
        }

        p = tmp + (p - buf);
        buf = tmp;
        end = tmp + nsize;
    }

    memcpy(p, inbuf, size);
    p += size;
}  
while (loop);
```

This segment performs the following tasks:
1. Allocates an initial buffer using `lexbor_malloc`.
2. Reads data from stdin in chunks of 4096 bytes.
3. Increases the buffer size dynamically through `lexbor_realloc` when required.
4. Continues reading until the end of the input (EOF) is reached.

### Trimming Input Data

The program ensures that the input data does not have trailing newlines or carriage return characters. Such characters might affect the conversion process.

```c
if (p - buf > 0) {
    if (p[-1] == '\n') {
        p -= 1;
    }
}
if (p - buf > 0) {
    if (p[-1] == '\r') {
        p -= 1;
    }
}
```

This code snippet checks whether the last character is a newline or carriage return and adjusts the pointer accordingly to exclude these characters from the data to be processed.

### Conversion to ASCII

The input data is converted from Unicode to ASCII using the `lxb_unicode_idna_to_ascii` function, which takes a callback function to handle the converted output.

```c
status = lxb_unicode_idna_to_ascii(&idna, buf, p - buf, callback, NULL, 0);
if (status != LXB_STATUS_OK) {
    printf("Failed convert to ASCII.\n");
    goto failed;
}
```

The callback function specified in this call (`callback`) will be invoked with the converted ASCII data.

### Callback Function

The callback function prints the converted ASCII text.

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

Using formatted printing, this function outputs the data received in the callback call.

## Notes

- Proper memory allocation and deallocation are crucial to avoid memory leaks. The `lexbor_malloc`, `lexbor_realloc`, and `lexbor_free` functions manage these tasks.
- The IDNA object’s lifecycle is handled with `lxb_unicode_idna_init` and `lxb_unicode_idna_destroy`.
- Error handling ensures that the program exits gracefully on failures.

## Summary

The example in [lexbor/unicode/idna_to_ascii.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/unicode/idna_to_ascii.c) illustrates how to use the `lexbor` library for converting Unicode text to ASCII in the context of IDNA. The main tasks include initializing the IDNA object, reading and managing input dynamically, and using a callback function for the conversion process. Understanding these steps is essential for implementing robust applications that leverage the `lexbor` library to handle internationalized domain names effectively.