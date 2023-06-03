[name]: Roadmap
[theme]: document.html

## Roadmap

This section describes the necessary modules for creating a browser engine. Here not everything is listed, only the main one. Over time, the section will be replenished.

Lists are compiled in order of implementation, excluding the main headings: DOM, HTML, CSS… order — as necessary.

### DOM

1. [DOM Interfaces](https://dom.spec.whatwg.org/#node-trees) ![In progress][progress]
2. [DOM Events](https://dom.spec.whatwg.org/#events)


### HTML

1. [HTML Parser](https://html.spec.whatwg.org/multipage/parsing.html#parsing) ![Done][done]
2. [HTML Interfaces](https://html.spec.whatwg.org/multipage/semantics.html#semantics) ![In progress][progress]
3. [Custom Elements](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-elements)
4. [Queuing a mutation record](https://dom.spec.whatwg.org/#queueing-a-mutation-record)


### CSS

1. [Syntax](https://drafts.csswg.org/css-syntax-3/) ![Done][done]
2. [Grammar](https://drafts.csswg.org/css-values-4/#component-combinators) for generate compact and fast code for parsing CSS properties
3. [Namespaces](https://drafts.csswg.org/css-namespaces-3/)
4. [Selectors](https://drafts.csswg.org/selectors-4/) ![Done][done]
5. [CSSOM](https://drafts.csswg.org/cssom-1/)
6. [Values](https://drafts.csswg.org/css-values-4/)
7. [Sizing](https://drafts.csswg.org/css-sizing-3/)
8. [Box](https://drafts.csswg.org/css-box-3/)
9. [Display](https://drafts.csswg.org/css-display-3/)
10. [Float](https://drafts.csswg.org/css-page-floats-3/)
11. [Font](https://drafts.csswg.org/css-fonts-3/)
12. [Text](https://drafts.csswg.org/css-text-3/)
13. [Position](https://drafts.csswg.org/css-position-3/)
14. [Color](https://drafts.csswg.org/css-color-4/)
15. [Flexbox](https://drafts.csswg.org/css-flexbox-1/)
16. [Background](https://drafts.csswg.org/css-backgrounds-3/)
17. [Content](https://drafts.csswg.org/css-content-3/)
18. [Overflow](https://drafts.csswg.org/css-overflow-3/)
19. [Media Queries](https://drafts.csswg.org/mediaqueries-4/)
20. [Page](https://drafts.csswg.org/css-page-3/)
21. [Variables](https://drafts.csswg.org/css-variables-1/)


### Font/OpenType

1. [Font/OpenType](https://docs.microsoft.com/ru-ru/typography/opentype/spec/)
    1. [Parsing OpenType Font File](https://docs.microsoft.com/ru-ru/typography/opentype/spec/otff)
    2. Calculating font metrics for glyph for HTML layout: baseline, ascender, descender, line-gap, x-height, cap-height, width, height


### Encoding

1. [Encoding](https://encoding.spec.whatwg.org/) ![Done][done]
2. [Prescan a byte stream to determine its encoding](https://html.spec.whatwg.org/multipage/parsing.html#prescan-a-byte-stream-to-determine-its-encoding) ![Done][done]


### URL

1. [URL](https://url.spec.whatwg.org/)
    1. [Parsing](https://url.spec.whatwg.org/#url-parsing)
    2. [Punycode](http://www.unicode.org/reports/tr46/)


### Unicode

1. [http://www.unicode.org/](http://www.unicode.org/)
    1. [Normalization Forms](https://www.unicode.org/reports/tr15/)


### Layout

1. Creating a rendering tree

This section will be described in more detail in the future.


<br>
************


![Done][done] Done. There is no need to return to this.
![In progress][progress] Always in developing state. Can be used.


[done]: img/done.svg
[progress]: img/in_progress.svg
