# Part Two - CSS

Hello, everyone!

We continue the series of articles on developing a browser engine. Yes, better
late than never. Yes, there was a long break. At the end of the article, I will
describe how the lexbor project is doing and what is happening with it.

In this article, I will try to delve into the peculiarities of parsing Cascading
Style Sheets (CSS). I'll explain how to turn the "hedgehog" inside out and how
to test the obtained result.

Everything in CSS specifications is explained, well, almost everything. Here, I
will tell you how everything is organized, where to look, and where to start.
This article is more of an overview, and it won't delve into implementation
details. Instead, it provides general information and basic algorithms. For the
smallest implementation details, please refer to the GitHub code.

And, of course, as usual, we will aim for the title of the fastest CSS parser.

## Where to Look?

There are two sources for CSS specifications:
1. https://drafts.csswg.org/ – all drafts of the latest specifications.
2. https://www.w3.org/TR/ – the consortium that maintains "all" internet
   specifications.

We will be working with [drafts.csswg.org](https://drafts.csswg.org/). It's
concise, and each module has links to all versions of the module, from draft to
recommended for use.

## How It's Organized?

CSS is organized into modules: [Syntax](https://drafts.csswg.org/css-syntax-3/),
[Namespaces](https://drafts.csswg.org/css-namespaces-3/),
[Selectors](https://drafts.csswg.org/selectors-4/),
[CSSOM](https://drafts.csswg.org/cssom-1/),
[Values](https://drafts.csswg.org/css-values-4/), and so on. You can find a
complete list on [csswg.org](https://drafts.csswg.org/).

Each module, or rather its version, has a status: Working Draft, Candidate
Recommendation, Recommendation, and so on. You can see all stages on
[w3.org](https://www.w3.org/standards/types/). In simple terms, each module has
a note: recommended for use, just started writing and it's unclear what will
come of it, maybe we'll delete this module altogether, and so on, but more
concise.

We are interested only in Editor’s Draft and Working Draft with a glance at
Recommendation. Honestly, W3 is a bit slow, and by the time they reach
Recommendation (billions of stars will burn in space), everything will be
outdated. In other words, we will treat CSS standards as living (living), just
like the HTML standard.

## Let's Get Started with the Basics

Of all the CSS modules, some are fundamental—without them, nothing works. This
is the BASIS.

1. `Syntax`

The [syntax module](https://drafts.csswg.org/css-syntax-3/) is the foundation.
It describes the structure of CSS, the principles of token construction, and
their subsequent parsing.

2. `Values`

The [module describes](https://drafts.csswg.org/css-values/) the grammar. In all
modules, we will encounter grammars and basic CSS types.

For example, for the `width` property, the grammar looks like:
```
width = auto | <length-percentage [0,∞]> | min-content | max-content | fit-content(<length-percentage [0,∞]>)
```

In addition, the module describes basic types and [mathematical
functions](https://drafts.csswg.org/css-values-4/#calc-syntax): `<length>`,
`<angle>`, `<time>`, `min()`, `max()`, and so on.

Let's look at how the `<length-percentage>` type breaks down:
```
<length-percentage> = <length> | <percentage-token>
<length> = <dimension-token> | <number-token [0,0]>
```

All types ending in `-token` are tokens obtained from the tokenizer, meaning
they carry various data. In this article, we won't go into detail about each
type. You'll find everything in the specifications I mention. I'm describing the
overall picture.

All of this is the foundation to not be intimidated by the other modules and to
understand what's written in them. And to understand what unequal battle we will
face next.

## `Syntax`: Tokenizer

Just like everywhere else, the tokenizer takes a data stream and breaks it into
tokens.

Let's consider an example, taking CSS:
```CSS
div {width: 10px !important}
```

The tokenizer will create tokens:
```html
"div"       — <ident-token>
" "         — <whitespace-token>
"{"         — <left-curly-bracket-token>
"width"     — <ident-token>
":"         — <colon-token>
" "         — <whitespace-token>
"10px"      — <dimension-token>
" "         — <whitespace-token>
"!"         — <delim-token>
"important" — <ident-token>
"}"         — <right-curly-bracket-token>
```

You can find all types of tokens and the algorithm for creating them [in the
specification](https://drafts.csswg.org/css-syntax-3/#tokenization). There's
nothing unique here.

## `Syntax`: Parsing

Parsing accumulates tokens into specific structures for further processing in
various CSS modules.

A specific structure includes:

1. Stylesheet (recently called List of Rules)
2. At-Rule
3. Qualified Rule
4. Block’s contents
5. Declaration
6. Component value
7. Simple block
8. Function

For example, let's take a closer look at `Qualified Rule`. Again, take our
example:
```CSS
div {width: 10px !important}
```

`Qualified Rule` can have a `prelude` and `rules`.

Here:
- `div ` — is the prelude.
- `{width: 10px !important}` — is the rules list.

In this case:
- The `Prelude` contains a `Component value`.
- The `Rules` contain `Lists of Declarations`.

`width: 10px !important` — is a declaration. When there are many, it becomes a
list of declarations (`Lists of Declarations`).

Therefore, the declaration contains:
- `width` — the name (`name`)
- `10px` — the value (`value`)
- `!important` — the `important` flag.

Ordinary users would describe this as:
- `div ` — CSS Selectors
- `{width: 10px !important}` — a list of CSS properties.

It's not complicated. Other structures are organized in a similar way. For
example, `Stylesheet` contains `Rules`, namely `At-Rule` and `Qualified Rule` in
any quantity.

As we have already understood, the created structures with lists of tokens must
be processed by someone else. That someone else is other CSS modules.

For example, the [CSS Selectors
module](https://drafts.csswg.org/selectors-4/#grammar) receives data from
`Qualified Rule` `Prelude` for parsing. The [Media Queries
module](https://drafts.csswg.org/mediaqueries

-4/#mq-syntax) receives the entire structure of `At-Rule` for parsing. Each to
its own!

## Theory is Over, Let's Begin Life

Let's take a well-known `bootstrap.css` whose weight is approximately `≈180KB`.
The tokenizer will create around `≈51700` tokens from this file, excluding
comments. That's a considerable number.

Now, let's imagine that in the first pass, we go through them when forming the
structure in syntax, and in the second and subsequent passes, we break them down
by modules. Of course, subsequent passes will deal with a smaller number of
tokens; `{`, `}`, `[`, `]`, and some others will be discarded depending on the
situation.

Here is where we start thinking together—how do we optimize this?! There are
several options to implement an optimized CSS parser; let's consider the main
ones.

## SAX Style

We can set up callbacks for all stages of CSS Syntax structures and pass tokens
there. It would look something like this:

```CSS
div {width: 10px !important}
```

```html
"div"       — callback_qualified_rule_prelude(<ident-token>)
" "         — callback_qualified_rule_prelude(<whitespace-token>)
            — callback_qualified_rule_prelude(<end-token>)
"{"         — skip <left-curly-bracket-token>
"width"     — callback_declaration_name(<ident-token>)
":"         — skip <colon-token>
" "         — skip <whitespace-token>
"10px"      — callback_declaration_value(<dimension-token>)
" "         — skip <whitespace-token>
"!"         — skip <delim-token>
"important" — skip <ident-token>
            - callback_declaration_important(true)
"}"         — skip <right-curly-bracket-token>
```

As seen from this small example, there will be many callbacks. It will be
challenging to keep track of this entire zoo.

In this variant, much is shifted to the user. Also, a significant problem is the
inability to look at the next token. Someone might argue and say, "I can call
the tokenizer and ask for the next token without violating the general
algorithm." The answer is simple: you cannot do that. We won't know if the next
token relates to our current stage or not. Therefore, we would be taking on
double work, analyzing the CSS structure again.

Pros:
1. Fixed memory for the tokenizer and parser's work.
2. Speed. The parser will be solely responsible for tracking the structure and
   invoking callbacks.
3. Easy to implement chunk-wise parsing support.

Cons:
1. Complexity in user support. Much is shifted to the user.
2. Inability to get the next/previous token.

## Wild Implementation - The Fastest One

Let's have each module keep track of the CSS structure by itself! In general,
let's shift everything onto the user; let them figure it out, they know better.

If the user starts parsing CSS Selectors, they should not only deal with the
selector grammar but also track nesting through tokens: `{`, `}`, `(`, `)`,
`function(`.

It will look something like this:

```CSS
div {width: 10px !important}
```

```html
"div {"                    — Selectors parse
"width: 10px !important}"  — Declarations parse
```

Parsing selectors will proceed as follows:
- Parse according to the selector grammar.
- Check each token. Is the token `{` at the current nesting depth?
- If the token is `{`, switch to the next parsing stage.

Sounds simple, but in reality, it's more complicated.
- Knowledge about the stage to switch to must be passed to each module; they
  don't know anything about it.
- Should we consume the `{` or `}` token before passing it to the next stage?
- It's necessary to track nesting depth. We can't just pass control to the next
  module when encountering, for example, `}`. What if it was `(})`? It's always
  essential to precisely understand how the CSS structure is described at the
  current moment. This is very problematic and significantly complicates
  development and debugging if something goes wrong.
- Often, if there is a parsing error, it occurs not where the parser stopped or
  made a mistake. Most likely, the error happens much earlier; some module
  incorrectly counted the nesting or captured an extra token. In general,
  supporting this variant is very complex.

Pros:
1. Full control over the tokenizer. Tokens can be obtained and looked ahead.
2. Speed. No callbacks, parsing directly.

Cons:
1. Very complex development and support.

Initially, I "played" with this parsing approach.

The idea was:
1. Not to write everything manually but to create a C code generator based on
   grammars.
2. Teach the code generator to track the global CSS structure.

In other words, we give the code generator the grammar of the Selectors module,
and it generates C code for parsing, taking into account the global CSS
structure. It mixes the understanding of the structure into the Selectors
grammar.

I achieved decent results with this approach but decided to stop in this
direction. Creating such a code generator is a very large and challenging task,
but interesting. Just one optimization stage is worth it. I decided to return to
this when the `lexbor` project is extensively used and a significant speed boost
is needed.

## Hedgehog Inside Out

We've already established that it's crucial for us to have the ability to
control tokens, obtain them independently.

When we talk about parsing any data, we always imagine a clear sequence:
1. The tokenizer creates tokens.
2. The parser processes them.

Everything is logical.

What if we make the tokenizer keep track of the global CSS structure? In other
words, when requesting a token from the tokenizer, it internally monitors the
CSS structure. A sort of inside-out parsing.

This approach is implemented in my `lexbor` project.

The principle is as follows: We set up callbacks for different stages of parsing
the CSS structure. At each stage, the callback is called only once. If the
prelude begins, the beginning callback is called. Not for every token, only at
the start.

Okay, but how do we track the structure in our callbacks?

We create several functions, proxy functions for tokenizer functions. The token
acquisition function `lxb_css_syntax_parser_token()` and the token consumption
function `lxb_css_syntax_parser_consume()`. The user interacts not directly with
the tokenizer but with our proxy functions.

The algorithm of the `lxb_css_syntax_parser_token()` function is simple:
1. Get a token from the tokenizer.
2. Analyze the token in the CSS structure.
3. Return the token to the user as it is if it belongs to the current parsing
   stage; otherwise, return the termination token
   `LXB_CSS_SYNTAX_TOKEN__TERMINATED`.

When the termination token `LXB_CSS_SYNTAX_TOKEN__TERMINATED` is returned to the
user, the CSS structure analyzer enters the stage of waiting for a decision from
the user. There can be several decisions:
- `lxb_css_parser_success()` — everything went successfully, the expected data.
- `lxb_css_parser_failed()` — unexpected data for us.
- `lxb_css_parser_memory_fail()` — a memory allocation error occurred, ending
  parsing.
- `lxb_css_parser_stop()` — simply stop further parsing.

In other words, if the user is in any parsing stage, for example, in the
`Prelude` stage of the `Qualified Rule`, they cannot exit it, and the CSS
structure analyzer will not switch further until the user returns `success` or
`failed`. In addition, decision-making functions can be called immediately. If
you call `lxb_css_parser_success()` and there are tokens not related to
`LXB_CSS_SYNTAX_TOKEN_WHITESPACE` in the current stage, the current stage
automatically switches to `failed`. This is convenient because we don't need to
check all tokens until `LXB_CSS_SYNTAX_TOKEN__TERMINATED` arrives. If we are
sure that everything is parsed in the current stage, we return
`lxb_css_parser_success()`. If there are still some tokens, everything will
automatically resolve.

The final algorithm looks something like this:
1. The user wants to parse `Qualified Rule`. Sets callbacks for the beginning of
   `Prelude`, the beginning of the `Rules` block, and the end of parsing
   `Qualified Rule`.
2. Starts parsing.
3. Start of the loop. 3.1. We call the token acquisition function
   `lxb_css_syntax_parser_token()`. 3.1.1. Get a token from the tokenizer.
      3.1.2. Analyze it in the CSS structure. 3.1.3. The user callback is set by
      the parser based on the CSS structure. 3.2. We call the set callback with
      the obtained token. 3.3. In the callback, the user retrieves all tokens
   until `LXB_CSS_SYNTAX_TOKEN__TERMINATED` using the function
   `lxb_css_syntax_parser_token()`. 3.4. The user returns control to us, go to
   step 3.1.

This is a very simplified picture of the world. Inside the
`lxb_css_syntax_parser_token()` function, there are phases—switching between CSS
structures like `Qualified Rule`, `At-Rule`, and so on + various system phases.
There is also a stack; CSS structure is recursive, and we don't like recursion.

Pros:
1. Complete control over the tokenizer.
2. Speed, everything happens on the fly.
3. Safety for the user. The CSS structure is fully respected.
4. Ease of developing user parsers.

Cons:
1. I didn't find any cons; in my opinion, this is the most balanced CSS parsing
   approach.

## Parsing is Good, How About Testing?

To grasp the scale of the parsing challenges, let's delve into how grammar
syntax is structured. Values in grammars can have combinators and multipliers.

### Combinators

**Sequential Order**:
```HTML
<my> = a b c
```

`<my>` can contain the following value:
- `<my> = a b c`

**One Value from the List**:
```HTML
<my> = a | b | c
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = b`
- `<my> = c`

**One or All Values from the List in Any Order**:
```HTML
<my> = a || b || c
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a b`
- `<my> = a c`
- `<my> = a b c`
- `<my> = a c b`
- `<my> = b`
- `<my> = b a`
- `<my> = b c`
- `<my> = b a c`
- `<my> = b c a`
- `<my> = c`
- `<my> = c a`
- `<my> = c b`
- `<my> = c a b`
- `<my> = c b a`

**All Values from the List in Any Order**:
```
<my> = a && b && c
```

`<my>` can contain the following values:
- `<my> = a b c`
- `<my> = a c b`
- `<my> = b a c`
- `<my> = b c a`
- `<my> = c a b`
- `<my> = c b a`

**Values can be Grouped**:
```
<my> = [ [a | b | c] && x ] r t v
```

### Multipliers

Those familiar with regex will understand immediately.

**Zero or Infinite Number of Times**:
```HTML
<my> = a*
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a a a a a a a a a a a a`
- `<my> = `

**One or Infinite Number of Times**:
```HTML
<my> = a+
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a a a a a a a a a a a a`

**May or May Not be Present**:
```HTML
<my> = a?
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = `

**May be Present from `A` to `B` Times, Period**:
```HTML
<my> = a{1,4}
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a`
- `<my> = a a a`
- `<my> = a a a a`

**One or Infinite Number of Times Separated by Comma**:
```HTML
<my> = a#
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a, a`
- `<my> = a, a, a`
- `<my> = a, a, a, a`

**Exactly One Value Must be Present**:
```HTML
<my> = [a? | b? | c?]!
```

In this example, absence of a value within the group is allowed, but the
exclamation mark `!` demands at least one, otherwise it's an error.

**Multipliers can be Combined**:
```HTML
<my> = a#{1,5}
```

Values of `a`, separated by commas, from one to five times.

That's all you need to know about grammar; the most crucial parts.

Now, let's look at the grammar syntax for color:

```
<color> = <absolute-color-base> | currentcolor | <system-color>

<absolute-color-base> = <hex-color> | <absolute-color-function> | <named-color> | transparent
<absolute-color-function> = <rgb()> | <rgba()> |
                            <hsl()> | <hsla()> | <hwb()> |
                            <lab()> | <lch()> | <oklab()> | <oklch()> |
                            <color()>
<rgb()> =  [ <legacy-rgb-syntax> | <modern-rgb-syntax> ]
<rgba()> = [ <legacy-rgba-syntax> | <modern-rgba-syntax> ]

<legacy-rgb-syntax> = rgb( <percentage>#{3} , <alpha-value>? ) |
                      rgb( <number>#{3} , <alpha-value>? )
<legacy-rgba-syntax> = rgba( <percentage>#{3} , <alpha-value>? ) |
                       rgba( <number>#{3} , <alpha-value>? )

<modern-rgb-syntax> = rgb(  [ <number> | <percentage> | none]{3}
                      [ / [<alpha-value> | none] ]?)
<modern-rgba-syntax> = rgba([ <number> | <percentage> | none]{3}
                      [ / [<alpha-value> | none] ]?)
...
```

It's hard to figure it out while nursing a hangover. However, writing a parser
for this is not difficult, even straightforward. But writing all test variations
for this is quite challenging. And if you consider the myriad CSS declarations,
your hands drop even more.

The logical thought here is to write a test generator for grammars! It turned
out to be easier said than done. Not rocket science, but it makes one ponder in
the cold.

The main problems I encountered:

1. Combinatorial bombs.

For example, take such a grammar:
```HTML
<text-decoration-line> = none | [ underline || overline || line-through || blink ]
<text-decoration-style> = solid | double | dotted | dashed | wavy
<text-decoration-color> = <color>
<text-decoration> = <text-decoration-line> || <text-decoration-style> || <text-decoration-color>
```

Generating tests for `<text-decoration>` would go on indefinitely. All `<color>`
values must be combined with `<text-decoration-line>` and
`<text-decoration-style>` in different variations, which is a lot.

Had to come up with a limiter for group options — `/1`. A slash and a value
indicating how many options should be taken from the group. As a result,
`<text-decoration>` was transformed into:

```HTML
<text-decoration> = <text-decoration-line> || <text-decoration-style> || <text-decoration-color>/1
```

2. Grammars ignore spaces (`LXB_CSS_SYNTAX_TOKEN_WHITESPACE`).

Usually, it is mentioned below the grammars that certain values should not have
spaces between them. This doesn't suit us; we need to consider this directly in
the grammar. The `^WS` modifier (Without Spaces) was introduced:

```HTML
<frequency> = <number-token> <frequency-units>^WS
<

frequency-units> = Hz | kHz
```

Spaces before `<frequency-units>` are not allowed.

3. Parsing order.

The order of input data can be arbitrary, but after parsing, values find their
positions in structures, and during serialization, they have a precise order.

For example:

```
<x> = a && b && c
```

Tests would be generated as follows:
```HTML
<x> = a b c
<x> = a c b
<x> = b a c
<x> = b c a
<x> = c a b
<x> = c b a
```

All these tests are valid, but our result after parsing will always be `<x> = a
b c`. The question arises — how to compare with the others? My inner sense
hinted that the task suddenly became much more complicated, but the sense of
courage (not foolishness) pushed to tackle it head-on. And, as you understand,
it didn't work out right away. I had to think!

Let's look at such an example:
```
<x> = a && [x || y || [f && g && h]] && c
```

It became clear that the result of generating tests for each group should return
not just a test but also the correct answer for that test. This became a bit of
a problem. The implementation got complicated.

Various solutions were tried, I would even say crutches, to avoid complicating
the code. But they all brought a bunch of exceptions and were 10% non-working
code. It seemed like assigning a unique index in ascending order, depending on
where the value is, and in the end, when the test is formed, sorting the indices
to get the result for the parser. Here you have a test and what result the
parser will return.

Still no. Each value has its own Combinators and Multipliers that can place
different values between them. For example, somewhere there might be a space,
somewhere not, somewhere commas between values. If we simply sort the final
result, we get a mess.

In the end, the most reliable solution is to generate the test and result
separately. In other words, forming the result will go through the same stages
as forming the test. Costly, of course, but okay, we're not real-time; we can
wait.

As a result, we got a wonderful tool that generates tests for grammars. Now
tests for CSS Declarations (properties) are generated in `1` second, and their
number is `82911`. On disk, they occupy about `20MB` in JSON format. Admit it,
manually writing so many tests is a time-consuming task.

This approach helped uncover quite a few parsing issues with properties; I think
I caught around 10 errors. But now there is 100% confidence that valid CSS will
be parsed correctly.

And here comes an urgent question — how to test invalid CSS? At this stage, I
actively use the `Clang` fuzzer. But, of course, it is necessary to implement
incorrect/broken tests using grammar. So that from incorrect tests, a false
correct result does not come out.

### Generally Speaking about Testing

Code testing takes as much time as its development, if not more. Currently, the
`lexbor` project undergoes continuous testing on approximately 30 operating
systems with enabled `asan`, `msan`, `UB`, and `memory leak` (where possible).
Additionally, `Clang` fuzzers are constantly at work.

## What is the Status of the lexbor Project?

Despite a long hiatus, which was indeed prolonged, the project is actively
evolving. Much has already been implemented, and currently, the implementation
of the layout/renderer tree is in progress. In other words, the project will
soon create windows, render glyphs, draw blocks, inlines, and so forth. The code
is abundant; it could fill five articles, provided one refrains from verbosity,
and possibly even more.

The break in development was tied to my work at NGINX, where I immersed myself
in developing the NJS JavaScript engine. This, in turn, benefitted the lexbor
project in terms of knowledge.

Fortunately, a very capable individual (proficient in English and technical
documentation) joined me, assisting with the project's documentation. He has
taken charge of all English language aspects and anything related to project
documentation in general.

## Where Are the Benchmarks?

They won't be available, at least not right now.

At present, the lexbor project only supports Selectors and Declarations for full
parsing. This suffices for the engine's further development. As soon as
`@media`, variables, and other features appear, we'll immediately measure
ourselves against others.

Anything unsupported by the CSS parser is categorized as `CUSTOM`. In other
words, in the final tree, all data will be present, just with a `*_custom`
structure.

I'll hint only that lightningcss, written in Rust and positioned as "An
extremely fast CSS parser," did not surprise me.

## Links

Project link: [lexbor](https://github.com/lexbor/lexbor). Modest CSS examples:
[CSS
Examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/css).
Examples of usage with HTML: [HTML +
CSS](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/styles).
