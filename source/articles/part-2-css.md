# Part Two: CSS

Hello, everyone!

We continue our series on developing a browser engine. Better late than never!
Despite the long break, I’ll update you on the lexbor project and its current
status at the end of this article.

In this article, we'll explore the specifics of parsing Cascading Style Sheets
(CSS). I'll explain how to approach the task and how to test the results.

The CSS specifications are mostly comprehensive, but here, I'll outline how
everything is organized, where to look, and where to start. This article
provides an overview and basic algorithms without delving into implementation
details. For detailed implementation, refer to the GitHub code.

Our goal remains to create the fastest CSS parser.

## Where to Look?

There are two primary sources for CSS specifications:
1. https://drafts.csswg.org/ – All drafts of the latest specifications.
2. https://www.w3.org/TR/ – The consortium that maintains comprehensive internet
   specifications.

We'll use [drafts.csswg.org](https://drafts.csswg.org/) because it's concise and
provides links to all versions of each module, from drafts to recommendations.

## How It's Organized

CSS is organized into modules: [Syntax](https://drafts.csswg.org/css-syntax-3/),
[Namespaces](https://drafts.csswg.org/css-namespaces-3/),
[Selectors](https://drafts.csswg.org/selectors-4/),
[CSSOM](https://drafts.csswg.org/cssom-1/),
[Values](https://drafts.csswg.org/css-values-4/), and more. You can find a
complete list on [csswg.org](https://drafts.csswg.org/).

Each module has a status: Working Draft, Candidate Recommendation,
Recommendation, etc. You can see all stages on
[w3.org](https://www.w3.org/standards/types/). In simple terms, each module is
marked with its current development stage, ranging from early drafts to final
recommendations.

We will focus on Editor’s Draft and Working Draft with a glance at
Recommendation. Since W3C standards evolve slowly, by the time a module reaches
Recommendation, it might already be outdated. Thus, we'll treat CSS standards as
living documents, like the HTML standard.

## Let's Get Started with the Basics

Some CSS modules are fundamental—without them, nothing works. These are the
BASICS.

1. `Syntax`

The [Syntax module](https://drafts.csswg.org/css-syntax-3/) is the foundation.
It describes CSS structure, token construction principles, and parsing.

2. `Values`

The [Values module](https://drafts.csswg.org/css-values-4/) describes the
grammar. All modules include grammars and basic CSS types.

For example, the grammar for the `width` property looks like:
```
width = auto | <length-percentage [0,∞]> | min-content | max-content | fit-content(<length-percentage [0,∞]>)
```

The module also covers basic types and [mathematical
functions](https://drafts.csswg.org/css-values-4/#calc-syntax) like `<length>`,
`<angle>`, `<time>`, `min()`, `max()`, etc.

For instance, the `<length-percentage>` type is defined as:
```
<length-percentage> = <length> | <percentage-token>
<length> = <dimension-token> | <number-token [0,0]>
```

Types ending in `-token` are tokens from the tokenizer, carrying various data.
This article outlines the general picture. For implementation details, refer to
the specifications mentioned.

## `Syntax`: Tokenizer

The tokenizer processes a data stream into tokens.

For example, with CSS:
```css
div {width: 10px !important}
```

The tokenizer generates tokens:
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

You can find all token types and the tokenization algorithm [in the
specification](https://drafts.csswg.org/css-syntax-3/#tokenization).

## `Syntax`: Parsing

Parsing organizes tokens into structures for further processing by various CSS
modules.

A specific structure includes:
1. Stylesheet (formerly List of Rules)
2. At-Rule
3. Qualified Rule
4. Block’s contents
5. Declaration
6. Component value
7. Simple block
8. Function

For example, consider `Qualified Rule`:
```css
div {width: 10px !important}
```

`Qualified Rule` can have a `prelude` and `rules`:
- `div` — The prelude.
- `{width: 10px !important}` — The rules list.

Here:
- The `Prelude` contains a `Component value`.
- The `Rules` contain `Lists of Declarations`.

`width: 10px !important` — is a declaration. Multiple declarations form a list
of declarations.

Therefore, the declaration contains:
- `width` — The name.
- `10px` — The value.
- `!important` — The important flag.

In simpler terms:
- `div` — CSS Selectors.
- `{width: 10px !important}` — A list of CSS properties.

Other structures are similarly organized. For example, `Stylesheet` contains
`Rules`, including `At-Rule` and `Qualified Rule`.

These structures must be processed by other CSS modules. For instance, the [CSS
Selectors module](https://drafts.csswg.org/selectors-4/#grammar) parses data
from `Qualified Rule`'s `Prelude`, while the [Media Queries
module](https://drafts.csswg.org/mediaqueries-4/#mq-syntax) processes the entire
`At-Rule` structure. Each module handles its specific part of the data.

## Theory is Over, Let's Begin Life

Let's take a well-known `bootstrap.css` file, which is approximately `≈180KB` in
size. The tokenizer will produce around `≈51700` tokens from this file,
excluding comments. That's a significant number.

Now, let's imagine that during the first pass, we process these tokens to form
the syntax structure. In the second and subsequent passes, we break them down by
modules. Subsequent passes will handle fewer tokens, as `{`, `}`, `[`, `]`, and
other elements will be discarded as appropriate.

Here is where we start thinking together—how can we optimize this? There are
several options for implementing an optimized CSS parser; let's consider the
main ones.

## SAX Style

We can set up callbacks for all stages of CSS syntax structures and pass tokens
to these callbacks. It would look something like this:

```css
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

As seen from this small example, there will be many callbacks, making it
challenging to manage them all.

In this approach, much responsibility falls on the user. Additionally, a major
issue is the inability to look ahead at the next token. One might argue that the
tokenizer could be called to get the next token without disrupting the overall
algorithm. However, this isn't feasible, as we wouldn't know whether the next
token is relevant to the current stage. This would result in redundant work, as
we'd need to reanalyze the CSS structure.

**Pros:**
1. Fixed memory usage for the tokenizer and parser.
2. Speed. The parser handles structure tracking and callback invocation.
3. Simplified support for chunk-wise parsing.

**Cons:**
1. Increased complexity for users. Much responsibility is transferred to them.
2. Inability to access the next/previous token.

## Wild Implementation - The Fastest One

Let's have each module manage the CSS structure independently. Essentially, we
shift all responsibilities to the user, assuming they know best.

If the user starts parsing CSS selectors, they must handle not only the selector
grammar but also track nesting through tokens such as `{`, `}`, `(`, `)`, and
`function(`.

It might look something like this:

```css
div {width: 10px !important}
```

```html
"div {"                    — Selectors parse
"width: 10px !important}"  — Declarations parse
```

Parsing selectors will proceed as follows:
- Parse according to the selector grammar.
- Check each token to determine if it is `{` at the current nesting depth.
- If the token is `{`, switch to the next parsing stage.

This sounds simple, but in practice, it's more complex:
- The knowledge about which stage to switch to must be passed to each module;
  they don’t inherently know this.
- We need to decide whether to consume the `{` or `}` token before passing it to
  the next stage.
- Nesting depth must be tracked. We can't just pass control to the next module
  when encountering `}` without understanding the context, such as whether it
  was part of a construct like `(})`. It's crucial to precisely understand the
  CSS structure at all times. This complicates development and debugging
  significantly if issues arise.
- Parsing errors often occur not where the parser fails but much earlier,
  possibly due to incorrect nesting or extra tokens captured by some module.
  Supporting this approach is very complex.

**Pros:**
1. Complete control over the tokenizer. Tokens can be obtained and looked ahead.
2. Speed. Direct parsing with no callbacks.

**Cons:**
1. Highly complex development and support.

Initially, I experimented with this parsing approach.

The idea was:
1. To avoid writing everything manually by creating a C code generator based on
   grammars.
2. To teach the code generator to track the global CSS structure.

In other words, we provide the code generator with the grammar of the Selectors
module, and it generates C code for parsing, incorporating the global CSS
structure into the Selectors grammar.

I achieved good results with this approach but decided to stop for now.
Developing such a code generator is a major and challenging task, albeit
interesting. The optimization stage alone is substantial. I plan to revisit this
once the `lexbor` project is more widely used and a significant speed
improvement is required.


## Hedgehog Inside Out

We've established the importance of controlling tokens and obtaining them
independently.

When parsing any data, we generally follow a clear sequence:
1. The tokenizer creates tokens.
2. The parser processes them.

This approach is straightforward.

But what if the tokenizer also tracked the global CSS structure? In other words,
while requesting a token from the tokenizer, it would internally monitor the CSS
structure. This is a form of inside-out parsing.

This approach is implemented in my `lexbor` project.

Here’s how it works: We set up callbacks for different stages of parsing the CSS
structure. Each callback is called only once at the beginning of a stage, not
for every token.

But how do we track the structure within these callbacks?

We create several proxy functions for the tokenizer functions:
`lxb_css_syntax_parser_token()` for token acquisition and
`lxb_css_syntax_parser_consume()` for token consumption. The user interacts with
these proxy functions rather than directly with the tokenizer.

The `lxb_css_syntax_parser_token()` function works as follows:
1. Get a token from the tokenizer.
2. Analyze the token in the CSS structure.
3. Return the token to the user if it belongs to the current parsing stage;
   otherwise, return the termination token `LXB_CSS_SYNTAX_TOKEN__TERMINATED`.

When the termination token `LXB_CSS_SYNTAX_TOKEN__TERMINATED` is returned, the
CSS structure analyzer waits for a decision from the user. Possible decisions
include:
- `lxb_css_parser_success()` — Parsing was successful, and the expected data was
  obtained.
- `lxb_css_parser_failed()` — Unexpected data encountered.
- `lxb_css_parser_memory_fail()` — Memory allocation error occurred, ending
  parsing.
- `lxb_css_parser_stop()` — Stop further parsing.

In other words, if the user is in any parsing stage, such as the `Prelude` stage
of the `Qualified Rule`, they cannot exit this stage until they return `success`
or `failed`. Additionally, decision-making functions can be called immediately.
If `lxb_css_parser_success()` is called and there are remaining tokens not
related to `LXB_CSS_SYNTAX_TOKEN_WHITESPACE` in the current stage, the stage
automatically switches to `failed`. This is convenient because we do not need to
check all tokens until `LXB_CSS_SYNTAX_TOKEN__TERMINATED` arrives. If we are
sure that everything is parsed in the current stage, we return
`lxb_css_parser_success()`. If there are still tokens, everything will
automatically resolve.

The final algorithm is as follows:
1. The user wants to parse a `Qualified Rule`. They set callbacks for the
   beginning of the `Prelude`, the start of the `Rules` block, and the end of
   parsing the `Qualified Rule`.
2. Begin parsing.
3. In the loop: 3.1. Call the token acquisition function
   `lxb_css_syntax_parser_token()`. 3.1.1. Get a token from the tokenizer.
      3.1.2. Analyze it in the CSS structure. 3.1.3. The parser sets the user
      callback based on the CSS structure. 3.2. Call the set callback with the
      obtained token. 3.3. In the callback, the user retrieves all tokens until
   `LXB_CSS_SYNTAX_TOKEN__TERMINATED` using `lxb_css_syntax_parser_token()`.
   3.4. The user returns control, and the process repeats from step 3.1.

This is a simplified overview. Inside the `lxb_css_syntax_parser_token()`
function, there are various phases, including switching between CSS structures
like `Qualified Rule`, `At-Rule`, etc., as well as different system phases.
There is also a stack due to the recursive nature of CSS structures, which
avoids recursion directly.

**Pros:**
1. Complete control over the tokenizer.
2. Speed, as everything happens on the fly.
3. Safety for the user, with full respect for the CSS structure.
4. Ease of developing user parsers.

**Cons:**
1. I did not find any cons; in my opinion, this is the most balanced CSS parsing
   approach.

## Parsing is Good, How About Testing?

To understand the scale of parsing challenges, let's explore how grammar syntax
is structured. Values in grammars can include combinators and multipliers.

### Combinators

**Sequential Order**

```html
<my> = a b c
```

`<my>` can contain the following value:
- `<my> = a b c`

**One Value from the List**:
```html
<my> = a | b | c
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = b`
- `<my> = c`

**One or All Values from the List in Any Order**:
```html
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

For those familiar with regular expressions, this concept will be immediately
clear.

**Zero or Infinite Number of Times**:
```html
<my> = a*
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a a a a a a a a a a a a`
- `<my> = `

**One or Infinite Number of Times**:
```html
<my> = a+
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a a a a a a a a a a a a`

**May or May Not be Present**:
```html
<my> = a?
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = `

**May be Present from `A` to `B` Times, Period**:
```html
<my> = a{1,4}
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a a`
- `<my> = a a a`
- `<my> = a a a a`

**One or Infinite Number of Times Separated by Comma**:
```html
<my> = a#
```

`<my>` can contain the following values:
- `<my> = a`
- `<my> = a, a`
- `<my> = a, a, a`
- `<my> = a, a, a, a`

**Exactly One Value Must be Present**:
```html
<my> = [a? | b? | c?]!
```

In this example, the absence of a value within the group is allowed, but the
exclamation mark `!` requires at least one value; otherwise, it results in an
error.

**Multipliers can be Combined**:

```html
<my> = a#{1,5}
```


This specifies that `a` can appear between one and five times, separated by
commas.

That covers the essential parts of grammar.

Now, let's examine the grammar syntax for color:

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

It's hard to work through this while nursing a hangover. However, writing a
parser for this is not difficult—it's even straightforward. But creating all the
test variations is quite challenging. Considering the multitude of CSS
declarations only adds to the complexity.

A logical solution is to write a test generator for grammars! This is easier
said than done. While it's not rocket science, it does require some thoughtful
consideration.

The main problems I encountered:

1. Combinatorial bombs.

For example, consider this grammar:

```html
<text-decoration-line> = none | [ underline || overline || line-through || blink ]
<text-decoration-style> = solid | double | dotted | dashed | wavy
<text-decoration-color> = <color>
<text-decoration> = <text-decoration-line> || <text-decoration-style> || <text-decoration-color>
```

Generating tests for `<text-decoration>` could go on indefinitely. All `<color>`
values need to be combined with `<text-decoration-line>` and
`<text-decoration-style>` in various ways, which is a considerable amount of
work.

To manage this, I implemented a limiter for group options using `/1`. This
notation indicates how many options should be selected from the group. As a
result, `<text-decoration>` was transformed into:

```html
<text-decoration> = <text-decoration-line> || <text-decoration-style> || <text-decoration-color>/1
```

2. Grammars Ignore Spaces (`LXB_CSS_SYNTAX_TOKEN_WHITESPACE`).

Typically, it's noted below the grammars that certain values should not have
spaces between them. This approach is insufficient; we need to address this
directly in the grammar. To handle this, the `^WS` modifier (Without Spaces) was
introduced:

```html
<frequency> = <number-token> <frequency-units>^WS
<

frequency-units> = Hz | kHz
```

Spaces before `<frequency-units>` are not allowed.

3. Parsing Order

The order of input data can be arbitrary, but after parsing, values are placed
in their respective structures. During serialization, these values must follow a
specific order.

For example:

```
<x> = a && b && c
```

Tests would be generated as follows:

```html
<x> = a b c
<x> = a c b
<x> = b a c
<x> = b c a
<x> = c a b
<x> = c b a
```

All these tests are valid, but the result after parsing will always be `<x> = a
b c`. The question arises—how do we compare this with others? My intuition
suggested that the task had become significantly more complicated, but a sense
of determination (not foolishness) drove me to address it directly. As expected,
it didn’t work out right away; it required some thought!

Consider this example:
```
<x> = a && [x || y || [f && g && h]] && c
```

It became evident that generating tests for each group should not only provide a
test but also the correct answer for that test. This added complexity to the
implementation.

Various solutions were attempted—sometimes involving workarounds—to avoid
complicating the code. However, these often led to exceptions and partially
non-functional code. The idea was to assign a unique index in ascending order
based on the value's position, and then sort the indices at the end to determine
the result for the parser. This would give both the test and the expected
result.

However, this approach fell short. Each value has its own combinators and
multipliers that can place different values between them. For instance, there
might be spaces or commas between values. Simply sorting the final result led to
inconsistencies.

The most reliable solution turned out to be generating the test and the result
separately. This means that forming the result goes through the same stages as
forming the test. Although this approach is costly, it’s manageable since
real-time performance is not a constraint.

As a result, we now have an excellent tool for generating tests for grammars.
Tests for CSS declarations (properties) are generated in `1` second, totaling
`82,911` tests. On disk, they occupy about `20MB` in JSON format. Manually
writing such a large number of tests would be extremely time-consuming.

This approach has helped identify several parsing issues with properties—about
10 errors so far. I now have complete confidence that valid CSS will be parsed
correctly.

The pressing question now is how to test invalid CSS. Currently, I use the
`Clang` fuzzer actively. However, it is also necessary to implement
incorrect/broken tests using grammar to ensure that invalid tests do not
incorrectly pass as valid.


### Generally Speaking about Testing

Code testing often takes as much time as development, if not more. The `lexbor`
project undergoes continuous testing on approximately 30 operating systems with
`asan`, `msan`, `UB`, and `memory leak` detection enabled (where possible).
Additionally, `Clang` fuzzers are constantly in use.

## What is the Status of the lexbor Project?

Despite a long hiatus, which was indeed prolonged, the project is actively
evolving. Significant progress has been made, and currently, the implementation
of the layout/renderer tree is underway. This means the project will soon handle
window creation, glyph rendering, block and inline drawing, and more. The code
is extensive; it could fill five articles, provided one avoids verbosity, and
possibly even more.

The development break was due to my work at NGINX, where I focused on developing
the NJS JavaScript engine. This experience has benefited the `lexbor` project in
terms of knowledge.

Fortunately, a highly skilled individual (proficient in English and technical
documentation) has joined me, assisting with the project's documentation. This
person now manages all aspects of English language documentation and general
project documentation.

## Where Are the Benchmarks?

Benchmarks are not available at this time.

Currently, the `lexbor` project supports full parsing of Selectors and
Declarations. This is sufficient for the engine's further development. Once
features like `@media`, variables, and others are implemented, we will promptly
compare our performance with others.

Any unsupported features by the CSS parser are categorized as `CUSTOM`. In other
words, all data will be present in the final tree, albeit with a `*_custom`
structure.

I'll only hint that lightningcss, written in Rust and billed as "An extremely
fast CSS parser," did not particularly impress me.

## Links

Project link: [lexbor](https://github.com/lexbor/lexbor). Modest CSS examples:
[CSS
Examples](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/css).
Examples of usage with HTML: [HTML +
CSS](https://github.com/lexbor/lexbor/tree/master/examples/lexbor/styles).
