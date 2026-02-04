# Amalgamation

Lexbor can be built as a **single-header/single-source amalgamation** for easy integration into your project without managing multiple files or dependencies.

The amalgamation combines all selected modules and their dependencies into one `.h` file, making it simple to drop into any C/C++ project.

## Generate Amalgamation

Use the `single.pl` script from the repository root to generate an amalgamated version:

```bash
# Generate amalgamation with all modules
perl single.pl --all > lexbor_single.h

# Generate amalgamation for specific modules (dependencies are included automatically)
perl single.pl html css > lexbor_html_css_single.h

# Generate with exported symbols (for dynamic linking)
perl single.pl --with-export-symbols html > lexbor_html_single.h

# Use a different port (default: posix)
perl single.pl --port=windows_nt html > lexbor_html_single.h
```

## Available Options

### Basic Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |
| `--all` | Include all modules if no modules specified |
| `--port=<port>` | Specify platform port to use (default: `posix`) |
| `--with-export-symbols` | Export symbols (for building shared libraries) |

### Information Options

| Option | Description |
|--------|-------------|
| `--modules` | Print all available modules |
| `--dependencies` | Print detailed dependencies of specified modules |
| `--graph` | Print dependency graph as a tree |
| `--stats` | Print statistics about module dependencies |
| `--reverse-deps` | Print reverse dependencies (which modules depend on specified ones) |
| `--size-info` | Print size information (lines of code, file counts) |
| `--minimal-deps` | Show minimal set of dependencies |
| `--versions` | Print version information for modules |
| `--version` | Print Lexbor version |

### Validation Options

| Option | Description |
|--------|-------------|
| `--check-cycles` | Check for cyclic dependencies |
| `--validate` | Validate that all dependencies exist |
| `--compare=mod1,mod2` | Compare dependencies between two modules |

### Export Options

| Option | Description |
|--------|-------------|
| `--dot-graph` | Export dependency graph in DOT format (Graphviz) |
| `--export-json` | Export dependency structure to JSON |
| `--export-yaml` | Export dependency structure to YAML |

## Usage Example

Generate the amalgamation file with the HTML module:

```bash
perl single.pl html > lexbor_html_single.h
```

Then include the generated file in your project:

```C
#include "lexbor_html_single.h"

int
main(void)
{
    lxb_html_document_t *document;
    lxb_status_t status;

    const lxb_char_t html[] = "<div>Hello!</div>";

    document = lxb_html_document_create();
    if (document == NULL) {
        return EXIT_FAILURE;
    }

    status = lxb_html_document_parse(document, (const lxb_char_t *) html,
                                     sizeof(html) - 1);
    if (status != LXB_STATUS_OK) {
        return EXIT_FAILURE;
    }

    lxb_html_document_destroy(document);

    return EXIT_SUCCESS;
}
```

Compile without any additional dependencies:

```bash
gcc -o myapp myapp.c
```
