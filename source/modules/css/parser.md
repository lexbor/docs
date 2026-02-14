# Parser

* **Includes:** `lexbor/css/css.h`
* **API Reference:** `source/lexbor/css/parser.h`, `source/lexbor/css/syntax/syntax.h` (all `lxb_css_syntax_parse_*` and `lxb_css_syntax_consume_*` functions)
* **Specification:** [CSS Syntax Module](https://drafts.csswg.org/css-syntax/)

## Overview

The Parser (`lxb_css_parser_t`) is the central object of the CSS module. All parsing operations -- stylesheets, selectors, declarations -- require a parser instance. The parser manages the tokenizer, state machine, and coordination between CSS subsystems.

You create a parser once, and then pass it to whatever you need to parse: a full stylesheet, a list of selectors, or a declaration block. Between operations, you call `lxb_css_parser_clean()` to reset state while keeping memory allocations.

## What's Inside

- [**How It Works**](#how-it-works)
- [**Reading Tokens Inside the Parser**](#reading-tokens-inside-the-parser)
- [**Lifecycle**](#lifecycle)
- [**Memory**](#memory)
- [**Example: Parse Declarations with Custom Callbacks**](#example-parse-declarations-with-custom-callbacks)
- [**State Machine Helpers**](#state-machine-helpers)
- [**Callback Reference**](#callback-reference)

## How It Works

The parser is a state machine built on top of the CSS Syntax tokenizer. It works in three layers:

1. **Tokenizer** -- breaks CSS text into tokens (identifiers, numbers, strings, delimiters, etc.)
2. **Syntax Parser** -- consumes tokens according to CSS grammar rules (at-rules, qualified rules, declarations, blocks)
3. **State Callbacks** -- user-provided (or built-in) functions that react to parsed constructs

When you use high-level functions like `lxb_css_stylesheet_parse()` or `lxb_css_declaration_list_parse()`, all three layers work together automatically. But you can also use the Syntax Parser directly with your own callbacks for full control.

### Processing Model

The Syntax Parser drives execution by matching the CSS grammar. As it recognizes constructs, it invokes callbacks on a `lxb_css_syntax_cb_*` structure that you provide:

```
CSS Text
  |
  v
Tokenizer --> tokens
  |
  v
Syntax Parser (grammar rules)
  |
  +--> cb.name()       -- declaration name found
  +--> state()         -- value tokens, one by one
  +--> cb.end()        -- declaration complete
  +--> cb.failed()     -- parse error, skip tokens
  +--> cb.end()        -- all done
```

Each callback struct corresponds to a CSS grammar production:

| Struct | Grammar Production | Key Callbacks |
|--------|--------------------|---------------|
| `lxb_css_syntax_cb_list_rules_t` | List of rules (stylesheet body) | `at_rule`, `qualified_rule`, `next`, `end` |
| `lxb_css_syntax_cb_at_rule_t` | At-rule (`@media`, `@font-face`) | `prelude`, `prelude_end`, `block`, `end` |
| `lxb_css_syntax_cb_qualified_rule_t` | Qualified rule (`div { ... }`) | `prelude`, `prelude_end`, `block`, `end` |
| `lxb_css_syntax_cb_block_t` | Block (`{ ... }`) | `at_rule`, `declarations`, `qualified_rule`, `next`, `end` |
| `lxb_css_syntax_cb_declarations_t` | Declarations (`color: red; ...`) | `name`, `end`, `failed` |
| `lxb_css_syntax_cb_components_t` | Component values | `prelude`, `end` |
| `lxb_css_syntax_cb_function_t` | Function (`rgb(...)`) | `value`, `end` |

All callback structs are defined in `lexbor/css/syntax/syntax.h`.

### Phases and the _END Token

The parser's internal structure is fully controlled by **phases**. Each grammar production (at-rule prelude, declaration value, block content, etc.) runs as a separate phase. Your callback never sees raw tokens from the entire CSS input — it only receives the tokens that belong to its current phase.

The mechanism is simple: the parser has an internal phase function that examines every token before your callback sees it. When the phase detects a grammar boundary — a `;` ending a declaration, a `{` opening a block, a `}` closing it, or EOF — it intercepts the real token and replaces it with a synthetic `_END` token (`LXB_CSS_SYNTAX_TOKEN__END`). Your callback receives `_END` instead of the boundary token, which tells it: "your tokens are over, decide the result."

For example, when parsing `color: red; font-size: 16px`:

```
Phase: declaration value for "color"
  Tokens your callback sees: "red", _END
  (the ";" is intercepted by the phase -- you never see it)

Phase: declaration value for "font-size"
  Tokens your callback sees: "16px", _END
  (the EOF is intercepted by the phase)
```

Each phase is isolated. Your callback does not need to know where one declaration ends and the next begins — the parser handles that. You just consume tokens until `_END`.

### success and failed

When your callback receives `_END`, it must decide: was parsing successful or not?

- Call `lxb_css_parser_success(parser)` — the value was parsed correctly.
- Call `lxb_css_parser_failed(parser)` — the value is invalid, let the error recovery handler deal with it.

**You must consume all non-whitespace tokens before calling `lxb_css_parser_success()`.** After you call it, the parser switches to an internal state that only accepts whitespace and `_END`. If there are unconsumed non-whitespace tokens left, the parser automatically switches to `failed` mode -- as if you had called `lxb_css_parser_failed()`.

Trailing whitespace is an exception: if you call `lxb_css_parser_success()` and the only remaining tokens are whitespace followed by `_END`, the parser consumes them for you. This means you don't have to worry about trailing spaces.

This safety mechanism ensures that your callback never silently ignores part of the input. If you only handle some tokens and call success, the parser treats it as an error — because the unconsumed tokens might be important.

### Callback Types and Token Consumption

Not all callbacks work with the token stream. The parser has three kinds of callbacks, and only one of them reads tokens:

**State callbacks** (return `bool`) — these are the only callbacks that consume tokens. They receive tokens one by one, process them until `_END`, and must call `lxb_css_parser_success()` or `lxb_css_parser_failed()`. These are: `prelude`, `value`, `next`, `cb.failed`, and the value state returned by `name`.

**Done callbacks** (return `lxb_status_t`) — called when a grammar production is complete. The consume is **blocked** inside these callbacks — `lxb_css_syntax_parser_consume()` does nothing because the parser has already set `skip_consume = true`. You receive a token as a parameter, but it is provided only for position information (offsets). Do not try to consume it or read more tokens. Just do your finalization work and return `LXB_STATUS_OK` or an error status. These are: `cb.end`, `prelude_end`, and `end` in declarations.

**Begin callbacks** (return a pointer to a callback struct) — called when the parser needs to decide which callbacks to use for a child production (e.g. which at-rule callbacks to use, or which block callbacks). The consume is also **blocked**. You receive a token for inspection (to look at the at-rule name, for example), but consuming it would break the parser's state. Return the callback struct pointer, or `NULL` on fatal error. These are: `at_rule`, `qualified_rule`, `block`, `declarations`.

In short: if your callback returns `bool`, you read and consume tokens. If it returns anything else (`lxb_status_t` or a pointer), the consume is blocked and you should not interact with the token stream.

## Reading Tokens Inside the Parser

When you write state callbacks (value handlers, `cb.failed`, etc.), you need to read and consume tokens. The parser provides its own set of token functions that wrap the low-level tokenizer functions from `lexbor/css/syntax/token.h`.

### Parser-Level vs Tokenizer-Level Functions

| Parser function | Tokenizer function it wraps | Extra behavior |
|-----------------|----------------------------|----------------|
| `lxb_css_syntax_parser_token(parser)` | `lxb_css_syntax_token(tkz)` | Runs the token through the parser's **phase logic** — the phase may intercept the token, generate `_END`, or change the parser's internal state before your callback sees it. |
| `lxb_css_syntax_parser_token_wo_ws(parser)` | `lxb_css_syntax_token(tkz)` | Same as above, but if the current token is whitespace, automatically consumes it and returns the next non-whitespace token. |
| `lxb_css_syntax_parser_consume(parser)` | `lxb_css_syntax_token_consume(tkz)` | Respects the parser's `skip_consume` flag — if the parser has already consumed the token internally (during phase transitions), the call does nothing. |

### Why Not Use the Tokenizer Functions Directly?

The tokenizer functions (`lxb_css_syntax_token`, `lxb_css_syntax_token_consume`) work with raw tokens from the CSS input. They know nothing about CSS grammar — they just produce tokens and advance the position.

The parser adds a layer on top: the **phase**. Each grammar rule (declarations, at-rules, qualified rules, etc.) has a phase function that examines tokens as they come in. When the phase detects a grammar boundary — a semicolon ending a declaration, a closing brace ending a block, EOF — it replaces the real token with a synthetic `_END` token. This is how the parser tells your callback: "your part is over."

If you call the tokenizer functions directly inside a callback, you bypass this mechanism. You would never see `_END` tokens, and you could consume tokens that the parser needs for its own state transitions.

### How Phase Interception Works

Here is what happens when you call `lxb_css_syntax_parser_token()`:

```
lxb_css_syntax_parser_token(parser)
  |
  +-- lxb_css_syntax_token(parser->tkz)     <-- get raw token from tokenizer
  |
  +-- rule->phase(parser, token, rule)      <-- phase examines the token
        |
        +-- return token                    <-- pass through to your callback
        |
        +-- return &parser->token_end       <-- replace with _END token
            (type = LXB_CSS_SYNTAX_TOKEN__END)
```

From your callback's perspective, you simply receive tokens one by one. When you receive `_END`, it means the parser has decided that the current grammar production is finished. You must stop consuming and call `lxb_css_parser_success()` or `lxb_css_parser_failed()`.

### skip_consume

When the parser transitions between phases (e.g. from "reading declaration value" to "declaration ended"), it sometimes needs to keep the current token for the next phase to see. It does this by setting `skip_consume = true` on the rule. When this flag is set, `lxb_css_syntax_parser_consume()` does nothing — the token stays in the buffer.

This is why you must use `lxb_css_syntax_parser_consume()` rather than `lxb_css_syntax_token_consume()` in callbacks. The parser-level function respects this flag; the tokenizer-level function does not.

### Usage Pattern in Callbacks

Inside a state callback, the standard pattern is:

```C
static bool
my_value_state(lxb_css_parser_t *parser,
               const lxb_css_syntax_token_t *token, void *ctx)
{
    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__END) {
        /* Process token... */

        lxb_css_syntax_parser_consume(parser);
        token = lxb_css_syntax_parser_token(parser);
    }

    return lxb_css_parser_success(parser);
}
```

To skip whitespace automatically, use `lxb_css_syntax_parser_token_wo_ws()`:

```C
/* Get first non-whitespace token. */
token = lxb_css_syntax_parser_token_wo_ws(parser);

/* If the raw token was whitespace, it has been consumed for you.
 * 'token' is now the first non-whitespace token (or _END). */
```

### Summary

| Rule | Why |
|------|-----|
| Use `lxb_css_syntax_parser_token()` inside callbacks | So the phase can intercept tokens and generate `_END` at grammar boundaries. |
| Use `lxb_css_syntax_parser_consume()` inside callbacks | So `skip_consume` is respected and you don't consume a token the parser still needs. |
| Use `lxb_css_syntax_token()` / `lxb_css_syntax_token_consume()` only outside the parser | These are for standalone tokenization without the parser (see [Syntax Tokenizer](/modules/css/syntax)). |

## Lifecycle

```C
/* Create parser */
lxb_css_parser_t *parser = lxb_css_parser_create();

/* Initialize. Pass NULL to create an internal tokenizer. */
lxb_status_t status = lxb_css_parser_init(parser, NULL);

/*
 * Create a memory pool for parsed objects and assign it to the parser.
 * The parser itself does not create a memory pool -- you must provide one.
 */
lxb_css_memory_t *memory = lxb_css_memory_create();
lxb_css_memory_init(memory, 4096);
lxb_css_parser_memory_set(parser, memory);

/* Use the parser for parsing operations... */

/* Reset parser state for reuse (keeps allocations) */
lxb_css_parser_clean(parser);

/* Use again... */

/* Destroy when done. */
lxb_css_memory_destroy(memory, true);
lxb_css_parser_destroy(parser, true);
```

## Memory

The parser and its parsed objects have separate lifetimes. The parser (`lxb_css_parser_t`) is a tool -- it tokenizes, runs the state machine, calls callbacks. The objects it produces (stylesheets, rules, declarations, selector lists) live in a separate memory pool: `lxb_css_memory_t`.

You create `lxb_css_memory_t` yourself and assign it to the parser before parsing:

```C
lxb_css_memory_t *memory = lxb_css_memory_create();
lxb_css_memory_init(memory, 4096);
lxb_css_parser_memory_set(parser, memory);
```

The parser does not own the memory -- it only holds a pointer. This means:

- **You can destroy the parser and keep the objects.** After parsing, destroy the parser to free its internal state (tokenizer, stack, etc.), while the parsed objects remain valid as long as `lxb_css_memory_t` is alive.
- **Destroying `lxb_css_memory_t` destroys all objects at once.** Every object allocated during parsing -- rules, declarations, selector lists, strings -- is freed when you call `lxb_css_memory_destroy()`. You don't need to destroy them individually.
- **Cleaning memory resets it for reuse.** `lxb_css_memory_clean()` marks all allocations as free without releasing the underlying buffers. After cleaning, all previously parsed objects are invalid, but the memory is ready for new parsing without reallocation overhead.

A typical pattern when you need to keep parsed results:

```C
/* Create memory and parser. */
lxb_css_memory_t *memory = lxb_css_memory_create();
lxb_css_memory_init(memory, 4096);

lxb_css_parser_t *parser = lxb_css_parser_create();
lxb_css_parser_init(parser, NULL);

/* Assign memory to parser. */
lxb_css_parser_memory_set(parser, memory);

/* Parse. */
lxb_css_selector_list_t *list = lxb_css_selectors_parse(parser, ...);

/* Done parsing -- destroy the parser, keep the results. */
lxb_css_parser_destroy(parser, true);

/* Use the selector list -- it's still alive in memory. */
lxb_css_selector_serialize_list(list, callback, NULL);

/* When done with all objects, destroy memory. */
lxb_css_memory_destroy(memory, true);
```

## Example: Parse Declarations with Custom Callbacks

This example shows how to parse CSS declarations directly using the Syntax Parser with your own callbacks. Each callback prints what the parser found to stdout.

This is useful when you need full control over the parsing process -- for example, to handle unknown properties, build your own data structures, or process declarations in a streaming fashion.

```C
#include <lexbor/css/css.h>


/* Forward declarations. */

static lxb_css_parser_state_f
my_declaration_name(lxb_css_parser_t *parser,
                    const lxb_css_syntax_token_t *token,
                    void *ctx, void **out_ctx);

static bool
my_declaration_value(lxb_css_parser_t *parser,
                     const lxb_css_syntax_token_t *token, void *ctx);

static lxb_status_t
my_declaration_end(lxb_css_parser_t *parser,
                   void *declarations, void *ctx,
                   const lxb_css_syntax_token_t *token,
                   lxb_css_syntax_declaration_offset_t *offset,
                   bool important, bool failed);

static lxb_status_t
my_declarations_end(lxb_css_parser_t *parser,
                    const lxb_css_syntax_token_t *token,
                    void *ctx, bool failed);

static bool
my_declarations_failed(lxb_css_parser_t *parser,
                       const lxb_css_syntax_token_t *token, void *ctx);

static lxb_status_t
serialize_cb(const lxb_char_t *data, size_t len, void *ctx);


/*
 * Declaration callbacks.
 *
 * This is the key structure: it tells the Syntax Parser what to do
 * when it encounters parts of a declaration.
 */
static const lxb_css_syntax_cb_declarations_t my_declarations_cb = {
    .name = my_declaration_name,         /* Called when property name is found. */
    .end  = my_declaration_end,          /* Called when declaration is complete. */
    .cb.failed = my_declarations_failed, /* Called on parse error. */
    .cb.end    = my_declarations_end     /* Called when all declarations done. */
};


int
main(void)
{
    lxb_status_t status;
    lxb_css_parser_t *parser;
    lxb_css_memory_t *memory;
    lxb_css_rule_declaration_list_t *list;

    static const lxb_char_t css[]
        = "color: red; font-size: 16px; width: 100% !important; "
          "--my-var: hello";

    printf("Input: %s\n\n", (const char *) css);

    /* Create and init the parser. */

    parser = lxb_css_parser_create();
    status = lxb_css_parser_init(parser, NULL);

    if (status != LXB_STATUS_OK) {
        fprintf(stderr, "Failed to init parser.\n");
        return EXIT_FAILURE;
    }

    /*
     * Create a memory pool and assign it to the parser.
     *
     * The parser does not create its own memory pool. All parsed objects
     * (declaration lists, rules, etc.) are allocated from this pool.
     */
    memory = lxb_css_memory_create();
    status = lxb_css_memory_init(memory, 128);

    if (status != LXB_STATUS_OK) {
        fprintf(stderr, "Failed to init memory.\n");
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    lxb_css_parser_memory_set(parser, memory);

    printf("Output:\n");

    /*
     * Parse declarations using our custom callbacks.
     *
     * lxb_css_syntax_parse_declarations() sets up the buffer,
     * pushes the declarations rule onto the parser stack,
     * and runs the parser loop.
     */
    list = lxb_css_syntax_parse_declarations(parser, &my_declarations_cb,
                                             css, sizeof(css) - 1);
    if (list == NULL) {
        fprintf(stderr, "Failed to parse declarations.\n");
        lxb_css_memory_destroy(memory, true);
        lxb_css_parser_destroy(parser, true);
        return EXIT_FAILURE;
    }

    /* Clean up. */

    lxb_css_rule_declaration_list_destroy(list, true);
    lxb_css_memory_destroy(memory, true);
    lxb_css_parser_destroy(parser, true);

    return EXIT_SUCCESS;
}

/*
 * Called when the parser finds a declaration name (e.g. "color", "width").
 *
 * The token is the IDENT token of the property name. The colon has already
 * been consumed by the Syntax Parser.
 *
 * Return a state callback that will receive value tokens. Return NULL to
 * signal a fatal error (OOM, etc.).
 */
static lxb_css_parser_state_f
my_declaration_name(lxb_css_parser_t *parser,
                    const lxb_css_syntax_token_t *token,
                    void *ctx, void **out_ctx)
{
    printf("  Name:  ");
    lxb_css_syntax_token_serialize(token, serialize_cb, NULL);
    printf("\n");

    printf("  Value: ");

    /* Return our value callback. The parser will call it with each token. */

    return my_declaration_value;
}

/*
 * Called for each token in the declaration value.
 *
 * We consume all tokens until the parser sends _END.
 *
 * Important: you must consume all tokens (or call lxb_css_parser_success())
 * before _END to avoid an infinite loop.
 */
static bool
my_declaration_value(lxb_css_parser_t *parser,
                     const lxb_css_syntax_token_t *token, void *ctx)
{
    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__END) {
        lxb_css_syntax_token_serialize(token, serialize_cb, NULL);

        lxb_css_syntax_parser_consume(parser);
        token = lxb_css_syntax_parser_token(parser);
    }

    printf("\n");

    return lxb_css_parser_success(parser);
}

/*
 * Called when a single declaration is finished.
 *
 * Here you receive: the declaration context, whether !important was set,
 * whether parsing failed, and offset information for the original text.
 */
static lxb_status_t
my_declaration_end(lxb_css_parser_t *parser,
                   void *declarations, void *ctx,
                   const lxb_css_syntax_token_t *token,
                   lxb_css_syntax_declaration_offset_t *offset,
                   bool important, bool failed)
{
    if (important) {
        printf("  Flags: !important\n");
    }

    if (failed) {
        printf("  Status: FAILED\n");
    }

    printf("\n");

    return LXB_STATUS_OK;
}

/*
 * Called when all declarations have been processed.
 */
static lxb_status_t
my_declarations_end(lxb_css_parser_t *parser,
                    const lxb_css_syntax_token_t *token,
                    void *ctx, bool failed)
{
    printf("Done.\n");

    return LXB_STATUS_OK;
}

/*
 * Called when the parser encounters an error in a declaration.
 *
 * We consume all remaining tokens and let the parser continue
 * with the next declaration.
 */
static bool
my_declarations_failed(lxb_css_parser_t *parser,
                       const lxb_css_syntax_token_t *token, void *ctx)
{
    while (token != NULL && token->type != LXB_CSS_SYNTAX_TOKEN__END) {
        lxb_css_syntax_parser_consume(parser);
        token = lxb_css_syntax_parser_token(parser);
    }

    return lxb_css_parser_success(parser);
}

/* Serialization callback: writes data to stdout. */
static lxb_status_t
serialize_cb(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);
    return LXB_STATUS_OK;
}
```

Output:

```
Input: color: red; font-size: 16px; width: 100% !important; --my-var: hello
Output:
  Name:  color
  Value: red

  Name:  font-size
  Value: 16px

  Name:  width
  Value: 100%
  Flags: !important

  Name:  --my-var
  Value: hello

Done.
```

### Key Points

**Callback lifecycle.** For each declaration, the Syntax Parser calls: `name` -> value state (your function) -> `end`. When all declarations are done, it calls `cb.end`. If a parse error occurs, `cb.failed` is called instead of the value state.

**Value state.** The function returned by `name` receives tokens one at a time. You must consume tokens until `LXB_CSS_SYNTAX_TOKEN__END` and call `lxb_css_parser_success()`. If the value doesn't match your expected grammar, call `lxb_css_parser_failed()` -- the parser will switch to the `cb.failed` handler.

**`lxb_css_syntax_parse_declarations()` vs `lxb_css_declaration_list_parse()`.** The first takes your custom callbacks and gives you full control. The second uses built-in callbacks (`lxb_css_state_cb_declarations()`) that create `lxb_css_rule_declaration_t` objects with typed property values. Use the second when you want ready-made data structures; use the first when you need custom processing.

## State Machine Helpers

The parser provides helper functions for use inside state callbacks:

| Function | What it does |
|----------|--------------|
| `lxb_css_parser_success(parser)` | Mark the current rule as successfully parsed. Switches to a state that consumes trailing whitespace and waits for `_END`. |
| `lxb_css_parser_failed(parser)` | Mark the current rule as failed. Switches to the rule's `cb.failed` handler for error recovery. |
| `lxb_css_parser_stop(parser)` | Stop the parser main loop immediately. |
| `lxb_css_parser_fail(parser, status)` | Hard failure (OOM, overflow). Sets status and stops the loop. |
| `lxb_css_parser_unexpected(parser)` | Mark token as unexpected. Sets `LXB_STATUS_ERROR_UNEXPECTED_DATA`. |

**Important:** In your value state callback, you must either consume all tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()` to let the error recovery handler consume them. Not doing so will cause an infinite loop.

## Callback Reference

Every callback struct has a base `cb` field with two common callbacks:

- **`cb.failed`** (`lxb_css_parser_state_f`) -- state callback for error recovery. Must consume tokens until `_END` and call `lxb_css_parser_success()`.
- **`cb.end`** (`lxb_css_syntax_cb_done_f`) -- called when the rule is finished. Returns `lxb_status_t`. Does **not** need `success`/`failed`.

Below is the full reference for each callback struct.

### lxb_css_syntax_cb_declarations_t

Parses a list of declarations (`color: red; font-size: 16px`).

```C
struct lxb_css_syntax_cb_declarations {
    lxb_css_syntax_cb_base_t          cb;
    lxb_css_syntax_declaration_name_f name;
    lxb_css_syntax_declaration_end_f  end;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `name` | `lxb_css_parser_state_f` -- the value state callback. `NULL` = fatal error. | No. Return a state function or `NULL`. |
| *(value state)* | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `end` | `lxb_status_t` | No. Return `LXB_STATUS_OK` or an error status. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_list_rules_t

Parses a list of rules (stylesheet body or block contents).

```C
struct lxb_css_syntax_cb_list_rules {
    lxb_css_syntax_cb_base_t              cb;
    lxb_css_parser_state_f                next;
    lxb_css_syntax_begin_at_rule_f        at_rule;
    lxb_css_syntax_begin_qualified_rule_f qualified_rule;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `at_rule` | `const lxb_css_syntax_cb_at_rule_t *` -- callbacks for this at-rule. `NULL` = fatal error. | No. |
| `qualified_rule` | `const lxb_css_syntax_cb_qualified_rule_t *`. `NULL` = fatal error. | No. |
| `next` | `bool` | **Yes.** Called after each child rule completes. Call `lxb_css_parser_success()`. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_at_rule_t

Parses an at-rule (`@media`, `@font-face`, etc.).

```C
struct lxb_css_syntax_cb_at_rule {
    lxb_css_syntax_cb_base_t     cb;
    lxb_css_parser_state_f       prelude;
    lxb_css_syntax_cb_done_f     prelude_end;
    lxb_css_syntax_begin_block_f block;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `prelude` | `bool` | **Yes.** Must consume prelude tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `prelude_end` | `lxb_status_t` | No. |
| `block` | `const lxb_css_syntax_cb_block_t *`. `NULL` = fatal error. | No. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_qualified_rule_t

Parses a qualified rule (`div { ... }`).

```C
struct lxb_css_syntax_cb_qualified_rule {
    lxb_css_syntax_cb_base_t     cb;
    lxb_css_parser_state_f       prelude;
    lxb_css_syntax_cb_done_f     prelude_end;
    lxb_css_syntax_begin_block_f block;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `prelude` | `bool` | **Yes.** Must consume prelude tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `prelude_end` | `lxb_status_t` | No. |
| `block` | `const lxb_css_syntax_cb_block_t *`. `NULL` = fatal error. | No. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_block_t

Parses a block (`{ ... }`). Decides what kind of content is inside.

```C
struct lxb_css_syntax_cb_block {
    lxb_css_syntax_cb_base_t              cb;
    lxb_css_parser_state_f                next;
    lxb_css_syntax_begin_at_rule_f        at_rule;
    lxb_css_syntax_begin_declarations_f   declarations;
    lxb_css_syntax_begin_qualified_rule_f qualified_rule;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `at_rule` | `const lxb_css_syntax_cb_at_rule_t *`. `NULL` = fatal error. | No. |
| `declarations` | `const lxb_css_syntax_cb_declarations_t *`. `NULL` = fatal error. | No. |
| `qualified_rule` | `const lxb_css_syntax_cb_qualified_rule_t *`. `NULL` = fatal error. | No. |
| `next` | `bool` | **Yes.** Called after each child completes. Call `lxb_css_parser_success()`. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_components_t

Parses component values (e.g. inside a property value or function argument).

```C
struct lxb_css_syntax_cb_components {
    lxb_css_syntax_cb_base_t cb;
    lxb_css_parser_state_f   prelude;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `prelude` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_function_t

Parses a function call (`rgb(...)`, `calc(...)`, etc.).

```C
struct lxb_css_syntax_cb_function {
    lxb_css_syntax_cb_base_t cb;
    lxb_css_parser_state_f   value;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `value` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### lxb_css_syntax_cb_pipe_t

Parses a pipe (passes tokens through without bracket tracking).

```C
struct lxb_css_syntax_cb_pipe {
    lxb_css_syntax_cb_base_t cb;
    lxb_css_parser_state_f   prelude;
};
```

| Callback | Returns | Must call `success`/`failed`? |
|----------|---------|-------------------------------|
| `prelude` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`, or call `lxb_css_parser_failed()`. |
| `cb.failed` | `bool` | **Yes.** Must consume tokens until `_END` and call `lxb_css_parser_success()`. |
| `cb.end` | `lxb_status_t` | No. |

### Summary

The rule is simple:

- **State callbacks** (type `lxb_css_parser_state_f`, return `bool`) -- **must** call `lxb_css_parser_success()` or `lxb_css_parser_failed()` before returning. These are: `prelude`, `value`, `next`, `cb.failed`, and the value state returned by `name`.
- **Done callbacks** (type `lxb_css_syntax_cb_done_f`, return `lxb_status_t`) -- must **not** call `success`/`failed`. Just return `LXB_STATUS_OK` or an error status. These are: `cb.end`, `prelude_end`, and `end` in declarations.
- **Begin callbacks** (return a pointer to another callback struct) -- must **not** call `success`/`failed`. Return the callback struct pointer, or `NULL` on fatal error. These are: `at_rule`, `qualified_rule`, `block`, `declarations`.
