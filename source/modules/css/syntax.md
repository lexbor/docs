# Syntax

* **Path:** `source/lexbor/css/syntax/`
* **Includes:** `lexbor/css/syntax/tokenizer.h`, `lexbor/css/syntax/token.h`, `lexbor/css/syntax/parser.h`, `lexbor/css/syntax/anb.h`
* **Specification:** [CSS Syntax Module](https://drafts.csswg.org/css-syntax/)

## Overview

The Syntax subsystem is the lowest-level component of the CSS module. It converts raw CSS text into tokens according to [CSS Syntax Module](https://drafts.csswg.org/css-syntax/).

## What's Inside

- [**Quick Start**](#quick-start) — minimal working example: tokenize CSS and print each token
- [**How the Tokenizer Works**](#how-the-tokenizer-works) — peek, lookahead, and consume: the three-function pattern
- [**Token Types**](#token-types) — complete list of token types produced by the tokenizer
- [**Tokenizer Errors**](#tokenizer-errors) — error types collected during tokenization and how to read them
- [**Parser**](#parser) — Syntax Parser documentation

## Quick Start

```C
#include <lexbor/css/css.h>

static lxb_status_t
callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}

int main(void)
{
    lxb_status_t status;
    const lxb_char_t *name;
    const lxb_css_syntax_token_t *token;
    const lxb_char_t css[] = "div { color: red; }";

    /* Create and initialize tokenizer */
    lxb_css_syntax_tokenizer_t *tkz = lxb_css_syntax_tokenizer_create();
    status = lxb_css_syntax_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        fprintf(stderr, "Failed to initialize tokenizer\n");
        return EXIT_FAILURE;
    }

    /* Set input buffer */
    lxb_css_syntax_tokenizer_buffer_set(tkz, css, sizeof(css) - 1);

    /* Read tokens one by one */
    token = lxb_css_syntax_token(tkz);

    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__EOF) {
        /* Get token type name */
        name = lxb_css_syntax_token_type_name_by_id(token->type);

        /* Serialize token value */
        printf("%s: \"", (const char *) name);
        lxb_css_syntax_token_serialize(token, callback, NULL);
        printf("\"\n");

        /* Advance to next token */
        lxb_css_syntax_token_consume(tkz);
        token = lxb_css_syntax_token(tkz);
    }

    /* Clean up */
    lxb_css_syntax_tokenizer_destroy(tkz);

    return EXIT_SUCCESS;
}
```

Output:
```
ident: "div"
whitespace: " "
left-curly-bracket: "{"
whitespace: " "
ident: "color"
colon: ":"
whitespace: " "
ident: "red"
semicolon: ";"
whitespace: " "
right-curly-bracket: "}"
```

## How the Tokenizer Works

The tokenizer works on a **peek / lookahead / consume** pattern. Three functions control the token stream:

| Function | Role | Description |
|----------|------|-------------|
| `lxb_css_syntax_token()` | **Peek** | Returns the current token. If no token has been generated yet, tokenizes the next one from the input. Calling it multiple times without consuming returns the same token. |
| `lxb_css_syntax_token_next()` | **Lookahead** | Always tokenizes the next token from the input and appends it to the internal buffer. Use this to look ahead without consuming the current token. |
| `lxb_css_syntax_token_consume()` | **Consume** | Removes the current (first) token from the buffer and frees its memory. After this call, the next buffered token becomes the current one. |

### Token Buffer

Internally, the tokenizer maintains a **linked list** of tokens (via `first` and `last` pointers). Tokens are allocated from an object pool and linked together:

```
first -> Token A -> Token B -> Token C -> NULL
                                 |
                                last
```

- `lxb_css_syntax_token()` returns `first`. If `first` is `NULL`, it tokenizes one token from the input, sets it as `first` (and `last`), and returns it.
- `lxb_css_syntax_token_next()` tokenizes a new token, links it after `last`, and updates `last`.
- `lxb_css_syntax_token_consume()` removes `first`, advances `first` to `first->next`, and returns the old token to the object pool.

Tokenization is **lazy**: tokens are generated only when requested via `lxb_css_syntax_token()` or `lxb_css_syntax_token_next()`.

### Basic Pattern: Sequential Reading

The most common usage is a simple loop: peek at the current token, process it, consume, repeat.

```C
token = lxb_css_syntax_token(tkz);

while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__EOF) {
    /* Process token... */

    lxb_css_syntax_token_consume(tkz);
    token = lxb_css_syntax_token(tkz);
}
```

At each iteration:

1. `lxb_css_syntax_token()` — returns the current token (generates it on first call).
2. You inspect and process the token.
3. `lxb_css_syntax_token_consume()` — removes the token from the buffer and frees it.
4. `lxb_css_syntax_token()` — generates the next token (buffer is now empty, so it tokenizes from input).

### Lookahead Pattern

Sometimes you need to see the next token before deciding what to do with the current one. Use `lxb_css_syntax_token_next()` for this:

```C
lxb_css_syntax_token_t *current = lxb_css_syntax_token(tkz);
lxb_css_syntax_token_t *next = lxb_css_syntax_token_next(tkz);

/* Buffer state:
 *   first -> current -> next -> NULL
 *                         |
 *                        last
 */

if (current->type == LXB_CSS_SYNTAX_TOKEN_IDENT
    && next->type == LXB_CSS_SYNTAX_TOKEN_COLON)
{
    /* This is a "name: ..." pair, handle accordingly. */
}

/* Consume current, next becomes the new current. */
lxb_css_syntax_token_consume(tkz);

/* Now lxb_css_syntax_token(tkz) returns what was 'next'. */
```

You can call `lxb_css_syntax_token_next()` multiple times to buffer several tokens ahead. They form a chain in the linked list and are consumed one at a time.

### Bulk Consume

To skip multiple tokens at once, use `lxb_css_syntax_token_consume_n()`:

```C
/* Skip 3 tokens. */
lxb_css_syntax_token_consume_n(tkz, 3);
```

This simply calls `lxb_css_syntax_token_consume()` the specified number of times.

### Memory and Lifetime

- Tokens are allocated from a **pre-allocated object pool** inside the tokenizer. There is no manual malloc/free for individual tokens.
- `lxb_css_syntax_token_consume()` returns the token object to the pool. After consuming, the pointer to the consumed token is **invalid** — do not use it.
- String data inside tokens (e.g. identifier names, string values) initially references a **temporary buffer** inside the tokenizer. When a new token is generated, the previous token's string data is automatically moved to stable memory. This means the `data` pointer in a token is valid as long as the token has not been consumed.

## Token Types

The tokenizer produces tokens defined in `lxb_css_syntax_token_type_t` enum. All token type constants have the prefix `LXB_CSS_SYNTAX_TOKEN_`. Types are grouped by their internal data structure.

### String Tokens

These tokens carry a string value accessible via the corresponding cast macro (e.g. `lxb_css_syntax_token_ident(token)->data`).

| Token Type | Description | CSS Example |
|------------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_IDENT` | An identifier — any CSS name such as a property name, tag name, keyword, or custom identifier. | `div`, `color`, `auto`, `--my-var` |
| `LXB_CSS_SYNTAX_TOKEN_FUNCTION` | A function token — an identifier immediately followed by `(`. The token value is the function name without the opening parenthesis. | `rgb(`, `calc(`, `var(` |
| `LXB_CSS_SYNTAX_TOKEN_AT_KEYWORD` | An at-keyword — `@` followed by an identifier. Used for CSS at-rules. The token value is the name without `@`. | `@media`, `@import`, `@keyframes` |
| `LXB_CSS_SYNTAX_TOKEN_HASH` | A hash token — `#` followed by name characters. Used for ID selectors and color values. | `#main`, `#ff0000`, `#content` |
| `LXB_CSS_SYNTAX_TOKEN_STRING` | A quoted string — text enclosed in matching single or double quotes. | `"hello"`, `'world'` |
| `LXB_CSS_SYNTAX_TOKEN_BAD_STRING` | A malformed string — a string token that was terminated by an unescaped newline instead of a matching quote. Indicates a parse error. | `"unterminated` + newline |
| `LXB_CSS_SYNTAX_TOKEN_URL` | A URL token — the contents of `url(...)` when the argument is not a quoted string. | `url(image.png)`, `url(https://example.com/bg.jpg)` |
| `LXB_CSS_SYNTAX_TOKEN_BAD_URL` | A malformed URL — a `url()` token that contains invalid characters (unescaped whitespace, quotes, or parentheses). Indicates a parse error. | `url(bad value)` |
| `LXB_CSS_SYNTAX_TOKEN_COMMENT` | A CSS comment (`/* ... */`). This token is **not part of the CSS specification** — it is a lexbor extension, since the spec says comments should be discarded during tokenization. | `/* comment */` |
| `LXB_CSS_SYNTAX_TOKEN_WHITESPACE` | One or more whitespace characters (spaces, tabs, newlines) collapsed into a single token. | ` `, `\t`, `\n` |

### Numeric Tokens

These tokens carry a numeric value. Access via `lxb_css_syntax_token_number(token)->num`.

| Token Type | Description | CSS Example |
|------------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_NUMBER` | A numeric value — integer or floating-point. The token stores whether it is a float (`is_float`) and whether it has an explicit sign (`have_sign`). | `42`, `3.14`, `-1`, `+0.5` |
| `LXB_CSS_SYNTAX_TOKEN_PERCENTAGE` | A number immediately followed by `%`. Internally has the same structure as a number token. | `100%`, `50%`, `33.3%` |

### Dimension Token

The dimension token combines a numeric value and a unit string.

| Token Type | Description | CSS Example |
|------------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_DIMENSION` | A number immediately followed by an identifier (the unit). Contains both a numeric part (accessible via `lxb_css_syntax_token_dimension(token)->num`) and a string part for the unit (accessible via `lxb_css_syntax_token_dimension_string(token)`). | `16px`, `2em`, `100vh`, `90deg`, `300ms` |

### Delimiter Token

| Token Type | Description | CSS Example |
|------------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_DELIM` | A single code point that doesn't match any other token type. The character is accessible via `lxb_css_syntax_token_delim_char(token)`. Used for operators, combinators, and other punctuation in CSS. | `.`, `>`, `+`, `~`, `*`, `=`, `\|`, `/` |

### Unicode Range Token

| Token Type | Description | CSS Example |
|------------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_UNICODE_RANGE` | A Unicode range used in `@font-face` rules. Contains a start and end code point accessible via `lxb_css_syntax_token_unicode_range(token)->start` and `->end`. | `U+0025-00FF`, `U+4E00-9FFF`, `U+26` |

### Punctuation Tokens

These tokens represent single punctuation characters. They carry only the base data (position and length), with no additional value.

| Token Type | Description | Character |
|------------|-------------|-----------|
| `LXB_CSS_SYNTAX_TOKEN_COLON` | A colon. Separates property names from values, and used in pseudo-class selectors. | `:` |
| `LXB_CSS_SYNTAX_TOKEN_SEMICOLON` | A semicolon. Separates declarations in a rule block. | `;` |
| `LXB_CSS_SYNTAX_TOKEN_COMMA` | A comma. Separates values in lists and selectors. | `,` |
| `LXB_CSS_SYNTAX_TOKEN_LS_BRACKET` | Left square bracket (U+005B). Used in attribute selectors. | `[` |
| `LXB_CSS_SYNTAX_TOKEN_RS_BRACKET` | Right square bracket (U+005D). Closes attribute selectors. | `]` |
| `LXB_CSS_SYNTAX_TOKEN_L_PARENTHESIS` | Left parenthesis (U+0028). Opens function arguments and grouped expressions. | `(` |
| `LXB_CSS_SYNTAX_TOKEN_R_PARENTHESIS` | Right parenthesis (U+0029). Closes function arguments and grouped expressions. | `)` |
| `LXB_CSS_SYNTAX_TOKEN_LC_BRACKET` | Left curly bracket (U+007B). Opens a declaration block or rule body. | `{` |
| `LXB_CSS_SYNTAX_TOKEN_RC_BRACKET` | Right curly bracket (U+007D). Closes a declaration block or rule body. | `}` |

### HTML Comment Tokens

Legacy tokens for compatibility with HTML-style comments embedded in CSS (from the era of `<style>` without proper parser support).

| Token Type | Description | CSS Representation |
|------------|-------------|--------------------|
| `LXB_CSS_SYNTAX_TOKEN_CDO` | Comment Data Open — the `<!--` sequence. In modern CSS this is effectively ignored but required by the specification for backwards compatibility. | `<!--` |
| `LXB_CSS_SYNTAX_TOKEN_CDC` | Comment Data Close — the `-->` sequence. Same as CDO: exists for backwards compatibility with HTML comments in CSS. | `-->` |

### Special Tokens

| Token Type | Description |
|------------|-------------|
| `LXB_CSS_SYNTAX_TOKEN_UNDEF` | Undefined/uninitialized token. Value `0x00`. Indicates the token has not been set.  |
| `LXB_CSS_SYNTAX_TOKEN__EOF` | End of file. The tokenizer reached the end of the input data. |
| `LXB_CSS_SYNTAX_TOKEN__END` | End of tokenization. Alias for the deprecated `LXB_CSS_SYNTAX_TOKEN__TERMINATED`. Signals that the tokenizer has been explicitly stopped. Used in parser states. |
| `LXB_CSS_SYNTAX_TOKEN__LAST_ENTRY` | Sentinel value marking the end of the enum. Used internally for bounds checking; not a real token type. |

## Tokenizer Errors

**API** `source/lexbor/css/syntax/tokenizer/error.h`

During tokenization the tokenizer collects parse errors. Errors do not stop tokenization — they are recorded and can be inspected after processing.

### Error Types

| Error | Description | CSS Example |
|-------|-------------|-------------|
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_UNEOF` | Unexpected end of file. | (empty input where a token is expected) |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINCO` | EOF in comment — a `/*` comment was never closed. | `/* unclosed comment` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINST` | EOF in string — a quoted string was never closed. | `"unterminated string` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINUR` | EOF in URL — a `url()` token was never closed. | `url(image.png` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINES` | EOF in escape — an escape sequence (`\`) at end of input. | `div\` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_QOINUR` | Quote in URL — a quote character inside an unquoted `url()`. | `url(ba"d)` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_WRESINUR` | Wrong escape in URL — an invalid escape sequence inside `url()`. | `url(bad\↵value)` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_NEINST` | Newline in string — an unescaped newline inside a quoted string. | `"line1↵line2"` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_BACH` | Bad character — a character that is not valid in CSS (e.g. NULL). | `\0` |
| `LXB_CSS_SYNTAX_TOKENIZER_ERROR_BACOPO` | Bad code point — an escape sequence that resolves to an invalid code point (surrogate or out of range). | `\DFFF` |

### Error Structure

Each error is stored as `lxb_css_syntax_tokenizer_error_t`:

```C
typedef struct {
    const lxb_char_t                    *pos;   /* position in the input buffer */
    lxb_css_syntax_tokenizer_error_id_t id;     /* error type */
} lxb_css_syntax_tokenizer_error_t;
```

Errors are accumulated in the tokenizer's `parse_errors` array (`lexbor_array_obj_t`). You can iterate them after tokenization using `lexbor_array_obj_length()` and `lexbor_array_obj_get()`.

### Example: Collecting Tokenizer Errors

```C
#include <lexbor/css/css.h>

int main(void)
{
    lxb_status_t status;
    const lxb_css_syntax_token_t *token;
    lxb_css_syntax_tokenizer_t *tkz;
    lxb_css_syntax_tokenizer_error_t *error;

    /* CSS with errors: unterminated string and unterminated comment. */
    const lxb_char_t css[] = "div { content: \"bad string\n } /* unclosed";

    /* Create and initialize tokenizer. */
    tkz = lxb_css_syntax_tokenizer_create();
    status = lxb_css_syntax_tokenizer_init(tkz);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    /* Set input buffer. */
    lxb_css_syntax_tokenizer_buffer_set(tkz, css, sizeof(css) - 1);

    /* Consume all tokens to trigger error detection. */
    token = lxb_css_syntax_token(tkz);

    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__EOF) {
        lxb_css_syntax_token_consume(tkz);
        token = lxb_css_syntax_token(tkz);
    }

    /* Print all tokenizer errors. */
    size_t errors_count = lexbor_array_obj_length(tkz->parse_errors);

    printf("Found %zu tokenizer error(s):\n", errors_count);

    for (size_t i = 0; i < errors_count; i++) {
        error = lexbor_array_obj_get(tkz->parse_errors, i);

        size_t pos = error->pos - css;

        switch (error->id) {
            case LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINCO:
                printf("  [%zu] EOF in comment (offset: %zu)\n", i, pos);
                break;
            case LXB_CSS_SYNTAX_TOKENIZER_ERROR_NEINST:
                printf("  [%zu] Newline in string (offset: %zu)\n", i, pos);
                break;
            case LXB_CSS_SYNTAX_TOKENIZER_ERROR_EOINST:
                printf("  [%zu] EOF in string (offset: %zu)\n", i, pos);
                break;
            default:
                printf("  [%zu] Error id: %d (offset: %zu)\n",
                       i, error->id, pos);
                break;
        }
    }

    /* Clean up. */
    lxb_css_syntax_tokenizer_destroy(tkz);

    return EXIT_SUCCESS;
}
```

Output:
```
Found 2 tokenizer error(s):
  [0] Newline in string (offset: 26)
  [1] EOF in comment (offset: 41)
```

## Parser

Please, see the [Parser documentation](/modules/css/parser) for details on parsing CSS syntax into higher-level structures like declarations, rules, and selectors.