# Core Module

* **Version:** 2.7.0
* **Path:** `source/lexbor/core`
* **Base Includes:** `lexbor/core/core.h`
* **Examples:** not present
* **Specification:** not present

## Overview

The Core module is the foundation of lexbor. It implements essential data structures, algorithms, and memory management used by all other modules.

Core provides the building blocks that all other modules depend on. It's written in pure C99 with zero external dependencies, making it highly portable and easy to embed.

## What's Inside

- **Memory Management** — custom allocators optimized for parser performance
  - `lexbor_malloc`, `lexbor_calloc`, `lexbor_realloc`, `lexbor_free`
  - Memory pools for fast object allocation

- **Data Structures**
  - AVL trees — self-balancing binary search trees
  - BST trees — binary search trees
  - Arrays — dynamic arrays with automatic growth
  - Strings — efficient string handling with SSO (Small String Optimization)
  - Hash tables — fast key-value lookups
  - Vectors — generic dynamic arrays

- **Base Types** — common types used across all modules
  - `lxb_status_t` — status codes for error handling
  - `lxb_char_t` — character type (unsigned char)
  - `lxb_codepoint_t` — Unicode code point
  - and more...

- **Utilities**
  - String operations (case conversion, comparison, hashing)
  - Number parsing and conversion
  - Bit operations
  - Debugging helpers

## Key Features

- **Zero Dependencies** — pure C99, no external libraries required
- **Performance-Optimized** — custom algorithms tuned for parser workloads
- **Memory Efficient** — pooled allocation reduces fragmentation
- **Platform Abstraction** — portable across different operating systems

*(Documentation is currently being developed, details will be available here soon.)*
