# Encoding Module

* **Version:** 2.2.0
* **Path:** `source/lexbor/encoding`
* **Base Includes:** `lexbor/encoding/encoding.h`
* **Examples:** `examples/lexbor/encoding`
* **Specification:** [WHATWG Encoding Living Standard](https://encoding.spec.whatwg.org/)

## Overview

The Encoding module implements [WHATWG Encoding Living Standard](https://encoding.spec.whatwg.org/) for converting between different character encodings.
The module provides comprehensive support for 40+ character encodings used across the web, with both streaming and buffer-pass conversion capabilities.

## Key Features

- **Specification Compliant** — follows WHATWG Encoding standard
- **40+ Encodings** — comprehensive support for legacy and modern encodings
- **Streaming Support** — decode/encode incrementally for large data
- **Buffer-Pass Conversion** — optimized functions for complete data conversion
- **Error Handling** — replacement character insertion on decode errors
- **Two Conversion Modes**:
  - **Decode** — convert from any encoding to Unicode codepoints
  - **Encode** — convert from Unicode codepoints to any encoding

## What's Inside

- **[Quick Start](#quick-start)** — basic examples for decoding and encoding
- **[Supported Encodings](#supported-encodings)** — list of all supported character encodings
- **[Decoder](#decoding)** — convert from any supported encoding to Unicode codepoints
- **[Encoder](#encoding)** — convert from Unicode codepoints to any supported encoding
- **[Encoding Data](#encoding-data)** — find encoding by name or label
- **[BOM (Byte Order Mark)](#bom-byte-order-mark)** — detect and skip BOM in data
- **[Integration with HTML Module](#integration-with-html-module)** — how Encoding works with HTML parsing

## Quick Start

### Basic Decoding (Convert to Unicode Codepoints)

```C
#include <lexbor/encoding/encoding.h>
#include <lexbor/core/core.h> /* For lexbor_str() */

int main(void)
{
    lxb_status_t status;
    lxb_encoding_decode_t decode;

    /* Define encoding name and input data */
    const lexbor_str_t win2151 = lexbor_str("windows-1251");

    /* "Привет" in Windows-1251 */
    const lexbor_str_t cyrillic_hi = lexbor_str("\xCF\xF0\xE8\xE2\xE5\xF2");

    /* Get encoding by name */
    const lxb_encoding_data_t *enc = lxb_encoding_data_by_name(win2151.data,
                                                               win2151.length);
    /* OR enc = lxb_encoding_data(LXB_ENCODING_WINDOWS_1251); for direct access */
    if (enc == NULL) {
        return EXIT_FAILURE;
    }

    /* Initialize single-pass decoder */
    status = lxb_encoding_decode_init_single(&decode, enc);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    lxb_codepoint_t cp;
    const lxb_char_t *pos;
    const lxb_char_t *p = cyrillic_hi.data;
    const lxb_char_t *end = cyrillic_hi.data + cyrillic_hi.length;

    printf("Decoding Windows-1251 to Unicode codepoints:\n");

    while (p < end) {
        pos = p;

        /* Decode single codepoint */
        cp = enc->decode_single(&decode, &p, end);
        if (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT) {
            /* In this example, this cannot happen. */
            continue;
        }

        printf("0x%02X => 0x%04X\n", *pos, cp);
    }

    /* Finalize decoding */
    status = lxb_encoding_decode_finish_single(&decode);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
```

**Output:**
```
Decoding Windows-1251 to Unicode codepoints:
0xCF => 0x041F
0xF0 => 0x0440
0xE8 => 0x0438
0xE2 => 0x0432
0xE5 => 0x0435
0xF2 => 0x0442
```

### Basic Encoding (Convert from Unicode Codepoints)

```C
#include <lexbor/encoding/encoding.h>
#include <lexbor/core/core.h> /* For lexbor_str() */

int main(void)
{
    lxb_status_t status;
    lxb_encoding_encode_t encode;

    const lexbor_str_t utf_8 = lexbor_str("UTF-8");

    /* "Привет" in Unicode codepoints */
    lxb_codepoint_t cps[] = {0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442, 0};

    /* Get encoding by name */
    const lxb_encoding_data_t *enc = lxb_encoding_data_by_name(utf_8.data,
                                                               utf_8.length);
    /* OR enc = lxb_encoding_data(LXB_ENCODING_UTF_8); */
    if (enc == NULL) {
        return EXIT_FAILURE;
    }

    /* Initialize single-pass encoder */
    status = lxb_encoding_encode_init_single(&encode, enc);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Output buffer */
    lxb_char_t buffer[1024];
    lxb_char_t *data = buffer;
    const lxb_char_t *end = data + sizeof(buffer);

    /* Encode each codepoint */
    int8_t len;
    const lxb_char_t *pos;

    printf("Encoding Unicode codepoints to UTF-8:\n");

    for (size_t i = 0; cps[i] != 0; i++) {
        pos = data;

        len = enc->encode_single(&encode, &data, end, cps[i]);
        if (len < LXB_ENCODING_ENCODE_OK) {
            /* In this example, this cannot happen. */
            continue;
        }

        printf("0x%04X => %.*s\n", cps[i], len, pos);
    }

    /* Finalize encoding */
    /* In fact, this is only necessary for one encoding: LXB_ENCODING_ISO_2022_JP. */
    pos = data;
    len = lxb_encoding_encode_finish_single(&encode, &data, end);
    if (len < LXB_ENCODING_ENCODE_OK) {
        /* In this example, this cannot happen. */
    }

    /* Terminate string */
    *data = 0x00;

    printf("Result: %s\n", (const char *) buffer);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Encoding Unicode codepoints to UTF-8:
0x041F => П
0x0440 => р
0x0438 => и
0x0432 => в
0x0435 => е
0x0442 => т
Result: Привет
```

## Supported Encodings

The module supports all encodings from the WHATWG Encoding standard:

### Unicode Encodings
- **UTF-8** — variable-length Unicode encoding (1-4 bytes)
- **UTF-16LE** — Unicode 16-bit Little Endian
- **UTF-16BE** — Unicode 16-bit Big Endian

### Western European (Latin)
- **ISO-8859-2** — Central/Eastern European Latin
- **ISO-8859-3** — South European Latin
- **ISO-8859-4** — North European Latin
- **ISO-8859-5** — Cyrillic
- **ISO-8859-6** — Arabic
- **ISO-8859-7** — Greek
- **ISO-8859-8** — Hebrew (visual)
- **ISO-8859-8-I** — Hebrew (logical)
- **ISO-8859-10** — Nordic Latin
- **ISO-8859-13** — Baltic Rim Latin
- **ISO-8859-14** — Celtic Latin
- **ISO-8859-15** — Western European Latin with Euro
- **ISO-8859-16** — South-Eastern European Latin
- **Windows-1250** — Central European (Windows)
- **Windows-1251** — Cyrillic (Windows)
- **Windows-1252** — Western European (Windows)
- **Windows-1253** — Greek (Windows)
- **Windows-1254** — Turkish (Windows)
- **Windows-1255** — Hebrew (Windows)
- **Windows-1256** — Arabic (Windows)
- **Windows-1257** — Baltic (Windows)
- **Windows-1258** — Vietnamese (Windows)
- **Windows-874** — Thai (Windows)
- **Macintosh** — Mac OS Roman
- **KOI8-R** — Russian Cyrillic
- **KOI8-U** — Ukrainian Cyrillic
- **IBM866** — Cyrillic (DOS)
- **x-mac-cyrillic** — Cyrillic (Mac)

### East Asian Encodings
- **Big5** — Traditional Chinese
- **GBK** — Simplified Chinese
- **GB18030** — Chinese National Standard
- **EUC-JP** — Japanese (Unix)
- **ISO-2022-JP** — Japanese (email)
- **Shift_JIS** — Japanese (Windows)
- **EUC-KR** — Korean

### Other
- **replacement** — Special encoding that always produces the replacement character
- **x-user-defined** — User-defined single-byte encoding

List of encoding names and aliases, see `source/lexbor/encoding/const.h`.

## Decoding

Decoding converts data from any supported encoding to Unicode codepoints. The module provides both streaming and buffer-pass decoding functions.

### Location

API for decoding is declared in `source/lexbor/encoding/encoding.h`.
All decoding functions are declared in `source/lexbor/encoding/decode.h`.

### Buffer-Pass Decoding

The simplest way to decode data when you have the entire input in memory.

### Important Notes

- **Pointer Updates**: Input and output pointers are advanced automatically
- **No Null Termination**: Output is not null-terminated automatically

#### Error Handling

- `LXB_STATUS_OK` — is returned on successful decoding.
- `LXB_STATUS_CONTINUE` — not enough data for decoding, more data is needed. You need to run the same decoding function with the continuation of the data.
- `LXB_STATUS_SMALL_BUFFER` — not enough buffer size to write decoded data.
- `LXB_STATUS_ERROR` — is returned for decoding errors; is returned only if no replacement character was set by user (the lxb_encoding_encode_replace_set() function).

#### Error Handling

The streaming decoder returns a codepoint or an error, i.e., a value greater than the maximum possible Unicode codepoint (cp > LXB_ENCODING_DECODE_MAX_CODEPOINT).

- `LXB_ENCODING_DECODE_ERROR` — indicates a decoding error; the replacement character (U+FFFD, LXB_ENCODING_REPLACEMENT_CODEPOINT) should be used. Important! The input buffer will not be increased, i.e. it will remain at the byte that could not be decoded. The user must increase the input buffer by one themselves.
- `LXB_ENCODING_DECODE_CONTINUE` — indicates that more data is needed to decode a complete codepoint. The user must provide more data. Essentially, this indicates that the input buffer is end and there is insufficient data to form a code point.

## Encoding

Encoding converts UTF-8 data to any supported encoding. This is the reverse operation of decoding.

### Location

API for encoding is declared in `source/lexbor/encoding/encoding.h`.
All encoding functions are declared in `source/lexbor/encoding/encode.h`.

### Buffer-Pass Encoding

Convert entire Unicode codepoints buffer to target encoding using buffer.

## Encoding Data

The `lxb_encoding_data_t` object contains the encoding name and pointers to functions for buffer/single encode/decode.

### Location

API for encoding data in `source/lexbor/encoding/encoding.h`.
Declared in `source/lexbor/encoding/base.h`.

### Finding Encoding by Name

#### lxb_encoding_data_by_name

Looks up encoding by its canonical name or alias.

```C
const lxb_encoding_data_t *
lxb_encoding_data_by_name(const lxb_char_t *name, size_t length);
```

**Parameters:**
- `name` — encoding name (case-insensitive)
- `length` — name length in bytes

**Returns:** Pointer to encoding descriptor, or `NULL` if not found

### Finding Encoding by Name with Whitespace Trimming

Before searching will be removed any leading and trailing ASCII whitespace in name.

```C
LXB_API const lxb_encoding_data_t *
lxb_encoding_data_by_pre_name(const lxb_char_t *name, size_t length);
```

### Get Encoding Data by ID

```C
const lxb_encoding_data_t *
lxb_encoding_data(lxb_encoding_t encoding);
```

### Example

```C
#include <lexbor/encoding/encoding.h>

int main(void)
{
    /* Try various encoding names and aliases */
    const lxb_encoding_data_t *enc;

    /* By Name */

    enc = lxb_encoding_data_by_name((const lxb_char_t *) "UTF-8", 5);
    printf("UTF-8: %s\n", (enc != NULL) ? "found" : "not found");

    enc = lxb_encoding_data_by_name((const lxb_char_t *) "utf8", 4);
    printf("utf8 (alias): %s\n", (enc != NULL) ? "found" : "not found");

    enc = lxb_encoding_data_by_name((const lxb_char_t *) "windows-1251", 12);
    printf("windows-1251: %s\n", (enc != NULL) ? "found" : "not found");

    enc = lxb_encoding_data_by_name((const lxb_char_t *) "cp1251", 6);
    printf("cp1251 (alias): %s\n", (enc != NULL) ? "found" : "not found");

    enc = lxb_encoding_data_by_name((const lxb_char_t *) "invalid", 7);
    printf("invalid: %s\n", (enc != NULL) ? "found" : "not found");

    /* By ID */

    enc = lxb_encoding_data(LXB_ENCODING_UTF_8);
    printf("UTF-8: %s\n", (enc != NULL) ? "found" : "not found");

    enc = lxb_encoding_data(LXB_ENCODING_WINDOWS_1251);
    printf("windows-1251: %s\n", (enc != NULL) ? "found" : "not found");

    return EXIT_SUCCESS;
}
```

**Output:**
```
UTF-8: found
utf8 (alias): found
windows-1251: found
cp1251 (alias): found
invalid: not found
UTF-8: found
windows-1251: found
```

## BOM (Byte Order Mark)

BOM (Byte Order Mark) is a special Unicode character (U+FEFF) placed at the beginning of a text file to indicate:
1. The encoding used (UTF-8, UTF-16, etc.)
2. The byte order (Little Endian or Big Endian for UTF-16)

The BOM is encoded differently depending on the encoding:
- **UTF-8**: `0xEF 0xBB 0xBF` (3 bytes)
- **UTF-16BE** (Big Endian): `0xFE 0xFF` (2 bytes)
- **UTF-16LE** (Little Endian): `0xFF 0xFE` (2 bytes)

### Location

BOM handling functions are declared in `source/lexbor/encoding/encoding.h`.

### Why Skip BOM?

When processing text files, the BOM should typically be skipped because:
1. It's not part of the actual content
2. It's a metadata marker for encoding detection
3. Including it in parsed content can cause issues (invisible characters, comparison failures)

### BOM Detection and Removal Functions

The Encoding module provides three functions to detect and skip BOM at the beginning of data:

#### lxb_encoding_utf_8_skip_bom

Detects and skips UTF-8 BOM (`0xEF 0xBB 0xBF`).

```C
void
lxb_encoding_utf_8_skip_bom(const lxb_char_t **begin, size_t *length);
```

**Parameters:**
- `begin` — pointer to data pointer (updated if BOM found)
- `length` — pointer to data length (updated if BOM found)

**Behavior:**
- If the first 3 bytes match UTF-8 BOM (`0xEF 0xBB 0xBF`):
  - Advances `begin` by 3 bytes
  - Decreases `length` by 3
- Otherwise, does nothing

#### lxb_encoding_utf_16be_skip_bom

Detects and skips UTF-16BE BOM (`0xFE 0xFF`).

```C
void
lxb_encoding_utf_16be_skip_bom(const lxb_char_t **begin, size_t *length);
```

**Parameters:**
- `begin` — pointer to data pointer (updated if BOM found)
- `length` — pointer to data length (updated if BOM found)

**Behavior:**
- If the first 2 bytes match UTF-16BE BOM (`0xFE 0xFF`):
  - Advances `begin` by 2 bytes
  - Decreases `length` by 2
- Otherwise, does nothing

#### lxb_encoding_utf_16le_skip_bom

Detects and skips UTF-16LE BOM (`0xFF 0xFE`).

```C
void
lxb_encoding_utf_16le_skip_bom(const lxb_char_t **begin, size_t *length);
```

**Parameters:**
- `begin` — pointer to data pointer (updated if BOM found)
- `length` — pointer to data length (updated if BOM found)

**Behavior:**
- If the first 2 bytes match UTF-16LE BOM (`0xFF 0xFE`):
  - Advances `begin` by 2 bytes
  - Decreases `length` by 2
- Otherwise, does nothing

### Usage Examples

#### Skipping UTF-8 BOM

```C
#include <lexbor/encoding/encoding.h>

int main(void)
{
    /* UTF-8 data with BOM */
    const lxb_char_t data[] = "\xEF\xBB\xBF" "Hello, World!";
    const lxb_char_t *ptr = data;
    size_t length = sizeof(data) - 1;

    printf("Before: length = %zu\n", length);
    printf("First 3 bytes: %02X %02X %02X\n", ptr[0], ptr[1], ptr[2]);

    /* Skip BOM if present */
    lxb_encoding_utf_8_skip_bom(&ptr, &length);

    printf("After: length = %zu\n", length);
    printf("Content: %.*s\n", (int)length, ptr);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Before: length = 16
First 3 bytes: EF BB BF
After: length = 13
Content: Hello, World!
```

#### Skipping UTF-16LE BOM

```C
#include <lexbor/encoding/encoding.h>

int main(void)
{
    /* UTF-16LE data with BOM */
    const lxb_char_t data[] = "\xFF\xFE" "H\x00" "i\x00";
    const lxb_char_t *ptr = data;
    size_t length = sizeof(data) - 1;

    printf("Before: length = %zu\n", length);
    printf("First 2 bytes: %02X %02X\n", ptr[0], ptr[1]);

    /* Skip BOM if present */
    lxb_encoding_utf_16le_skip_bom(&ptr, &length);

    printf("After: length = %zu\n", length);
    printf("Remaining bytes: %02X %02X %02X %02X\n",
           ptr[0], ptr[1], ptr[2], ptr[3]);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Before: length = 6
First 2 bytes: FF FE
After: length = 4
Remaining bytes: 48 00 69 00
```

#### Handling Data Without BOM

```C
#include <lexbor/encoding/encoding.h>

int main(void)
{
    /* UTF-8 data WITHOUT BOM */
    const lxb_char_t data[] = "Hello, World!";
    const lxb_char_t *ptr = data;
    size_t length = sizeof(data) - 1;

    printf("Before: length = %zu\n", length);

    /* Try to skip BOM (nothing happens if not present) */
    lxb_encoding_utf_8_skip_bom(&ptr, &length);

    printf("After: length = %zu\n", length);
    printf("Content: %.*s\n", (int)length, ptr);

    return EXIT_SUCCESS;
}
```

**Output:**
```
Before: length = 13
After: length = 13
Content: Hello, World!
```

### Important Notes

1. **Safe to Call**: BOM skip functions are safe to call even if there's no BOM — they simply do nothing
2. **No Allocation**: These functions don't allocate memory, they only adjust pointers
3. **In-Place Operation**: The original data is not modified, only the pointer and length are updated
4. **Minimum Length**: Functions check if enough bytes are available before checking BOM:
   - UTF-8: requires at least 3 bytes
   - UTF-16: requires at least 2 bytes
5. **One-Time Use**: Call these functions once at the beginning of data processing
6. **Not Automatic**: The decoder does NOT skip BOM automatically — you must call these functions explicitly before decoding

### BOM Values Reference

| Encoding | BOM Bytes | Size | Hexadecimal |
|----------|-----------|------|-------------|
| **UTF-8** | `0xEF 0xBB 0xBF` | 3 bytes | `EF BB BF` |
| **UTF-16BE** | `0xFE 0xFF` | 2 bytes | `FE FF` |
| **UTF-16LE** | `0xFF 0xFE` | 2 bytes | `FF FE` |
| **UTF-32BE** | `0x00 0x00 0xFE 0xFF` | 4 bytes | Not supported by lexbor |
| **UTF-32LE** | `0xFF 0xFE 0x00 0x00` | 4 bytes | Not supported by lexbor |

**Note:** Lexbor only provides BOM handling for UTF-8, UTF-16BE, and UTF-16LE. Other encodings typically don't use BOM.

## Integration with HTML Module

The Encoding module is typically used in combination with the HTML module for processing web documents in different character encodings.

**Typical Workflow:**

1. **HTML Module** — detects encoding from `<meta>` tags in raw HTML bytes
2. **Encoding Module** — converts detected encoding to UTF-8
3. **HTML Module** — parses the UTF-8 HTML

**Minimal Example:**

```C
#include <lexbor/html/html.h>
#include <lexbor/encoding/encoding.h>

int main(void)
{
    /* Raw HTML in Windows-1251 with meta tag */
    const lxb_char_t html_raw[] =
        "<meta charset=\"windows-1251\">"
        "\xCF\xF0\xE8\xE2\xE5\xF2"; /* "Привет" in Windows-1251 */

    /* Step 1: Detect encoding from <meta> tag */
    lxb_html_encoding_t *enc_detect = lxb_html_encoding_create();
    lxb_html_encoding_init(enc_detect);
    lxb_html_encoding_determine(enc_detect, html_raw,
                                html_raw + sizeof(html_raw) - 1);

    /* Get detected encoding name */
    lxb_html_encoding_entry_t *entry = lxb_html_encoding_meta_entry(enc_detect, 0);

    /* Step 2: Get encoding data (with whitespace trimming) */
    const lxb_encoding_data_t *encoding = lxb_encoding_data_by_pre_name(
        entry->name, entry->end - entry->name);

    /* Step 3: Convert to UTF-8 using Encoding module */
    /* ... decode using encoding->decode_single() ... */

    /* Step 4: Parse converted UTF-8 HTML */
    /* ... lxb_html_document_parse() ... */

    lxb_html_encoding_destroy(enc_detect, true);

    return EXIT_SUCCESS;
}
```

**Note:** For automatic encoding detection and conversion, consider using the **Engine module** which combines HTML encoding detection, Encoding conversion, and HTML parsing into a single high-level API.

See:
- [HTML Module - Encoding Detection](html.md#encoding-detection) — how to extract encoding from `<meta>` tags
- Engine Module — automated HTML processing with encoding conversion
