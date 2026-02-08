# Intercept Tokenizer Callbacks Before Tree Building

In this tutorial, we will learn how to:

1. Set up the HTML parser and access its internal tokenizer.
2. Intercept the tokenizer callback that feeds tokens to the tree builder.
3. Inspect each token (tag, text, comment) before it reaches the DOM tree.
4. Filter out whitespace-only text tokens so they never appear in the final tree.

This technique is useful when you want to preprocess, log, or selectively discard
tokens during parsing — for example, to strip insignificant whitespace, remove
comments, or reject certain elements before the tree builder ever sees them.

**Important:** Filtering tokens before the tree builder violates the
[HTML specification](https://html.spec.whatwg.org/multipage/parsing.html),
which requires all tokens to be processed by the tree construction algorithm.
The resulting DOM tree may differ from what a spec-compliant parser would produce.
However, this approach can be valuable in practice — for data extraction,
preprocessing pipelines, template engines, or any scenario where strict
spec compliance is not required and you need full control over which tokens
enter the tree.


## Prerequisites

- `lexbor` library installed on your system. See the [Quick Start](../documentation.md)
  guide for installation instructions.
- Basic knowledge of C.


## The Complete Example

Here is the full source code. We will break it down step by step below.

```c
#include <lexbor/html/html.h>


typedef struct {
    lxb_html_tokenizer_token_f original_callback;
    void                       *original_ctx;
    unsigned                   skipped;
} filter_ctx_t;


static lxb_html_token_t *
token_filter(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    filter_ctx_t *fctx = ctx;

    if (token->tag_id == LXB_TAG__TEXT) {
        const lxb_char_t *p = token->text_start;

        /* Check whether the text is whitespace-only. */

        while (p < token->text_end) {
            switch (*p) {
                case 0x09: /* Tab */
                case 0x0A: /* LF */
                case 0x0C: /* FF */
                case 0x0D: /* CR */
                case 0x20: /* Space */
                    break;

                default:
                    /* Found a non-whitespace character — keep the token. */
                    goto pass;
            }

            p++;
        }

        /* Entirely whitespace — skip this token. */

        fctx->skipped++;

        printf("Skipped whitespace-only text token (%zu bytes)\n",
               (size_t) (token->text_end - token->text_start));

        return token;
    }

pass:

    /* Forward the token to the original tree-builder callback. */

    return fctx->original_callback(tkz, token, fctx->original_ctx);
}

static lxb_status_t
serialize_callback(const lxb_char_t *data, size_t len, void *ctx)
{
    printf("%.*s", (int) len, (const char *) data);

    return LXB_STATUS_OK;
}

int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    lxb_html_parser_t *parser;
    lxb_html_tokenizer_t *tkz;
    lxb_html_document_t *document;
    filter_ctx_t fctx;

    static const lxb_char_t html[] =
        "<html>\n"
        "  <head>\n"
        "    <title>Example</title>\n"
        "  </head>\n"
        "  <body>\n"
        "    <h1>Hello</h1>\n"
        "    \n"
        "    <p>World</p>\n"
        "    \n"
        "  </body>\n"
        "</html>";
    size_t html_len = sizeof(html) - 1;

    /* Step 1: Create and initialize the parser. */

    parser = lxb_html_parser_create();
    status = lxb_html_parser_init(parser);
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Step 2: Save the original tree-builder callback. */

    tkz = lxb_html_parser_tokenizer(parser);

    fctx.original_callback = tkz->callback_token_done;
    fctx.original_ctx = lxb_html_tokenizer_callback_token_done_ctx(tkz);
    fctx.skipped = 0;

    /* Step 3: Replace the callback with our filter. */

    lxb_html_tokenizer_callback_token_done_set(tkz, token_filter, &fctx);

    /* Step 4: Parse the HTML document. */

    document = lxb_html_parse(parser, html, html_len);
    if (document == NULL) {
        goto failed;
    }

    /* Step 5: Print results. */

    printf("\nSkipped %u whitespace-only text token(s).\n\n", fctx.skipped);

    printf("Resulting tree:\n");

    status = lxb_html_serialize_pretty_tree_cb(
        lxb_dom_interface_node(document),
        LXB_HTML_SERIALIZE_OPT_UNDEF, 0,
        serialize_callback, NULL
    );
    if (status != LXB_STATUS_OK) {
        goto failed;
    }

    /* Cleanup. */

    lxb_html_document_destroy(document);
    lxb_html_parser_destroy(parser);

    return EXIT_SUCCESS;

failed:

    printf("Something went wrong.\n");

    return EXIT_FAILURE;
}
```


## Step-by-Step Explanation

### Step 1: Create and Initialize the Parser

```c
parser = lxb_html_parser_create();
status = lxb_html_parser_init(parser);
```

When we call `lxb_html_parser_init()`, it creates both a tokenizer and a tree
builder internally. The tree builder registers its own callback on the tokenizer
so that every token emitted during parsing is forwarded to the tree-building
algorithm.

### Step 2: Save the Original Tree-Builder Callback

```c
tkz = lxb_html_parser_tokenizer(parser);

fctx.original_callback = tkz->callback_token_done;
fctx.original_ctx = lxb_html_tokenizer_callback_token_done_ctx(tkz);
```

After `lxb_html_parser_init()` completes, the tokenizer's `callback_token_done`
field points to the internal tree-builder callback. We save both the function
pointer and its context so we can call the original callback later for tokens we
want to keep.

`lxb_html_parser_tokenizer()` returns a pointer to the parser's internal
tokenizer.

### Step 3: Replace the Callback With Our Filter

```c
lxb_html_tokenizer_callback_token_done_set(tkz, token_filter, &fctx);
```

Now we replace the tokenizer's callback with our own `token_filter` function.
From this point, every token will go through our filter first. The filter decides
which tokens are forwarded to the tree builder and which are silently discarded.

### Step 4: The Filter Callback

```c
static lxb_html_token_t *
token_filter(lxb_html_tokenizer_t *tkz, lxb_html_token_t *token, void *ctx)
{
    /* ... */
}
```

The callback receives three arguments:

1. `tkz` — the tokenizer that emitted the token.
2. `token` — the token itself (see `lxb_html_token_t`).
3. `ctx` — the user context we passed in Step 3.

The key fields of `lxb_html_token_t` for filtering are:

- `tag_id` — identifies the token kind. `LXB_TAG__TEXT` for text nodes,
  `LXB_TAG__EM_COMMENT` for comments, `LXB_TAG__END_OF_FILE` for EOF, or any
  HTML tag id (`LXB_TAG_DIV`, `LXB_TAG_P`, etc.) for element tokens.
- `type` — flags such as `LXB_HTML_TOKEN_TYPE_CLOSE` (closing tag) and
  `LXB_HTML_TOKEN_TYPE_CLOSE_SELF` (self-closing tag).
- `text_start` / `text_end` — pointers to the text content (for text tokens).
- `attr_first` — the first attribute in a linked list (for element tokens).

**To skip a token**, return it without calling the original callback — the tree
builder never sees it and it will not appear in the DOM tree.

**To keep a token**, call the original callback:

```c
return fctx->original_callback(tkz, token, fctx->original_ctx);
```

In this tutorial, we check whether a text token contains only whitespace
characters (space, tab, LF, CR, FF). If it does, we skip it. Otherwise, we
forward it to the tree builder.

### Step 5: Parse and Serialize

```c
document = lxb_html_parse(parser, html, html_len);
```

Parsing works exactly as usual. The only difference is that our filter sits
between the tokenizer and the tree builder, intercepting every token.

After parsing, we serialize the resulting DOM tree using
`lxb_html_serialize_pretty_tree_cb()` to see the effect of our filtering.


## Expected Output

```
Skipped whitespace-only text token (3 bytes)
Skipped whitespace-only text token (5 bytes)
Skipped whitespace-only text token (3 bytes)
Skipped whitespace-only text token (3 bytes)
Skipped whitespace-only text token (5 bytes)
Skipped whitespace-only text token (10 bytes)
Skipped whitespace-only text token (8 bytes)
Skipped whitespace-only text token (1 bytes)

Skipped 8 whitespace-only text token(s).

Resulting tree:
<html>
  <head>
    <title>
      "Example"
    </title>
  </head>
  <body>
    <h1>
      "Hello"
    </h1>
    <p>
      "World"
    </p>
  </body>
</html>
```

The whitespace-only text nodes (newlines and spaces between tags) have been
removed from the tree. The meaningful text content inside `<title>`, `<h1>`, and
`<p>` elements is preserved.


## Building

Compile the example and run:

```sh
gcc filter_tokens.c -llexbor -o filter_tokens
./filter_tokens
```


## Going Further

You can adapt this approach for many use cases:

- **Remove comments:** Check `token->tag_id == LXB_TAG__EM_COMMENT` and skip.
- **Block specific tags:** Check `token->tag_id == LXB_TAG_SCRIPT` (or any other
  tag) and skip both the opening and closing tokens.
- **Log all tokens:** Print token information for debugging without changing the
  parsing behavior.
- **Modify attributes:** Inspect `token->attr_first` and alter attribute values
  before they reach the tree builder.


## Summary

In this tutorial, we learned how to:

- Access the parser's internal tokenizer with `lxb_html_parser_tokenizer()`.
- Save and chain the tree-builder callback for token interception.
- Inspect token fields (`tag_id`, `text_start`, `text_end`) to make filtering
  decisions.
- Skip whitespace-only text tokens by not forwarding them to the tree builder.
- Serialize the resulting DOM tree with `lxb_html_serialize_pretty_tree_cb()`.
