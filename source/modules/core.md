# Core Module

* **Version:** 2.7.0
* **Path:** `source/lexbor/core`
* **Base Includes:** `lexbor/core/core.h`
* **Examples:** not present
* **Specification:** not present

## Overview

The Core module is the foundation of lexbor. It implements essential data structures, memory management, and utilities used by all other modules. Written in pure C99 with zero external dependencies.

## Status Codes (`lxb_status_t`)

All lexbor functions return `lxb_status_t` for error handling. Defined in `lexbor/core/base.h`.

```c
typedef enum {
    LXB_STATUS_OK                      = 0x0000,
    LXB_STATUS_ERROR                   = 0x0001,
    LXB_STATUS_ERROR_MEMORY_ALLOCATION,
    LXB_STATUS_ERROR_OBJECT_IS_NULL,
    LXB_STATUS_ERROR_SMALL_BUFFER,
    LXB_STATUS_ERROR_INCOMPLETE_OBJECT,
    LXB_STATUS_ERROR_NO_FREE_SLOT,
    LXB_STATUS_ERROR_TOO_SMALL_SIZE,
    LXB_STATUS_ERROR_NOT_EXISTS,
    LXB_STATUS_ERROR_WRONG_ARGS,
    LXB_STATUS_ERROR_WRONG_STAGE,
    LXB_STATUS_CONTINUE,
    LXB_STATUS_STOP,
    LXB_STATUS_ABORTED,
    LXB_STATUS_STOPPED,
    LXB_STATUS_NEXT,
    LXB_STATUS_WARNING
} lxb_status_t;
```

`LXB_STATUS_OK` (`0x0000`) indicates success. All other values indicate errors or control flow signals.


## Action Type (`lexbor_action_t`)

Used as callback return values to control iteration:

```c
typedef enum {
    LEXBOR_ACTION_OK   = 0x00,  /* continue */
    LEXBOR_ACTION_STOP = 0x01,  /* stop iteration */
    LEXBOR_ACTION_NEXT = 0x02   /* skip to next */
} lexbor_action_t;
```


## Base Types

Common types used across all modules (defined in `lexbor/core/base.h`):

- `lxb_char_t` — character type (`unsigned char`)
- `lxb_codepoint_t` — Unicode code point
- `lexbor_serialize_cb_f` — serialization callback: `lxb_status_t (*)(const lxb_char_t *data, size_t len, void *ctx)`
- `lexbor_callback_f` — general callback: `lxb_status_t (*)(const lxb_char_t *data, size_t len, void *ctx)`


## Memory Allocator (`lexbor_mraw_t`)

A pooled memory allocator with caching for reallocation. Used throughout lexbor for efficient allocation. Defined in `lexbor/core/mraw.h`.

```c
typedef struct {
    lexbor_mem_t  *mem;
    lexbor_bst_t  *cache;
    size_t        ref_count;
} lexbor_mraw_t;
```

### Lifecycle

```c
lexbor_mraw_t *
lexbor_mraw_create(void);

lxb_status_t
lexbor_mraw_init(lexbor_mraw_t *mraw, size_t chunk_size);

void
lexbor_mraw_clean(lexbor_mraw_t *mraw);

lexbor_mraw_t *
lexbor_mraw_destroy(lexbor_mraw_t *mraw, bool destroy_self);
```

### Allocation

```c
void *lexbor_mraw_alloc(lexbor_mraw_t *mraw, size_t size);
void *lexbor_mraw_calloc(lexbor_mraw_t *mraw, size_t size);
void *lexbor_mraw_realloc(lexbor_mraw_t *mraw, void *data, size_t new_size);
void  lexbor_mraw_free(lexbor_mraw_t *mraw, void *data);
```

### Utility

```c
/* Duplicate a memory block */
void *lexbor_mraw_dup(lexbor_mraw_t *mraw, const void *src, size_t size);

/* Get the allocated size of a block */
size_t lexbor_mraw_data_size(void *data);

/* Get reference count */
size_t lexbor_mraw_reference_count(lexbor_mraw_t *mraw);
```


## Dynamic Object Pool (`lexbor_dobject_t`)

A pool allocator for frequently created and destroyed fixed-size objects. Allocates objects from chunks and recycles freed objects via an internal cache. Defined in `lexbor/core/dobject.h`.

```c
typedef struct {
    lexbor_mem_t   *mem;
    lexbor_array_t *cache;
    size_t         allocated;
    size_t         struct_size;
} lexbor_dobject_t;
```

### Lifecycle

```c
lexbor_dobject_t *
lexbor_dobject_create(void);

lxb_status_t
lexbor_dobject_init(lexbor_dobject_t *dobject, size_t chunk_size, size_t struct_size);

void
lexbor_dobject_clean(lexbor_dobject_t *dobject);

lexbor_dobject_t *
lexbor_dobject_destroy(lexbor_dobject_t *dobject, bool destroy_self);
```

### Operations

```c
void *lexbor_dobject_alloc(lexbor_dobject_t *dobject);   /* allocate (uninitialized) */
void *lexbor_dobject_calloc(lexbor_dobject_t *dobject);  /* allocate (zeroed) */
void *lexbor_dobject_free(lexbor_dobject_t *dobject, void *data);  /* return to pool */

void *lexbor_dobject_by_absolute_position(lexbor_dobject_t *dobject, size_t pos);

size_t lexbor_dobject_allocated(lexbor_dobject_t *dobject);      /* total allocated */
size_t lexbor_dobject_cache_length(lexbor_dobject_t *dobject);   /* cached (free) count */
```


## Array (`lexbor_array_t`)

A dynamic array of `void *` pointers. Defined in `lexbor/core/array.h`.

```c
typedef struct {
    void   **list;
    size_t size;      /* capacity */
    size_t length;    /* current count */
} lexbor_array_t;
```

### Lifecycle

```c
lexbor_array_t *
lexbor_array_create(void);

lxb_status_t
lexbor_array_init(lexbor_array_t *array, size_t size);

void
lexbor_array_clean(lexbor_array_t *array);

lexbor_array_t *
lexbor_array_destroy(lexbor_array_t *array, bool self_destroy);
```

### Operations

```c
lxb_status_t lexbor_array_expand(lexbor_array_t *array, size_t up_to);
lxb_status_t lexbor_array_push(lexbor_array_t *array, void *value);
void *       lexbor_array_pop(lexbor_array_t *array);
lxb_status_t lexbor_array_insert(lexbor_array_t *array, size_t idx, void *value);
lxb_status_t lexbor_array_set(lexbor_array_t *array, size_t idx, void *value);
void         lexbor_array_delete(lexbor_array_t *array, size_t begin, size_t length);

void * lexbor_array_get(const lexbor_array_t *array, size_t idx);  /* NULL if out of bounds */
size_t lexbor_array_length(lexbor_array_t *array);
size_t lexbor_array_size(lexbor_array_t *array);
```


## Object Array (`lexbor_array_obj_t`)

A dynamic array that stores objects by value (not by pointer). Elements are stored in a contiguous byte buffer, accessed by index and struct size. Defined in `lexbor/core/array_obj.h`.

```c
typedef struct {
    uint8_t *list;
    size_t  size;          /* capacity */
    size_t  length;        /* current count */
    size_t  struct_size;   /* size of each element */
} lexbor_array_obj_t;
```

### Lifecycle

```c
lexbor_array_obj_t *
lexbor_array_obj_create(void);

lxb_status_t
lexbor_array_obj_init(lexbor_array_obj_t *array, size_t size, size_t struct_size);

void
lexbor_array_obj_clean(lexbor_array_obj_t *array);

lexbor_array_obj_t *
lexbor_array_obj_destroy(lexbor_array_obj_t *array, bool self_destroy);
```

### Operations

```c
void *lexbor_array_obj_push(lexbor_array_obj_t *array);       /* allocate and zero at end */
void *lexbor_array_obj_push_wo_cls(lexbor_array_obj_t *array); /* allocate without zeroing */
void *lexbor_array_obj_push_n(lexbor_array_obj_t *array, size_t count); /* allocate N */
void *lexbor_array_obj_pop(lexbor_array_obj_t *array);         /* remove last */
void  lexbor_array_obj_delete(lexbor_array_obj_t *array, size_t begin, size_t length);

void * lexbor_array_obj_get(const lexbor_array_obj_t *array, size_t idx);
void * lexbor_array_obj_last(lexbor_array_obj_t *array);
size_t lexbor_array_obj_length(lexbor_array_obj_t *array);
size_t lexbor_array_obj_size(lexbor_array_obj_t *array);
size_t lexbor_array_obj_struct_size(lexbor_array_obj_t *array);
```

Note: `push()` returns a pointer to the newly allocated slot in the array. The caller writes the object data into this slot.


## String (`lexbor_str_t`)

Dynamically resizable string. Uses `lexbor_mraw_t` for memory allocation. Defined in `lexbor/core/str.h`.

```c
typedef struct {
    lxb_char_t *data;
    size_t     length;
} lexbor_str_t;
```

### Lifecycle

```c
lexbor_str_t *
lexbor_str_create(void);

lxb_char_t *
lexbor_str_init(lexbor_str_t *str, lexbor_mraw_t *mraw, size_t size);

lxb_char_t *
lexbor_str_init_append(lexbor_str_t *str, lexbor_mraw_t *mraw,
                       const lxb_char_t *data, size_t length);

void
lexbor_str_clean(lexbor_str_t *str);

void
lexbor_str_clean_all(lexbor_str_t *str);

lexbor_str_t *
lexbor_str_destroy(lexbor_str_t *str, lexbor_mraw_t *mraw, bool destroy_obj);
```

### Operations

```c
/* Resize */
lxb_char_t *lexbor_str_realloc(lexbor_str_t *str, lexbor_mraw_t *mraw, size_t new_size);
lxb_char_t *lexbor_str_check_size(lexbor_str_t *str, lexbor_mraw_t *mraw, size_t plus_len);

/* Append */
lxb_char_t *lexbor_str_append(lexbor_str_t *str, lexbor_mraw_t *mraw,
                               const lxb_char_t *data, size_t length);
lxb_char_t *lexbor_str_append_before(lexbor_str_t *str, lexbor_mraw_t *mraw,
                                      const lxb_char_t *buff, size_t length);
lxb_char_t *lexbor_str_append_one(lexbor_str_t *str, lexbor_mraw_t *mraw, lxb_char_t data);
lxb_char_t *lexbor_str_append_lowercase(lexbor_str_t *str, lexbor_mraw_t *mraw,
                                         const lxb_char_t *data, size_t length);

/* Copy */
lxb_char_t *lexbor_str_copy(lexbor_str_t *dest, const lexbor_str_t *target,
                             lexbor_mraw_t *mraw);

/* Whitespace */
void lexbor_str_stay_only_whitespace(lexbor_str_t *target);
void lexbor_str_strip_collapse_whitespace(lexbor_str_t *target);
void lexbor_str_crop_whitespace_from_begin(lexbor_str_t *target);
```

### Accessors

```c
lxb_char_t *lexbor_str_data(lexbor_str_t *str);
size_t      lexbor_str_length(lexbor_str_t *str);
size_t      lexbor_str_size(lexbor_str_t *str);
```

### Data Comparison Functions

```c
/* Exact match */
const lxb_char_t *lexbor_str_data_ncmp(const lxb_char_t *first,
                                        const lxb_char_t *sec, size_t size);
bool lexbor_str_data_cmp(const lxb_char_t *first, const lxb_char_t *sec);

/* Case-insensitive */
const lxb_char_t *lexbor_str_data_ncasecmp(const lxb_char_t *first,
                                            const lxb_char_t *sec, size_t size);
bool lexbor_str_data_casecmp(const lxb_char_t *first, const lxb_char_t *sec);

/* Substring search */
const lxb_char_t *lexbor_str_data_ncmp_contain(const lxb_char_t *where, size_t where_size,
                                                const lxb_char_t *what, size_t what_size);
const lxb_char_t *lexbor_str_data_ncasecmp_contain(const lxb_char_t *where, size_t where_size,
                                                    const lxb_char_t *what, size_t what_size);

/* Case conversion */
lxb_char_t *lexbor_str_data_to_lowercase(lxb_char_t *to, const lxb_char_t *from, size_t len);
lxb_char_t *lexbor_str_data_to_uppercase(lxb_char_t *to, const lxb_char_t *from, size_t len);
```


## Hash Table (`lexbor_hash_t`)

Hash table with configurable key handling, collision chaining, and short string optimization for keys. Defined in `lexbor/core/hash.h`.

### Key Types

```c
typedef struct {
    lexbor_dobject_t    *entries;
    lexbor_mraw_t       *mraw;
    lexbor_hash_entry_t **table;
    size_t              table_size;
    size_t              struct_size;
} lexbor_hash_t;

typedef struct {
    union {
        lxb_char_t *long_str;
        lxb_char_t short_str[LEXBOR_HASH_SHORT_SIZE + 1];  /* 17 bytes inline */
    } u;
    size_t              length;
    lexbor_hash_entry_t *next;
} lexbor_hash_entry_t;
```

Hash entries use short string optimization: keys up to 16 bytes are stored inline in `short_str`, avoiding a separate allocation. `LEXBOR_HASH_SHORT_SIZE` is `16`.

### Lifecycle

```c
lexbor_hash_t *
lexbor_hash_create(void);

lxb_status_t
lexbor_hash_init(lexbor_hash_t *hash, size_t table_size, size_t struct_size);

void
lexbor_hash_clean(lexbor_hash_t *hash);

lexbor_hash_t *
lexbor_hash_destroy(lexbor_hash_t *hash, bool destroy_obj);
```

The `struct_size` parameter allows embedding custom data after the hash entry header. Pass `sizeof(lexbor_hash_entry_t)` for entries with no extra data.

### Operations

```c
lexbor_hash_entry_t *
lexbor_hash_insert(lexbor_hash_t *hash, const lexbor_hash_insert_t *insert,
                   const lxb_char_t *key, size_t length);

lexbor_hash_entry_t *
lexbor_hash_search(lexbor_hash_t *hash, const lexbor_hash_search_t *search,
                   const lxb_char_t *key, size_t length);

void *
lexbor_hash_remove(lexbor_hash_t *hash, const lexbor_hash_search_t *search,
                   const lxb_char_t *key, size_t length);
```

Pre-defined insert/search strategies:

- `lexbor_hash_insert_raw` / `lexbor_hash_search_raw` — exact key matching
- `lexbor_hash_insert_lower` / `lexbor_hash_search_lower` — case-insensitive (lowercase)
- `lexbor_hash_insert_upper` / `lexbor_hash_search_upper` — case-insensitive (uppercase)


## AVL Tree (`lexbor_avl_t`)

Self-balancing AVL tree for ordered data. Defined in `lexbor/core/avl.h`.

```c
typedef struct {
    lexbor_dobject_t  *nodes;
    lexbor_avl_node_t *last_right;
} lexbor_avl_t;

typedef struct lexbor_avl_node {
    size_t                  type;    /* key */
    short                   height;
    void                    *value;
    struct lexbor_avl_node  *left;
    struct lexbor_avl_node  *right;
    struct lexbor_avl_node  *parent;
} lexbor_avl_node_t;
```

### Lifecycle

```c
lexbor_avl_t *lexbor_avl_create(void);
lxb_status_t  lexbor_avl_init(lexbor_avl_t *avl, size_t chunk_len, size_t struct_size);
void          lexbor_avl_clean(lexbor_avl_t *avl);
lexbor_avl_t *lexbor_avl_destroy(lexbor_avl_t *avl, bool self_destroy);
```

### Operations

```c
lexbor_avl_node_t *lexbor_avl_insert(lexbor_avl_t *avl, lexbor_avl_node_t **scope,
                                      size_t type, void *value);
lexbor_avl_node_t *lexbor_avl_search(lexbor_avl_t *avl, lexbor_avl_node_t *scope,
                                      size_t type);
void *             lexbor_avl_remove(lexbor_avl_t *avl, lexbor_avl_node_t **scope,
                                      size_t type);

lxb_status_t lexbor_avl_foreach(lexbor_avl_t *avl, lexbor_avl_node_t **scope,
                                 lexbor_avl_node_f cb, void *ctx);
```

The `scope` parameter is a pointer to the root node pointer, allowing the tree to update the root during balancing.


## Key Features

- **Zero Dependencies** — pure C99, no external libraries required
- **Object Lifecycle** — all types follow the `create`/`init`/`clean`/`destroy` pattern
- **Dual Function Variants** — performance-critical accessors have both inline and non-inline (`_noi`) versions for ABI stability
- **Pool Allocation** — `lexbor_dobject_t` recycles fixed-size objects; `lexbor_mraw_t` provides general-purpose pooled allocation
- **Platform Abstraction** — portable across operating systems via `source/lexbor/ports/`
