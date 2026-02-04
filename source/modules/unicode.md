# Unicode Module

* **Version:** 0.4.0
* **Path:** `source/lexbor/unicode`
* **Base Includes:** `lexbor/unicode/unicode.h`
* **Examples:** `examples/lexbor/unicode`
* **Specifications:** [Unicode TR#15 (Normalization Forms)](https://www.unicode.org/reports/tr15/), [Unicode TR#46 (IDNA Compatibility Processing)](https://www.unicode.org/reports/tr46/)

## Overview

The Unicode module implements Unicode normalization algorithms and IDNA (Internationalized Domain Names in Applications) processing according to Unicode Technical Reports.
The module provides complete support for all four Unicode normalization forms (NFC, NFD, NFKC, NFKD) and domain name internationalization with Punycode encoding.

## Key Features

- **Specification Compliant** — follows Unicode TR#15 and TR#46 standards
- **Four Normalization Forms** — NFC, NFD, NFKC, NFKD
- **Streaming Support** — normalize data incrementally by chunks
- **Quick Check** — fast detection if normalization is needed
- **IDNA Processing** — domain name mapping, validation, and conversion
- **Punycode** — ASCII-compatible encoding for internationalized domain names
- **Two Input Modes**:
  - **UTF-8 characters** — work directly with UTF-8 encoded strings
  - **Code points** — work with Unicode code points array

## What's Inside

- **[Quick Start](#quick-start)** — basic examples for normalization and IDNA
- **[Normalization](#normalization)** — Unicode text normalization (NFC, NFD, NFKC, NFKD)
- **[Quick Check](#quick-check)** — fast check if text needs normalization
- **[IDNA Processing](#idna-processing)** — internationalized domain name handling

## Quick Start

### Basic Normalization (NFC)

```C
#include <lexbor/unicode/unicode.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    /* U+1E9B U+0323 — LATIN SMALL LETTER LONG S WITH DOT ABOVE + COMBINING DOT BELOW */
    lxb_char_t source[] = "\u1E9B\u0323";

    /* Create normalizer */
    lxb_unicode_normalizer_t *uc = lxb_unicode_normalizer_create();
    if (uc == NULL) {
        return EXIT_FAILURE;
    }

    /* Initialize with NFC form */
    lxb_status_t status = lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);
    if (status != LXB_STATUS_OK) {
        lxb_unicode_normalizer_destroy(uc, true);
        return EXIT_FAILURE;
    }

    /* Normalize */
    status = lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                                   callback, NULL, true);
    if (status != LXB_STATUS_OK) {
        lxb_unicode_normalizer_destroy(uc, true);
        return EXIT_FAILURE;
    }

    /* Cleanup */
    lxb_unicode_normalizer_destroy(uc, true);

    return EXIT_SUCCESS;
}
```

### Basic IDNA (Domain to ASCII)

```C
#include <lexbor/unicode/unicode.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    /* Unicode domain name */
    const lxb_char_t domain[] = "привет.рф";

    /* Create IDNA processor */
    lxb_unicode_idna_t *idna = lxb_unicode_idna_create();
    if (idna == NULL) {
        return EXIT_FAILURE;
    }

    /* Initialize */
    lxb_status_t status = lxb_unicode_idna_init(idna);
    if (status != LXB_STATUS_OK) {
        lxb_unicode_idna_destroy(idna, true);
        return EXIT_FAILURE;
    }

    /* Convert to ASCII (Punycode) */
    status = lxb_unicode_idna_to_ascii(idna, domain, sizeof(domain) - 1,
                                       callback, NULL, 0);
    if (status != LXB_STATUS_OK) {
        lxb_unicode_idna_destroy(idna, true);
        return EXIT_FAILURE;
    }

    printf("\n");

    /* Cleanup */
    lxb_unicode_idna_destroy(idna, true);

    return EXIT_SUCCESS;
}
```

**Output:**
```
xn--b1agh1afp.xn--p1ai
```

## Normalization

Unicode normalization transforms text into a canonical form, ensuring that equivalent strings have identical binary representations. This is essential for string comparison, searching, and data storage.

### Location

All normalization functions are declared in `source/lexbor/unicode/unicode.h`.

### Normalization Forms

The module supports all four Unicode Normalization Forms:

| Form | Name | Description | Use Case |
|------|------|-------------|----------|
| **NFC** | Canonical Composition | Composed characters (e.g., é as single codepoint) | Most common, web, storage |
| **NFD** | Canonical Decomposition | Decomposed characters (e.g., e + combining accent) | Text processing, sorting |
| **NFKC** | Compatibility Composition | Like NFC + compatibility mappings (e.g., ﬁ → fi) | Search, indexing |
| **NFKD** | Compatibility Decomposition | Like NFD + compatibility mappings | Search, comparison |

### Normalizer Lifecycle

```C
/* Create normalizer object */
lxb_unicode_normalizer_t *
lxb_unicode_normalizer_create(void);

/* Initialize with specific normalization form */
lxb_status_t
lxb_unicode_normalizer_init(lxb_unicode_normalizer_t *uc,
                            lxb_unicode_form_t form);

/* Reset normalizer state for reuse */
void
lxb_unicode_normalizer_clean(lxb_unicode_normalizer_t *uc);

/* Destroy normalizer */
lxb_unicode_normalizer_t *
lxb_unicode_normalizer_destroy(lxb_unicode_normalizer_t *uc, bool self_destroy);
```

### Normalization Functions

#### For UTF-8 Characters

```C
/* Normalize UTF-8 data */
lxb_status_t
lxb_unicode_normalize(lxb_unicode_normalizer_t *uc, const lxb_char_t *data,
                      size_t length, lexbor_serialize_cb_f cb, void *ctx,
                      bool is_last);

/* Complete normalization (same as calling normalize with is_last=true) */
lxb_status_t
lxb_unicode_normalize_end(lxb_unicode_normalizer_t *uc, lexbor_serialize_cb_f cb,
                          void *ctx);
```

#### For Code Points

```C
/* Normalize code points array */
lxb_status_t
lxb_unicode_normalize_cp(lxb_unicode_normalizer_t *uc, const lxb_codepoint_t *cps,
                         size_t length, lexbor_serialize_cb_cp_f cb, void *ctx,
                         bool is_last);

/* Complete normalization for code points */
lxb_status_t
lxb_unicode_normalize_cp_end(lxb_unicode_normalizer_t *uc,
                             lexbor_serialize_cb_cp_f cb, void *ctx);
```

### Callback Functions

The normalization results are delivered through callback functions:

```C
/* Callback for UTF-8 output */
typedef lxb_status_t
(*lexbor_serialize_cb_f)(const lxb_char_t *data, size_t len, void *ctx);

/* Callback for code points output */
typedef lxb_status_t
(*lexbor_serialize_cb_cp_f)(const lxb_codepoint_t *cps, size_t len, void *ctx);
```

**Important:** Return `LXB_STATUS_OK` from callback to continue processing. Any other status will stop normalization.

### Single-Pass Normalization Example

```C
#include <lexbor/unicode/unicode.h>
#include <lexbor/encoding/encoding.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    const lxb_char_t *p = data;
    const lxb_char_t *end = data + len;
    const char *name = ctx;

    printf("%s: ", name);

    /* Print each codepoint in hex */
    while (p < end) {
        lxb_codepoint_t cp = lxb_encoding_decode_valid_utf_8_single(&p, end);
        printf("%04X ", cp);
    }

    printf("(%.*s)\n", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}

int main(void)
{
    /* U+1E9B U+0323 — ẛ̣ */
    lxb_char_t source[] = "\u1E9B\u0323";

    printf("Unicode Normalization Form for: 1E9B 0323\n");

    /* Create and initialize normalizer */
    lxb_unicode_normalizer_t *uc = lxb_unicode_normalizer_create();
    lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);

    /* NFC */
    lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                          callback, "NFC", true);

    /* NFD — change form and normalize again */
    lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFD);
    lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                          callback, "NFD", true);

    /* NFKC */
    lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFKC);
    lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                          callback, "NFKC", true);

    /* NFKD */
    lxb_unicode_normalization_form_set(uc, LXB_UNICODE_NFKD);
    lxb_unicode_normalize(uc, source, sizeof(source) - 1,
                          callback, "NFKD", true);

    lxb_unicode_normalizer_destroy(uc, true);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Unicode Normalization Form for: 1E9B 0323
NFC: 1E9B 0323 (ẛ̣)
NFD: 017F 0323 0307 (ẛ̣)
NFKC: 1E69 (ṩ)
NFKD: 0073 0323 0307 (ṩ)
```

### Streaming Normalization (Chunks)

For large data or network streams, normalize incrementally:

```C
#include <lexbor/unicode/unicode.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    lxb_char_t chunk1[] = "Hello ";
    lxb_char_t chunk2[] = "Wörld!";

    /* Create and initialize normalizer */
    lxb_unicode_normalizer_t *uc = lxb_unicode_normalizer_create();
    lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);

    /* Process first chunk (is_last = false) */
    lxb_unicode_normalize(uc, chunk1, sizeof(chunk1) - 1,
                          callback, NULL, false);

    /* Process second chunk (is_last = true to finalize) */
    lxb_unicode_normalize(uc, chunk2, sizeof(chunk2) - 1,
                          callback, NULL, true);

    printf("\n");

    lxb_unicode_normalizer_destroy(uc, true);

    return EXIT_SUCCESS;
}
```

### Changing Normalization Form

You can reuse the same normalizer for different normalization forms:

```C
lxb_status_t
lxb_unicode_normalization_form_set(lxb_unicode_normalizer_t *uc,
                                   lxb_unicode_form_t form);
```

**Important:** Only call this function after:
1. Completing previous normalization (`is_last = true`), OR
2. Calling `lxb_unicode_normalize_end()`, OR
3. Calling `lxb_unicode_normalizer_clean()`

### Flush Control

By default, the normalizer accumulates 1024 codepoints before calling your callback. You can control this:

```C
/* Set flush count (0 = call callback for every codepoint) */
void
lxb_unicode_flush_count_set(lxb_unicode_normalizer_t *uc, size_t count);

/* Force flush current buffer */
lxb_status_t
lxb_unicode_flush(lxb_unicode_normalizer_t *uc, lexbor_serialize_cb_f cb,
                  void *ctx);

/* Force flush for code points */
lxb_status_t
lxb_unicode_flush_cp(lxb_unicode_normalizer_t *uc, lexbor_serialize_cb_cp_f cb,
                     void *ctx);
```

## Quick Check

The Quick Check algorithm efficiently determines whether text needs normalization without performing full normalization. This is useful for optimization when most text is already normalized.

### Location

All quick check functions are declared in `source/lexbor/unicode/unicode.h`.

### Functions

#### For UTF-8 Characters

```C
/* Check if text needs normalization */
bool
lxb_unicode_quick_check(lxb_unicode_normalizer_t *uc, const lxb_char_t *data,
                        size_t length, bool is_last);

/* Complete quick check (same as calling with is_last=true) */
bool
lxb_unicode_quick_check_end(lxb_unicode_normalizer_t *uc);
```

#### For Code Points

```C
/* Check if code points need normalization */
bool
lxb_unicode_quick_check_cp(lxb_unicode_normalizer_t *uc,
                           const lxb_codepoint_t *cps, size_t length,
                           bool is_last);

/* Complete quick check for code points */
bool
lxb_unicode_quick_check_cp_end(lxb_unicode_normalizer_t *uc);
```

### Return Value

- `true` — text needs normalization
- `false` — text is already in the specified normalization form

### Quick Check Example

```C
#include <lexbor/unicode/unicode.h>

int main(void)
{
    lxb_char_t text1[] = "Hello World";      /* ASCII, already NFC */
    lxb_char_t text2[] = "\u0041\u030A";     /* A + combining ring = needs NFC */

    lxb_unicode_normalizer_t *uc = lxb_unicode_normalizer_create();
    lxb_unicode_normalizer_init(uc, LXB_UNICODE_NFC);

    /* Check first text */
    bool needs_norm = lxb_unicode_quick_check(uc, text1, sizeof(text1) - 1, true);
    printf("text1 needs NFC: %s\n", needs_norm ? "yes" : "no");

    /* Check second text */
    needs_norm = lxb_unicode_quick_check(uc, text2, sizeof(text2) - 1, true);
    printf("text2 needs NFC: %s\n", needs_norm ? "yes" : "no");

    lxb_unicode_normalizer_destroy(uc, true);

    return EXIT_SUCCESS;
}
```

**Output:**
```
text1 needs NFC: no
text2 needs NFC: yes
```

### Streaming Quick Check

```C
/* Check large text in chunks */
bool needs_norm;

needs_norm = lxb_unicode_quick_check(uc, chunk1, chunk1_len, false);
if (needs_norm) {
    /* Text needs normalization, no need to check further */
}

needs_norm = lxb_unicode_quick_check(uc, chunk2, chunk2_len, false);
if (needs_norm) {
    /* Text needs normalization */
}

/* Finalize check */
needs_norm = lxb_unicode_quick_check_end(uc);
```

## IDNA Processing

IDNA (Internationalized Domain Names in Applications) allows domain names to contain non-ASCII characters. The module implements Unicode TR#46 for domain name processing.

### Location

All IDNA functions are declared in `source/lexbor/unicode/idna.h`.

### IDNA Lifecycle

```C
/* Create IDNA processor */
lxb_unicode_idna_t *
lxb_unicode_idna_create(void);

/* Initialize IDNA processor */
lxb_status_t
lxb_unicode_idna_init(lxb_unicode_idna_t *idna);

/* Reset IDNA processor for reuse */
void
lxb_unicode_idna_clean(lxb_unicode_idna_t *idna);

/* Destroy IDNA processor */
lxb_unicode_idna_t *
lxb_unicode_idna_destroy(lxb_unicode_idna_t *idna, bool self_destroy);
```

### IDNA Flags

Control IDNA processing behavior with flags (can be combined with `|`):

| Flag | Description |
|------|-------------|
| `LXB_UNICODE_IDNA_FLAG_UNDEF` | Default behavior (no flags) |
| `LXB_UNICODE_IDNA_FLAG_USE_STD3ASCII_RULES` | Apply STD3 ASCII rules |
| `LXB_UNICODE_IDNA_FLAG_CHECK_HYPHENS` | Check hyphen placement |
| `LXB_UNICODE_IDNA_FLAG_CHECK_BIDI` | Check bidirectional text (not implemented) |
| `LXB_UNICODE_IDNA_FLAG_CHECK_JOINERS` | Check ZWNJ/ZWJ usage (not implemented) |
| `LXB_UNICODE_IDNA_FLAG_TRANSITIONAL_PROCESSING` | Use transitional mappings |
| `LXB_UNICODE_IDNA_FLAG_VERIFY_DNS_LENGTH` | Verify DNS length limits |

### ToASCII (Domain to Punycode)

Converts internationalized domain names to ASCII-compatible encoding:

```C
/* Convert UTF-8 domain to ASCII */
lxb_status_t
lxb_unicode_idna_to_ascii(lxb_unicode_idna_t *idna, const lxb_char_t *data,
                          size_t length, lexbor_serialize_cb_f cb, void *ctx,
                          lxb_unicode_idna_flag_t flags);

/* Convert code points domain to ASCII */
lxb_status_t
lxb_unicode_idna_to_ascii_cp(lxb_unicode_idna_t *idna, const lxb_codepoint_t *cps,
                             size_t length, lexbor_serialize_cb_f cb, void *ctx,
                             lxb_unicode_idna_flag_t flags);
```

### ToUnicode (Punycode to Domain)

Converts ASCII-encoded domain names back to Unicode:

```C
/* Convert ASCII domain to Unicode */
lxb_status_t
lxb_unicode_idna_to_unicode(lxb_unicode_idna_t *idna, const lxb_char_t *data,
                            size_t length, lexbor_serialize_cb_f cb, void *ctx,
                            lxb_unicode_idna_flag_t flags);

/* Convert ASCII domain to Unicode (code points input) */
lxb_status_t
lxb_unicode_idna_to_unicode_cp(lxb_unicode_idna_t *idna, const lxb_codepoint_t *cps,
                               size_t length, lexbor_serialize_cb_f cb, void *ctx,
                               lxb_unicode_idna_flag_t flags);
```

### Domain Processing

Process domain names with mapping, normalization, and validation:

```C
/* Process domain (callback invoked for each label) */
lxb_status_t
lxb_unicode_idna_processing(lxb_unicode_idna_t *idna, const lxb_char_t *data,
                            size_t length, lxb_unicode_idna_cb_f cb, void *ctx,
                            lxb_unicode_idna_flag_t flags);

/* Process domain with code points input */
lxb_status_t
lxb_unicode_idna_processing_cp(lxb_unicode_idna_t *idna,
                               const lxb_codepoint_t *cps, size_t length,
                               lxb_unicode_idna_cb_f cb, void *ctx,
                               lxb_unicode_idna_flag_t flags);
```

**Processing Callback:**

```C
typedef lxb_status_t
(*lxb_unicode_idna_cb_f)(const lxb_codepoint_t *part, size_t len,
                         void *ctx, lxb_status_t status);
```

The callback is invoked for each domain label (e.g., "lexbor" and "com" for "lexbor.com").

### Validity Criteria

Check if a domain label meets IDNA validity requirements:

```C
/* Check domain validity (UTF-8 input) */
bool
lxb_unicode_idna_validity_criteria(const lxb_char_t *data, size_t length,
                                   lxb_unicode_idna_flag_t flags);

/* Check domain validity (code points input) */
bool
lxb_unicode_idna_validity_criteria_cp(const lxb_codepoint_t *data, size_t length,
                                      lxb_unicode_idna_flag_t flags);
```

### IDNA ToASCII Example

```C
#include <lexbor/unicode/unicode.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    const lxb_char_t domains[][64] = {
        "example.com",
        "münchen.de",
        "россия.рф",
        "日本語.jp"
    };

    lxb_unicode_idna_t *idna = lxb_unicode_idna_create();
    lxb_unicode_idna_init(idna);

    for (size_t i = 0; i < 4; i++) {
        printf("Domain: %s\n", domains[i]);
        printf("ASCII:  ");

        lxb_unicode_idna_to_ascii(idna, domains[i], strlen((char *) domains[i]),
                                  callback, NULL, 0);
        printf("\n\n");

        lxb_unicode_idna_clean(idna);
    }

    lxb_unicode_idna_destroy(idna, true);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Domain: example.com
ASCII:  example.com

Domain: münchen.de
ASCII:  xn--mnchen-3ya.de

Domain: россия.рф
ASCII:  xn--h1alffa9f.xn--p1ai

Domain: 日本語.jp
ASCII:  xn--wgv71a119e.jp
```
