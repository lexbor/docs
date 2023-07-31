[name]: lexbor
[title]: Documentation
[theme]: document.html


# Quick Start

These steps show how to use `lexbor` in your code;
they assume you have Linux and `gcc`.

1. [Install](#installation) `lexbor` library in your system.

2. Let's parse some sample HTML markup.
   Save this code as `myhtml.c`:

   ```C
   #include <lexbor/html/parser.h>
   #include <lexbor/dom/interfaces/element.h>


   int
   main(int argc, const char *argv[])
   {
       lxb_status_t status;
       const lxb_char_t *tag_name;
       lxb_html_document_t *document;

       static const lxb_char_t html[] = "<div>Works fine!</div>";
       size_t html_len = sizeof(html) - 1;

       document = lxb_html_document_create();
       if (document == NULL) {
           exit(EXIT_FAILURE);
       }

       status = lxb_html_document_parse(document, html, html_len);
       if (status != LXB_STATUS_OK) {
           exit(EXIT_FAILURE);
       }

      tag_name = lxb_dom_element_qualified_name(lxb_dom_interface_element(document->body),
                                                 NULL);

       printf("Element tag name: %s\n", tag_name);

       lxb_html_document_destroy(document);

       return EXIT_SUCCESS;
   }
   ```

3. Compile `myhtml.c` and run the resulting executable:

   ```sh
   gcc myhtml.c -llexbor -o myhtml
   ./myhtml
   ```


# Installation

To install `lexbor` from binary packages, refer to the [Download](download.md)
section.


## Source code

The source code is available on
[GitHub](https://github.com/lexbor/lexbor).

To build and install `Lexbor`from source, use
[CMake](https://cmake.org/);
it's an open-source, cross-platform build system.


### Linux, *BSD, macOS

At the project root:

```sh
cmake .
make
sudo make install
```

Optional flags recognized by the `cmake` command:

| Flags | Default | Description |
|---|:---:|---|
|LEXBOR_OPTIMIZATION_LEVEL| -O2 |   |
|LEXBOR_C_FLAGS|  | Default `C` compilation flags.<br>For details, see the `port.cmake` files in the [ports](https://github.com/lexbor/lexbor/tree/master/source/lexbor/ports) directory. |
|LEXBOR_CXX_FLAGS|  | Default `C++` compilation flags. |
|LEXBOR_WITHOUT_THREADS| ON | Reserved for future use. |
|LEXBOR_BUILD_SHARED| ON | Create a shared library. |
|LEXBOR_BUILD_STATIC| ON | Create a static library. |
|LEXBOR_BUILD_SEPARATELY| OFF | Build all modules separately.  Each project module will have its own library (both shared and static). |
|LEXBOR_BUILD_EXAMPLES| OFF | Build examples. |
|LEXBOR_BUILD_TESTS| OFF | Build tests. |
|LEXBOR_BUILD_TESTS_CPP| ON | Build C++ tests. Tests verify the correct operation of the library in C++. Used with LEXBOR_BUILD_TESTS. |
|LEXBOR_BUILD_UTILS| OFF | Build project utilities and helpers. |
|LEXBOR_BUILD_WITH_ASAN| OFF | If possible, build with Address Sanitizer enabled. |
|LEXBOR_INSTALL_HEADERS| ON | Install library headers (all `.h` files). |
|LEXBOR_PRINT_MODULE_DEPENDENCIES| OFF | List dependencies between modules. |


### Windows

Use the [CMake](https://cmake.org/) GUI tool.
For Windows with [MSYS2](https://www.msys2.org/):

```sh
cmake . -G "Unix Makefiles"
make
make install
```


### Command Line Examples

We recommend building the project in a separate directory, which can be easily
deleted later, because `cmake` produces lots of clutter:

```sh
mkdir build
cd build
```

To build a debug version of `lexbor` with Address Sanitizer enabled:

```sh
cmake . -DCMAKE_C_FLAGS="-fsanitize=address -g" -DLEXBOR_OPTIMIZATION_LEVEL="-O0" -DLEXBOR_BUILD_TESTS=ON -DLEXBOR_BUILD_EXAMPLES=ON
make
make test
```

To build `lexbor` with tests:

```sh
cmake .. -DLEXBOR_BUILD_TESTS=ON
make
make test
sudo make install
```

To set the installation location (`prefix`):

```sh
cmake .. -DCMAKE_INSTALL_PREFIX=/my/path/usr
make
make install
```

To install only the shared library (without headers):

```sh
cmake .. -DLEXBOR_BUILD_STATIC=OFF -DLEXBOR_INSTALL_HEADERS=OFF
make
sudo make install
```


### Code Samples

All code samples are available on the `lexbor` repo in the [`/examples/`
directory](https://github.com/lexbor/lexbor/tree/master/examples).

To build and run the samples:

```sh
cmake .. -DLEXBOR_BUILD_EXAMPLES=ON
make
./examples/lexbor/html/element_create
./examples/lexbor/html/document_title
```


# General Considerations

## Our Approach: Dependencies, Algorithms, Platforms

- The project is developed in pure `C` without external dependencies.
  Go hard or go home.

- We're not reinventing every algo known to humankind, but we approach object
  creation and memory management in our own way.  Most classic algorithms
  `lexbor` uses are noticeably tweaked for the needs of the project.

- We're not averse to using third-party code, but it's often easier to start
  from scratch than incorporate an extra dependency (Node.js, we're looking at
  you).

- A number of funcions are platform dependent, such as threading, timers, I/0,
  blocking primitives (spinlocks, mutexes).  To help their implementation, a
  separate `port` module exists; its structure and build rules differ from the
  other modules.


## Memory Management

There are four major dynamic memory functions:

```C
void *
lexbor_malloc(size_t size);

void *
lexbor_calloc(size_t num, size_t size);

void *
lexbor_realloc(void *dst, size_t size);

void *
lexbor_free(void *dst);
```

They are:

- Defined in `/source/lexbor/core/lexbor.h` (the [core](#core) module)

- Implemented in `/source/port/*/lexbor/core/memory.c`
  (the `port` module mentioned above)

- Open to redefining

As their names hint, they are intended as a replacement for the standard
`malloc`, `calloc`, `realloc`, and `free` functions.  Unlike `free`, though,
the `lexbor_free` function returns a `void *` value which is always `NULL`;
this is some syntactic sugar to avoid explicitly nullifying `free`'d variables:

```C
if (object->table != NULL) {
    object->table = lexbor_free(object->table);
}
```

Otherwise, we would have to nullify `object->table`:

```C
if (object->table != NULL) {
	lexbor_free(object->table);
	object->table = NULL;
}
```

We'll talk about other discrepancies later.


## Status Codes

If a function can fail somehow, it should report the failure.
We have two big rules when working with status codes:

- If the status is `LXB_STATUS_OK` (`0`), all is fine; otherwise,
  **something went wrong**.

- Always return **meaningful** statuses. That is, if memory wasn't allocated,
  the `LXB_STATUS_ERROR_MEMORY_ALLOCATION` status is returned, not a fake value
  such as `0x1f1f`.

Status codes are passed around as `lxb_status_t`.  The typedef occurs
throughout the code and is defined in `/source/lexbor/core/types.h`; all
available status codes reside in `/source/lexbor/core/base.h`.


## Function Naming

Almost all functions follow this naming pattern:

[naming1]: /img/naming1.png

![Common Naming Pattern][naming1]

<style>
    img[alt="Common Naming Pattern"] {width: 500; height: 405; display: block; margin: auto}
</style>

The exception is the [core](#core) module (`/source/lexbor/core/`), which uses
the following pattern:

[naming2]: /img/naming2.png

![Core Naming Pattern][naming2]

<style>
    img[alt="Core Naming Pattern"] {width: 500; height: 405; display: block; margin: auto}
</style>

In other words, `lexbor_*` functions occur in the `core` module, full stop.


## Header Locations

All paths are relative to the `/source/` directory. For example, to include a
header file from the [html](#html) module in the `/source/lexbor/html/`
directory: `#include "lexbor/html/tree.h"`.


## Data Structures

Most structures and objects have an API to create, initialize, clean, and
delete them according to the following pattern:

```C
<structure-name> *
<function-prefix>_create(void);

lxb_status_t
<function-name>_init(<structure-name> *obj);

void
<function-name>_clean(<structure-name> *obj);

void
<function-name>_erase(<structure-name> *obj);

<structure-name> *
<function-name>_destroy(<structure-name> *obj, bool self_destroy);
```

- The `*_init` function accepts any number of arguments and always returns
  `lxb_status_t`.

- Cleanup functions, `*_clean` and `*_erase`, can return any
  value, but usually it's `void`.

- If `NULL` is passed as the first argument (object) to the `*_init` function,
  the function returns `LXB_STATUS_ERROR_OBJECT_NULL`.

- If the `*_destroy` function is called with `self_destroy` equal to `true`,
  the returned value is always `NULL`; otherwise, `obj` is returned.

- The `*_destroy` functions always check the object for `NULL`; if the object
  is `NULL`, the function returns `NULL` as well.

- If the `*_destroy` function wasn't passed the `bool self_destroy` argument,
  the object can only be created using the `*_create` function (i. e., not on
  the stack).

Typical usage:

```C
lexbor_avl_t *avl = lexbor_avl_create();
lxb_status_t status = lexbor_avl_init(avl, 1024);

if (status != LXB_STATUS_OK) {
    lexbor_avl_node_destroy(avl, true);

    exit(EXIT_FAILURE);
}

/* Do something super useful */

lexbor_avl_node_destroy(avl, true);
```

Now, with an object on the stack:

```C
lexbor_avl_t avl = {0};
lxb_status_t status = lexbor_avl_init(&avl, 1024);

if (status != LXB_STATUS_OK) {
    lexbor_avl_node_destroy(&avl, false);

    exit(EXIT_FAILURE);
}

/* Do something even more useful */

lexbor_avl_node_destroy(&avl, false);
```

Note that this approach is not an absolute must, even if ubiqutious.  There are
cases where a different API fits better.


# Modules

The `lexbor` project is modular by design, and each module can be built
separately (at least potentially). Modules can depend on each other; for
example, now all modules rely on the [core](#core) module.

Each module is a subdirectory in the `/source/` directory of the project.


## Versions

Each module stores its version in the `base.h` file at the module root. For
example, with `/source/lexbor/html/base.h`:

```C
#define <MODULE-NAME>_VERSION_MAJOR 1
#define <MODULE-NAME>_VERSION_MINOR 0
#define <MODULE-NAME>_VERSION_PATCH 3

#define <MODULE-NAME>_VERSION_STRING LXB_STR(<MODULE-NAME>_VERSION_MAJOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_MINOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_PATCH)
```


## Core Module

This is the base module; it implements all algorithms that are essential for
the project, such as AVL and BST trees, arrays, strings and so on.  It also
implements memory management.  The module is continually evolving.  New
algorithms are being added; existing ones, optimized.

The documentation for this module will be available later.


## DOM

This module implements the [DOM specification](https://dom.spec.whatwg.org/).
Its functions manipulate the DOM tree: its nodes, attributes, and events.

The documentation for this module will be available later.


## HTML

This module implements the [HTML
specification](https://html.spec.whatwg.org/multipage/).

Implemented now: Tokenizer, Tree Builder, Parser, Fragment Parser, Interfaces
for HTML Elements.

The documentation for this module will be available later.  For guidance, refer
to the
[examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/html).


## Encoding

This module implements the [Encoding
specification](https://encoding.spec.whatwg.org/).

Implemented now: streaming encode/decode.  Available encodings:
```
big5, euc-jp, euc-kr, gbk, ibm866, iso-2022-jp, iso-8859-10, iso-8859-13,
iso-8859-14, iso-8859-15, iso-8859-16, iso-8859-2, iso-8859-3, iso-8859-4,
iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-8-i, koi8-r, koi8-u,
shift_jis, utf-16be, utf-16le, utf-8, gb18030, macintosh, replacement,
windows-1250, windows-1251, windows-1252, windows-1253, windows-1254,
windows-1255, windows-1256, windows-1257, windows-1258, windows-874,
x-mac-cyrillic, x-user-defined
```

The documentation for this module will be available later.  For guidance, refer
to the
[examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/encoding).


## CSS

This module implements the [CSS
specification](https://drafts.csswg.org/).

The documentation for this module will be available later.  For guidance, refer
to the
[examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/css).
