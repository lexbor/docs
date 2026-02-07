# Modules

```{toctree}
:hidden:
:maxdepth: 2

/modules/core
/modules/html
/modules/dom
/modules/css
/modules/selectors
/modules/encoding
/modules/url
/modules/unicode
```

The `lexbor` project is designed with a modular architecture, where each module can be built and used independently or as part of the complete engine. This approach provides flexibility — you can use only the components you need, keeping your application lightweight and focused.

## Modular Design Philosophy

Lexbor is built around the idea that you should use only what you need. Each module is designed to work independently, so you can include just the HTML parser without dragging in CSS parsing, or use the Encoding module on its own without any HTML dependencies.

This architecture offers several practical benefits:

- **Self-contained** — Each module has its own version and configuration, and can be built separately. You get clean separation without unnecessary coupling.
- **Standards-compliant** — Every module strictly implements WHATWG and W3C specifications. If a browser does it, lexbor does it the same way.
- **Flexible integration** — Use any combination of modules that fits your needs. The HTML parser works great on its own, or pair it with CSS and Selectors for more advanced use cases.

## Module Location

All modules are located in the `source/lexbor/` directory of the project. Each module has:

- A `base.h` file with version information and type definitions
- A `config.cmake` file for build configuration (most modules)
- Implementation files (`.c`) and headers (`.h`)

## Available Modules

### Production-Ready Modules

These modules are stable, fully tested, and ready for production use:

| Module | Version | Specification | Description |
|--------|---------|---------------|-------------|
| [Core](/modules/core/) | 2.7.0 | — | Base algorithms and memory management |
| [HTML](/modules/html/) | 2.8.0 | [WHATWG HTML](https://html.spec.whatwg.org/) | Full HTML parser |
| [DOM](/modules/dom/) | 2.0.0 | [WHATWG DOM](https://dom.spec.whatwg.org/) | DOM tree manipulation |
| [CSS](/modules/css/) | 1.4.0 | [CSS](https://www.w3.org/Style/CSS/) | CSS parser and CSS modules |
| [Selectors](/modules/selectors/) | 0.5.0 | [CSS Selectors Level 4](https://drafts.csswg.org/selectors-4/) | CSS selectors engine |
| [Encoding](/modules/encoding/) | 2.2.0 | [WHATWG Encoding](https://encoding.spec.whatwg.org/) | 40+ character encodings |
| [URL](/modules/url/) | 0.4.0 | [WHATWG URL](https://url.spec.whatwg.org/) | URL parsing and manipulation |
| [Unicode](/modules/unicode/) | 0.4.0 | [Unicode TR#15](https://www.unicode.org/reports/tr15/), [TR#46](https://unicode.org/reports/tr46/) | Normalization and IDNA |
| Punycode | — | [RFC 3492](https://www.rfc-editor.org/rfc/rfc3492.html) | Punycode encoding/decoding |

### Supporting Modules

These modules provide internal functionality and are typically used by other modules:

| Module | Description |
|--------|-------------|
| NS | Namespace handling (HTML, SVG, MathML, XLink, XML, XMLNS) |
| Tag | HTML and SVG tag definitions and lookup |
| Style | CSS Style event handling and integration. Combines HTML and CSS |
| Ports | Platform-specific implementations |
| Utils | Utility functions and helpers |

### Modules in Development

| Module | Status | Description |
|--------|--------|-------------|
| Layout | 🚧 In progress | CSS layout engine (currently at rendering tree stage) |
| Fonts | 🚧 Planned | Font parsing and text rendering |
| Engine | 🚧 Planned | Full browser engine integration |

## Module Versioning

Each module maintains its own version number. Versions follow semantic versioning:

- **Major** — breaking API changes
- **Minor** — new features, backward compatible
- **Patch** — bug fixes, backward compatible

```c
#include <lexbor/html/base.h>

printf("HTML module version: %s\n", LXB_HTML_VERSION_STRING);
printf("Core version: %s\n", LEXBOR_VERSION_STRING);
```

Or:

```c
printf("Core version: %d.%d.%d\n",
       LEXBOR_VERSION_MAJOR,
       LEXBOR_VERSION_MINOR,
       LEXBOR_VERSION_PATCH);
```
