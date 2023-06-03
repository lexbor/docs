[name]: DOM
[title]: <> (DOM Module)
[theme]: document.html
[main_class]: dom-module
[refs_deep_max]: 2

# DOM

This is documentation for `DOM` module for [Lexbor library](/). Module created by [whatwg specification](https://dom.spec.whatwg.org/).


## Interface Types

| [](#class-hide) | [](#class-hide) |
|---|---|
| Attr | [lxb_dom_attr_t](#lxb_dom_attr_t) |
| CDATASection | [lxb_dom_cdata_section_t](#lxb_dom_cdata_section_t) |
| CharacterData | [lxb_dom_character_data_t](#lxb_dom_character_data_t) |
| Comment | [lxb_dom_comment_t](#lxb_dom_comment_t) |
| Document | [lxb_dom_document_t](#lxb_dom_document_t) |
| DocumentFragment | [lxb_dom_document_fragment_t](#lxb_dom_document_fragment_t) |
| DocumentType | [lxb_dom_document_type_t](#lxb_dom_document_type_t) |
| Element | [lxb_dom_element_t](#lxb_dom_element_t) |
| EventTarget | [lxb_dom_event_target_t](#lxb_dom_event_target_t) |
| Node | [lxb_dom_node_t](#lxb_dom_node_t) |
| ProcessingInstruction | [lxb_dom_processing_instruction_t](#lxb_dom_processing_instruction_t) |
| ShadowRoot | [lxb_dom_shadow_root_t](#lxb_dom_shadow_root_t) |
| Text | [lxb_dom_text_t](#lxb_dom_text_t) |

### lxb_dom_attr_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/attr.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Attr |
| Inherits: | lxb_dom_node_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| lxb_status_t | lxb_dom_attr_set_name(lxb_dom_attr_t \*attr, const lxb_char_t \*local_name, size_t local_name_len, const lxb_char_t \*prefix, size_t prefix_len, bool lowercase) |
| lxb_status_t | lxb_dom_attr_set_name_wo_copy(lxb_dom_attr_t \*attr, lxb_char_t \*local_name, size_t local_name_len, const lxb_char_t \*prefix, size_t prefix_len) |
| lxb_status_t | lxb_dom_attr_set_value(lxb_dom_attr_t \*attr, const lxb_char_t \*value, size_t value_len) |
| lxb_status_t | lxb_dom_attr_set_value_wo_copy(lxb_dom_attr_t \*attr, lxb_char_t \*value, size_t value_len) |
| lxb_status_t | lxb_dom_attr_set_existing_value(lxb_dom_attr_t \*attr, const lxb_char_t \*value, size_t value_len) |
| lxb_status_t | lxb_dom_attr_clone_name_value(lxb_dom_attr_t \*attr_from, lxb_dom_attr_t \*attr_to) |
| bool | lxb_dom_attr_compare(lxb_dom_attr_t \*first, lxb_dom_attr_t \*second) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_attr_qualified_name(lxb_dom_attr_t \*attr, size_t \*len) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_attr_local_name(lxb_dom_attr_t \*attr, size_t \*len) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_attr_value(lxb_dom_attr_t \*attr, size_t \*len) |


### lxb_dom_cdata_section_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/cdata_section.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | CDATASection |
| Inherits: | lxb_dom_text_t |

### lxb_dom_character_data_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/character_data.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | CharacterData |
| Inherits: | lxb_dom_node_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| lxb_status_t | [lxb_dom_character_data_replace](#lxb_dom_character_data_replace)(lxb_dom_character_data_t \*ch_data, const lxb_char_t \*data, size_t len, size_t offset, size_t count) |

#### lxb_dom_character_data_replace

This function replaces data in a text node.

```c-api-function
LXB_API lxb_status_t
lxb_dom_character_data_replace(lxb_dom_character_data_t *ch_data,
                               const lxb_char_t *data, size_t len,
                               size_t offset, size_t count);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | ch_data | Pointer to character data node. Not `NULL`. |
| In | data | Pointer to data. Not `NULL`.  |
| In | len | Length of `data`. |
| In | offset | Where to begin replacing characters. Start value starts at 0. |
| In | count | How many characters to replace. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise `NULL` value. ||


### lxb_dom_comment_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/comment.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Comment |
| Inherits: | lxb_dom_character_data_t |

### lxb_dom_document_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/document.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Document |
| Inherits: | lxb_dom_node_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| void | lxb_dom_document_attach_doctype(lxb_dom_document_t \*document, lxb_dom_document_type_t \*doctype) |
| void | lxb_dom_document_attach_element(lxb_dom_document_t \*document, lxb_dom_element_t \*element) |
| [lxb_dom_element_t](#lxb_dom_element_t)&nbsp;* | lxb_dom_document_create_element(lxb_dom_document_t \*document, const lxb_char_t \*local_name, size_t lname_len, void \*reserved_for_opt) |
| [lxb_dom_element_t](#lxb_dom_element_t)&nbsp;* | lxb_dom_document_destroy_element(lxb_dom_element_t \*element) |
| [lxb_dom_document_fragment_t](#lxb_dom_document_fragment_t) * | lxb_dom_document_create_document_fragment(lxb_dom_document_t \*document) |
| [lxb_dom_text_t](#lxb_dom_text_t)&nbsp;* | lxb_dom_document_create_text_node(lxb_dom_document_t \*document, const lxb_char_t \*data, size_t len) |
| [lxb_dom_cdata_section_t](#lxb_dom_cdata_section_t)&nbsp;* | lxb_dom_document_create_cdata_section(lxb_dom_document_t \*document, const lxb_char_t \*data, size_t len) |
| lxb_dom_processing_instruction_t&nbsp;* | lxb_dom_document_create_processing_instruction(lxb_dom_document_t \*document, const lxb_char_t \*target, size_t target_len, const lxb_char_t \*data, size_t data_len) |
| lxb_dom_comment_t&nbsp;* | lxb_dom_document_create_comment(lxb_dom_document_t \*document, const lxb_char_t \*data, size_t len) |
| lxb_dom_interface_t&nbsp;* | lxb_dom_document_create_interface(lxb_dom_document_t \*document, lxb_tag_id_t tag_id, lxb_ns_id_t ns) |
| lxb_dom_interface_t&nbsp;* | lxb_dom_document_destroy_interface(lxb_dom_interface_t \*interface) |
| void&nbsp;* | lxb_dom_document_create_struct(lxb_dom_document_t \*document, size_t struct_size) |
| void&nbsp;* | lxb_dom_document_destroy_struct(lxb_dom_document_t \*document, void \*structure) |
| lxb_char_t&nbsp;* | lxb_dom_document_create_text(lxb_dom_document_t \*document, size_t len) |
| void&nbsp;* | lxb_dom_document_destroy_text(lxb_dom_document_t \*document, lxb_char_t \*text) |


### lxb_dom_document_fragment_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/document_fragment.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | DocumentFragment |
| Inherits: | lxb_dom_node_t |

### lxb_dom_document_type_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/document_type.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | DocumentType |
| Inherits: | lxb_dom_node_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_document_type_name(lxb_dom_document_type_t \*doc_type, size_t \*len) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_document_type_public_id(lxb_dom_document_type_t \*doc_type, size_t \*len) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_document_type_system_id(lxb_dom_document_type_t \*doc_type, size_t \*len) |


#### lxb_dom_document_type_name

This function returns name of document type node.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_document_type_name(lxb_dom_document_type_t *doc_type, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | pi | Pointer to DOM document type node. Not `NULL`. |
| Out | len | Pointer to length of name. Can be `NULL`. |
| Return | const lxb_char_t * | Pointer to the name data, otherwise `NULL` value. ||


#### lxb_dom_document_type_public_id

This function returns public id of document type node.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_document_type_public_id(lxb_dom_document_type_t *doc_type, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | pi | Pointer to DOM document type node. Not `NULL`. |
| Out | len | Pointer to length of public id. Can be `NULL`. |
| Return | const lxb_char_t * | Pointer to the public id data, otherwise `NULL` value. ||


#### lxb_dom_document_type_system_id

This function returns system id of document type node.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_document_type_system_id(lxb_dom_document_type_t *doc_type, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | pi | Pointer to DOM document type node. Not `NULL`. |
| Out | len | Pointer to length of system id. Can be `NULL`. |
| Return | const lxb_char_t * | Pointer to the system id data, otherwise `NULL` value. ||


### lxb_dom_element_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/element.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Element |
| Inherits: | lxb_dom_node_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| bool | [lxb_dom_element_has_attributes](#lxb_dom_element_has_attributes)(lxb_dom_element_t \*element) |
| lxb_dom_attr_t * | [lxb_dom_element_set_attribute](#lxb_dom_element_set_attribute)(lxb_dom_element_t \*element, const lxb_char_t \*qualified_name, size_t qn_len, const lxb_char_t \*value, size_t value_len) |
| const lxb_char_t&nbsp;* | [lxb_dom_element_get_attribute](#lxb_dom_element_get_attribute)(lxb_dom_element_t \*element, const lxb_char_t \*qualified_name, size_t qn_len, size_t \*value_len) |
| lxb_status_t | [lxb_dom_element_remove_attribute](#lxb_dom_element_remove_attribute)(lxb_dom_element_t \*element, const lxb_char_t \*qualified_name, size_t qn_len) |
| bool | [lxb_dom_element_has_attribute](#lxb_dom_element_has_attribute)(lxb_dom_element_t \*element, const lxb_char_t \*qualified_name, size_t qn_len) |
| lxb_status_t | [lxb_dom_element_attr_append](#lxb_dom_element_attr_append)(lxb_dom_element_t \*element, lxb_dom_attr_t \*attr) |
| lxb_status_t | [lxb_dom_element_attr_remove](#lxb_dom_element_attr_remove)(lxb_dom_element_t \*element, lxb_dom_attr_t \*attr) |
| lxb_dom_attr_t * | [lxb_dom_element_attr_by_name](#lxb_dom_element_attr_by_name)(lxb_dom_element_t \*element, const lxb_char_t \*qualified_name, size_t qn_len) |
| bool | [lxb_dom_element_compare](#lxb_dom_element_compare)(lxb_dom_element_t \*first, lxb_dom_element_t \*second) |
| lxb_status_t | [lxb_dom_element_qualified_name_set](#lxb_dom_element_qualified_name_set)(lxb_dom_element_t \*element, const lxb_char_t \*prefix, unsigned int prefix_len, const lxb_char_t \*lname, unsigned int lname_len) |
| bool | [lxb_dom_element_qualified_name_cmp](#lxb_dom_element_qualified_name_cmp)(lxb_dom_element_t \*element, lxb_tag_id_t tag_id, const lxb_char_t \*prefix, size_t prefix_len, const lxb_char_t \*lname, size_t lname_len) |
| lxb_status_t | [lxb_dom_element_is_set](#lxb_dom_element_is_set)(lxb_dom_element_t \*element, const lxb_char_t \*is, size_t is_len) |
| lxb_status_t | [lxb_dom_elements_by_tag_name](#lxb_dom_elements_by_tag_name)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*qualified_name, size_t len) |
| lxb_status_t | [lxb_dom_elements_by_class_name](#lxb_dom_elements_by_class_name)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*class_name, size_t len) |
| lxb_status_t | [lxb_dom_elements_by_attr](#lxb_dom_elements_by_attr)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*qualified_name, size_t qname_len, const lxb_char_t \*value, size_t value_len, bool case_insensitive) |
| lxb_status_t | [lxb_dom_elements_by_attr_begin](#lxb_dom_elements_by_attr_begin)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*qualified_name, size_t qname_len, const lxb_char_t \*value, size_t value_len, bool case_insensitive) |
| lxb_status_t | [lxb_dom_elements_by_attr_end](#lxb_dom_elements_by_attr_end)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*qualified_name, size_t qname_len, const lxb_char_t \*value, size_t value_len, bool case_insensitive) |
| lxb_status_t | [lxb_dom_elements_by_attr_contain](#lxb_dom_elements_by_attr_contain)(lxb_dom_element_t \*root, lxb_dom_collection_t \*collection, const lxb_char_t \*qualified_name, size_t qname_len, const lxb_char_t \*value, size_t value_len, bool case_insensitive) |
| const&nbsp;lxb_char_t&nbsp;* | [lxb_dom_element_qualified_name](#lxb_dom_element_qualified_name)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_qualified_name_upper](#lxb_dom_element_qualified_name_upper)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_local_name](#lxb_dom_element_local_name)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_prefix](#lxb_dom_element_prefix)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_tag_name](#lxb_dom_element_tag_name)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_id](#lxb_dom_element_id)(lxb_dom_element_t \*element, size_t \*len) |
| const lxb_char_t * | [lxb_dom_element_class](#lxb_dom_element_class)(lxb_dom_element_t \*element, size_t \*len) |
| bool |[lxb_dom_element_is_custom](#lxb_dom_element_is_custom)(lxb_dom_element_t \*element) |
| bool | [lxb_dom_element_custom_is_defined](#lxb_dom_element_custom_is_defined)(lxb_dom_element_t \*element) |
| lxb_dom_attr_t * | [lxb_dom_element_first_attribute](#lxb_dom_element_first_attribute)(lxb_dom_element_t \*element) |
| lxb_dom_attr_t * | [lxb_dom_element_next_attribute](#lxb_dom_element_next_attribute)(lxb_dom_attr_t \*attr) |
| lxb_dom_attr_t * | [lxb_dom_element_prev_attribute](#lxb_dom_element_prev_attribute)(lxb_dom_attr_t \*attr) |
| lxb_dom_attr_t * | [lxb_dom_element_last_attribute](#lxb_dom_element_last_attribute)(lxb_dom_element_t \*element) |
| lxb_dom_attr_t * | [lxb_dom_element_id_attribute](#lxb_dom_element_id_attribute)(lxb_dom_element_t \*element) |
| lxb_dom_attr_t * | [lxb_dom_element_class_attribute](#lxb_dom_element_class_attribute)(lxb_dom_element_t \*element) |

#### lxb_dom_element_has_attributes

This function checks the presence of an attributes on an element.

```c-api-function
LXB_API bool
lxb_dom_element_has_attributes(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | bool | `true` if exists, otherwise `false`. ||

#### lxb_dom_element_set_attribute

This function adds attribute to an element, and gives it the specified value.

If the attribute already exists, only the value is set/changed.

```c-api-function
LXB_API lxb_dom_attr_t *
lxb_dom_element_set_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len,
                              const lxb_char_t *value, size_t value_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | qn_len | Length of `qualified_name`. |
| In | value | Pointer to value data. Can be `NULL`. |
| In | value_len | Length of `value`. |
| Return | lxb_dom_attr_t * | Attribute object if successful, otherwise `NULL` value. ||

#### lxb_dom_element_get_attribute

This function returns value of attribute by name, from element.

```c-api-function
LXB_API const lxb_char_t *
lxb_dom_element_get_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len,
                              size_t *value_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | qn_len | Length of `qualified_name`. |
| Out | value_len | Length of `value`. |
| Return | const lxb_char_t * | Pointer to value data if attribute exists, otherwise `NULL` value. ||

#### lxb_dom_element_remove_attribute

This function removes the attribute from an element by name.

```c-api-function
LXB_API lxb_status_t
lxb_dom_element_remove_attribute(lxb_dom_element_t *element,
                                 const lxb_char_t *qualified_name, size_t qn_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | qn_len | Length of `qualified_name`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_element_has_attribute

This function checks the presence of an attribute on an element by name.

```c-api-function
LXB_API bool
lxb_dom_element_has_attribute(lxb_dom_element_t *element,
                              const lxb_char_t *qualified_name, size_t qn_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | qn_len | Length of `qualified_name`. |
| Return | bool | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_element_attr_append

This function adds an attribute to the element.

```c-api-function
LXB_API lxb_status_t
lxb_dom_element_attr_append(lxb_dom_element_t *element, lxb_dom_attr_t *attr);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | attr | Pointer to attribute. Not `NULL`. |
| Return | bool | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_element_attr_remove

This function removes the attribute from an element by pointer.

```c-api-function
LXB_API lxb_status_t
lxb_dom_element_attr_remove(lxb_dom_element_t *element, lxb_dom_attr_t *attr);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | attr | Pointer to attribute. Not `NULL`. |
| Return | bool | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_element_attr_by_name

This function returns pointer of attribute by name, from element.

```c-api-function
LXB_API lxb_dom_attr_t *
lxb_dom_element_attr_by_name(lxb_dom_element_t *element,
                             const lxb_char_t *qualified_name, size_t qn_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | qn_len | Length of `qualified_name`. |
| Return | lxb_dom_attr_t * | Pointer to attribute if exists, otherwise `NULL` value. ||


#### lxb_dom_element_compare

This function returns pointer of attribute by name, from element.

```c-api-function
LXB_API bool
lxb_dom_element_compare(lxb_dom_element_t *first, lxb_dom_element_t *second);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | first | Pointer to DOM element. Not `NULL`. |
| In | second | Pointer to DOM element. Not `NULL`. |
| Return | bool | `true` if equal, otherwise `false`. ||


#### lxb_dom_element_qualified_name_set

This function sets the qualified name for the element.

```c-api-function
LXB_API lxb_status_t
lxb_dom_element_qualified_name_set(lxb_dom_element_t *element,
                                   const lxb_char_t *prefix, unsigned int prefix_len,
                                   const lxb_char_t *lname, unsigned int lname_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | prefix | Pointer to prefix data. Can be `NULL`. |
| In | prefix_len | Length of `prefix`. |
| In | lname | Pointer to name data. Not `NULL`. |
| In | lname_len | Length of `qualified_name`. |
| Return | lxb_dom_attr_t * | Pointer to attribute if exists, otherwise `NULL` value. ||


#### lxb_dom_element_qualified_name_cmp

This function compares the qualified name of the element with the one passed.

```c-api-function
LXB_API bool
lxb_dom_element_qualified_name_cmp(lxb_dom_element_t *element, lxb_tag_id_t tag_id,
                                   const lxb_char_t *prefix, size_t prefix_len,
                                   const lxb_char_t *lname, size_t lname_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | prefix | Pointer to prefix data. Can be `NULL`. |
| In | prefix_len | Length of `prefix`. |
| In | lname | Pointer to name data. Not `NULL`. |
| In | lname_len | Length of `qualified_name`. |
| Return | bool | `true` if equal, otherwise `false`. ||


#### lxb_dom_element_is_set

This function sets IS value for element.

```c-api-function
LXB_API lxb_status_t
lxb_dom_element_is_set(lxb_dom_element_t *element,
                       const lxb_char_t *is, size_t is_len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| In | is | Pointer to is data. Not `NULL`. |
| In | is_len | Length of `is`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_tag_name

This function searches for elements by tag name and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_tag_name(lxb_dom_element_t *root,
                             lxb_dom_collection_t *collection,
                             const lxb_char_t *qualified_name, size_t len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | len | Length of `qualified_name`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_class_name

This function searches for elements by class name and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_class_name(lxb_dom_element_t *root,
                               lxb_dom_collection_t *collection,
                               const lxb_char_t *class_name, size_t len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | class_name | Pointer to class name data. Not `NULL`. |
| In | len | Length of `class_name`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_attr

This function searches for elements by attribute name and value (optional) and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_attr(lxb_dom_element_t *root,
                         lxb_dom_collection_t *collection,
                         const lxb_char_t *qualified_name, size_t qname_len,
                         const lxb_char_t *value, size_t value_len,
                         bool case_insensitive);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | len | Length of `qualified_name`. |
| In | value | Pointer to name data. Can be `NULL`. |
| In | value_len | Length of `value`. |
| In | case_insensitive | Case insensitive if set to `true`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_attr_begin

This function searches for elements at the beginning of the attribute value and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_attr_begin(lxb_dom_element_t *root,
                               lxb_dom_collection_t *collection,
                               const lxb_char_t *qualified_name, size_t qname_len,
                               const lxb_char_t *value, size_t value_len,
                               bool case_insensitive);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | len | Length of `qualified_name`. |
| In | value | Pointer to name data. Can be `NULL`. |
| In | value_len | Length of `value`. |
| In | case_insensitive | Case insensitive if set to `true`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_attr_end

This function searches for elements at the end of an attribute value and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_attr_end(lxb_dom_element_t *root,
                             lxb_dom_collection_t *collection,
                             const lxb_char_t *qualified_name, size_t qname_len,
                             const lxb_char_t *value, size_t value_len,
                             bool case_insensitive);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | len | Length of `qualified_name`. |
| In | value | Pointer to name data. Can be `NULL`. |
| In | value_len | Length of `value`. |
| In | case_insensitive | Case insensitive if set to `true`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_elements_by_attr_contain

This function searches for elements at contain of an attribute value and adds them to the collection.

```c-api-function
LXB_API lxb_status_t
lxb_dom_elements_by_attr_contain(lxb_dom_element_t *root,
                                 lxb_dom_collection_t *collection,
                                 const lxb_char_t *qualified_name, size_t qname_len,
                                 const lxb_char_t *value, size_t value_len,
                                 bool case_insensitive);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM element. Not `NULL`. |
| In | collection | Pointer to collection object. Not `NULL`. Must be created and initialized. |
| In | qualified_name | Pointer to name data. Not `NULL`. |
| In | len | Length of `qualified_name`. |
| In | value | Pointer to name data. Can be `NULL`. |
| In | value_len | Length of `value`. |
| In | case_insensitive | Case insensitive if set to `true`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_element_qualified_name

This function returns the qualified name of the element.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_qualified_name(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to name data, otherwise `NULL` value. ||


#### lxb_dom_element_qualified_name_upper

This function returns qualified name of an element in uppercase.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_qualified_name_upper(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to name data, otherwise `NULL` value. ||


#### lxb_dom_element_local_name

This function returns local name of an element.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_local_name(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to local name data, otherwise `NULL` value. ||


#### lxb_dom_element_prefix

This function returns namespace prefix of an element.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_prefix(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to prefix data, otherwise `NULL` value. ||


#### lxb_dom_element_tag_name

This function returns tag name of an element.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_tag_name(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to tag name data, otherwise `NULL` value. ||


#### lxb_dom_element_id

This function returns id of an element. In other words, returns the value from the `id` attribute.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_id(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to id data, otherwise `NULL` value. ||


#### lxb_dom_element_class

This function returns class of an element. In other words, returns the value from the `class` attribute.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_element_class(lxb_dom_element_t *element, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to class data, otherwise `NULL` value. ||


#### lxb_dom_element_is_custom

This function checks for element is custom.

```c-api-function
lxb_inline bool
lxb_dom_element_is_custom(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | bool | `true` if custom, otherwise `false`. ||


#### lxb_dom_element_custom_is_defined

This function checks for element is custom defined.

```c-api-function
lxb_inline bool
lxb_dom_element_custom_is_defined(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | bool | `true` if defined, otherwise `false`. ||


#### lxb_dom_element_first_attribute

This function returns the first attribute from the element attribute list.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_first_attribute(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


#### lxb_dom_element_next_attribute

This function returns the next attribute from the element attribute list.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_next_attribute(lxb_dom_attr_t *attr);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


#### lxb_dom_element_prev_attribute

This function returns the previous attribute from the element attribute list.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_prev_attribute(lxb_dom_attr_t *attr);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


#### lxb_dom_element_last_attribute

This function returns the last attribute from the element attribute list.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_last_attribute(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


#### lxb_dom_element_id_attribute

This function returns pointer to `id` attribute of element.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_id_attribute(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


#### lxb_dom_element_class_attribute

This function returns pointer to `class` attribute of element.

```c-api-function
lxb_inline lxb_dom_attr_t *
lxb_dom_element_class_attribute(lxb_dom_element_t *element);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | element | Pointer to DOM element. Not `NULL`. |
| Return | lxb_dom_attr_t * | Attribute object if exists, otherwise `NULL` value. ||


### lxb_dom_event_target_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/event_target.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | EventTarget |
| Inherits: | None |

### lxb_dom_node_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/node.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Node |
| Inherits: | lxb_dom_event_target_t |

#### Attributes

| Value [](#class-function-list-return) | Name [](#class-function-list-name) | Description [](#class-function-list-desc) |
|---:|---|
| [lxb_dom_document_t](#lxb_dom_document_t)&nbsp;* | owner_document | Pointer to the document that owns the node. |
| [lxb_dom_node_t](#lxb_dom_node_t) * | next | Pointer to the next node. |
| [lxb_dom_node_t](#lxb_dom_node_t) * | prev | Pointer to the next node. |
| [lxb_dom_node_t](#lxb_dom_node_t) * | parent | Pointer to the previous node. |
| [lxb_dom_node_t](#lxb_dom_node_t) * | first_child | Pointer to the first child. |
| [lxb_dom_node_t](#lxb_dom_node_t) * | last_child | Pointer to the last child. |
| unsigned int | ns | Namespace identifier. |
| unsigned int | tag_id | Tag name identifier. |
| [lxb_dom_node_type_t](#lxb_dom_node_type_t) | type | Node type. |


#### Enums

#### lxb_dom_node_type_t

```C
LXB_DOM_NODE_TYPE_UNDEF                  = 0x00,
LXB_DOM_NODE_TYPE_ELEMENT                = 0x01,
LXB_DOM_NODE_TYPE_ATTRIBUTE              = 0x02,
LXB_DOM_NODE_TYPE_TEXT                   = 0x03,
LXB_DOM_NODE_TYPE_CDATA_SECTION          = 0x04,
LXB_DOM_NODE_TYPE_ENTITY_REFERENCE       = 0x05, /* historical */
LXB_DOM_NODE_TYPE_ENTITY                 = 0x06, /* historical */
LXB_DOM_NODE_TYPE_PROCESSING_INSTRUCTION = 0x07,
LXB_DOM_NODE_TYPE_COMMENT                = 0x08,
LXB_DOM_NODE_TYPE_DOCUMENT               = 0x09,
LXB_DOM_NODE_TYPE_DOCUMENT_TYPE          = 0x0A,
LXB_DOM_NODE_TYPE_DOCUMENT_FRAGMENT      = 0x0B,
LXB_DOM_NODE_TYPE_NOTATION               = 0x0C, /* historical */
LXB_DOM_NODE_TYPE_LAST_ENTRY             = 0x0D
```

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| [lxb_dom_node_t](#lxb_dom_node_t)&nbsp;* | lxb_dom_node_destroy(lxb_dom_node_t \*node) |
| [lxb_dom_node_t](#lxb_dom_node_t) * | lxb_dom_node_destroy_deep(lxb_dom_node_t \*root) |
| const&nbsp;lxb_char_t&nbsp;* | lxb_dom_node_name(lxb_dom_node_t \*node, size_t \*len) |
| void | lxb_dom_node_insert_child(lxb_dom_node_t \*to, lxb_dom_node_t \*node) |
| void | lxb_dom_node_insert_before(lxb_dom_node_t \*to, lxb_dom_node_t \*node) |
| void | lxb_dom_node_insert_after(lxb_dom_node_t \*to, lxb_dom_node_t \*node) |
| void | lxb_dom_node_remove(lxb_dom_node_t \*node) |
| lxb_status_t | lxb_dom_node_replace_all(lxb_dom_node_t \*parent, lxb_dom_node_t \*node) |
| void | lxb_dom_node_simple_walk(lxb_dom_node_t \*root, lxb_dom_node_simple_walker_f walker_cb, void \*ctx) |
| lxb_char_t * | lxb_dom_node_text_content(lxb_dom_node_t \*node, size_t \*len) |
| lxb_status_t | lxb_dom_node_text_content_set(lxb_dom_node_t\*node, const lxb_char_t \*content, size_t len) |


#### lxb_dom_node_destroy

This function destroys the node and frees the memory.

```c-api-function
LXB_API lxb_dom_node_t *
lxb_dom_node_destroy(lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | node | Pointer to DOM node. Not `NULL`. |
| Return | lxb_dom_node_t * | `NULL` value. ||


#### lxb_dom_node_destroy_deep

This function destroys the node and all child nodes and frees the memory.

```c-api-function
LXB_API lxb_dom_node_t *
lxb_dom_node_destroy_deep(lxb_dom_node_t *root);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM node. Not `NULL`. |
| Return | lxb_dom_node_t * | `NULL` value. ||


#### lxb_dom_node_name

This function returns the name of the node.

```c-api-function
LXB_API const lxb_char_t *
lxb_dom_node_name(lxb_dom_node_t *node, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | node | Pointer to DOM node. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of name. |
| Return | const lxb_char_t * | Pointer to the name data, otherwise `NULL` value. ||


#### lxb_dom_node_insert_child

This function inserts a child node to the specified node. The node is inserted at the end.

```c-api-function
LXB_API void
lxb_dom_node_insert_child(lxb_dom_node_t *to, lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | to | Pointer to DOM node. Not `NULL`. Where to insert. |
| In | node | Pointer to DOM node. Not `NULL`. Whom to insert. |
| Return | void | Returns nothing. ||


#### lxb_dom_node_insert_before

This function inserts a node before the specified node.

```c-api-function
LXB_API void
lxb_dom_node_insert_before(lxb_dom_node_t *to, lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | to | Pointer to DOM node. Not `NULL`. Before whom. |
| In | node | Pointer to DOM node. Not `NULL`. Whom to insert. |
| Return | void | Returns nothing. ||


#### lxb_dom_node_insert_after

This function inserts a node after the specified node.

```c-api-function
LXB_API void
lxb_dom_node_insert_after(lxb_dom_node_t *to, lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | to | Pointer to DOM node. Not `NULL`. After whom. |
| In | node | Pointer to DOM node. Not `NULL`. Whom to insert. |
| Return | void | Returns nothing. ||


#### lxb_dom_node_remove

This function remove a node without freeing memory.

```c-api-function
LXB_API void
lxb_dom_node_remove(lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | node | Pointer to DOM node. Not `NULL`. |
| Return | void | Returns nothing. ||


#### lxb_dom_node_replace_all

This function destroy all child nodes, freeing memory, and then inserts the node.

```c-api-function
LXB_API lxb_status_t
lxb_dom_node_replace_all(lxb_dom_node_t *root, lxb_dom_node_t *node);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM node. Not `NULL`. |
| In | node | Pointer to DOM node. Not `NULL`. Whom to insert. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


#### lxb_dom_node_simple_walk

This function walk the tree and calls a callback function to each node.

```c-api-function
LXB_API void
lxb_dom_node_simple_walk(lxb_dom_node_t *root,
                         lxb_dom_node_simple_walker_f walker_cb, void *ctx);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | root | Pointer to DOM node. Not `NULL`. |
| In | walker_cb | Pointer to callback function. Not `NULL`. This function will be called on each element in the tree. |
| In | ctx | Pointer to user context. Can be `NULL`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||

Prototype for `lxb_dom_node_simple_walker_f`:
```C
typedef lexbor_action_t
(*lxb_dom_node_simple_walker_f)(lxb_dom_node_t *node, void *ctx);
```


#### lxb_dom_node_text_content

This function returns the text content of the specified node.

```c-api-function
LXB_API lxb_char_t *
lxb_dom_node_text_content(lxb_dom_node_t *node, size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | node | Pointer to DOM node. Not `NULL`. |
| Out | len | Pointer to length. Can be `NULL`. Length of content. |
| Return | const lxb_char_t * | Pointer to the content data, otherwise `NULL` value. ||


#### lxb_dom_node_text_content_set

This function sets the text content of the specified node.

```c-api-function
LXB_API lxb_status_t
lxb_dom_node_text_content_set(lxb_dom_node_t *node,
                              const lxb_char_t *content, size_t len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | node | Pointer to DOM node. Not `NULL`. |
| In | content | Pointer to content data. Not `NULL`. |
| In | len | Length of `content`. |
| Return | lxb_status_t | `LXB_STATUS_OK` if successful, otherwise error occurred. ||


### lxb_dom_processing_instruction_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/processing_instruction.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | ProcessingInstruction |
| Inherits: | lxb_dom_character_data_t |

#### Functions

| Return value [](#class-function-list-return) |  Name [](#class-function-list-name) |
|---:|---|
| const&nbsp;lxb_char_t&nbsp;* | [lxb_dom_processing_instruction_target](#lxb_dom_processing_instruction_target)(lxb_dom_processing_instruction_t \*pi, size_t \*len) |

#### lxb_dom_processing_instruction_target

This function returns target of processing instruction node.

```c-api-function
lxb_inline const lxb_char_t *
lxb_dom_processing_instruction_target(lxb_dom_processing_instruction_t *pi,
                                      size_t *len);
```

| Action [](#class-api-function-action) | Name [](#class-api-function-name) | Description [](#class-api-function-description) |
|---|---|---|
| In | pi | Pointer to DOM processing instruction node. Not `NULL`. |
| Out | len | Pointer to length of target. Can be `NULL`. |
| Return | const lxb_char_t * | Pointer to the target data, otherwise `NULL` value. ||


### lxb_dom_shadow_root_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/shadow_root.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | ShadowRoot |
| Inherits: | lxb_dom_document_fragment_t |

### lxb_dom_text_t

| [](#class-hide) | [](#class-hide) |
|---:|---|
| Header: [](#class-typedef-header) | `#include <lexbor/dom/interfaces/text.h>`|
| Since: | Lexbor HTML 0.1.0 |
| Spec name: | Text |
| Inherits: | lxb_dom_character_data_t |
