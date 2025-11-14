# Punycode Encoding

This article explains the operation of the [lexbor/punycode/encode.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/punycode/encode.c) example from the `lexbor` library. The intent of this example is to demonstrate how to read input from standard input (stdin), handle dynamic memory allocation for growing input, and utilize the `lexbor` Punycode encoding capabilities.

## Key Code Sections

### Input Handling and Memory Allocation

The example code begins by allocating a buffer and reading input data from stdin. It dynamically adjusts the size of the buffer as needed.

```c
char inbuf[4096];
lxb_char_t *buf, *end, *p, *tmp;

buf = lexbor_malloc(sizeof(inbuf));
if (buf == NULL) {
    printf("Failed memory allocation.\n");
    return EXIT_FAILURE;
}

p = buf;
end = buf + sizeof(inbuf);
```

The `buf`, `p`, and `end` pointers manage the input data and the buffer's current size. The initial buffer allocation is done using `lexbor_malloc`.

### Data Reading Loop

The example reads input in chunks and handles the dynamic buffer resizing if the input exceeds the initial buffer size.

```c
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

The loop uses `fread` to read chunks of data. If the buffer is about to exceed its current capacity, it reallocates memory using `lexbor_realloc`, ensuring enough space for the additional input data.

### Trimming Newline Characters

After reading the input, the example trims any trailing newline characters.

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

This logic ensures that the input data is sanitized and free of newline characters before processing.

### Encoding via Punycode

The core functionality of the example is the Punycode encoding, which is achieved through the call to `lxb_punycode_encode`.

```c
status = lxb_punycode_encode(buf, p - buf, callback, NULL);
if (status != LXB_STATUS_OK) {
    printf("Failed decode.\n");
    goto failed;
}
```

The `lxb_punycode_encode` function performs the encoding, and the `callback` function handles the encoded output.

### Output Callback

The `callback` function is responsible for outputting the encoded data. It is invoked by `lxb_punycode_encode`.

```c
static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx, bool unchanged)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}
```

By using `printf`, the callback outputs the encoded Punycode data to stdout.

## Notes

- The example demonstrates the handling of dynamic memory allocation with `lexbor_malloc` and `lexbor_realloc`.
- Proper input sanitization is performed by trimming trailing newline characters.
- `lxb_punycode_encode` is used for Punycode encoding, highlighting `lexbor`'s encoding functions.
- The `callback` function is crucial for handling encoded output.

## Summary

This example illustrates how to read, resize buffers, and sanitize input data from stdin, along with utilizing `lexbor`'s Punycode encoding capabilities. Understanding these concepts is essential for effectively using the `lexbor` library for text processing tasks.