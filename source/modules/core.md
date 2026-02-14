# Core Module

* **Version:** 2.7.0
* **Path:** `source/lexbor/core`
* **Base Includes:** `lexbor/core/core.h`
* **Examples:** not present
* **Specification:** not present

## Overview

The Core module is the foundation of lexbor. It provides essential data structures, memory management, and utility functions that all other modules depend on.

Written in pure C99 with zero external dependencies. All objects in Core follow a unified lifecycle pattern: `create -> init -> use -> clean -> use -> destroy`.

## Key Features

- **Zero Dependencies** — pure C99, no external libraries
- **Pluggable Memory** — replace malloc/free with custom allocators
- **Performance-Optimized** — chunk allocation, object pools, SWAR bit tricks
- **Memory Efficient** — pooled allocation reduces fragmentation and syscalls

## What's Inside

- **[Custom Memory Allocator](#custom-memory-allocator)** — pluggable malloc/free replacement
- **[Chunk Memory (mem)](#chunk-memory-mem)** — contiguous memory allocation in large chunks
- **[Raw Memory Allocator (mraw)](#raw-memory-allocator-mraw)** — malloc/free with automatic caching of freed blocks
- **[Object Pool (dobject)](#object-pool-dobject)** — fast allocation of fixed-size objects
- **[Dynamic Array (array)](#dynamic-array-array)** — growable array of pointers
- **[Object Array (array_obj)](#object-array-array_obj)** — growable array of inline fixed-size objects
- **[Hash Table (hash)](#hash-table-hash)** — key-value storage with pluggable hash/compare functions
- **[AVL Tree (avl)](#avl-tree-avl)** — self-balancing binary search tree
- **[Binary Search Tree (bst)](#binary-search-tree-bst)** — unbalanced BST with duplicate key support
- **[BST Map (bst_map)](#bst-map-bst_map)** — BST specialized for string keys
- **[String (str)](#string-str)** — mutable dynamic string
- **[Static BST (sbst)](#static-bst-sbst)** — compile-time read-only BST for character lookup
- **[Static Hash Search (shs)](#static-hash-search-shs)** — compile-time hash table for static datasets
- **[Parse Log (plog)](#parse-log-plog)** — error/warning log for parsers
- **[Conversions (conv, dtoa, strtod)](#conversions-conv-dtoa-strtod)** — number-to-string and string-to-number
- **[Serialization (serialize)](#serialization-serialize)** — callback-based output abstraction
- **[SWAR (swar)](#swar-swar)** — SIMD Within A Register for fast character scanning
- **[Status Codes](#status-codes)** — unified error handling across all modules

## Architecture

### Memory Allocation Layers

All memory in lexbor flows through a layered allocation system:

```
+-------------------------------------------------------+
|  Application Code                                     |
|  (strings, hash entries, tree nodes, DOM elements)    |
+-------------------------------------------------------+
|  Object Pool (dobject) -- fixed-size object recycling |
+-------------------------------------------------------+
|  Raw Allocator (mraw) -- size-tracked, cached free    |
+-------------------------------------------------------+
|  Chunk Memory (mem) -- large contiguous blocks        |
+-------------------------------------------------------+
|  System malloc/free (pluggable via lexbor_memory)     |
+-------------------------------------------------------+
```

### Object Lifecycle Pattern

Every Core object follows the same lifecycle:

```C
/* 1. Create — allocate the object itself */
lexbor_xxx_t *obj = lexbor_xxx_create();

/* 2. Init — allocate internal resources */
lxb_status_t status = lexbor_xxx_init(obj, ...);

/* 3. Use — work with the object */
lexbor_xxx_do_something(obj, ...);

/* 4. Clean — reset state, keep allocated memory for reuse */
lexbor_xxx_clean(obj);

/* 5. Destroy — free all resources */
lexbor_xxx_destroy(obj, true);
```

The `clean` step resets the object to its post-init state without freeing memory, making it ready for reuse. This is key for performance — reusing objects avoids repeated allocation/deallocation overhead.

## Custom Memory Allocator

### Location

Declared in `source/lexbor/core/lexbor.h`.

### Purpose

All memory allocation in lexbor goes through wrapper functions: `lexbor_malloc()`, `lexbor_realloc()`, `lexbor_calloc()`, `lexbor_free()`. By default these call the standard C library functions, but you can replace them with a custom allocator.

### Usage

```C
#include <lexbor/core/lexbor.h>

/* Custom allocator functions */
static void *my_malloc(size_t size) { /* ... */ }
static void *my_realloc(void *ptr, size_t size) { /* ... */ }
static void *my_calloc(size_t num, size_t size) { /* ... */ }
static void  my_free(void *ptr) { /* ... */ }

int main(void) {
    /* Install custom allocator — must be called before any other lexbor function */
    lxb_status_t status = lexbor_memory_setup(my_malloc, my_realloc,
                                              my_calloc, my_free);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Now all lexbor allocations go through your functions */
    /* ... */

    return EXIT_SUCCESS;
}
```

This is useful for integrating lexbor into environments with custom memory management, such as arena allocators or debugging memory wrappers.

## Chunk Memory (mem)

### Location

Declared in `source/lexbor/core/mem.h`.

### Purpose

Provides contiguous memory allocation in large chunks. Instead of calling `malloc` for every small request, `lexbor_mem_t` allocates a large block and serves requests from within it. When the current chunk is full, a new chunk is allocated and linked to the previous one.

This reduces the number of system allocation calls and improves cache locality.

### How It Works

```
Chunk 1 (first)          Chunk 2 (current)
+----------------+       +----------------+
| used | free    | ----> | used | free    |
| data | space   | next  | data | space   |
+----------------+       +----------------+
  <-- length -->           <-- length -->
<----- size ----->       <----- size ------>
```

Each chunk tracks:
- `data` — pointer to the allocated memory block
- `length` — how many bytes are used
- `size` — total capacity of the chunk
- `next`/`prev` — doubly-linked list of chunks

### Example

```C
#include <lexbor/core/mem.h>

int main(void) {
    lexbor_mem_t *mem = lexbor_mem_create();
    lxb_status_t status = lexbor_mem_init(mem, 4096); /* min chunk size */
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Allocate from chunk memory */
    void *data1 = lexbor_mem_alloc(mem, 128);
    void *data2 = lexbor_mem_calloc(mem, 256); /* zero-initialized */

    /* Memory is freed all at once when the allocator is destroyed */
    lexbor_mem_destroy(mem, true);

    return EXIT_SUCCESS;
}
```

**Important:** Memory allocated with `lexbor_mem_alloc()` cannot be individually freed — it is all released when the `lexbor_mem_t` is destroyed. For individual free capability, use `lexbor_mraw_t`.

### Alignment

`lexbor_mem_t` provides alignment helpers:

```C
/* Round up to alignment boundary (sizeof(void*)) */
size_t aligned = lexbor_mem_align(17);             /* -> 24 on 64-bit */

/* Round down to alignment boundary */
size_t aligned_floor = lexbor_mem_align_floor(17); /* -> 16 on 64-bit */
```

## Raw Memory Allocator (mraw)

### Location

Declared in `source/lexbor/core/mraw.h`.

### Purpose

A malloc/free-style allocator built on top of `lexbor_mem_t`. It adds two key features:

1. **Size tracking** — stores the allocation size in metadata before each block, so `realloc` and `free` don't need an explicit size parameter.
2. **Free block caching** — freed blocks are stored in a BST by size, so subsequent allocations can reuse them instead of allocating new memory.

### How It Works

```
Memory layout for an allocation:
+----------+----------------------+
| metadata | user data            |
| (size_t) | (returned pointer)   |
+----------+----------------------+
           ^
           pointer returned to caller
```

When you free memory, the block is inserted into a BST keyed by size. When you allocate again, the BST is searched for a matching or close-enough block.

### Example

```C
#include <lexbor/core/mraw.h>

int main(void) {
    lexbor_mraw_t *mraw = lexbor_mraw_create();
    lxb_status_t status = lexbor_mraw_init(mraw, 4096);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Allocate like malloc */
    void *data = lexbor_mraw_alloc(mraw, 128);

    /* Reallocate — size is tracked internally */
    data = lexbor_mraw_realloc(mraw, data, 256);

    /* Free — block goes to cache for reuse */
    lexbor_mraw_free(mraw, data);

    /* Next allocation may reuse the cached block */
    void *data2 = lexbor_mraw_alloc(mraw, 200);

    /* Duplicate memory block */
    const char *src = "Hello";
    void *copy = lexbor_mraw_dup(mraw, src, 6);

    /* Query allocation size */
    size_t size = lexbor_mraw_data_size(data2); /* -> 256 (from cached block) */

    lexbor_mraw_destroy(mraw, true);

    return EXIT_SUCCESS;
}
```

## Object Pool (dobject)

### Location

Declared in `source/lexbor/core/dobject.h`.

### Purpose

Fast allocation and recycling of fixed-size objects. Pre-allocates objects in chunks and maintains a cache of freed objects for instant reuse. This is the primary allocator for frequently created/destroyed objects like DOM nodes, hash entries, and tree nodes.

### How It Works

```
Chunk Memory (mem):
+-----+-----+-----+-----+-----+--------+
| obj | obj | obj | obj | obj | free   |
|  0  |  1  |  2  |  3  |  4  | space  |
+-----+-----+-----+-----+-----+--------+
  All objects are the same size (struct_size)

Cache (freed objects available for reuse):
+----------------------+
| ptr to obj 1         |
| ptr to obj 3         |
| (ready for reuse)    |
+----------------------+
```

When you call `alloc`:
1. If the cache has freed objects -> return one instantly
2. Otherwise -> allocate from the next position in the chunk

When you call `free`:
- The object pointer is added to the cache (not actually freed)

### Example

```C
#include <lexbor/core/dobject.h>

typedef struct {
    int x;
    int y;
    char name[32];
}
my_point_t;

int main(void) {
    lexbor_dobject_t *pool = lexbor_dobject_create();

    /* Init: 128 objects per chunk, each of sizeof(my_point_t) */
    lxb_status_t status = lexbor_dobject_init(pool, 128, sizeof(my_point_t));
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Allocate — uninitialized */
    my_point_t *p1 = lexbor_dobject_alloc(pool);

    /* Allocate — zero-initialized */
    my_point_t *p2 = lexbor_dobject_calloc(pool);
    p2->x = 10;
    p2->y = 20;

    /* Return to cache for reuse */
    lexbor_dobject_free(pool, p1);

    /* This may return the same memory as p1 */
    my_point_t *p3 = lexbor_dobject_alloc(pool);

    /* How many objects are currently allocated */
    size_t count = lexbor_dobject_allocated(pool);

    lexbor_dobject_destroy(pool, true);

    return EXIT_SUCCESS;
}
```

## Dynamic Array (array)

### Location

Declared in `source/lexbor/core/array.h`.

### Purpose

A growable array of `void *` pointers. Automatically expands when full. Used internally for caches, lists of nodes, and other collections where elements are pointers to objects.

### Example

```C
#include <lexbor/core/array.h>

int main(void) {
    lexbor_array_t *arr = lexbor_array_create();
    lxb_status_t status = lexbor_array_init(arr, 16); /* initial capacity */
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    int a = 10, b = 20, c = 30;

    /* Append elements */
    lexbor_array_push(arr, &a);
    lexbor_array_push(arr, &b);
    lexbor_array_push(arr, &c);

    /* Access by index */
    int *val = lexbor_array_get(arr, 1);  /* → &b */

    /* Remove last element */
    int *last = lexbor_array_pop(arr);    /* → &c */

    /* Insert at position */
    lexbor_array_insert(arr, 0, &c);

    /* Current length and capacity */
    size_t len = lexbor_array_length(arr); /* → 3 */
    size_t cap = lexbor_array_size(arr);   /* → 16 */

    lexbor_array_destroy(arr, true);

    return EXIT_SUCCESS;
}
```

## Object Array (array_obj)

### Location

Declared in `source/lexbor/core/array_obj.h`.

### Purpose

A growable array that stores fixed-size objects **inline** (contiguously in memory), unlike `lexbor_array_t` which stores pointers. This provides better cache locality because the objects themselves are packed together, not scattered across the heap.

**Important:** Because objects are stored inline in a contiguous buffer, any operation that grows the array (e.g., `push`) may trigger a `realloc`, which moves the entire buffer to a new address. After that, **all previously obtained pointers to elements become invalid**. Do not store pointers to `array_obj` elements long-term — always re-fetch them via `lexbor_array_obj_get()` after any operation that may grow the array.

### When to Use What

| | `lexbor_array_t` | `lexbor_array_obj_t` |
|---|---|---|
| **Stores** | Pointers (`void *`) | Objects inline (contiguous bytes) |
| **Cache locality** | Poor (objects scattered) | Excellent (objects packed) |
| **Element access** | Direct pointer dereference | Computed offset |
| **Use case** | Lists of existing objects | Collections of small structs |

### Example

```C
#include <lexbor/core/array_obj.h>

typedef struct {
    double x;
    double y;
}
point_t;

int main(void) {
    lexbor_array_obj_t *arr = lexbor_array_obj_create();

    /* Init: 32 slots, each sizeof(point_t) */
    lxb_status_t status = lexbor_array_obj_init(arr, 32, sizeof(point_t));
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Push returns pointer to new zero-initialized element */
    point_t *p1 = lexbor_array_obj_push(arr);
    p1->x = 1.0;
    p1->y = 2.0;

    point_t *p2 = lexbor_array_obj_push(arr);
    p2->x = 3.0;
    p2->y = 4.0;

    /* Push without zero-initialization (faster) */
    point_t *p3 = lexbor_array_obj_push_wo_cls(arr);
    p3->x = 5.0;
    p3->y = 6.0;

    /* Access by index */
    point_t *got = lexbor_array_obj_get(arr, 0);  /* → p1 */

    /* Get last element */
    point_t *last = lexbor_array_obj_last(arr);    /* → p3 */

    /* Length */
    size_t len = lexbor_array_obj_length(arr);     /* → 3 */

    lexbor_array_obj_destroy(arr, true);

    return EXIT_SUCCESS;
}
```

## Hash Table (hash)

### Location

Declared in `source/lexbor/core/hash.h`.

### Purpose

A hash table for string keys with collision chaining. Supports pluggable hash, compare, and copy functions — allowing case-sensitive, case-insensitive (lower or upper), and other custom strategies.

Used internally for storing tag names, attribute names, CSS properties, and namespace identifiers.

### Key Design Feature: Short String Optimization

Keys up to 16 bytes are stored **inline** in the entry structure, avoiding a separate memory allocation:

```
lexbor_hash_entry_t:
+------------------------------+
| union {                      |
|   short_str[17]  <= 16 bytes |  Inline, no extra allocation
|   *long_str       > 16 bytes |  Pointer to mraw-allocated string
| }                            |
| length                       |
| *next (collision chain)      |
+------------------------------+
```

### Insert/Search Strategies

Three built-in strategies are provided:

| Strategy | Insert | Search | Use Case |
|----------|--------|--------|----------|
| **Raw** | `lexbor_hash_insert_raw` | `lexbor_hash_search_raw` | Case-sensitive matching |
| **Lower** | `lexbor_hash_insert_lower` | `lexbor_hash_search_lower` | Keys stored lowercase |
| **Upper** | `lexbor_hash_insert_upper` | `lexbor_hash_search_upper` | Keys stored uppercase |

### Example

```C
#include <lexbor/core/hash.h>

int main(void) {
    lexbor_hash_t *hash = lexbor_hash_create();

    /* Init: 128 buckets, entry struct size */
    lxb_status_t status = lexbor_hash_init(hash, 128, sizeof(lexbor_hash_entry_t));
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Insert — case-sensitive */
    lexbor_hash_entry_t *entry;

    entry = lexbor_hash_insert(hash, lexbor_hash_insert_raw,
                               (lxb_char_t *) "div", 3);

    /* Search */
    entry = lexbor_hash_search(hash, lexbor_hash_search_raw,
                               (lxb_char_t *) "div", 3);
    if (entry != NULL) {
        /* Found. Access key string: */
        lxb_char_t *key = lexbor_hash_entry_str(entry);
        size_t key_len = entry->length;
    }

    /* Case-insensitive insert — key is stored in lowercase */
    entry = lexbor_hash_insert(hash, lexbor_hash_insert_lower,
                               (lxb_char_t *) "SPAN", 4);

    /* Case-insensitive search — "span", "SPAN", "Span" all match */
    entry = lexbor_hash_search(hash, lexbor_hash_search_lower,
                               (lxb_char_t *) "Span", 4);

    /* Remove */
    lexbor_hash_remove(hash, lexbor_hash_search_raw,
                       (lxb_char_t *) "div", 3);

    lexbor_hash_destroy(hash, true);

    return EXIT_SUCCESS;
}
```

### Custom Entry Extension

You can embed `lexbor_hash_entry_t` as the first field of a larger struct to attach custom data:

```C
typedef struct {
    lexbor_hash_entry_t entry;  /* Must be first field */
    int                 my_id;
    void                *my_data;
}
my_hash_entry_t;

/* Init with custom struct size */
lexbor_hash_init(hash, 128, sizeof(my_hash_entry_t));

/* Insert returns pointer to your extended entry */
my_hash_entry_t *my = lexbor_hash_insert(hash, lexbor_hash_insert_raw,
                                         (lxb_char_t *) "key", 3);
my->my_id = 42;
my->my_data = some_pointer;
```

## AVL Tree (avl)

### Location

Declared in `source/lexbor/core/avl.h`.

### Purpose

A self-balancing binary search tree. After every insertion or deletion, the tree automatically rebalances using rotations to maintain O(log n) height. The key is a `size_t` value (the `type` field), and each node carries a `void *` value.

### Algorithm

AVL trees maintain the invariant that for every node, the heights of the left and right subtrees differ by at most 1. When this invariant is violated after an insert or delete, the tree performs rotations (single or double) to restore balance.

- **Search:** O(log n)
- **Insert:** O(log n) — with at most 2 rotations
- **Delete:** O(log n) — with at most O(log n) rotations

### Example

```C
#include <lexbor/core/avl.h>

int main(void) {
    lexbor_avl_t *avl = lexbor_avl_create();
    lxb_status_t status = lexbor_avl_init(avl, 64, sizeof(lexbor_avl_node_t));
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    lexbor_avl_node_t *root = NULL;

    /* Insert nodes: key (type) → value */
    lexbor_avl_insert(avl, &root, 50, (void *) "fifty");
    lexbor_avl_insert(avl, &root, 30, (void *) "thirty");
    lexbor_avl_insert(avl, &root, 70, (void *) "seventy");
    lexbor_avl_insert(avl, &root, 10, (void *) "ten");

    /* Search by key */
    lexbor_avl_node_t *found = lexbor_avl_search(avl, root, 30);
    if (found != NULL) {
        printf("Found: %s\n", (char *) found->value);  /* → "thirty" */
    }

    /* Remove by key — returns the value */
    void *removed = lexbor_avl_remove(avl, &root, 30);

    /* Iterate all nodes */
    /* lexbor_avl_foreach(avl, &root, my_callback, my_ctx); */

    lexbor_avl_destroy(avl, true);

    return EXIT_SUCCESS;
}
```

## Binary Search Tree (bst)

### Location

Declared in `source/lexbor/core/bst.h`.

### Purpose

A simple (unbalanced) binary search tree keyed by `size_t`. Unlike AVL, it doesn't rebalance, so worst-case is O(n). However, it supports duplicate keys through linked lists (`next` pointer) and provides a "search closest" operation.

Used internally by `lexbor_mraw_t` to cache freed memory blocks by size, where the ability to find a close-enough block is more important than strict balance.

### Key Feature: Closest Search

`lexbor_bst_search_close()` finds the node with the smallest key that is greater than or equal to the requested size. This is essential for memory reuse — if you need 100 bytes and a 128-byte block is cached, that's close enough.

### Example

```C
#include <lexbor/core/bst.h>

int main(void) {
    lexbor_bst_t *bst = lexbor_bst_create();
    lxb_status_t status = lexbor_bst_init(bst, 64);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Insert: key (size) -> value */
    lexbor_bst_insert(bst, lexbor_bst_root_ref(bst), 128, (void *) "block_128");
    lexbor_bst_insert(bst, lexbor_bst_root_ref(bst), 256, (void *) "block_256");
    lexbor_bst_insert(bst, lexbor_bst_root_ref(bst), 64,  (void *) "block_64");

    /* Exact search */
    lexbor_bst_entry_t *entry = lexbor_bst_search(bst, lexbor_bst_root(bst), 128);

    /* Closest search — find smallest key ≥ 100 */
    entry = lexbor_bst_search_close(bst, lexbor_bst_root(bst), 100);
    /* -> returns node with key 128 */

    /* Remove by key — returns value */
    void *val = lexbor_bst_remove(bst, lexbor_bst_root_ref(bst), 128);

    lexbor_bst_destroy(bst, true);

    return EXIT_SUCCESS;
}
```

## BST Map (bst_map)

### Location

Declared in `source/lexbor/core/bst_map.h`.

### Purpose

A BST specialized for string keys. Wraps `lexbor_bst_t` with `lexbor_str_t` keys and provides insert/search/remove by string. Used for tag name tables, attribute mappings, and other string-keyed associative arrays.

### Example

```C
#include <lexbor/core/bst_map.h>

int main(void) {
    lexbor_bst_map_t *map = lexbor_bst_map_create();
    lxb_status_t status = lexbor_bst_map_init(map, 64);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Insert string key → value */
    lexbor_bst_map_entry_t *entry;

    entry = lexbor_bst_map_insert(map, lexbor_bst_map_root_ref(map),
                                  (lxb_char_t *) "content-type", 12);
    if (entry != NULL) {
        entry->value = (void *) "text/html";
    }

    /* Search by string */
    entry = lexbor_bst_map_search(map, lexbor_bst_map_root(map),
                                  (lxb_char_t *) "content-type", 12);
    if (entry != NULL) {
        printf("Value: %s\n", (char *) entry->value);
    }

    /* Insert only if not exists */
    entry = lexbor_bst_map_insert_not_exists(map, lexbor_bst_map_root_ref(map),
                                             (lxb_char_t *) "content-type", 12);
    /* -> returns existing entry without creating a duplicate */

    lexbor_bst_map_destroy(map, true);

    return EXIT_SUCCESS;
}
```

## String (str)

### Location

Declared in `source/lexbor/core/str.h`.

### Purpose

A mutable, dynamically-growing string backed by `lexbor_mraw_t`. The string buffer is null-terminated, and the allocation size is tracked in mraw metadata (stored before the buffer), so reallocation and size queries are efficient.

### Structure

```C
typedef struct {
    lxb_char_t *data;    /* null-terminated buffer */
    size_t     length;   /* string length (not including null terminator) */
}
lexbor_str_t;
```

### Example

```C
#include <lexbor/core/str.h>
#include <lexbor/core/mraw.h>

int main(void) {
    lexbor_mraw_t *mraw = lexbor_mraw_create();
    lexbor_mraw_init(mraw, 4096);

    /* Create and initialize a string */
    lexbor_str_t str = {0};
    lexbor_str_init(&str, mraw, 64); /* pre-allocate 64 bytes */

    /* Append data */
    lexbor_str_append(&str, mraw, (lxb_char_t *) "Hello", 5);
    lexbor_str_append(&str, mraw, (lxb_char_t *) ", ", 2);
    lexbor_str_append(&str, mraw, (lxb_char_t *) "World!", 6);

    /* Append single character */
    lexbor_str_append_one(&str, mraw, '!');

    printf("%s\n", str.data);             /* -> "Hello, World!!" */
    printf("Length: %zu\n", str.length);  /* -> 14 */

    /* Append with lowercasing */
    lexbor_str_t lower = {0};
    lexbor_str_init(&lower, mraw, 32);
    lexbor_str_append_lowercase(&lower, mraw,
                                (lxb_char_t *) "DIV", 3);
    printf("%s\n", lower.data);  /* → "div" */

    /* Copy string */
    lexbor_str_t copy = {0};
    lexbor_str_copy(&copy, &str, mraw);

    /* Whitespace operations */
    lexbor_str_t ws = {0};
    lexbor_str_init_append(&ws, mraw, (lxb_char_t *) "  hello   world  ", 17);
    lexbor_str_strip_collapse_whitespace(&ws);
    printf("'%s'\n", ws.data);  /* → "hello world" */

    /* Cleanup */
    /* 
    lexbor_str_destroy(&str, mraw, false);
    lexbor_str_destroy(&lower, mraw, false);
    lexbor_str_destroy(&copy, mraw, false);
    lexbor_str_destroy(&ws, mraw, false);
    */

    /* Destroy all */
    lexbor_mraw_destroy(mraw, true);

    return EXIT_SUCCESS;
}
```

### String Comparison Functions

The module provides a rich set of comparison functions:

| Function | Description |
|----------|-------------|
| `lexbor_str_data_ncmp()` | Case-sensitive comparison, N bytes |
| `lexbor_str_data_ncasecmp()` | Case-insensitive comparison, N bytes |
| `lexbor_str_data_cmp()` | Case-sensitive, null-terminated |
| `lexbor_str_data_casecmp()` | Case-insensitive, null-terminated |
| `lexbor_str_data_ncmp_contain()` | Check if one buffer contains another |
| `lexbor_str_data_ncasecmp_contain()` | Same, case-insensitive |
| `lexbor_str_data_nlocmp_right()` | Compare with right side lowercased |

## Static BST (sbst)

### Location

Declared in `source/lexbor/core/sbst.h`.

### Purpose

A read-only binary search tree compiled into a static array. Used for character-by-character lookup tables generated at build time (e.g., HTML entity names, tag name recognition). Zero runtime allocation — the tree is just an array of structs with index-based navigation.

### Structure

```C
typedef struct {
    lxb_char_t key;       /* character to match */
    void       *value;    /* associated data */
    size_t     left;      /* index of left child (0 = none) */
    size_t     right;     /* index of right child (0 = none) */
    size_t     next;      /* index of next character in sequence */
}
lexbor_sbst_entry_static_t;
```

The tree is traversed by reading one character at a time and following `left`/`right` indices to find a match, then following `next` to match the next character in the string.

### Usage

Static BSTs are generated at build time and used as constant arrays. They are not created at runtime.

## Static Hash Search (shs)

### Location

Declared in `source/lexbor/core/shs.h`.

### Purpose

A compile-time hash table for small, static datasets. The table is a constant array — no allocation or initialization needed at runtime. Used for looking up HTML entity names, CSS keywords, and other fixed sets of string keys.

### How It Works

Uses modulo hashing with collision chains stored as array indices. Lookup is O(1) average case.

```C
typedef struct {
    char     *key;
    void     *value;
    size_t   key_len;
    size_t   next;     /* collision chain — index in array (0 = end) */
}
lexbor_shs_entry_t;
```

### Usage

Static hash tables are generated at build time. Runtime code simply calls inline search functions on the constant array data.

## Parse Log (plog)

### Location

Declared in `source/lexbor/core/plog.h`.

### Purpose

Collects parse errors and warnings during HTML/CSS parsing. Errors are stored in an object array for deferred processing — no exceptions or immediate error handling needed. This follows the WHATWG specification approach where parsing errors are recorded but processing continues.

### Structure

```C
typedef struct {
    const lxb_char_t *data;    /* position in source where error occurred */
    void             *context; /* parser context */
    unsigned         id;       /* error code/type */
}
lexbor_plog_entry_t;
```

### Example

```C
#include <lexbor/core/plog.h>

int main(void) {
    lexbor_plog_t plog;
    lxb_status_t status = lexbor_plog_init(&plog, 16, sizeof(lexbor_plog_entry_t));
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* During parsing, errors are pushed */
    const lxb_char_t *error_pos = (lxb_char_t *) "<div";
    lexbor_plog_push(&plog, error_pos, NULL, 0x01);

    /* After parsing, check errors */
    size_t count = lexbor_plog_length(&plog);
    printf("Parse errors: %zu\n", count);

    lexbor_plog_destroy(&plog, false);

    return EXIT_SUCCESS;
}
```

## Conversions (conv, dtoa, strtod)

### Location

Declared in `source/lexbor/core/conv.h`, `source/lexbor/core/dtoa.h`, `source/lexbor/core/strtod.h`.

### Purpose

Fast and accurate number <--> string conversions. The `conv` module provides the public API, while `dtoa` (double-to-ASCII) and `strtod` (string-to-double) implement the core algorithms using the Grisu2 algorithm for precise floating-point formatting.

### Functions

| Function | Description |
|----------|-------------|
| `lexbor_conv_float_to_data()` | `double` → decimal string |
| `lexbor_conv_long_to_data()` | `long` → decimal string |
| `lexbor_conv_int64_to_data()` | `int64_t` → decimal string |
| `lexbor_conv_data_to_double()` | String → `double` |
| `lexbor_conv_data_to_ulong()` | String → `unsigned long` |
| `lexbor_conv_data_to_long()` | String → `long` |
| `lexbor_conv_data_to_uint()` | String → `unsigned int` |
| `lexbor_conv_dec_to_hex()` | Decimal → hexadecimal string |

### Example

```C
#include <lexbor/core/conv.h>

int main(void) {
    lxb_char_t buf[64];

    /* Number to string */
    size_t len = lexbor_conv_float_to_data(3.14159, buf, sizeof(buf));
    printf("Float: %.*s\n", (int) len, buf);

    len = lexbor_conv_long_to_data(-42, buf, sizeof(buf));
    printf("Long: %.*s\n", (int) len, buf);

    /* String to number */
    const lxb_char_t *str = (lxb_char_t *) "123.456";
    double val = lexbor_conv_data_to_double(&str, 7);
    printf("Parsed: %f\n", val);

    /* Decimal to hex */
    len = lexbor_conv_dec_to_hex(255, buf, sizeof(buf), false);
    printf("Hex: %.*s\n", (int) len, buf); /* -> "ff" */

    return EXIT_SUCCESS;
}
```

## Serialization (serialize)

### Location

Declared in `source/lexbor/core/serialize.h`.

### Purpose

Provides a callback-based output abstraction for serializing data. Instead of always writing to a string, serialization code writes through a callback function — allowing output to go to strings, files, network sockets, or just be counted.

### Built-in Callbacks

| Callback | Purpose |
|----------|---------|
| `lexbor_serialize_copy_cb()` | Copy data to a `lexbor_str_t` buffer |
| `lexbor_serialize_length_cb()` | Count output bytes without writing (dry run) |

### Helper Macro

```C
/* Write data through callback with error handling */
lexbor_serialize_write(callback, data, length, ctx, status);
```

This macro calls the callback and checks the return status — if the callback returns an error, the macro immediately returns from the calling function.

### Context Structure

```C
typedef struct {
    lexbor_serialize_cb_f cb;    /* output callback */
    void                  *ctx;  /* callback context */
    intptr_t              opt;   /* serialization options */
    size_t                count; /* bytes written */
}
lexbor_serialize_ctx_t;
```

## SWAR (swar)

### Location

Declared in `source/lexbor/core/swar.h`.

### Purpose

SWAR (SIMD Within A Register) is a technique for processing multiple bytes at once using standard integer operations, without requiring actual SIMD instructions. It searches for specific characters by processing `sizeof(size_t)` bytes (typically 8 on 64-bit systems) per iteration.

Based on the [Stanford Bithacks](https://graphics.stanford.edu/~seander/bithacks.html) collection.

### How It Works

The algorithm broadcasts a target character across a machine word, XORs it with the data, and checks for zero bytes (which indicate a match). This allows scanning 4 or 8 bytes per iteration instead of 1.

### Functions

| Function | Description |
|----------|-------------|
| `lexbor_swar_seek4()` | Find first occurrence of any of 4 characters |
| `lexbor_swar_seek3()` | Find first occurrence of any of 3 characters |

### Usage

SWAR functions are used in hot parsing loops to quickly skip past irrelevant characters. For example, the HTML tokenizer can use `lexbor_swar_seek4()` to find the next `<`, `>`, `&`, or `\0` character in the input — processing 8 bytes at a time.

```C
#include <lexbor/core/swar.h>

const lxb_char_t *data = (lxb_char_t *) "Hello, World!<div>";
const lxb_char_t *end = data + 18;

/* Find first '<', '>', '&', or '\0' */
const lxb_char_t *found = lexbor_swar_seek4(data, end, '<', '>', '&', '\0');
/* found now points close to or at '<' */
```

## Status Codes

### Location

Defined in `source/lexbor/core/base.h`.

### Purpose

All lexbor functions use `lxb_status_t` (alias for `lexbor_status_t`) for error reporting. A function succeeds if it returns `LXB_STATUS_OK` (0).

### Status Values

| Status | Value | Description |
|--------|-------|-------------|
| `LXB_STATUS_OK` | `0x0000` | Success |
| `LXB_STATUS_ERROR` | `0x0001` | Generic error |
| `LXB_STATUS_ERROR_MEMORY_ALLOCATION` | `0x0002` | malloc/alloc failed |
| `LXB_STATUS_ERROR_OBJECT_IS_NULL` | `0x0003` | NULL pointer passed |
| `LXB_STATUS_ERROR_SMALL_BUFFER` | `0x0004` | Buffer too small |
| `LXB_STATUS_ERROR_INCOMPLETE_OBJECT` | `0x0005` | Object not fully initialized |
| `LXB_STATUS_ERROR_NO_FREE_SLOT` | `0x0006` | No available slot |
| `LXB_STATUS_ERROR_TOO_SMALL_SIZE` | `0x0007` | Requested size too small |
| `LXB_STATUS_ERROR_NOT_EXISTS` | `0x0008` | Entry not found |
| `LXB_STATUS_ERROR_WRONG_ARGS` | `0x0009` | Invalid arguments |
| `LXB_STATUS_ERROR_WRONG_STAGE` | `0x000A` | Wrong operation stage |
| `LXB_STATUS_ERROR_UNEXPECTED_RESULT` | `0x000B` | Unexpected result |
| `LXB_STATUS_ERROR_UNEXPECTED_DATA` | `0x000C` | Unexpected data |
| `LXB_STATUS_ERROR_OVERFLOW` | `0x000D` | Numeric overflow |
| `LXB_STATUS_CONTINUE` | `0x000E` | Continue processing |
| `LXB_STATUS_SMALL_BUFFER` | `0x000F` | Buffer too small (non-error) |
| `LXB_STATUS_ABORTED` | `0x0010` | Operation aborted |
| `LXB_STATUS_STOPPED` | `0x0011` | Operation stopped |
| `LXB_STATUS_NEXT` | `0x0012` | Move to next |
| `LXB_STATUS_STOP` | `0x0013` | Stop processing |
| `LXB_STATUS_WARNING` | `0x0014` | Warning |

### Callback Action Codes

For iteration callbacks, `lexbor_action_t` controls the flow:

| Action | Description |
|--------|-------------|
| `LEXBOR_ACTION_OK` | Continue iteration |
| `LEXBOR_ACTION_STOP` | Stop iteration |
| `LEXBOR_ACTION_NEXT` | Skip to next item |

### Error Handling Pattern

There is no need to check the return value of `create()` for NULL separately. If `create()` fails (returns NULL) and you pass NULL to `init()`, it will return `LXB_STATUS_ERROR_OBJECT_IS_NULL`. So it is enough to check only the `init()` result:

```C
lexbor_xxx_t *obj = lexbor_xxx_create();

lxb_status_t status = lexbor_xxx_init(obj, ...);
if (status != LXB_STATUS_OK) {
    lexbor_xxx_destroy(obj, true);
    return EXIT_FAILURE;
}

/* Use the object... */

lexbor_xxx_destroy(obj, true);
```
