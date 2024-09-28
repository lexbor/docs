# HTML Document Title Example

This article will explain the functionality of the HTML document title example implemented in the source code found in [lexbor/html/document_title.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/document_title.c). The purpose of this code is to demonstrate how to parse an HTML string, retrieve its title, modify the title, and then display the resulting HTML document structure using the Lexbor library.

## Code Breakdown

### Initialization

The code begins with the inclusion of the required headers and the setup of the `main` function, which is the entry point of the program. Here, the main task involves creating an HTML document instance and specifying the necessary variables.

```c
lxb_html_document_t *document;
```
This line declares a pointer to an `lxb_html_document_t` structure which represents the HTML document being created. The succeeding lines define variables for storing the title and its length.

### Creating the Document

The next significant step is the initialization of the HTML document:

```c
document = lxb_html_document_create();
if (document == NULL) {
    FAILED("Failed to create HTML Document");
}
```
In this snippet, the `lxb_html_document_create` function is called to allocate memory for a new HTML document. If the document fails to create, the program invokes the `FAILED` macro to signal an error.

### Parsing HTML

After successfully creating the document, the code proceeds to parse the HTML string:

```c
status = lxb_html_document_parse(document, html, html_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to parse HTML");
}
```
Here, the HTML content defined in the `html` array—specifically the title tag which contains extra spaces—is parsed. The variable `status` checks if the operation was successful. If not, the program exits with an error message.

### Retrieving the Title

Once the document is parsed, the code retrieves the title of the document:

```c
title = lxb_html_document_title(document, &title_len);
```
This function call extracts the title text from the document, storing it into the `title` variable. The length of the title is also provided through the `title_len` reference. The subsequent `if` statement checks whether the title exists, printing the title or an empty message accordingly.

### Obtaining the Raw Title

The following code retrieves the raw title, which includes the original formatting (e.g., extra spaces):

```c
title = lxb_html_document_title_raw(document, &title_len);
```
Much like the previous title retrieval, this extracts the unformatted title, allowing a comparison between the cleaned and raw titles.

### Modifying the Title

The code then demonstrates how to change the document's title:

```c
status = lxb_html_document_title_set(document, new_title, new_title_len);
if (status != LXB_STATUS_OK) {
    FAILED("Failed to change HTML title");
}
```
By invoking `lxb_html_document_title_set`, the title is altered to a new value defined by the `new_title` variable. An error check follows to ensure the title change was successful.

### Displaying the New Title and HTML Structure

The final steps involve displaying the updated title and the entire HTML document structure after modification:

```c
title = lxb_html_document_title(document, &title_len);
```
This repeats the earlier title retrieval process to print the new title. Finally, the code prints the altered HTML structure to show the impact of the title change.

### Cleanup

Lastly, the document is destroyed to free the allocated memory, which is crucial for preventing memory leaks:

```c
lxb_html_document_destroy(document);
```

## Conclusion

This example illustrates the basic operations for handling HTML document titles using the Lexbor library, including parsing content, accessing and modifying the title, and ensuring proper resource management. The structure of the code is straightforward, aiming to provide a clear understanding of each step involved in managing an HTML document's title. As developers familiarize themselves with the functionalities offered by Lexbor, they will be better equipped to manipulate HTML content programmatically.