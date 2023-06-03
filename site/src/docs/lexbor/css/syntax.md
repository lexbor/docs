[name]: Syntax
[title]: <> (CSS Syntax)
[theme]: document.html
[main_class]: dom-module
[refs_deep_max]: 2

# CSS Syntax

This is documentation for `CSS Syntax` module for [Lexbor library](/). Module created by [csswg specification](https://drafts.csswg.org/css-syntax-3/).

This module parses the СSS data, splits СSS data into tokens and builds the AST tree.


## Parsing

Two ways to parsing CSS:

#### Single buffer

This method is suitable if you have CSS data in one buffer then select the data parsing approach.
Function `lxb_css_syntax_tokenizer_parse` implements parsing **without copying** the input buffer.

```C
lxb_css_syntax_tokenizer_t *tkz;

tkz = lxb_css_syntax_tokenizer_create();
lxb_css_syntax_tokenizer_init(tkz);

lxb_css_syntax_tokenizer_parse(tkz, css_data, css_size);

lxb_css_syntax_tokenizer_destroy(tkz);
```

#### Chunks

This method is suitable if you have СSS data splits into many buffers.
Incoming buffers will be copied and released as they are used.

```C
lxb_css_syntax_tokenizer_t *tkz;

tkz = lxb_css_syntax_tokenizer_create();
lxb_css_syntax_tokenizer_init(tkz);

lxb_css_syntax_tokenizer_begin(tkz);

lxb_css_syntax_tokenizer_chunk(tkz, css_buf_one, css_buf_one_size);
lxb_css_syntax_tokenizer_chunk(tkz, css_buf_two, css_buf_two_size);

lxb_css_syntax_tokenizer_end(tkz);

lxb_css_syntax_tokenizer_destroy(tkz);
```


## Token callback

By default, the tokenizer does not use the received tokens in any way while parsing the CSS.
To change this behavior it is necessary to define a callback for ready tokens using the function `lxb_css_syntax_tokenizer_token_cb_set`.

```C
#include "lexbor/css/syntax/tokenizer.h"

lxb_css_syntax_token_t *
token_ready_callback(lxb_css_syntax_tokenizer_t *tkz, 
                     lxb_css_syntax_token_t *token, void *ctx)
{
    /* Do anything with a token */

    return token;
}

int 
main(int argc, const char *argv[])
{
    lxb_css_syntax_tokenizer_t *tkz;

    lxb_char_t css_data[] = "div {display: block}";
    size_t css_size = sizeof(css_data) - 1;

    tkz = lxb_css_syntax_tokenizer_create();
    lxb_css_syntax_tokenizer_init(tkz);

    /* Sets callback */
    lxb_css_syntax_tokenizer_token_cb_set(tkz, token_ready_callback, NULL);

    lxb_css_syntax_tokenizer_parse(tkz, css_data, css_size);

    lxb_css_syntax_tokenizer_destroy(tkz);
}
```


## Data of Token

There are two types of tokens:
1. Have data: `Ident`, `String`, `Bad string`, `Function`, `At keyword`, `Hash`, `URL`, `Bad URL`, `Dimension`, `Whitespaces`, `Comment`
2. No data: `Number`, `Percentage`, `CDO`, `CDC`, `Colon`, `Semicolon`, `Comma`, `Left/Right Square Bracket`, `Left/Right Parenthesis`, `Left/Right Curly Bracket`

Tokens coming to a callback from a tokenizer have no data, only pointers to incoming buffer from begin to end token data.

For example, we have incoming buffer: `*data = "d\69v {display: block}"`.
In callback will come nine tokens:

| [](#class-hide) | [](#class-hide) |
|---|---|---|
|1.| Ident: `d\69v` | Token: `*begin = 'd'`, `*end = ' '` |
|2.| Whitespace: ` ` | Token: `*begin = ' '`, `*end = '{'` |
|3.| Left Curly Bracket: `{` | Token: `*begin = NULL`, `*end = NULL` |
|4.| Ident: `display` | Token: `*begin = 'd'`, `*end = ':'` |
|5.| Colon: `:` | Token: `*begin = NULL`, `*end = NULL` |
|6.| Whitespace: ` ` | Token: `*begin = ' '`, `*end = 'b'` |
|7.| Ident: `block` | Token: `*begin = 'b'`, `*end = '}'` |
|8.| Right Curly Bracket: `}` | Token: `*begin = NULL`, `*end = NULL` |
|9.| End of File | Token: `*begin = NULL`, `*end = NULL` |

From the table we see that the token has only pointers to the data. 
We need to process the token to correctly receive the data on the pointers.
To process data, there are two functions with almost identical functionality:
1. 
```C
lxb_inline lxb_status_t
lxb_css_syntax_tokenizer_make_data(lxb_css_syntax_tokenizer_t *tkz,
                                      lxb_css_syntax_token_t *token);
```
2. 
```C
LXB_API lxb_status_t
lxb_css_syntax_token_make_data(lxb_css_syntax_token_t *token, lexbor_in_node_t *in,
                                  lexbor_mraw_t *mraw, lxb_css_syntax_token_data_t *td);
```

For example, look at the first function (full example):
```C
#include "lexbor/css/syntax/tokenizer.h"

lxb_css_syntax_token_t *
token_ready_callback(lxb_css_syntax_tokenizer_t *tkz, 
                     lxb_css_syntax_token_t *token, void *ctx)
{
    lxb_status_t status;

    status = lxb_css_syntax_tokenizer_make_data(tkz, token);
    if (status != LXB_STATUS_OK) {
        return NULL;
    }

    if (lxb_css_syntax_token_type(token) == LXB_CSS_SYNTAX_TOKEN_IDENT) {
        lxb_css_syntax_token_ident_t *ident;

        ident = lxb_css_syntax_token_ident(token);
        /* or ident = &token->types.ident; */

        printf("Ident data: %s\n", ident->data.data);
    }
    /* Do anything with a token */

    return token;
}

int 
main(int argc, const char *argv[])
{
    lxb_css_syntax_tokenizer_t *tkz;

    lxb_char_t css_data[] = "d\\69v {display: block}";
    size_t css_size = sizeof(css_data) - 1;

    tkz = lxb_css_syntax_tokenizer_create();
    lxb_css_syntax_tokenizer_init(tkz);

    /* Sets callback */
    lxb_css_syntax_tokenizer_token_cb_set(tkz, token_ready_callback, NULL);

    lxb_css_syntax_tokenizer_parse(tkz, css_data, css_size);

    lxb_css_syntax_tokenizer_destroy(tkz);
}
```

The output of the program:
```
Ident data: div
Ident data: display
Ident data: block
```


## Token types

| Name | Example | ID | type | Cast macro | 
|---|---|
| At-keyword                     | `@media`        | `LXB_CSS_SYNTAX_TOKEN_AT_KEYWORD`    | `lxb_css_syntax_token_at_keyword_t`    | `lxb_css_syntax_token_at_keyword(token)` |
| Bad&nbsp;string                | `"my\nbest"`    | `LXB_CSS_SYNTAX_TOKEN_BAD_STRING`    | `lxb_css_syntax_token_bad_string_t`    | `lxb_css_syntax_token_bad_string(token)` |
| Bad&nbsp;URL                   | `url(http bad)` | `LXB_CSS_SYNTAX_TOKEN_BAD_URL`       | `lxb_css_syntax_token_bad_url_t`       | `lxb_css_syntax_token_bad_url(token)` |
| CDC                            | `-->`           | `LXB_CSS_SYNTAX_TOKEN_CDC`           | `lxb_css_syntax_token_cdc_t`           | `lxb_css_syntax_token_cdc(token)` |
| CDO                            | `<!--`          | `LXB_CSS_SYNTAX_TOKEN_CDO`           | `lxb_css_syntax_token_cdo_t`           | `lxb_css_syntax_token_cdo(token)` |
| Colon                          | `:`             | `LXB_CSS_SYNTAX_TOKEN_COLON`         | `lxb_css_syntax_token_colon_t`         | `lxb_css_syntax_token_colon(token)` |
| Comma                          | `,`             | `LXB_CSS_SYNTAX_TOKEN_COMMA`         | `lxb_css_syntax_token_comma_t`         | `lxb_css_syntax_token_comma(token)` |
| Comment                        | `/* some */`    | `LXB_CSS_SYNTAX_TOKEN_COMMENT`       | `lxb_css_syntax_token_comment_t`       | `lxb_css_syntax_token_comment(token)` |
| Delim                          | `*`             | `LXB_CSS_SYNTAX_TOKEN_DELIM`         | `lxb_css_syntax_token_delim_t`         | `lxb_css_syntax_token_delim(token)` |
| Dimension                      | `1.2em`         | `LXB_CSS_SYNTAX_TOKEN_DIMENSION`     | `lxb_css_syntax_token_dimension_t`     | `lxb_css_syntax_token_dimension(token)` |
| Function                       | `not(`          | `LXB_CSS_SYNTAX_TOKEN_FUNCTION`      | `lxb_css_syntax_token_function_t`      | `lxb_css_syntax_token_function(token)` |
| Hash                           | `#id`           | `LXB_CSS_SYNTAX_TOKEN_HASH`          | `lxb_css_syntax_token_hash_t`          | `lxb_css_syntax_token_hash(token)` |
| Ident                          |  `div`          | `LXB_CSS_SYNTAX_TOKEN_IDENT`         | `lxb_css_syntax_token_ident_t`         | `lxb_css_syntax_token_ident(token)` |
| Left&nbsp;curly&nbsp;bracket   | `{`             | `LXB_CSS_SYNTAX_TOKEN_LC_BRACKET`    | `lxb_css_syntax_token_lc_bracket_t`    | `lxb_css_syntax_token_lc_bracket(token)` |
| Left&nbsp;square&nbsp;bracket  | `[`             | `LXB_CSS_SYNTAX_TOKEN_LS_BRACKET`    | `lxb_css_syntax_token_ls_bracket_t`    | `lxb_css_syntax_token_ls_bracket(token) ` |
| Left&nbsp;parenthesis          | `(`             | `LXB_CSS_SYNTAX_TOKEN_L_PARENTHESIS` | `lxb_css_syntax_token_l_parenthesis_t` | `lxb_css_syntax_token_l_parenthesis(token)` |
| Number                         | `1.4`           | `LXB_CSS_SYNTAX_TOKEN_NUMBER`        | `lxb_css_syntax_token_number_t`        | `lxb_css_syntax_token_number(token)` |
| Percentage                     | `10%`           | `LXB_CSS_SYNTAX_TOKEN_PERCENTAGE`    | `lxb_css_syntax_token_percentage_t`    | `lxb_css_syntax_token_percentage(token)` |
| Right&nbsp;curly&nbsp;bracket  | `}`             | `LXB_CSS_SYNTAX_TOKEN_RC_BRACKET`    | `lxb_css_syntax_token_rc_bracket_t`    | `lxb_css_syntax_token_rc_bracket(token)` |
| Right&nbsp;square&nbsp;bracket | `]`             | `LXB_CSS_SYNTAX_TOKEN_RS_BRACKET`    | `lxb_css_syntax_token_rs_bracket_t`    | `lxb_css_syntax_token_rs_bracket(token)` |
| Right&nbsp;parenthesis         | `)`             | `LXB_CSS_SYNTAX_TOKEN_R_PARENTHESIS` | `lxb_css_syntax_token_r_parenthesis_t` | `lxb_css_syntax_token_r_parenthesis(token)` |
| Semicolon                      | `;`             | `LXB_CSS_SYNTAX_TOKEN_SEMICOLON`     | `lxb_css_syntax_token_semicolon_t`     | `lxb_css_syntax_token_semicolon(token)` |
| String                         | `"my best"`     | `LXB_CSS_SYNTAX_TOKEN_STRING`        | `lxb_css_syntax_token_string_t`        | `lxb_css_syntax_token_string(token)` |
| URL                            | `url(http)`     | `LXB_CSS_SYNTAX_TOKEN_URL`           | `lxb_css_syntax_token_url_t`           | `lxb_css_syntax_token_url(token)` |
| Whitespace                     | ` `             | `LXB_CSS_SYNTAX_TOKEN_WHITESPACE`    | `lxb_css_syntax_token_whitespace_t`    | `lxb_css_syntax_token_whitespace(token)` |


### Documentation in under construction.

Documentation in under construction.
