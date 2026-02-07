# Part one: HTML

**Note:** This article was written during the early development of the Lexbor HTML parser. Some code examples and internal values (such as token type flags) may differ from the current implementation. For up-to-date API reference, see the [HTML module documentation](../modules/html.md).

Hello, everyone!

In this article, I will explain how to create a superfast HTML parser that
supports DOM. We will examine the HTML specification and its limitations in
terms of performance and resource consumption during HTML parsing.

I assume the reader has a basic understanding of HTML: tags, nodes, elements,
and namespaces.

## HTML Specification

Before implementing the parser, we need to decide which HTML specification to
follow.

There are two main HTML specifications:

1. [WHATWG](https://html.spec.whatwg.org/multipage/): Maintained by Apple,
   Mozilla, Google, and Microsoft
2. [W3C](https://www.w3.org/TR/html/): Maintained by a long list of companies


We chose to follow WHATWG. It is a living standard maintained by major
companies, each managing its own browser or browser engine.

UPDATE: Unfortunately, the links might not work if you are located in Russia.
This issue seems to be related to Telegram throttling attempts by the
authorities.

## HTML Parsing Details

HTML tree construction can be divided into four parts:

1. Decoder
2. Preprocessing
3. Tokenizer
4. Tree Construction

Let's examine each stage separately.


## Decoder

The tokenizer accepts Unicode characters (code points) as input. Therefore, we
need to convert the byte stream to Unicode characters using the Encoding
specification.

If the HTML encoding is unknown (e.g., there's no HTTP header), we need to
determine it before decoding. This is done using the encoding sniffing
algorithm.

The algorithm works as follows: we wait for 500ms or until we have received the
first 1024 bytes from the byte stream. We then perform a prescan to identify the
encoding, attempting to find a `<meta>` tag with `http-equiv`, `content`, or
`charset` attributes to determine the encoding assumed by the HTML developer.

The Encoding specification lists the minimum set of supported encodings for a
browser engine (21 in total): UTF-8, ISO-8859-2, ISO-8859-7, ISO-8859-8,
windows-874, windows-1250, windows-1251, windows-1252, windows-1254,
windows-1255, windows-1256, windows-1257, windows-1258, gb18030, Big5,
ISO-2022-JP, Shift_JIS, EUC-KR, UTF-16BE, UTF-16LE, and x-user-defined.

For details on Lexbor's encoding support, see the [Encoding module documentation](../modules/encoding.md).

## Preprocessing

Once we have decoded the bytes into Unicode characters, we need to perform a
"sweep". Specifically, we replace all carriage return characters (`\r`) followed
by a newline character (`\n`) with a single carriage return character (`\r`).
Next, we replace all remaining carriage return characters with newline
characters (`\n`).

According to the specification, this means transforming `\r\n` into `\r`, and
then `\r` into `\n`.

In practice, this is simplified:

If a carriage return character (`\r`) is followed by a newline character (`\n`),
replace both with a single newline character (`\n`). If there is no newline
character following, replace only the carriage return (`\r`) with a newline
(`\n`).

This preprocessing step ensures that carriage return characters are removed
before the data reaches the tokenizer, which does not expect or handle carriage
returns.

## Parsing Errors

To address potential questions, it's important to clarify what constitutes a
parse error.

A parse error is essentially a warning that the HTML being parsed is invalid. It
does not halt data processing or prevent tree construction. Instead, it
indicates a discrepancy between what was expected and what was found.

Parse errors can occur due to issues like surrogate pairs, null characters
(`\0`), incorrect tag locations, or invalid `<!DOCTYPE>` declarations.

Some parse errors can have consequences. For instance, an invalid `<!DOCTYPE>`
can result in the HTML tree being labeled as `QUIRKS`, which affects certain DOM
functions.

## Tokenizer

As mentioned, the tokenizer processes Unicode characters as input. It operates
as a state machine with 80 states. Each state has conditions for Unicode
characters, and depending on the input symbol, the tokenizer may:

1. Change state
2. Generate a token and change state
3. Do nothing and wait for the next character

The tokenizer generates six types of tokens: `DOCTYPE`, `Start Tag`, `End Tag`,
`Comment`, `Character`, and `End-Of-File`, which are passed to the tree
construction stage.

Note that the tokenizer does not have explicit knowledge of all its states, only
about 40% of them (approximately). The remaining 60% are used for tree
construction.

This distinction is necessary for properly parsing tags like `<textarea>`,
`<style>`, `<script>`, and `<title>`. These are tags where we do not expect
other tags; they simply close.

For example, the `<title>` tag cannot contain any other tags. Any tags within
`<title>` will be treated as text until the closing tag `</title>` is
encountered.

Why is this approach used? It could be simplified if the tokenizer were
instructed to follow a specific path upon encountering a `<title>` tag. However,
namespaces affect the behavior of the tree construction stage, which in turn
influences the tokenizer's behavior.

Consider the behavior of the `<title>` tag in different namespaces like HTML and
SVG:

HTML:

```html
<title><span>text</span></title>
```

The resulting tree:

```html
<title>
    "<span>text</span>"
```

SVG:

```html
<svg><title><span>text</span></title></svg>
```

The resulting tree:

```html
<svg>
    <title>
        <span>
            "text"
```


In the HTML namespace, the `<span>` tag is treated as text, so no `<span>`
element is created. In the SVG namespace, however, an element is created based
on the `<span>` tag. Thus, tags behave differently depending on the namespace.

But there’s more. The tokenizer must also be aware of the current namespace to
process `CDATA` correctly.

Consider two examples involving `CDATA` and two different namespaces:

1. **HTML Namespace**:
   ```
   <script>
   <![CDATA[<span>This is a test</span>]]>
   </script>
   ```
   In this example, the `CDATA` section is treated as raw text, and the `<span>`
   tag is not processed as an HTML element but as part of the script content.

2. **SVG Namespace**:
   ```
   <svg>
   <![CDATA[<span>This is a test</span>]]>
   </svg>
   ```
   Here, the `CDATA` section is still treated as raw text, but the `<span>` tag
   is interpreted according to SVG rules if it appears within the SVG namespace.

The tokenizer's awareness of the namespace ensures that elements and content are
handled appropriately in each context.

HTML:

```html
<div><![CDATA[ text ]]></div>
```

The resulting tree:

```html
<div>
    <!--[CDATA[ text ]]-->
```

SVG:

```html
<div><svg><![CDATA[ text ]]></svg></div>
```

The resulting tree:

```html
<div>
    <svg>
        " text "
```

In the first case (HTML namespace), the tokenizer interpreted `CDATA` as a
comment. In the second case, the tokenizer parsed the `CDATA` structure and
extracted data from it. As a general rule: if `CDATA` is encountered outside
HTML namespaces, it is parsed; otherwise, it is treated as a comment.

This illustrates the relationship between the tokenizer and the tree. The
tokenizer must be aware of the namespace during the tree construction stage, and
the construction stage can influence the tokenizer's state.

### Tokens

Next, we will examine all six types of tokens generated by the tokenizer. Note
that all tokens contain processed data and are "ready for use." This means all
named character references (such as `&copy`) are converted to Unicode
characters.

### DOCTYPE Token

The DOCTYPE token has a unique structure compared to other tags. It includes:

1. Name
2. Public identifier
3. System identifier

In modern HTML, a valid `DOCTYPE` appears as follows:

```html
<!DOCTYPE html>
```


All other `<!DOCTYPE>` declarations will be treated as parse errors.

### Start Tag Token

The opening tag may include:

1. Tag name
2. Attributes
3. Flags

For example:
```html
<div key="value" />
```

The opening tag can include a `self-closing` flag. This flag does not impact the
closing of the tag but may cause a parse error for non-void elements.

### End Tag Token

A closing tag. It shares all properties of the opening tag token but has a slash
(`/`) before the tag name.

```
</div key="value" />
```

The closing tag can also include a `self-closing` flag, which will result in a
`parse error`. Additionally, any attributes in the closing tag will cause a
parse error. They will be properly parsed but discarded during the tree
construction stage.

### Comment Token

The comment token includes the entire text of the comment. It is copied directly
from the stream into the token.

Example:
```html
<!-- A comment -->
```

### Character Token

The character token is one of the most interesting token types. It represents a
single Unicode character. Each character in HTML generates a separate token,
which is then sent to the tree construction stage. This process can be quite
resource-intensive. Let's see how it works.

Consider this HTML:
```html
<span>Слава императору! &reg;</span>
```

How many tokens do you think are created for this example? Answer: 22.

Here is the list of generated tokens:

```
Start tag token: `<span>`
Character token: С
Character token: л
Character token: а
Character token: в
Character token: а
Character token: 
Character token: и
Character token: м
Character token: п
Character token: е
Character token: р
Character token: а
Character token: т
Character token: о
Character token: р
Character token: у
Character token: !
Character token: 
Character token: ®
End tag token: `</span>`
End-of-file token
```

Not exactly comforting, is it? Indeed, many HTML parser authors use only one
token during this processing step, recycling it by clearing the data each time.

Let's move forward and address a key question: Why is this approach used instead
of processing the text in one piece? The answer lies in the tree construction
stage.

The tokenizer alone is insufficient without the HTML tree construction stage,
where the text is assembled according to various conditions.

The conditions generally include:

1. If a `U+0000 (NULL)` character token is encountered, a parse error is
   triggered, and the token is ignored.
2. If a `U+0009 (CHARACTER TABULATION)`, `U+000A (LINE FEED (LF))`, `U+000C
   (FORM FEED (FF))`, or `U+0020 (SPACE)` character token is encountered, an
   algorithm is invoked to restore active formatting elements and insert the
   token into the tree.

The character token is added to the tree based on the following algorithm:

1. If the current insertion position is not a text node, create a text node,
   insert it into the tree, and add the token data to it.
2. Otherwise, add the token data to the existing text node.

This approach has its drawbacks. The need to create a token and send it for
analysis to the tree construction stage for each character is inefficient. Since
we don't know the size of the text node in advance, we either need to
pre-allocate a large amount of memory or perform frequent reallocations. Both
approaches are costly in terms of memory and time.

### End-Of-File Token

A straightforward token indicating that no data is left; it simply informs the
tree construction stage of this fact.

## Tree Construction

Tree construction involves a finite state machine with `23 states` and numerous
token-related conditions (tags, text). It is the most complex stage and occupies
a significant portion of the specification (the side effects may include
lethargy and extreme frustration).

In essence, tokens are processed as input, and based on the token, the state of
tree construction is adjusted. The output is a fully-formed DOM.

## Problems

Several issues are apparent:

### Character-by-Character Copying

At the entry point, each state of the tokenizer processes one symbol at a time,
copying or converting it as needed—whether tag names, attributes, comments, or
symbols.

This process is highly inefficient in terms of both memory and time. We must
allocate an unknown amount of memory for each attribute, tag name, comment,
etc., leading to frequent reallocations and wasted time.

For example, if an HTML document contains 1000 tags, each with at least one
attribute, the parser will be extremely slow.


### Character Token

The second problem is related to the character token. We create a token for each
character and pass it to tree construction. Since the construction stage does
not know how many tokens will be generated, it cannot immediately allocate the
necessary memory. As a result, there are frequent reallocations and continuous
checks for text nodes in the current state of the tree.

### Monolithic System

The pervasive dependencies between nearly all components pose a significant
issue. The tokenizer depends on tree construction, and tree construction can
affect the tokenizer. These dependencies are largely due to namespaces.

## How to Solve Issues?

I will outline an HTML parser implementation for my Lexbor project, along with
solutions to the problems discussed.

### Preprocessing

First, we eliminate preprocessing. Instead, we update the tokenizer to treat
carriage return (`\r`) as a whitespace character. It will then be passed to the
tree construction stage, where it will be handled appropriately.

### Tokens

We simplify token management by using a single token for all purposes. This
unified token will exist throughout the entire parsing process.

Our unified token contains the following fields:

1. Tag ID
2. Begin
3. End
4. Attributes
5. Flags

### Tag ID

We will not use the text representation of tag names. Instead, we will convert
everything into numeric IDs, which are easier to compare and manage.

We create a static hash table for all known tags, assigning a specific ID to
each tag. In this hash table, the key will be the tag name, and the value will
be the corresponding ID from the enumeration.

Example:

```C
typedef enum {
    LXB_TAG__UNDEF       = 0x0000,
    LXB_TAG__END_OF_FILE = 0x0001,
    LXB_TAG__TEXT        = 0x0002,
    LXB_TAG__DOCUMENT    = 0x0003,
    LXB_TAG__EM_COMMENT  = 0x0004,
    LXB_TAG__EM_DOCTYPE  = 0x0005,
    LXB_TAG_A            = 0x0006,
    LXB_TAG_ABBR         = 0x0007,
    LXB_TAG_ACRONYM      = 0x0008,
    LXB_TAG_ADDRESS      = 0x0009,
    LXB_TAG_ALTGLYPH     = 0x000a,
    /* ... */
}
```

As shown in the example, we have created tags for the `END-OF-FILE` token, text,
and document to facilitate further processing. To streamline this, each node in
the DOM (Document Object Model) will include a `Tag ID`. This approach avoids
the need for two comparisons: one for the node type and one for the element.
Instead, a single check can be performed:

```C
if (node->tag_id == LXB_TAG_DIV) {
    /* Optimal code */
}
```

Alternatively, you could use:

```C
if (node->type == LXB_DOM_NODE_TYPE_ELEMENT && node->tag_id == LXB_TAG_DIV) {
    /* Oh my code */
}
```

The double underscores in `LXB_TAG__` are used to distinguish between common
tags and system tags. User-defined tags can include names like `text` or
`end-of-file`, which will not cause errors when searching for tag names. System
tags are prefixed with the `#` character.

However, the node can still store a textual representation of the tag name,
although this property will be `NULL` for 98.99999% of nodes. In some
namespaces, tags need to be prefixed or named with specific case sensitivity,
such as `baseProfile` in the SVG namespace.

The logic is straightforward:

1. Add the tag in lowercase to the general tag base and obtain the tag ID.
2. Store the tag ID and the original tag name in plain text in the node.


### Custom Tags (Custom Elements)

Developers can create custom tags in HTML. Since our static hash table only
contains known tags, we need a dynamic hash table to handle custom tags.

The process is straightforward: When a tag is encountered, we first check the
static hash table. If the tag is not found, we then search the dynamic table. If
the tag is not in the dynamic table either, we increment the ID counter and add
the tag to the dynamic table.

This process happens within the tokenizer, where all comparisons and later uses
involve the Tag ID (with rare exceptions).

### Begin and End

We have eliminated data processing within the tokenizer. We no longer copy or
convert data; instead, we obtain start and end pointers for data.

All data, including symbolic links, will be processed during the tree
construction stage, allowing us to determine the data size for subsequent memory
allocation.

### Attributes

The handling of attributes is similarly simplified. We do not copy attribute
data; instead, we maintain start and end pointers for attribute names and
values. All transformations are performed during tree construction.

### Flags

With the streamlining of token types, we need to record the token type for the
tree. This is achieved using the Flags bitmap field.

The field can contain the following values:

```C
enum {
    LXB_HTML_TOKEN_TYPE_OPEN         = 0x0000,
    LXB_HTML_TOKEN_TYPE_CLOSE        = 0x0001,
    LXB_HTML_TOKEN_TYPE_CLOSE_SELF   = 0x0002,
    LXB_HTML_TOKEN_TYPE_TEXT         = 0x0004,
    LXB_HTML_TOKEN_TYPE_DATA         = 0x0008,
    LXB_HTML_TOKEN_TYPE_RCDATA       = 0x0010,
    LXB_HTML_TOKEN_TYPE_CDATA        = 0x0020,
    LXB_HTML_TOKEN_TYPE_NULL         = 0x0040,
    LXB_HTML_TOKEN_TYPE_FORCE_QUIRKS = 0x0080,
    LXB_HTML_TOKEN_TYPE_DONE         = 0x0100
};
```

**Note:** This enum reflects an earlier version of the codebase. In the current implementation (see `source/lexbor/html/token.h`), the `TEXT`, `DATA`, `RCDATA`, `CDATA`, and `NULL` token types have been removed, and the remaining values have been renumbered.

Besides the opening/closing token type, there are additional values for the data
converter. Only the tokenizer knows how to correctly convert data, and it marks
the token to indicate how the data should be processed.

### Character Token

We can now conclude that the character token has effectively been removed. We
now have a new type of token: `LXB_HTML_TOKEN_TYPE_TEXT`. This new token
represents the entire text between tags, specifying how it should be processed
in the future.

As a result, the tree construction conditions need to be updated to handle text
tokens instead of character tokens. This includes converting text, removing
unnecessary characters, skipping spaces, and so on.

These changes in tree construction will be minimal. However, the tokenizer now
significantly deviates from the specification. This deviation is acceptable as
long as the HTML/DOM tree is fully compliant with the specification.

### Tokenizer Stages

To improve data processing speed in the tokenizer, we introduce our own iterator
at each stage. According to the specification, each stage processes one symbol
at a time and makes decisions based on that symbol. This approach can be very
inefficient.

For example, to transition from the `ATTRIBUTE_NAME` stage to the
`ATTRIBUTE_VALUE` stage, we need to identify a whitespace character in the
attribute name, which marks its end. The specification requires feeding
characters one by one to the `ATTRIBUTE_NAME` stage until a whitespace character
is encountered, causing the stage to switch. This process is costly, typically
implemented with a function call for each character or a callback like
`tkz->next_code_point()`.

Instead, we add a loop to the `ATTRIBUTE_NAME` stage to process the entire
incoming buffer at once. The loop looks for characters that indicate a stage
transition, allowing the stage to continue working efficiently. This change
provides significant performance improvements, even without compiler
optimizations.

However, this update breaks the original chunking support. Previously, with
character-by-character processing at each stage, chunking was supported. With
the new approach, chunking support is lost.

To address this, we introduce the concept of incoming buffers to restore
chunking support.


### Incoming Buffer

HTML is often parsed in chunks, such as when receiving data over the network. To
avoid waiting for the entire data to arrive, we process and parse the received
data as it comes in. Naturally, the data can be split across multiple buffers.
For example, we may have two buffers:

First buffer:
```html
<div clas
```

Second buffer:
```html
s="oh-no-oh-no">
```

Since we do not copy data during tokenization but instead use start/end pointers
to the data, we face the issue of dealing with pointers to different user
buffers. This problem arises because developers often use a single buffer to
store data, which means a pointer may refer to non-existent data.

To address this issue, we need to determine when the data from the user buffer
is no longer needed. The solution involves the following steps:

1. When parsing data in chunks, copy each incoming chunk into an incoming
   buffer.
2. After parsing the current chunk (which was copied), check if there were any
   unfinished tokens from the previous chunk. Specifically, check if the last
   token has pointers to the current user buffer. If no such pointers exist,
   release the incoming buffer. Otherwise, retain it until it is no longer
   needed. In most cases, the incoming buffer will be discarded when the next
   chunk arrives.

The "copy incoming buffer" flag can be adjusted as needed. For single-chunk
data, no copying is required.

This logic can be optimized further. Instead of copying the entire buffer in
advance, we could copy only the necessary data (the remaining tail) after
processing and update the token pointer to the new buffer. This approach would
be more efficient. However, such optimizations are not yet necessary, as the
current implementation is sufficiently fast and memory-efficient.


### A Problem: The Data in the Token

With chunk parsing addressed, we can relax a bit. However, another issue with
our pointer-based approach remains: when we need to inspect the token data, we
can't simply access it directly. If token data spans multiple chunks, we would
need to concatenate it, which is time-consuming. The specification specifies a
few cases where it's necessary to examine the accumulated data in a token.

This issue is resolved by adding new processing steps in the tokenizer. By
anticipating when checks will occur, we can handle data processing differently
in the tokenizer.

### Tree Construction Stage

Changes to the tree construction stage are minimal.

Since we no longer use character tokens but instead use text tokens, we need to
update the construction stage to support this new token type.

Here's how it looks.

According to the specification:
```
tree_build_in_body_character(token) {
    if (token.code_point == '\0') {
        /* Parse error, ignore token */
    }
    else if (token.code_point == whitespaces) {
        /* Insert element */'
    }
    /* ... */
}
```

In Lexbor HTML:
```C
tree_build_in_body_character(token) {
    lexbor_str_t str = {0};
    lxb_html_parser_char_t pc = {0};

    pc.drop_null = true;

    tree->status = lxb_html_token_parse_data(token, &pc, &str,
                                             tree->document->mem->text);

    if (token->type & LXB_HTML_TOKEN_TYPE_NULL) {
        /* Parse error */
    }

    /* Insert element if not empty */
}
```


As illustrated by the example, we have removed all character-based conditions
and created a common function for text processing. This function takes an
argument with data transformation settings:

```C
pc.replace_null /* Replace each '\0' with REPLACEMENT CHARACTER (U+FFFD) */
pc.drop_null    /* Delete all '\0's */
pc.is_attribute /* If data is an attribute value, we need smarter parsing */
pc.state        /* Processing stage. We can use symlink parsing or do without it. */
```

Each stage of tree construction has specific conditions for handling character
tokens. Depending on the situation, we may need to drop `\0` characters, replace
them with a REPLACEMENT CHARACTER, or convert symbolic links. These modes can
overlap in various ways.

While this approach may seem straightforward, it requires careful handling. For
instance, whitespace characters before the `<head>` tag should be discarded. If
a text token arrives with leading whitespace, such as " some text here ", we
should remove the spaces at the beginning of the text. After removing the
spaces, we check if there is any remaining data. If so, we continue processing
the remaining text as a new token.


## Summary

With all the updates completed, we now have a highly efficient HTML parser with
full support for DOM/HTML interfaces that builds an HTML/DOM tree in full
compliance with the HTML specification.

To summarize the changes made:

1. Removed pre-processing (moved to the tokenizer)
2. Tokenizer
   * Added support for incoming buffers
   * Streamlined tokens
   * Used Tag IDs instead of names
   * Replaced character tokens with N+ characters
   * Introduced an iterator in each state
   * Implemented token processing during tree construction
   * Consolidated to a single token type
3. Tree Construction
   * Updated character-based conditions

As a result, a single-core 2012 i7 processor achieves an average parsing rate of
`235MB per second` (for Amazon pages).

I have methods to potentially increase this rate by 1.5–2 times, but I need to
move forward. Next, I will focus on CSS parsing and developing a custom grammar
(Grammar-based parsing).

## Sources

The approach to parsing and HTML tree construction described here is implemented
in my [Lexbor](https://github.com/lexbor/lexbor) HTML library.

## P.S.

Our next article will cover CSS parsing and grammar, complete with real code
examples.

### For Those Interested

Feel free to contribute to the project. If you enjoy writing documentation or
supporting projects, your help is appreciated. If you wish to support the
project financially, please [email me](mailto:borisov@lexbor.com) for details.

### Thank you for your attention!
