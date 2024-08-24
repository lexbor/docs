# Part One - HTML

Hello, everyone!

In this article, I will tell you how to create a superfast HTML parser
supporting DOM. We will look at the HTML specification and its disadvantages in
terms of performance and resource consumption during HTML parsing.

I assume the reader has a basic knowledge of HTML: tags, nodes, elements, and
namespace.

## HTML Specification

Before we implement the parser, it is necessary to understand which HTML
specification we should rely upon.

There are two HTML specifications:

1. [WHATWG](https://html.spec.whatwg.org/multipage/)
   * Apple, Mozilla, Google, Microsoft
2. [W3C](https://www.w3.org/TR/html/)
   * A long list of companies

Naturally, our choice fell on the industry leaders, namely, WHATWG. It's a
living standard; these are large companies, each maintaining its own browser or
a browser engine.

UPDATE: Unfortunately, the links don't work if you are located in Russia.
Apparently, it's the "echo" of the Telegram throttling attempts by the Man.

## HTML Parsing Details

HTML tree construction can be divided into four parts:

1. Decoder
2. Preprocessing
3. Tokenizer
4. Tree construction

Let's consider each stage separately.

## Decoder

The tokenizer accepts Unicode characters (code points) as input. Accordingly, we
need to convert the byte stream to Unicode characters. For this, we use the
Encoding specification.

If our HTML encoding is unknown (there's no HTTP header), we need to identify it
to start decoding. To do so, we use the encoding sniffing algorithm.

Essentially, the algorithm is as follows: we wait for `500ms` or the first `1024
bytes` from the byte stream and run a prescan for the byte stream to determine
its encoding; this algorithm attempts to find the `<meta>` tag with
`http-equiv`, content, or charset attributes to understand which encoding the
HTML developer has assumed.

The Encoding specification identifies the minimum set of supported encodings for
a browser engine (21 in total): UTF-8, ISO-8859-2, ISO-8859-7, ISO-8859-8,
windows-874, windows-1250, windows-1251, windows-1252, windows-1254,
windows-1255, windows-1256, windows-1257, windows-1258, gb18030, Big5,
ISO-2022-JP, Shift_JIS, EUC-KR, UTF-16BE, UTF-16LE, and x-user-defined.

## Preprocessing

Once we have decoded the bytes into Unicode characters, we need to perform a
"sweep". Specifically, we have replace all carriage return characters (`\r`)
followed by a newline character (`\n`) with a single carriage return character
(`\r`). Next, we replace all carriage return characters with newline characters
(`\n`).

That's how the specification has it. Namely, `\r\n` => `\r`, `\r` => `\n`.

However, in fact, no one does exactly this. It's done in a simpler manner:

If you've got a carriage return character (`\r`), check whether there is a
newline character (`\n`) coming. If there is one, we replace both characters
with a newline character (`\n`); otherwise, we replace only the first character
(`\r`) with a newline (`\n`).

This completes the preprocessing. Yes, all you have to do is get rid of the
carriage return symbols so they don't get into the tokenizer. The tokenizer does
not expect them and does not know what to do with the carriage returns.

## Parsing Errors

To answer upcoming questions in advance, I should tell now what a parse error
is.

It's really not a big deal. It sounds menacing, but in fact it is only a
warning: we expect one thing and receive another.

A parse error does not stop data processing or prevent us from constructing a
tree. It is a message which says that our HTML is invalid.

The parse error can occur due to a surrogate pair, `\0`, wrong tag location,
wrong `<!DOCTYPE>`, etc.

By the way, some parse errors actually have consequences. For example, if you
get "bad" `<!DOCTYPE>`, the HTML tree will be labeled as `QUIRKS` which affects
the logic of some DOM functions.

## Tokenizer

As mentioned earlier, the tokenizer accepts Unicode characters as input. It is a
state machine which has `80 states`. Each state has conditions for Unicode
characters. Depending on the arriving symbol, the tokenizer may:

1. Change state
2. Generate token and change state
3. Do nothing and wait for the next character

The tokenizer generates six types of tokens: `DOCTYPE`, `Start Tag`, `End Tag`,
`Comment`, `Character`, `End-Of-File`. Which enter the tree construction stage.

Note that the tokenizer does not actually know all its states, only about 40% of
them (approximately). "Why all the others?", one might ask. The remaining 60%
are used to build the tree.

This is required to parse such tags as `<textarea>`, `<style>`, `<script>`,
`<title>`, and so on properly. Usually, these are tags which we do not expect to
contain other tags; they just close.

For example, the `<title>` tag cannot contain any other tags. Any tags in
`<title>` will be treated as text until a closing tag is encountered:
`</title>`.

Why is it done in such a manner? After all, we could just tell the tokenizer to
follow the "path we need" if it meets a `<title>` tag. And that would be true —
if not for namespaces! Yes, the namespace affects the behavior of the tree
construction stage, which in turn changes the behavior of the tokenizer.

For example, consider the behavior of the `<title>` tag in HTML and SVG
namespaces:

HTML
```HTML
<title><span>text</span></title>
```

The resulting tree:
```HTML
<title>
    "<span>text</span>"
```

SVG
```HTML
<svg><title><span>text</span></title></svg>
```

The resulting tree:
```HTML
<svg>
    <title>
        <span>
            "text"
```

In the first case (HTML namespace), the `<span>` tag is text, so no span element
was created. In the second case (SVG namespace), an element was created based on
the `<span>` tag. That is, tags behave differently depending on the namespace.

But that's not all. The cherry on top is the fact that the tokenizer itself must
know in which namespace the tree construction is happening right now. It is
necessary to process `CDATA` properly.

Consider two examples with `CDATA` and two namespaces:

HTML
```HTML
<div><![CDATA[ text ]]></div>
```

The resulting tree:
```HTML
<div>
    <!--[CDATA[ text ]]-->
```

SVG
```HTML
<div><svg><![CDATA[ text ]]></svg></div>
```

The resulting tree:
```HTML
<div>
    <svg>
        " text "
```

In the first case (HTML namespace), the tokenizer took `CDATA` for a comment. In
the second case, the tokenizer parsed the `CDATA` structure and extracted data
from it. The rule of thumb is as follows: If we meet `CDATA` outside HTML
namespaces, we parse it, otherwise we consider it a comment.

That's the connection between the tokenizer and the tree. The tokenizer needs to
know which namespace it is in during the tree construction stage, whereas the
stage itself can affect the state of the tokenizer.

### Tokens

Next we consider all six types of tokens that the tokenizer creates. Note that
all tokens contain prepared data; they are already processed and "ready for
use". This means that all named character references (like `&copy`) will be
converted to Unicode characters.

### DOCTYPE Token

The DOCTYPE token has a structure unlike other tags. The token contains:

1. Name
2. Public identifier
3. System identifier

In modern HTML, the only way valid `DOCTYPE` can look is similar to this:

```HTML
<!DOCTYPE html>
```

All other `<!DOCTYPE>`s will be considered parse errors.

### Start Tag Token

The opening tag may contain:

1. Tag name
2. Attributes
3. Flags

For example,
```HTML
<div key="value" />
```

The opening tag can contain a `self-closing` flag. This flag does not affect the
closing of the tag, but it can cause a parse error for non-void elements.

### End Tag Token

A closing tag. It shares all properties of the opening tag token, but has a
slash (`/`) before the tag name.

```
</div key="value" />
```

The closing tag can contain a `self-closing` flag which will cause a `parse
error`. Also, a parse error will be caused by any attributes in the closing tag.
They will be properly parsed, but discarded during the tree construction stage.

### Comment Token

The comment token contains the entire text of the comment. That is, it is
completely copied from the stream into the token.

Example:
```HTML
<!-- A comment -->
```

### Character Token

Perhaps the most interesting token type. It's a Unicode character token. It can
contain one (and only one) character.

For each character in HTML, a token will be created and sent to the tree
construction stage. It's really expensive. Let's look at how it works.

Consider this HTML:
```HTML
<span>Слава императору! &reg;</span>
```

How many tokens do you think will be created for this example? Answer: 22.

Consider the list of generated tokens:
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

Not really comforting, is it? Of course, many HTML parser authors in fact use
only one token during this processing step. They recycle it, erasing the data
each time.

Let's skip ahead a bit and answer a question: Why is it done in such a manner?
Why not accept this text in one piece? The answer is related to the tree
construction stage.

The tokenizer is useless without the HTML tree construction stage. It is where
the text is glued together according to various conditions.

The conditions roughly resemble the following:

1. If a `U+0000 (NULL)`  character token arrives, we trigger a parse error and
   ignore the token.
2. If one of `U+0009 (CHARACTER TABULATION)`, `U+000A (LINE FEED (LF)`, `U+000C
   (FORM FEED (FF)`, or `U+0020 (SPACE)` character tokens arrives, we invoke an
   algorithm to restore active formatting elements and insert the token into the
   tree.

The character token is added to the tree according to an algorithm:

1. If current insert position is not a text node, create a text node, insert it
   into the tree, and add the token data to it.
2. Otherwise, add the token data to the existing text node.

This behavior causes lots of problems. There's the need to create a token and
send it for analysis to the tree construction stage for each character. We don't
know the size of the text node, so we have to either pre-allocate a lot of
memory or perform reallocations. All this is extremely expensive memory and
time-wise.

### End-Of-File Token

A simple and clear token. There's no data left; we simply pass this news to the
tree construction stage.

## Tree construction

Tree construction involves a finite state machine with `23 states` and many
token-related conditions (tags, text). Tree construction is the largest stage;
it occupies a significant part of the specification itself (the side effects may
include lethargy and extreme frustration).

Everything is very simple. Tokens are accepted as input; depending on the token,
the state of tree construction is altered. As the output, we have a real DOM.

## Problems

The following issues seem obvious:

Character-by-character copying

At the entry point, each state of the tokenizer takes one symbol, which it
copies or converts if necessary: these are tag names, attributes, comments,
symbols.

It is very wasteful both in memory and in time. We have to allocate an unknown
amount of memory for each attribute, tag name, comment, and so on. This,
consequently, leads to reallocations and eventually to wasted time.

If we assume, for example, that our HTML contains 1000 tags, and each tag has at
least an attribute, then we get a hell of a slow parser.

### Character token

The second problem is the character token. Apparently, we create a token for
each character and pass it to tree construction. The construction stage does not
know how many tokens we will have and can not immediately allocate memory for
the desired number of characters. Accordingly, here we have all the same
reallocations and continual checks for text nodes in the current state of the
tree.

### Monolithic system

The ubiquitous dependencies between virtually everything are a real issue. The
tokenizer depends on the tree construction, and the tree construction can affect
the tokenizer. All of this happens because of namespaces.

## How to solve issues?

I am going to outline an HTML parser implementation in my Lexbor project, as
well as solutions to all problems voiced here.

### Preprocessing

For starters, let's get rid of the preprocessing. Instead, we upgrade the
tokenizer to understand carriage return (`\r`) as a whitespace character.
Therefore, it will be passed to the tree construction stage where we shall
actually deal with it.

### Tokens

With a slight movement of the hand we unify all tokens. Instead, we use a single
token for everything. Moreover, there will be only one token in existence during
the entire parsing process.

Our unified token contains the following fields:

1. Tag ID
2. Begin
3. End
4. Attributes
5. Flags

### Tag ID

We will not deal with the text representation of the tag name. Instead, we
translate everything into numbers. They are easier to compare and to work with.

We create a static hash table for all known tags. Let's create an enumeration of
all known tags. That is, we need to assign a specific ID for each tag.
Accordingly, in the hash table, the key will be the name of the tag and the
value will come from the enumeration.

An example:
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

As you can see from the example, we have created tags for the `END-OF-FILE`
token, the text, and the document. All this for sake of further convenience.
Opening the curtain somewhat, I should say that we will have a `Tag ID` in the
node (DOM Node Interface). This is done to avoid two comparisons: for the node
type and for the element. That is, if we need a DIV element, we perform a single
check in the node:

```C
if (node->tag_id == LXB_TAG_DIV) {
    /* Optimal code */
}
```

But you can certainly do this:
```C
if (node->type == LXB_DOM_NODE_TYPE_ELEMENT && node->tag_id == LXB_TAG_DIV) {
    /* Oh my code */
}
```

The two underscores in `LXB_TAG__` are required to separate the common tags from
the system tags. In other words, the user can create a tag called text or
`end-of-file`; if we later search for the name of a tag, no errors will occur.
All system tags start with the `#` character.

But still, the node can store a textual representation of the tag name. For
98.99999% of nodes, this property will be set to `NULL`. In some namespaces we
need to prefix or name the tag using specific case. For example, `baseProfile`
in SVG namespace.

The logic is simple. If we have a tag with a specific case:

1.	Add it to the general tag base in lower case. Get the tag ID. 2.	Add the
tag ID and the original tag name in plain text to the node.

### Custom tags (custom elements)

The developer can create any tags in HTML. Because our static hash table stores
only those tags that we know about, but the user can create any tags, we need a
dynamic hash table.

It looks very simple. When a tag arrives, we check if it exists in the static
hash table. If there is no such tag, we search the dynamic table; if it stores
no such tag as well, we increment the ID counter and add the tag in the dynamic
table.

All of the above occurs at the tokenizer. All comparisons in the tokenizer and
later use Tag ID (with rare exceptions).

### Begin and End

Now we've got rid of data processing in the tokenizer. We do not copy or convert
anything. We only get start/end data pointers.

All data, such as symbolic links, will be processed during the tree construction
stage. Thus, we will know the data size for subsequent memory allocation.

### Attributes

It's just as simple. We don't copy anything, we just maintain start/end pointers
of name and attribute values. All transformations occur at tree construction.

### Flags

We have streamlined the token types, so we need to make a note of the token type
for the tree. For this, we use the Flags bitmap field.

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

Beside the opening/closing token type, there are values for the data converter.
Only the tokenizer knows how to convert data correctly. The tokenizer marks the
token so that the data is processed accordingly.

### Character Token

We can now conclude that the character token has effectively disappeared. Yes,
now we have a new type of token: `LXB_HTML_TOKEN_TYPE_TEXT`. Again, we create a
token for the entire text between tags, noting how it should be processed in the
future.

As a result, we need to change the conditions in tree construction. We need to
update it to support text tokens instead of character tokens: convert them,
delete unnecessary characters, skip spaces, and so on.

There is nothing complicated. Changes in tree construction will be minimal.
However, the tokenizer now vastly deviates from the specification. But we don't
actually need this, that's OK. Our task is to get the HTML/DOM tree fully
compliant with the specification.

### Tokenizer stages

To speed up data processing in the tokenizer, we add our own iterator at each
stage. According to the specification, each stage accepts a single symbol and,
depending on the symbol, makes some decisions. But the truth is, it's very
expensive.

For example, to move from the `ATTRIBUTE_NAME` stage to the `ATTRIBUTE_VALUE`
stage, we need to find a whitespace character in the attribute name, which will
indicate its end. According to the specification, we have to feed characters one
by one to the `ATTRIBUTE_NAME` stage until we meet a whitespace character, so
the stage toggles to another stage. This is very expensive; usually it is
implemented with a function call for each character or a callback like
"`tkz->next_code_point()`".

Instead, we add a cycle to the `ATTRIBUTE_NAME` stage to pass the entire
incoming buffer. In the cycle, we look out for the characters that alter the
stage to continue working at the next stage. Here we get a lot of gain, even
without the compiler optimization.

But! The worst thing is, we break the out-of-the-box chunking support with this
update. When we had character-by-character processing at each stage of the
tokenizer, we supported chunks, but now we have broken the support.

How to fix it? How to implement chunking support?! It's simple: enter the
concept of incoming buffers.

### Incoming buffer

Often, HTML is parsed in chunks; for example, if we receive data over the
network. To avoid idling for the remaining data to arrive, we can send the
received data to processing/parsing. Naturally, the data can be "split"
anywhere. For example, we may have two buffers:

First buffer
```HTML
<div clas
```

Second buffer
```HTML
s="oh-no-oh-no">
```

Since we do not copy anything at tokenization but only get start/end pointers to
the data instead, now we have a problem. It's effectively pointers to different
user buffers. Given the fact that developers often use a single buffer to store
data, we are dealing with a pointer to the beginning of non-existent data.

To resolve the issues, we need to understand when the data from the user buffer
is no longer needed. The solution is basic:

1. If we parse data in chunks, copy every incoming chunk into an incoming
   buffer.
2. Having parsed the current chunk (previously copied), we check whether there
   was an unfinished token earlier. That is, whether there are pointers to
   current user buffer in the last token. If there are no pointers, we release
   the incoming buffer; if not, we leave it as is until it is needed. In 99% of
   cases, the incoming buffer will be destroyed when the next chunk arrives.

The "copy incoming buffer" flag can be controlled. For single-chunk data,
there's no copying.

Of course, this logic can be optimized and expanded. We can avoid copying the
entire buffer in advance, instead copying only the necessary data (the remaining
tail) after processing and retargeting the token pointer to our new buffer. It
would be better and faster. However, this optimization is premature at the
moment. Current implementation is fast and memory-efficient enough.

### A problem: the data in the token

With chunk parsing figured out, you can breathe easier. But there is another
problem with our pointer-based approach: At some point, we need to look at the
token data. And we can't do just that. If we need to look at the token data, we
will have to glue them together (if they belong to different chunks), and it is
wildly time-consuming. The specification indicates a couple moments where it's
necessary to see what we have accumulated in the token so far.

This problem is solved in a simple manner: We add new processing steps in the
tokenizer. That is, we know in advance when the checks occur, so we can go
different ways during data processing in the tokenizer.

### Tree construction stage

Here, changes are minimal.

We no longer have character tokens, but we use text tokens instead. As a result,
we need to update the construction stage to support the new token type.

Here's how it looks:

According to the specification,
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

As you can see from the example, we have removed all character-based conditions
and created a common function for text processing. An argument with data
transformation settings is passed to the function:

```C
pc.replace_null /* Replace each '\0' with REPLACEMENT CHARACTER (U+FFFD) */
pc.drop_null    /* Delete all '\0's */
pc.is_attribute /* If data is an attribute value, we need smarter parsing */
pc.state        /* Processing stage. We can use symlink parsing or do without it. */
```

Each stage of tree construction has its own conditions for character tokens.
Sometimes we need to drop `\0`s, and sometimes we replace them with a
REPLACEMENT CHARACTER. Sometimes it is necessary to convert the symbolic links,
sometimes not. All these modes can collide in any conceivable way.

Of course, it all sounds simple. In fact, you need to be very careful. For
example, all whitespace characters before the `<head>` tag should be discarded.
There's a problem if a text token arrives with whitespace before text: " some
text here ". We should drop the spaces at the beginning of the text and see if
there is anything left; if there's data to be processed, continue processing it
as a new token.

## Summary

After all updates, we have a complete superfast HTML parser with support for
DOM/HTML Interfaces that builds an HTML/DOM tree in full compliance with the
HTML specification.

To sum up everything we've changed:

1. Removed pre-processing (relocated to the tokenizer)
2. Tokenizer
   * Added incoming buffers
   * Streamlined the tokens
   * Used Tag IDs instead of names
   * Character token: Not one character, but N+ characters
   * An iterator in each state
   * Token processing during tree construction
   * A single token for everything
3. Tree construction
   * Modified character-based conditions

As a result, a single core of 2012 i7 yields an average parsing rate of `235MB
per second` (Amazon pages).

Of course I know how to increase this measure by 1.5–2 times, so there's still
an opportunity. But I need to move on. Actually, next comes CSS parsing and
creating your own grammar (Grammar, that is, generation of effective code for
Grammar-based parsing).

## Sources

The approach to parsing and HTML tree construction outlined here is implemented
in my own [Lexbor](https://github.com/lexbor/lexbor) HTML.

## P.S.

Our next article will discuss CSS parsing and Grammar. As usual, the article
will be accompanied by real code.

### For those who have time

Feel free to help the project. For example, if you like to write documentation
in your spare time. Do not hesitate to support the project with your hard-earned
money. [PM](mailto:borisov@lexbor.com) me for details.

### Thank you for your attention!
