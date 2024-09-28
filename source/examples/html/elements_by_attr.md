# Retrieving Elements by Attribute Example

This article will explain the functionality and implementation of the code found in **lexbor/html/elements_by_attr.c**, which demonstrates how to retrieve DOM elements based on specific attributes using the lexbor library.

## Overview

The provided code showcases how to extract elements from an HTML document based on their attributes. It specifically focuses on obtaining elements by 'class' and 'href' attributes, employing methods that match, search from the beginning, and search from the end of the attribute values.

## Code Breakdown

### Including Necessary Headers

The code starts with including essential headers:

```c
#include "base.h"
#include <lexbor/dom/dom.h>
```

The `base.h` header seems to contain definitions and functions crucial for this example, while `lexbor/dom/dom.h` provides the necessary DOM manipulations for lexbor.

### Print Collection Function

The function `print_collection_elements` is defined to handle the output of the retrieved elements:

```c
static void print_collection_elements(lxb_dom_collection_t *collection)
```

This function loops through the elements within the provided collection using its length and utilizes the `serialize_node` function to print each element. After processing, it ensures to clean up the collection to prevent memory leaks.

### Main Function Execution

The `main` function is where the key processes occur:

```c
int main(int argc, const char *argv[])
```

#### Parsing HTML

The HTML content is defined statically:

```c
const lxb_char_t html[] = "<div class=\"best blue some\"><span></div>"
"<div class=\"red pref_best grep\"></div>"
"<div class=\"green best grep\"></div>"
"<a href=\"http://some.link/\">ref</a>"
"<div class=\"red c++ best\"></div>";
```

This string contains several `<div>` and `<a>` tags with diverse class attributes and an `href`. The length of this HTML string is then calculated.

#### Creating Document and Collection

Following that, the HTML is parsed, creating a document object:

```c
document = parse(html, html_szie);
```

Next, a collection object is created that will hold the elements found based on the attribute queries:

```c
collection = lxb_dom_collection_make(&document->dom_document, 128);
```

A check is performed to ensure that the collection was created successfully.

#### Searching Elements by Attributes

The program performs several searches:

1. **Full Match:**
   Using `lxb_dom_elements_by_attr`, it searches for elements with the exact class `red c++ best`:

   ```c
   status = lxb_dom_elements_by_attr(body, collection,
                                     (const lxb_char_t *) "class", 5,
                                     (const lxb_char_t *) "red c++ best", 12,
                                     true);
   ```

   If the search is successful, the found elements are printed.

2. **From Beginning:**
   The code retrieves elements with an `href` that starts with `http`:

   ```c
   status = lxb_dom_elements_by_attr_begin(body, collection,
                                           (const lxb_char_t *) "href", 4,
                                           (const lxb_char_t *) "http", 4,
                                           true);
   ```

3. **From End:**
   This search targets elements with classes ending in `grep`:

   ```c
   status = lxb_dom_elements_by_attr_end(body, collection,
                                         (const lxb_char_t *) "class", 5,
                                         (const lxb_char_t *) "grep", 4,
                                         true);
   ```

4. **Contain:**
   Finally, it looks for elements where the class contains the substring `c++ b`:

   ```c
   status = lxb_dom_elements_by_attr_contain(body, collection,
                                             (const lxb_char_t *) "class", 5,
                                             (const lxb_char_t *) "c++ b", 5,
                                             true);
   ```

Each of these searches utilizes the collection to retrieve relevant elements, printing them as they are found.

#### Cleanup

After the searches, cleanup processes are executed to free the allocated resources:

```c
lxb_dom_collection_destroy(collection, true);
lxb_html_document_destroy(document);
```

This is critical for maintaining memory hygiene in C programs.

## Conclusion

This code snippet demonstrates how to efficiently query and manipulate DOM elements in an HTML document using the lexbor library. By utilizing various search strategies based on attributes, developers can effectively streamline their DOM interactions, showcasing the flexibility and power of the lexbor library for handling HTML content.