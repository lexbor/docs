# Tutorials

```{toctree}
:hidden:
:maxdepth: 1

extract-links
extract-links-css-selectors
filter-tokenizer-callbacks
```

Step-by-step tutorials to help you solve practical tasks with `lexbor`. Each
tutorial includes a complete, working code example that you can compile and run.

## Available Tutorials

### [Extract All Links and Resolve URLs](extract-links.md)

Parse an HTML document, find all `<a>` elements using
`lxb_dom_elements_by_tag_name()`, extract their `href` attributes, and resolve
relative URLs into absolute ones using the URL module.

**Modules used:** HTML, DOM, URL

### [Extract All Links Using CSS Selectors](extract-links-css-selectors.md)

Same task as above, but uses CSS selectors (`a[href]`) instead of DOM lookup.
Shows how to combine the CSS parser, Selectors engine, and URL module to find
and process links with precise filtering.

**Modules used:** HTML, CSS, Selectors, URL

### [Intercept Tokenizer Callbacks Before Tree Building](filter-tokenizer-callbacks.md)

Intercept the tokenizer callback before tokens reach the tree builder. Demonstrates
how to inspect, filter, and skip tokens during parsing — for example, removing
whitespace-only text nodes from the resulting DOM tree.

**Modules used:** HTML
