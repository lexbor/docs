[name]: HTML
[title]: <> (HTML Module)
[theme]: document.html
[main_class]: html-module
[refs_deep_max]: 2

# HTML

This is documentation for `HTML` module for [Lexbor library](/). Module created by [whatwg specification](https://html.spec.whatwg.org/multipage/).

## Parsing

There are two ways to parse HTML pages:

1. Through the `Document` Object
2. Through the `Parser` object

Both approaches have same functionality regarding page parsing: parsing a fragment, chunks parsing.
In both cases, the result of parsing is the DOM tree ready for use.

#### Parsing through the Document object

In this approach, we first create a Document object, and then call the parsing function:

```C
lxb_html_document_t *document;

const lxb_char_t html[] = "<div>V</div>";
size_t html_len = sizeof(html) - 1;

document = lxb_html_document_create();

lxb_html_document_parse(document, html, html_len);

/* Work with Document */
```

Inside the `lxb_html_document_parse` function, a `Parser` object will be created and destroyed immediately after processing the data.

This approach is simpler and suitable for cases when you do not have a large number of HTML pages for parsing.


#### Parsing through the Parser object

In this approach, we create a `Parser` object that create a `Document` object for each HTML page.
This approach is more advantageous in that the `Parser` object will be created only once.

```C
lxb_html_parser_t *parser;
lxb_html_document_t *document_one, *document_two;

const lxb_char_t html[] = "<div>V</div>";
size_t html_len = sizeof(html) - 1;

parser = lxb_html_parser_create();
lxb_html_parser_init(parser);

document_one = lxb_html_parse(parser, html, html_len);
document_two = lxb_html_parse(parser, html, html_len);

/* Work with document_one */

lxb_html_parser_destroy(parser);

/* Work with document_two */
```

This approach is suitable for processing a large number of HTML pages.


## Document

Documentation in under construction.

## Parser



## Interfaces

Each element in the DOM tree has its own interface. One interface can be in different elements.
All elements in the DOM tree are inherited from the `DOM Node` interface.

An attentive reader will notice that there is no inheritance in `C`. 
In our case, inheritance means that one interface is present in another at beginning of the structure.

Consider the example of `lxb_html_head_element_t` (`HTMLHeadElement`):

```C
typedef struct lxb_html_head_element lxb_html_head_element_t;
typedef struct lxb_html_element lxb_html_element_t;
typedef struct lxb_dom_element lxb_dom_element_t;
typedef struct lxb_dom_node lxb_dom_node_t;


struct lxb_html_head_element {
    lxb_html_element_t element;
};

struct lxb_html_element {
    lxb_dom_element_t element;
};

struct lxb_dom_element {
    lxb_dom_node_t node;
};

struct lxb_dom_node {
    /* ... */
};
```

In order not to have to write long chains to the desired interface, the project introduce typecasting for all interfaces.

1. Without cast:

```C
lxb_tag_id_t tag_id = head->element.element.node.tag_id;
lxb_ns_id_t ns_id = head->element.element.node.ns_id;
```

2. With cast:

```C
lxb_dom_node_t *node = lxb_dom_interface_node(head);

lxb_tag_id_t tag_id = node->tag_id;
lxb_ns_id_t ns_id = node->ns_id;
```

3. With cast without var on stack:

```C
lxb_tag_id_t tag_id = lxb_dom_interface_node(head)->tag_id;
lxb_ns_id_t ns_id = lxb_dom_interface_node(head)->ns_id;
```

As a result, from the above example with `lxb_html_head_element_t` we can access the following interfaces:

```C
void
something_function_for_example(lxb_html_head_element_t *head)
{
    lxb_html_element_t *html_element = lxb_html_interface_element(head);
    lxb_dom_element_t *dom_element = lxb_dom_interface_element(head);
    lxb_dom_node_t *dom_node = lxb_dom_interface_node(head);

    /* ... */
}
```

The following is a list of all HTML interfaces.

## Interface Types

| [](#class-hide) | [](#class-hide) |
|---|---|
| HTMLDocument [](#class-typedef-header) | [lxb_html_document_t](#lxb_html_document_t) |
| HTMLAnchorElement | [lxb_html_anchor_element_t](#lxb_html_anchor_element_t) |
| HTMLAreaElement | [lxb_html_area_element_t](#lxb_html_area_element_t) |
| HTMLAudioElement | [lxb_html_audio_element_t](#lxb_html_audio_element_t) |
| HTMLBRElement | [lxb_html_br_element_t](#lxb_html_br_element_t) |
| HTMLBaseElement | [lxb_html_base_element_t](#lxb_html_base_element_t) |
| HTMLBodyElement | [lxb_html_body_element_t](#lxb_html_body_element_t) |
| HTMLButtonElement | [lxb_html_button_element_t](#lxb_html_button_element_t) |
| HTMLCanvasElement | [lxb_html_canvas_element_t](#lxb_html_canvas_element_t) |
| HTMLDListElement | [lxb_html_d_list_element_t](#lxb_html_d_list_element_t) |
| HTMLDataElement | [lxb_html_data_element_t](#lxb_html_data_element_t) |
| HTMLDataListElement | [lxb_html_data_list_element_t](#lxb_html_data_list_element_t) |
| HTMLDetailsElement | [lxb_html_details_element_t](#lxb_html_details_element_t) |
| HTMLDialogElement | [lxb_html_dialog_element_t](#lxb_html_dialog_element_t) |
| HTMLDirectoryElement | [lxb_html_directory_element_t](#lxb_html_directory_element_t) |
| HTMLDivElement | [lxb_html_div_element_t](#lxb_html_div_element_t) |
| HTMLElement | [lxb_html_element_t](#lxb_html_element_t) |
| HTMLEmbedElement | [lxb_html_embed_element_t](#lxb_html_embed_element_t) |
| HTMLFieldSetElement | [lxb_html_field_set_element_t](#lxb_html_field_set_element_t) |
| HTMLFontElement | [lxb_html_font_element_t](#lxb_html_font_element_t) |
| HTMLFormElement | [lxb_html_form_element_t](#lxb_html_form_element_t) |
| HTMLFrameElement | [lxb_html_frame_element_t](#lxb_html_frame_element_t) |
| HTMLFrameSetElement | [lxb_html_frame_set_element_t](#lxb_html_frame_set_element_t) |
| HTMLHRElement | [lxb_html_hr_element_t](#lxb_html_hr_element_t) |
| HTMLHeadElement | [lxb_html_head_element_t](#lxb_html_head_element_t) |
| HTMLHeadingElement | [lxb_html_heading_element_t](#lxb_html_heading_element_t) |
| HTMLHtmlElement | [lxb_html_html_element_t](#lxb_html_html_element_t) |
| HTMLIFrameElement | [lxb_html_iframe_element_t](#lxb_html_iframe_element_t) |
| HTMLImageElement | [lxb_html_image_element_t](#lxb_html_image_element_t) |
| HTMLInputElement | [lxb_html_input_element_t](#lxb_html_input_element_t) |
| HTMLLIElement | [lxb_html_li_element_t](#lxb_html_li_element_t) |
| HTMLLabelElement | [lxb_html_label_element_t](#lxb_html_label_element_t) |
| HTMLLegendElement | [lxb_html_legend_element_t](#lxb_html_legend_element_t) |
| HTMLLinkElement | [lxb_html_link_element_t](#lxb_html_link_element_t) |
| HTMLMapElement | [lxb_html_map_element_t](#lxb_html_map_element_t) |
| HTMLMarqueeElement | [lxb_html_marquee_element_t](#lxb_html_marquee_element_t) |
| HTMLMediaElement | [lxb_html_media_element_t](#lxb_html_media_element_t) |
| HTMLMenuElement | [lxb_html_menu_element_t](#lxb_html_menu_element_t) |
| HTMLMetaElement | [lxb_html_meta_element_t](#lxb_html_meta_element_t) |
| HTMLMeterElement | [lxb_html_meter_element_t](#lxb_html_meter_element_t) |
| HTMLModElement | [lxb_html_mod_element_t](#lxb_html_mod_element_t) |
| HTMLOListElement | [lxb_html_o_list_element_t](#lxb_html_o_list_element_t) |
| HTMLObjectElement | [lxb_html_object_element_t](#lxb_html_object_element_t) |
| HTMLOptGroupElement | [lxb_html_opt_group_element_t](#lxb_html_opt_group_element_t) |
| HTMLOptionElement | [lxb_html_option_element_t](#lxb_html_option_element_t) |
| HTMLOutputElement | [lxb_html_output_element_t](#lxb_html_output_element_t) |
| HTMLParagraphElement | [lxb_html_paragraph_element_t](#lxb_html_paragraph_element_t) |
| HTMLParamElement | [lxb_html_param_element_t](#lxb_html_param_element_t) |
| HTMLPictureElement | [lxb_html_picture_element_t](#lxb_html_picture_element_t) |
| HTMLPreElement | [lxb_html_pre_element_t](#lxb_html_pre_element_t) |
| HTMLProgressElement | [lxb_html_progress_element_t](#lxb_html_progress_element_t) |
| HTMLQuoteElement | [lxb_html_quote_element_t](#lxb_html_quote_element_t) |
| HTMLScriptElement | [lxb_html_script_element_t](#lxb_html_script_element_t) |
| HTMLSelectElement | [lxb_html_select_element_t](#lxb_html_select_element_t) |
| HTMLSlotElement | [lxb_html_slot_element_t](#lxb_html_slot_element_t) |
| HTMLSourceElement | [lxb_html_source_element_t](#lxb_html_source_element_t) |
| HTMLSpanElement | [lxb_html_span_element_t](#lxb_html_span_element_t) |
| HTMLStyleElement | [lxb_html_style_element_t](#lxb_html_style_element_t) |
| HTMLTableCaptionElement | [lxb_html_table_caption_element_t](#lxb_html_table_caption_element_t) |
| HTMLTableCellElement | [lxb_html_table_cell_element_t](#lxb_html_table_cell_element_t) |
| HTMLTableColElement | [lxb_html_table_col_element_t](#lxb_html_table_col_element_t) |
| HTMLTableElement | [lxb_html_table_element_t](#lxb_html_table_element_t) |
| HTMLTableRowElement | [lxb_html_table_row_element_t](#lxb_html_table_row_element_t) |
| HTMLTableSectionElement | [lxb_html_table_section_element_t](#lxb_html_table_section_element_t) |
| HTMLTemplateElement | [lxb_html_template_element_t](#lxb_html_template_element_t) |
| HTMLTextAreaElement | [lxb_html_text_area_element_t](#lxb_html_text_area_element_t) |
| HTMLTimeElement | [lxb_html_time_element_t](#lxb_html_time_element_t) |
| HTMLTitleElement | [lxb_html_title_element_t](#lxb_html_title_element_t) |
| HTMLTrackElement | [lxb_html_track_element_t](#lxb_html_track_element_t) |
| HTMLUListElement | [lxb_html_u_list_element_t](#lxb_html_u_list_element_t) |
| HTMLUnknownElement | [lxb_html_unknown_element_t](#lxb_html_unknown_element_t) |
| HTMLVideoElement | [lxb_html_video_element_t](#lxb_html_video_element_t) |
| Window | [lxb_html_window_t](#lxb_html_window_t) |

### lxb_html_document_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/document.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDocument |
| Inherits: | lxb_dom_document_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| lxb_html_document_t&nbsp;* | [lxb_html_document_create](#lxb_html_document_create)(void) |
| void | [lxb_html_document_clean](#lxb_html_document_clean)(lxb_html_document_t \*document) |
| lxb_html_document_t&nbsp;* | [lxb_html_document_destroy](#lxb_html_document_destroy)(lxb_html_document_t \*document) |
| lxb_status_t | [lxb_html_document_parse](#lxb_html_document_parse)(lxb_html_document_t \*document, const lxb_char_t \*html, size_t size) |
| lxb_status_t | [lxb_html_document_parse_chunk_begin](#lxb_html_document_parse_chunk_begin)(lxb_html_document_t \*document) |
| lxb_status_t | [lxb_html_document_parse_chunk](#lxb_html_document_parse_chunk)(lxb_html_document_t \*document, const lxb_char_t \*html, size_t size) |
| lxb_status_t | [lxb_html_document_parse_chunk_end](#lxb_html_document_parse_chunk_end)(lxb_html_document_t \*document) |
| lxb_dom_node_t&nbsp;* | [lxb_html_document_parse_fragment](#lxb_html_document_parse_fragment)(lxb_html_document_t \*document, lxb_dom_element_t \*element, const lxb_char_t \*html, size_t size) |
| lxb_status_t | [lxb_html_document_parse_fragment_chunk_begin](#lxb_html_document_parse_fragment_chunk_begin)(lxb_html_document_t \*document, lxb_dom_element_t \*element) |
| lxb_status_t | [lxb_html_document_parse_fragment_chunk](#lxb_html_document_parse_fragment_chunk)(lxb_html_document_t \*document, const lxb_char_t \*html, size_t size) |
| lxb_dom_node_t&nbsp;* | [lxb_html_document_parse_fragment_chunk_end](#lxb_html_document_parse_fragment_chunk_end)(lxb_html_document_t \*document) |
| const lxb_char_t&nbsp;* | [lxb_html_document_title](#lxb_html_document_title)(lxb_html_document_t \*document, size_t \*len) |
| lxb_status_t | [lxb_html_document_title_set](#lxb_html_document_title_set)(lxb_html_document_t \*document, const lxb_char_t \*title, size_t len) |
| const lxb_char_t&nbsp;* | [lxb_html_document_title_raw](#lxb_html_document_title_raw)(lxb_html_document_t \*document, size_t \*len) |
| lxb_html_head_element_t&nbsp;* | [lxb_html_document_head_element](#lxb_html_document_head_element)(lxb_html_document_t \*document) |
| lxb_html_body_element_t&nbsp;* | [lxb_html_document_body_element](#lxb_html_document_body_element)(lxb_html_document_t \*document) |
| lxb_dom_document_t&nbsp;* | [lxb_html_document_original_ref](#lxb_html_document_original_ref)(lxb_html_document_t \*document) |
| bool | [lxb_html_document_is_original](#lxb_html_document_is_original)(lxb_html_document_t \*document) |
| lexbor_mraw_t&nbsp;* | [lxb_html_document_mraw](#lxb_html_document_mraw)(lxb_html_document_t \*document) |
| lexbor_mraw_t&nbsp;* | [lxb_html_document_mraw_text](#lxb_html_document_mraw_text)(lxb_html_document_t \*document) |
| lxb_tag_heap_t&nbsp;* | [lxb_html_document_tag_heap](#lxb_html_document_tag_heap)(lxb_html_document_t \*document) |
| lxb_ns_heap_t&nbsp;* | [lxb_html_document_ns_heap](#lxb_html_document_ns_heap)(lxb_html_document_t \*document) |
| lxb_html_document_opt_t | [lxb_html_document_opt](#lxb_html_document_opt)(lxb_html_document_t \*document) |
| void | [lxb_html_document_opt_set](#lxb_html_document_opt_set)(lxb_html_document_t \*document, lxb_html_document_opt_t opt) |
| void&nbsp;* | [lxb_html_document_create_struct](#lxb_html_document_create_struct)(lxb_html_document_t \*document, size_t struct_size) |
| void&nbsp;* | [lxb_html_document_destroy_struct](#lxb_html_document_destroy_struct)(lxb_html_document_t \*document, void \*data) |
| lxb_dom_element_t&nbsp;* | [lxb_html_document_create_element](#lxb_html_document_create_element)(lxb_html_document_t \*document, const lxb_char_t \*local_name, size_t lname_len, void \*reserved_for_opt) |
| lxb_dom_element_t&nbsp;* | [lxb_html_document_destroy_element](#lxb_html_document_destroy_element)(lxb_dom_element_t \*element) |

#### lxb_html_document_create

This function create and initialize Document `lxb_html_document_t` object.

```c-api-function
LXB_API lxb_html_document_t *
lxb_html_document_create(void);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| Return | lxb_html_document_t * | Pointer to object if successful, otherwise `NULL` value. ||

For destroy this object use [lxb_html_document_destroy](#lxb_html_document_destroy) function.

#### lxb_html_document_clean

This function clears the `lxb_html_document_t` object.
The memory of all nodes, structures, text, and other things related for this object will be erased.

```c-api-function
LXB_API void
lxb_html_document_clean(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Not `NULL`. Pointer to document. |
| Return | void | Returns nothing. ||

#### lxb_html_document_destroy

This function destroy the `lxb_html_document_t` object. 
All memory used for nodes, interfaces, text will be freed.

```c-api-function
LXB_API lxb_html_document_t *
lxb_html_document_destroy(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Can be `NULL`. If `NULL`, then `NULL` will be returned. |
| Return | lxb_html_document_t * | Always returns `NULL` value. ||


#### lxb_html_document_parse

This function for parsing and build HTML Tree for current Document.

Note:
If this function is called with an already esists HTML tree in Document object, then current HTML tree will be erased and create new. The memory of all nodes, structures, text, and other things related to the exist Document will be erased.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse(lxb_html_document_t *document,
                        const lxb_char_t *html, size_t size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | html | Not `NULL`. The function will not create a copy of incoming data. |
| In | size | Data length. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_html_document_parse_chunk_begin

This is prepare function for chunks parsing.
Called once before parsing chunks.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse_chunk_begin(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||

Usage example:
```C
lxb_html_document_parse_chunk_begin(document);

lxb_html_document_parse_chunk(document, chunk_one, chunk_one_size);
lxb_html_document_parse_chunk(document, chunk_two, chunk_two_size);
/* Or loop for lxb_html_document_parse_chunk */

lxb_html_document_parse_chunk_end(document);

```


#### lxb_html_document_parse_chunk

This function for parsing chunks.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse_chunk(lxb_html_document_t *document,
                              const lxb_char_t *html, size_t size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | html | Not `NULL`. Data for parsing. |
| In | size | Data length. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||

Incoming data will be copied to buffer. At the moment when the buffer will not be needed, the parser freed created buffer.

For example, we have two chunks:

```HTML
<div clas
```

```HTML
s="entry">text
```

For the first chunk, a buffer will be created, and the parser will freed it only after it receives the end of the `div` element.

Another example:

```HTML
<div class="entry">text
```

```HTML
 for best example</div>
```

For the chunks above, the buffer will be created and destroyed immediately after each chunk parsed.

It is possible to disable copying of incoming data. But remember that you will have to store all the data until the end of the parsing.
Before begin parsing chunks:

```C
lxb_html_document_opt_set(document, LXB_HTML_DOCUMENT_PARSE_WO_COPY);

lxb_html_document_parse_chunk_begin(document);
lxb_html_document_parse_chunk(document, chunk_one, chunk_one_size);
/* ... */
```


#### lxb_html_document_parse_chunk_end

This function inform the parser about end of parsing. After that the tree mark as complete.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse_chunk_end(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_html_document_parse_fragment

This function for parsing and build HTML fragment tree.
This function does not affect the current HTML tree. Function creates an additional tree using the current document and returns the root element.
In other words, this is the implementation `innerHTML`.


```c-api-function
LXB_API lxb_dom_node_t *
lxb_html_document_parse_fragment(lxb_html_document_t *document,
                                 lxb_dom_element_t *element,
                                 const lxb_char_t *html, size_t size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | element | Pointer to element. Not `NULL`. Based on this element a tree will be built. |
| In | html | Not `NULL`. The function will not create a copy of incoming data. |
| In | size | Data length. |
| Return | lxb_dom_node_t * | If successful: pointer to the root node of fragment tree, otherwise `NULL` value. ||


#### lxb_html_document_parse_fragment_chunk_begin

This is prepare function for chunks parsing.
Called once before parsing chunks.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse_fragment_chunk_begin(lxb_html_document_t *document,
                                             lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | element | Pointer to element. Not `NULL`. Based on this element a tree will be built. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||

Usage example:
```C
lxb_html_document_parse_fragment_chunk_begin(document, element);

lxb_html_document_parse_fragment_chunk(document, chunk_one, chunk_one_size);
lxb_html_document_parse_fragment_chunk(document, chunk_two, chunk_two_size);
/* Or loop for lxb_html_document_parse_fragment_chunk */

root_node = lxb_html_document_parse_fragment_chunk_end(document);
```


#### lxb_html_document_parse_fragment_chunk

This function for parsing chunks.
The logic of this function is similar to [lxb_html_document_parse_chunk](#lxb_html_document_parse_chunk) function, please see it.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_parse_fragment_chunk(lxb_html_document_t *document,
                                       const lxb_char_t *html, size_t size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | html | Not `NULL`. Data for parsing. |
| In | size | Data length. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_html_document_parse_fragment_chunk_end

This function inform the parser about end of parsing.

```c-api-function
LXB_API lxb_dom_node_t *
lxb_html_document_parse_fragment_chunk_end(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_dom_node_t * | If successful: pointer to the root node of fragment tree, otherwise `NULL` value. ||


#### lxb_html_document_title

This function returns the document's title, as given by the title element.
Returned data will be strip and collapse. All consecutive ASCII whitespace characters will be merged into one. At the beginning and end, all ASCII whitespace characters will be truncated.

```c-api-function
LXB_API const lxb_char_t *
lxb_html_document_title(lxb_html_document_t *document, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of title. |
| Return | const lxb_char_t * | If title element was be found in tree: pointer to the title data, otherwise `NULL` value. ||

For example:
```HTML
<title>  Oh, title  
    
    
    my    title.   </title>
```

Function returns:
```
Oh, title my title.
```


#### lxb_html_document_title_set

This function update the document title. If there is no appropriate element to update, the new element will be created.

```c-api-function
LXB_API lxb_status_t
lxb_html_document_title_set(lxb_html_document_t *document,
                            const lxb_char_t *title, size_t len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | title | Not `NULL`. |
| In | len | Length of title. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_html_document_title_raw

This function returns the document's title as it is.

```c-api-function
LXB_API const lxb_char_t *
lxb_html_document_title_raw(lxb_html_document_t *document, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of title. |
| Return | const lxb_char_t * | If title element was be found in tree: pointer to the title data, otherwise `NULL` value. ||


#### lxb_html_document_head_element

This function returns a head element from HTML Tree.
Head element always present in HTML Tree.

```c-api-function
lxb_inline lxb_html_head_element_t *
lxb_html_document_head_element(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_html_head_element_t * | Head element if exist, otherwise `NULL` value. ||


#### lxb_html_document_body_element

This function returns a body element from HTML Tree.
Body element always present in HTML Tree.

```c-api-function
lxb_inline lxb_html_body_element_t *
lxb_html_document_body_element(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_html_body_element_t * | Body element if exist, otherwise `NULL` value. ||


#### lxb_html_document_original_ref

A document can be created based on an existing document. This function returns original/base document object. 
If the current document is original then it will be returned.

```c-api-function
lxb_inline lxb_dom_document_t *
lxb_html_document_original_ref(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_dom_document_t * |  ||


#### lxb_html_document_is_original

This function checks document for original.

```c-api-function
lxb_inline bool
lxb_html_document_is_original(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | bool | `true` if document is original, otherwise `false` ||


#### lxb_html_document_mraw

This function returns `mraw` object for work with objects memory. 
Through the `mraw` object, memory is allocated for all nodes and structures.

```c-api-function
lxb_inline lexbor_mraw_t *
lxb_html_document_mraw(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lexbor_mraw_t * |  ||


#### lxb_html_document_mraw_text

This function returns `mraw` object for work with strings memory. 
Through the `mraw` object, memory is allocated for all text, strings.

```c-api-function
lxb_inline lexbor_mraw_t *
lxb_html_document_mraw_text(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lexbor_mraw_t * |  ||


#### lxb_html_document_tag_heap

This function returns `lxb_tag_heap_t` object for work with tags.

```c-api-function
lxb_inline lxb_tag_heap_t *
lxb_html_document_tag_heap(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_tag_heap_t * |  ||


#### lxb_html_document_ns_heap

This function returns `lxb_ns_heap_t` object for work with namespaces.

```c-api-function
lxb_inline lxb_ns_heap_t *
lxb_html_document_ns_heap(lxb_html_document_t *document);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_ns_heap_t * |  ||


#### lxb_html_document_opt_set

This function sets options for the document.

```c-api-function
lxb_inline void
lxb_html_document_opt_set(lxb_html_document_t *document,
                          lxb_html_document_opt_t opt);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | opt | Options bitmask. |
| Return | void | Returns nothing. ||


#### lxb_html_document_opt

This function returns current options for document.

```c-api-function
lxb_inline lxb_html_document_opt_t
lxb_html_document_opt(lxb_html_document_t *document)
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| Return | lxb_html_document_opt_t | Current options. ||


#### lxb_html_document_create_struct

This function create and return users structures.
The created structures will be destroyed along with the document.

```c-api-function
lxb_inline void *
lxb_html_document_create_struct(lxb_html_document_t *document,
                                size_t struct_size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | struct_size | User structure size. |
| Return | void * | Pointer to user object if successful, otherwise `NULL` value. ||

Example:
```C
my_best_struct_t *my_best;
my_best = lxb_html_document_create_struct(document, 
                                          sizeof(my_best_struct_t));
/* Do something */
```


#### lxb_html_document_destroy_struct

This function destroy and freed users structures.

```c-api-function
lxb_inline void *
lxb_html_document_destroy_struct(lxb_html_document_t *document, void *data);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | data | Pointer to user object. Not `NULL`. |
| Return | void * | `NULL` value. ||


#### lxb_html_document_create_element

This function create element by tag name.

```c-api-function
lxb_inline lxb_dom_element_t *
lxb_html_document_create_element(lxb_html_document_t *document,
                                 const lxb_char_t *local_name, size_t lname_len,
                                 void *reserved_for_opt);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | local_name | Not `NULL`. Tag name. |
| In | lname_len | Length of local_name. |
| In | reserved_for_opt | Reserved for future. |
| Return | lxb_dom_element_t * | Pointer to created element if successful, otherwise `NULL` value. ||


#### lxb_html_document_destroy_element

This function destroy HTML element.

```c-api-function
lxb_inline lxb_dom_element_t *
lxb_html_document_destroy_element(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | document | Pointer to document. Not `NULL`. |
| In | element | Pointer to element. Not `NULL`. |
| Return | lxb_dom_element_t * | `NULL` value. ||


### lxb_html_anchor_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/anchor_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLAnchorElement |
| Inherits: | lxb_html_element_t |

### lxb_html_area_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/area_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLAreaElement |
| Inherits: | lxb_html_element_t |

### lxb_html_audio_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/audio_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLAudioElement |
| Inherits: | lxb_html_media_element_t |

### lxb_html_br_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/br_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLBRElement |
| Inherits: | lxb_html_element_t |

### lxb_html_base_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/base_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLBaseElement |
| Inherits: | lxb_html_element_t |

### lxb_html_body_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/body_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLBodyElement |
| Inherits: | lxb_html_element_t |

### lxb_html_button_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/button_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLButtonElement |
| Inherits: | lxb_html_element_t |

### lxb_html_canvas_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/canvas_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLCanvasElement |
| Inherits: | lxb_html_element_t |

### lxb_html_d_list_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/d_list_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDListElement |
| Inherits: | lxb_html_element_t |

### lxb_html_data_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/data_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDataElement |
| Inherits: | lxb_html_element_t |

### lxb_html_data_list_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/data_list_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDataListElement |
| Inherits: | lxb_html_element_t |

### lxb_html_details_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/details_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDetailsElement |
| Inherits: | lxb_html_element_t |

### lxb_html_dialog_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/dialog_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDialogElement |
| Inherits: | lxb_html_element_t |

### lxb_html_directory_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/directory_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDirectoryElement |
| Inherits: | lxb_html_element_t |

### lxb_html_div_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/div_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLDivElement |
| Inherits: | lxb_html_element_t |

### lxb_html_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLElement |
| Inherits: | lxb_dom_element_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| lxb_html_element_t&nbsp;* | [lxb_html_element_inner_html_set](#lxb_html_element_inner_html_set)(lxb_html_element_t \*element, const lxb_char_t \*html, size_t size) |

#### lxb_html_element_inner_html_set

This function builds a tree from a HTML fragment and replaces all the child elements of the set element with the created ones.

```c-api-function
LXB_API lxb_html_element_t *
lxb_html_element_inner_html_set(lxb_html_element_t *element,
                                const lxb_char_t *html, size_t size);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to element in which all child elements will be replaced. Not `NULL`. |
| In | html | Pointer to HTML fragment. Not `NULL`. |
| In | size | Length of `html`. |
| Return | lxb_html_element_t * | Pointer to `element` if successful, otherwise `NULL` value. ||


### lxb_html_embed_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/embed_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLEmbedElement |
| Inherits: | lxb_html_element_t |

### lxb_html_field_set_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/field_set_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLFieldSetElement |
| Inherits: | lxb_html_element_t |

### lxb_html_font_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/font_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLFontElement |
| Inherits: | lxb_html_element_t |

### lxb_html_form_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/form_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLFormElement |
| Inherits: | lxb_html_element_t |

### lxb_html_frame_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/frame_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLFrameElement |
| Inherits: | lxb_html_element_t |

### lxb_html_frame_set_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/frame_set_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLFrameSetElement |
| Inherits: | lxb_html_element_t |

### lxb_html_hr_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/hr_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLHRElement |
| Inherits: | lxb_html_element_t |

### lxb_html_head_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/head_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLHeadElement |
| Inherits: | lxb_html_element_t |

### lxb_html_heading_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/heading_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLHeadingElement |
| Inherits: | lxb_html_element_t |

### lxb_html_html_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/html_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLHtmlElement |
| Inherits: | lxb_html_element_t |

### lxb_html_iframe_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/iframe_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLIFrameElement |
| Inherits: | lxb_html_element_t |

### lxb_html_image_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/image_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLImageElement |
| Inherits: | lxb_html_element_t |

### lxb_html_input_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/input_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLInputElement |
| Inherits: | lxb_html_element_t |

### lxb_html_li_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/li_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLLIElement |
| Inherits: | lxb_html_element_t |

### lxb_html_label_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/label_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLLabelElement |
| Inherits: | lxb_html_element_t |

### lxb_html_legend_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/legend_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLLegendElement |
| Inherits: | lxb_html_element_t |

### lxb_html_link_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/link_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLLinkElement |
| Inherits: | lxb_html_element_t |

### lxb_html_map_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/map_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMapElement |
| Inherits: | lxb_html_element_t |

### lxb_html_marquee_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/marquee_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMarqueeElement |
| Inherits: | lxb_html_element_t |

### lxb_html_media_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/media_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMediaElement |
| Inherits: | lxb_html_element_t |

### lxb_html_menu_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/menu_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMenuElement |
| Inherits: | lxb_html_element_t |

### lxb_html_meta_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/meta_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMetaElement |
| Inherits: | lxb_html_element_t |

### lxb_html_meter_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/meter_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLMeterElement |
| Inherits: | lxb_html_element_t |

### lxb_html_mod_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/mod_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLModElement |
| Inherits: | lxb_html_element_t |

### lxb_html_o_list_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/o_list_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLOListElement |
| Inherits: | lxb_html_element_t |

### lxb_html_object_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/object_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLObjectElement |
| Inherits: | lxb_html_element_t |

### lxb_html_opt_group_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/opt_group_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLOptGroupElement |
| Inherits: | lxb_html_element_t |

### lxb_html_option_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/option_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLOptionElement |
| Inherits: | lxb_html_element_t |

### lxb_html_output_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/output_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLOutputElement |
| Inherits: | lxb_html_element_t |

### lxb_html_paragraph_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/paragraph_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLParagraphElement |
| Inherits: | lxb_html_element_t |

### lxb_html_param_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/param_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLParamElement |
| Inherits: | lxb_html_element_t |

### lxb_html_picture_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/picture_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLPictureElement |
| Inherits: | lxb_html_element_t |

### lxb_html_pre_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/pre_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLPreElement |
| Inherits: | lxb_html_element_t |

### lxb_html_progress_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/progress_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLProgressElement |
| Inherits: | lxb_html_element_t |

### lxb_html_quote_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/quote_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLQuoteElement |
| Inherits: | lxb_html_element_t |

### lxb_html_script_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/script_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLScriptElement |
| Inherits: | lxb_html_element_t |

### lxb_html_select_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/select_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLSelectElement |
| Inherits: | lxb_html_element_t |

### lxb_html_slot_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/slot_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLSlotElement |
| Inherits: | lxb_html_element_t |

### lxb_html_source_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/source_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLSourceElement |
| Inherits: | lxb_html_element_t |

### lxb_html_span_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/span_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLSpanElement |
| Inherits: | lxb_html_element_t |

### lxb_html_style_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/style_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLStyleElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_caption_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_caption_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableCaptionElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_cell_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_cell_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableCellElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_col_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_col_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableColElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_row_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_row_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableRowElement |
| Inherits: | lxb_html_element_t |

### lxb_html_table_section_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/table_section_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTableSectionElement |
| Inherits: | lxb_html_element_t |

### lxb_html_template_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/template_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTemplateElement |
| Inherits: | lxb_html_element_t |

### lxb_html_text_area_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/text_area_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTextAreaElement |
| Inherits: | lxb_html_element_t |

### lxb_html_time_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/time_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTimeElement |
| Inherits: | lxb_html_element_t |

### lxb_html_title_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/title_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTitleElement |
| Inherits: | lxb_html_element_t |

### lxb_html_track_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/track_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLTrackElement |
| Inherits: | lxb_html_element_t |

### lxb_html_u_list_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/u_list_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLUListElement |
| Inherits: | lxb_html_element_t |

### lxb_html_unknown_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/unknown_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLUnknownElement |
| Inherits: | lxb_html_element_t |

### lxb_html_video_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/video_element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | HTMLVideoElement |
| Inherits: | lxb_html_media_element_t |

### lxb_html_window_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/html/interfaces/window.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Window |
| Inherits: | lxb_dom_event_target_t |
