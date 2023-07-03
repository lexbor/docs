[name]: lexbor
[title]: Documentation
[theme]: document.html


# Quick Start

A small example of how to use the Lexbor library in program. Example for create Linux program using GCC compiler.

1. [Install](#installation) `lexbor` library on your system.

2. Create the following file named `myhtml.c`:

```C
 #include <lexbor/html/parser.h>
 #include <lexbor/dom/interfaces/element.h>
 
 
 int
 main(int argc, const char *argv[])
 {
     lxb_status_t status;
     const lxb_char_t *tag_name;
     lxb_html_document_t *document;
 
     static const lxb_char_t html[] = "<div>Work fine!</div>";
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

3. Compile file `myhtml.c` using GCC: `gcc myhtml.c -llexbor -o myhtml`

4. Done! You can run created programm: `./myhtml`


# Installation

To install `lexbor` from binary packages, refer to the [Download](../download.md) section.

## Source code

The source code of the library is provided on [our GitHub account](https://github.com/lexbor/lexbor).

For build and install `Lexbor` library from [source code](https://github.com/lexbor/lexbor/), use [CMake](https://cmake.org/) (open-source, cross-platform build system).

### Linux, *BSD, macOS

In root directory of project (`/`):

```bash
cmake .
make
sudo make install
```

Flags that can be passed to cmake:

| Flags | Default | Description |
|---|:---:|---|
|LEXBOR_OPTIMIZATION_LEVEL| -O2 |   |
|LEXBOR_C_FLAGS|  | Default compilation flags to be used when compiling `C` files.<br>See `port.cmake` files in [ports](https://github.com/lexbor/lexbor/tree/master/source/lexbor/ports) directory. |
|LEXBOR_CXX_FLAGS|  | Default compilation flags to be used when compiling `C++` files. |
|LEXBOR_WITHOUT_THREADS| ON | Not used now, for the future. |
|LEXBOR_BUILD_SHARED| ON | Create shaded library. |
|LEXBOR_BUILD_STATIC| ON | Create static library. |
|LEXBOR_BUILD_SEPARATELY| OFF | Build all modules separately. Each project module will have its own library (shared and static). |
|LEXBOR_BUILD_EXAMPLES| OFF | Build examples. |
|LEXBOR_BUILD_TESTS| OFF | Build tests. |
|LEXBOR_BUILD_TESTS_CPP| ON | Build C++ tests. Tests verify the correct operation of the library in C++. Used with LEXBOR_BUILD_TESTS. |
|LEXBOR_BUILD_UTILS| OFF | Build utils/helpers for project. |
|LEXBOR_BUILD_WITH_ASAN| OFF | Build with address sanitizer if possible. |
|LEXBOR_INSTALL_HEADERS| ON | Install headers (all *.h files). |
|LEXBOR_PRINT_MODULE_DEPENDENCIES| OFF | Prints dependencies between modules. |

### Windows

Use the [CMake](https://cmake.org/) GUI.

For Windows with MSYS:

```bash
cmake . -G "Unix Makefiles"
make
make install
```

### Debug and Sanitizer

```bash
cmake . -DCMAKE_C_FLAGS="-fsanitize=address -g" -DLEXBOR_OPTIMIZATION_LEVEL="-O0" -DLEXBOR_BUILD_TESTS=ON -DLEXBOR_BUILD_EXAMPLES=ON
make
make test
```

### Examples

I recommend creating a separate directory to build the project. It can be easily removed together with all garbage.

All examples work from created `build` directory in the root directory of project:
```bash
mkdir build
cd build
```

Build together with tests:

```bash
cmake .. -DLEXBOR_BUILD_TESTS=ON
make
make test
sudo make install
```

Set installation location (`prefix`):

```bash
cmake .. -DCMAKE_INSTALL_PREFIX=/my/path/usr
make
make install
```

Installation only shared library (without headers):

```bash
cmake .. -DLEXBOR_BUILD_STATIC=OFF -DLEXBOR_INSTALL_HEADERS=OFF 
make
sudo make install
```

Build and run examples:

```bash
cmake .. -DLEXBOR_BUILD_EXAMPLES=ON
make
./examples/lexbor/html/element_create
./examples/lexbor/html/document_title
```


# General

## Dependencies

The project develops without external dependencies.

We are not fans of repeatedly writing all known algorithms, like AVL Tree, Binary Search Tree and so on, but it is important for us to use our own approach to creating objects and managing memory.
Most of the implemented algorithms are not "clean", the logic of them has somehow been changed/optimized for needs of the project.

There is no contradiction to using third-party code, but often all that is needed for a project is easier to write independently than to adapt someone's code, licenses.

## Platform-dependent

Despite the fact that the project is written in pure `C` without external dependencies, the implementation of some functions depends for each platform. Namely: multithreading, timers, input-output, blocking (spinlock, mutex).

For this, a separate module `port` is implemented which has its own structure and build rules different from the other modules.

## Memory

Four functions for working with dynamic memory:

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

Functions are defined in `/source/lexbor/core/lexbor.h`, implemented in`/source/port/*/lexbor/core/memory.c` and can be redefined.

From the names it is clear that these are bindings for standard functions `malloc, calloc, realloc, free`.
Unlike the standard `free` function, the` lexbor_free` function returns the value `void *` which is always equal to `NULL` - this is a kind of syntactic sugar, for not to nullify variables after free.

For example:

```C
if (object->table != NULL) {
    object->table = lexbor_free(object->table);
}
```

Otherwise we would have to write:

```C
if (object->table != NULL) {
	lexbor_free(object->table);
	object->table = NULL:
}
```

## Statuses

If something inside a function can go "wrong", then the function should definitely say about it.

Two main rules when working with statuses:

1. If the status is `LXB_STATUS_OK` (`0`), then everything is fine, otherwise something went wrong.
2. We always return real statuses. That is, if memory is not allocated, then the `LXB_STATUS_ERROR_MEMORY_ALLOCATION` status will be returned, not some fake 0x1f1f.

There is a type of `lxb_status_t` (`unsigned int`), common to all, defined in `/source/lexbor/core/types.h`.
All available statuses can be seen in `/source/lexbor/core/base.h` file.

## Naming

Almost all functions are created according to the following pattern:

```
lxb_<module-name>_<path-to-file>_<file-name>_<name>(...);
|_| |___________| |____________| |_________| |____|
 |        |              |            |        |
 |        -------        |            |        |
 ----------     |     ----     --------        |
          |     |     |        |               |
/source/lexbor/html/tree/open_elements.h       |
          |     |     |        |               |
          |    --     |        |       ---------
          |    |    ---      ---       |
          |    |    |        |         |
         |‾| |‾‾| |‾‾| |‾‾‾‾‾‾‾‾‾‾‾| |‾‾|
         lxb_html_tree_open_elements_find(...);
```

For example, let's take the function `lxb_html_tree_create(...)`. Find it easily in `/source/lexbor/html/tree.c`

The exception is the main module (`/source/lexbor/core`) of the `Lexbor` project. Which has the following pattern:
```
lexbor_<path-to-file>_<file-name>_<name>(...);
|____| |____________| |_________| |____|
   |                      |         |
   -------           ------         |
         |           |              |
|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| |‾|             |
/source/lexbor/core/avl.h           |
|_________________| |_|             |
         |           |              |
         --------    |    -----------
                |    |    |
             |‾‾‾‾| |‾| |‾‾‾‾|
             lexbor_avl_create(...);
```

In other words, if in the project we have `lexbor_*` functions, then this means that it is the main module — `core`.

## Headers

All paths relative to the `/source` directory. For example, if we need to `include` a header file from the `html` module which is in the directory `/source/lexbor/html`: `#include "lexbor/html/tree.h"`.

## Objects

Most structures/objects have the API to create, initialize, clean, and delete used the following pattern:

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

The function of initialization object `*_init` can take any number of arguments and always returns `lxb_status_t`.
The cleanup functions `*_clean` and `*_erase` can return any value, usually `void`.

If you pass `NULL` as the first argument (object) to the initialization function `*_init`, the function will return `LXB_STATUS_ERROR_OBJECT_NULL` status.

If the `*_destroy` function calls with `self_destroy` equal `true`, then returned value always will be `NULL`, otherwise will be returned `obj`.
In `*_destroy` functions we always check object for `NULL` value. If object is `NULL` value, then function returned `NULL` value.

If the `*_destroy` function does not have the `bool self_destroy` argument, then object can only be created using the `*_create` function (not on stack).

Typical usage example:

```C
lexbor_avl_t *avl = lexbor_avl_create();
lxb_status_t status = lexbor_avl_init(avl, 1024);

if (status != LXB_STATUS_OK) {
    lexbor_avl_node_destroy(avl, true);

    exit(EXIT_FAILURE);
}

/* Do something */

lexbor_avl_node_destroy(avl, true);
```

Example with object on stack:

```C
lexbor_avl_t avl = {0};
lxb_status_t status = lexbor_avl_init(&avl, 1024);

if (status != LXB_STATUS_OK) {
    lexbor_avl_node_destroy(&avl, false);

    exit(EXIT_FAILURE);
}

/* Do something */

lexbor_avl_node_destroy(&avl, false);
```

It is worth noting that this approach is not an absolute postulate. There are cases when you have to implement a different API, but still, in most cases, it is.

# Modules

The Lexbor project is modular. Theoretically, each module can be build separately from the whole project. Modules can have dependencies among themselves. For example, at the moment all modules are dependent on the [core module](#core).

All modules are located in the `/source` directory of the Lexbor project.

## Versions

Each module contain information about its version in the header file `base.h` in the module root. For example, see `/source/lexbor/html/base.h`.

```C
#define <MODULE-NAME>_VERSION_MAJOR 1
#define <MODULE-NAME>_VERSION_MINOR 0
#define <MODULE-NAME>_VERSION_PATCH 3

#define <MODULE-NAME>_VERSION_STRING LXB_STR(<MODULE-NAME>_VERSION_MAJOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_MINOR) LXB_STR(.) \
                                     LXB_STR(<MODULE-NAME>_VERSION_PATCH)
```


## Core

This is the base module. The `Core` contains all the necessary algorithms for the project: AVL Tree, Binary Search Tree, Array, Strings and other. All work with memory is implemented in this module.

This module is constantly evoluting, new algorithms are added and optimized existing ones.

Documentation for this module is not ready.


## DOM

This module for working with DOM. For more detail, please, see [DOM specifications](https://dom.spec.whatwg.org/).
`DOM` module contains functions for manipulating DOM tree: nodes, attributes, events.

Documentation for this module is not ready.


## HTML

This module contains implementation of [HTML specification](https://html.spec.whatwg.org/multipage/).

Implemented in this module: Tokenizer, Tree Builder, Parser, Fragment Parser, Interfaces for HTML Elements.

Documentation for this module is not ready. Please, see [examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/html).


## Encoding

This module contains implementation of [Encoding specification](https://encoding.spec.whatwg.org/).

Implemented in this module: streaming encode/decode.
Available encodings:
```
big5, euc-jp, euc-kr, gbk, ibm866, iso-2022-jp, iso-8859-10, iso-8859-13,
iso-8859-14, iso-8859-15, iso-8859-16, iso-8859-2, iso-8859-3, iso-8859-4,
iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-8-i, koi8-r, koi8-u,
shift_jis, utf-16be, utf-16le, utf-8, gb18030, macintosh, replacement,
windows-1250, windows-1251, windows-1252, windows-1253, windows-1254,
windows-1255, windows-1256, windows-1257, windows-1258, windows-874,
x-mac-cyrillic, x-user-defined
```

Documentation for this module is not ready. Please, see [examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/encoding).


## CSS

This module contains implementation of [CSS specification](https://drafts.csswg.org/).

Documentation for this module is not ready. Please, see [examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/css).


# Examples (source code)

All examples you can see in [`/examples` directory](https://github.com/lexbor/lexbor/tree/master/examples) on our repository.

How to compile and run the examples, please, see [Build and Installation](#build_and_installation) section.
