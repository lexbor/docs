# HTML Parsing and Serialization Example

This example demonstrates how to create an HTML parser using the `lexbor` library,
parse simple HTML strings into document objects, and serialize those documents
back to a readable format. The code is found in the source file
[lexbor/html/parse.c](https://github.com/lexbor/lexbor/blob/master/examples/lexbor/html/parse.c).

## Code Overview

The program begins by including the necessary header files and defining the main
function, which is the entry point for execution. It declares several variables
that will be needed throughout the parsing process, including the status of the
parser, pointers to HTML document objects, and the HTML strings to be parsed.

## Initialization

First, the HTML parser is created with `lxb_html_parser_create()`, which
allocates memory for the parser. It is essential to check that the parser was
created successfully. The program initializes the parser with
`lxb_html_parser_init(parser)`, and again checks for successful initialization.
If there is a failure at either point, a failure message is printed, and the
process is terminated. This aspect of the code ensures that the parser is
correctly set up before proceeding further.

## Parsing HTML

Next, the program prepares two simple HTML snippets for parsing: `html_one` and
`html_two`. These strings represent basic HTML structures containing a `div`
with a `p` element. The lengths of these strings are calculated to facilitate
parsing. 

The parsing occurs with `lxb_html_parse(parser, html_one, html_one_len)`, which
attempts to parse the first HTML string and store the resulting document object
in `doc_one`. A similar approach is taken for `doc_two`. In both cases, it is
crucial to verify that the parsing was successful—if either document object is
`NULL`, the program reports a failure.

## Serialization

Once both documents are successfully created, the program proceeds to serialize
them. The method `lxb_html_serialize_pretty_tree_cb()` is called for each
document. This function is responsible for converting the document object back
into a structured HTML format, with an option for pretty printing. The first
argument converts the document into a DOM node interface, while the remaining
arguments provide options for serialization. Again, the program checks the
status to ensure serialization succeeded.

## Cleanup

After serialization, it is important to clean up resources. The program destroys
the parser and the HTML document objects with `lxb_html_parser_destroy()` and
`lxb_html_document_destroy()`, respectively. This step prevents memory leaks and
ensures that all allocated resources are properly released.

## Conclusion

This example is a clear demonstration of the workflow when utilizing the lexbor
library for HTML parsing and serialization. By handling initialization, parsing,
serialization, and cleanup, the program effectively showcases how to work with
HTML documents in a structured manner. The checks for status at each stage
ensure robustness, making it easier to identify issues during development.