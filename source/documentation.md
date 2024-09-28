# Documentation

## Quick Start

These steps show how to use `lexbor` in your code. They assume you are using Linux and `gcc`.

1. [Install](#installation) the `lexbor` library on your system.

2. Let's parse some sample HTML markup.
   Save the following code as `myhtml.c`:

   ```c
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

## Installation

To install `lexbor` from binary packages, refer to the [Download](download.md) section.

## Source code

The source code is available on [GitHub](https://github.com/lexbor/lexbor).

To build and install `lexbor` from source, use [CMake](https://cmake.org/), an open-source, cross-platform build system.

### Linux, *BSD, macOS

At the project root:

```sh
cmake .
make
sudo make install
```

Optional flags recognized by the `cmake` command:

| Flag                          | Default | Description                                                                                              |
|-------------------------------|:-------:|----------------------------------------------------------------------------------------------------------|
| LEXBOR_OPTIMIZATION_LEVEL      |   -O2   | Optimization level for building.                                                                          |
| LEXBOR_C_FLAGS                 |         | Default `C` compilation flags. See the `port.cmake` files in the [ports](https://github.com/lexbor/lexbor/tree/master/source/lexbor/ports) directory. |
| LEXBOR_CXX_FLAGS               |         | Default `C++` compilation flags.                                                                          |
| LEXBOR_WITHOUT_THREADS         |   ON    | Reserved for future use.                                                                                  |
| LEXBOR_BUILD_SHARED            |   ON    | Create a shared library.                                                                                  |
| LEXBOR_BUILD_STATIC            |   ON    | Create a static library.                                                                                  |
| LEXBOR_BUILD_SEPARATELY        |  OFF    | Build all modules separately. Each module will have its own library (shared and static).                   |
| LEXBOR_BUILD_EXAMPLES          |  OFF    | Build example programs.                                                                                   |
| LEXBOR_BUILD_TESTS             |  OFF    | Build tests.                                                                                              |
| LEXBOR_BUILD_TESTS_CPP         |   ON    | Build C++ tests to verify library operation in C++. Requires `LEXBOR_BUILD_TESTS`.                        |
| LEXBOR_BUILD_UTILS             |  OFF    | Build project utilities and helpers.                                                                      |
| LEXBOR_BUILD_WITH_ASAN         |  OFF    | Enable Address Sanitizer if possible.                                                                     |
| LEXBOR_INSTALL_HEADERS         |   ON    | Install library headers (`.h` files).                                                                     |
| LEXBOR_PRINT_MODULE_DEPENDENCIES|  OFF    | Print module dependencies.                                                                                |

### Windows

Use the [CMake](https://cmake.org/) GUI tool.

For Windows with [MSYS2](https://www.msys2.org/):

```sh
cmake . -G "Unix Makefiles"
make
make install
```


### Command Line Examples

We recommend building the project in a separate directory to easily clean up later, as `cmake` generates many temporary files:

```sh
mkdir build
cd build
```

To build a debug version of `lexbor` with Address Sanitizer enabled:

```sh
cmake .. -DCMAKE_C_FLAGS="-fsanitize=address -g" -DLEXBOR_OPTIMIZATION_LEVEL="-O0" -DLEXBOR_BUILD_TESTS=ON -DLEXBOR_BUILD_EXAMPLES=ON
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

To install only the shared library without headers:

```sh
cmake .. -DLEXBOR_BUILD_STATIC=OFF -DLEXBOR_INSTALL_HEADERS=OFF
make
sudo make install
```


### Code Samples

All code samples are available in the `lexbor` repository under the [`/examples/` directory](https://github.com/lexbor/lexbor/tree/master/examples).

To build and run the samples:

```sh
cmake .. -DLEXBOR_BUILD_EXAMPLES=ON
make
./examples/lexbor/html/element_create
./examples/lexbor/html/document_title
```


## General Considerations

### Our Approach: Dependencies, Algorithms, Platforms

- The project is written in pure `C` without external dependencies. We believe
  in a "go hard or go home" approach.

- While we're not reinventing every algorithm known to humankind, we handle
  object creation and memory management in our own way. Many classic algorithms
  used in `lexbor` are adapted to meet the specific needs of the project.

- We're open to using third-party code, but it's often simpler to start from
  scratch than to add extra dependencies (looking at you, Node.js).

- Some functions are platform-dependent, such as threading, timers, I/O, and
  blocking primitives (spinlocks, mutexes). For these, we have a separate `port`
  module with its own structure and build rules, distinct from the other
  modules.


## Memory Management

There are four main dynamic memory functions:

```c
void *
lexbor_malloc(size_t size);

void *
lexbor_calloc(size_t num, size_t size);

void *
lexbor_realloc(void *dst, size_t size);

void *
lexbor_free(void *dst);
```

These functions:

- Are defined in `/source/lexbor/core/lexbor.h` (in the [core](#core) module).

- Are implemented in `/source/port/*/lexbor/core/memory.c` (in the `port`
  module).

- Can be redefined if needed.


As the names suggest, they serve as replacements for the standard `malloc`,
`calloc`, `realloc`, and `free`. However, unlike `free`, the `lexbor_free`
function returns a `void *` that is always `NULL`. This simplifies the process
of nullifying freed variables:

```c
if (object->table != NULL) {
    object->table = lexbor_free(object->table);
}
```

Without this, you'd need to explicitly nullify `object->table`:

```c
if (object->table != NULL) {
    lexbor_free(object->table);
    object->table = NULL;
}
```

We'll discuss other differences later.


## Status Codes

If a function can fail, it should report the failure. We follow two main rules when working with status codes:

- If the status is `LXB_STATUS_OK` (`0`), everything is fine; otherwise,
  **something went wrong**.

- Always return **meaningful** status codes. For example, if memory allocation
  fails, return `LXB_STATUS_ERROR_MEMORY_ALLOCATION`, not a generic value like
  `0x1f1f`.


Status codes are passed as `lxb_status_t`. This type is defined throughout the
codebase in `/source/lexbor/core/types.h`, and all available status codes are
listed in `/source/lexbor/core/base.h`.


## Function Naming

Most functions follow this naming pattern:

[naming1]: img/naming1.png

![Common Naming Pattern][naming1]

<style>
    img[alt="Common Naming Pattern"] { height: 305px; display: block; margin: auto; }
</style>


The exception is the [core](#core) module (`/source/lexbor/core/`), which uses a
different pattern:

[naming2]: img/naming2.png

![Core Naming Pattern][naming2]

<style>
    img[alt="Core Naming Pattern"] { height: 305px; display: block; margin: auto; }
</style>


In other words, all `lexbor_*` functions are located in the `core` module,
without exceptions.


## Header Locations

All paths are relative to the `/source/` directory. For example, to include a
header file from the [html](#html) module located in `/source/lexbor/html/`,
use:

```c
#include "lexbor/html/tree.h"
```

## Data Structures

Most structures and objects have an API for creating, initializing, cleaning,
and deleting them. This follows the general pattern:

```c
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

- The `*_init` function can accept any number of arguments and always returns
  `lxb_status_t`.

- Cleanup functions, `*_clean` and `*_erase`, may return any value, but they
  typically return `void`.

- If `NULL` is passed as the first argument (the object) to the `*_init`
  function, it returns `LXB_STATUS_ERROR_OBJECT_NULL`.

- When the `*_destroy` function is called with `self_destroy` set to `true`, the
  returned value is always `NULL`; otherwise, the object (`obj`) is returned.

- The `*_destroy` functions always check if the object is `NULL`; if so, they
  return `NULL`.

- If the `*_destroy` function doesn't take the `bool self_destroy` argument, the
  object can only be created using the `*_create` function (i.e., not on the
  stack).

Typical usage:

```c
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

```c
lexbor_avl_t avl = {0};
lxb_status_t status = lexbor_avl_init(&avl, 1024);

if (status != LXB_STATUS_OK) {
    lexbor_avl_node_destroy(&avl, false);

    exit(EXIT_FAILURE);
}

/* Do something even more useful */

lexbor_avl_node_destroy(&avl, false);
```

Note that this approach is not an absolute requirement, even though it is
common. There are cases where a different API may be more suitable.


## Modules

The `lexbor` project is designed to be modular, allowing each module to be built
separately if desired. Modules can depend on each other; for instance, all
modules currently rely on the [core](#core) module.

Each module is located in a subdirectory within the `/source/` directory of the
project.


## Versions

Each module records its version in the `base.h` file located at the module root.
For example, see `/source/lexbor/html/base.h`:

```c
#define <MODULE-NAME>_VERSION_MAJOR 1
#define <MODULE-NAME>_VERSION_MINOR 0
#define <MODULE-NAME>_VERSION_PATCH 3

#define <MODULE-NAME>_VERSION_STRING LXB_STR(<MODULE-NAME>_VERSION_MAJOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_MINOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_PATCH)
```


## Core

This is the base module, implementing essential algorithms for the project, such
as AVL and BST trees, arrays, and strings. It also handles memory management.
The module is continuously evolving with new algorithms being added and existing
ones optimized.

Documentation for this module will be available later.


## DOM

This module implements the [DOM specification](https://dom.spec.whatwg.org/).
Its functions manage the DOM tree, including its nodes, attributes, and events.

Documentation for this module will be available later.


## HTML

This module implements the [HTML
specification](https://html.spec.whatwg.org/multipage/).

Current implementations include: Tokenizer, Tree Builder, Parser, Fragment
Parser, and Interfaces for HTML Elements.

Documentation for this module will be available later. For guidance, refer to
the
[HTML examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/html) in our repo
or the corresponding [articles](articles/index).


## Encoding

This module implements the [Encoding
specification](https://encoding.spec.whatwg.org/).

Current implementations include streaming encode/decode. Available encodings:

```
big5, euc-jp, euc-kr, gbk, ibm866, iso-2022-jp, iso-8859-10, iso-8859-13,
iso-8859-14, iso-8859-15, iso-8859-16, iso-8859-2, iso-8859-3, iso-8859-4,
iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-8-i, koi8-r, koi8-u,
shift_jis, utf-16be, utf-16le, utf-8, gb18030, macintosh, replacement,
windows-1250, windows-1251, windows-1252, windows-1253, windows-1254,
windows-1255, windows-1256, windows-1257, windows-1258, windows-874,
x-mac-cyrillic, x-user-defined
```

Documentation for this module will be available later. For guidance, refer to
the [Encoding
examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/encoding)
in our repo or the corresponding [articles](articles/index).


## CSS

This module implements the [CSS specification](https://drafts.csswg.org/).

Documentation for this module will be available later. For guidance, refer to
the [CSS
examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/css) in
our repo or the corresponding [articles](articles/index).
