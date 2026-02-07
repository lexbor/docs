# Roadmap

This section lists the most important modules involved in creating a browser
engine. The list will grow over time.

Specific list items appear in their respective sections (`DOM`, `HTML`, etc.) in
the order of their implementation.


## Legend

- ![Done][done]: There is no need to revisit this item; it is complete.

- ![In Progress][progress]: Continually in development but available for use.

- If no status is given, the work has not yet started.


[done]: img/done.svg
[progress]: img/in_progress.svg


## DOM

1. [DOM Interfaces](https://dom.spec.whatwg.org/#node-trees): ![In Progress][progress]
2. [DOM Events](https://dom.spec.whatwg.org/#events)


## HTML

1. [HTML Parser](https://html.spec.whatwg.org/multipage/parsing.html#parsing): ![Done][done]
2. [HTML Interfaces](https://html.spec.whatwg.org/multipage/semantics.html#semantics): ![In Progress][progress]
3. [Custom Elements](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-elements)
4. [Queuing a mutation record](https://dom.spec.whatwg.org/#queueing-a-mutation-record)


## CSS

1. [Syntax](https://drafts.csswg.org/css-syntax-3/):![Done][done]
2. [Grammar](https://drafts.csswg.org/css-values-4/#component-combinators): for generating CSS tests by grammars. ![Done][done]
3. [Namespaces](https://drafts.csswg.org/css-namespaces-3/): ![Done][done]
4. [Selectors](https://drafts.csswg.org/selectors-4/): ![Done][done]
5. [CSSOM](https://drafts.csswg.org/cssom-1/): ![In Progress][progress]
6. [Values](https://drafts.csswg.org/css-values-4/): ![In Progress][progress]
7. [Sizing](https://drafts.csswg.org/css-sizing-3/): ![In Progress][progress]
8. [Box](https://drafts.csswg.org/css-box-3/): ![In Progress][progress]
9. [Display](https://drafts.csswg.org/css-display-3/): ![In Progress][progress]
10. [Float](https://drafts.csswg.org/css-page-floats-3/): ![In Progress][progress]
11. [Font](https://drafts.csswg.org/css-fonts-3/): ![In Progress][progress]
12. [Text](https://drafts.csswg.org/css-text-3/): ![In Progress][progress]
13. [Position](https://drafts.csswg.org/css-position-3/): ![In Progress][progress]
14. [Color](https://drafts.csswg.org/css-color-4/): ![In Progress][progress]
15. [Flexbox](https://drafts.csswg.org/css-flexbox-1/): ![In Progress][progress]
16. [Background](https://drafts.csswg.org/css-backgrounds-3/): ![In Progress][progress]
17. [Content](https://drafts.csswg.org/css-content-3/)
18. [Overflow](https://drafts.csswg.org/css-overflow-3/): ![In Progress][progress]
19. [Media Queries](https://drafts.csswg.org/mediaqueries-4/): ![In Progress][progress]
20. [Page](https://drafts.csswg.org/css-page-3/)
21. [Variables](https://drafts.csswg.org/css-variables-1/)


## Fonts, OpenType

1. [Font/OpenType](https://learn.microsoft.com/en-us/typography/opentype/spec/)<br>
   1.1. [Parsing OpenType font files](https://learn.microsoft.com/en-us/typography/opentype/spec/otff)<br>
   1.2. Calculating font metrics for glyphs in HTML layout: `baseline`,
        `ascender`, `descender`, `line-gap`, `x-height`, `cap-height`,
        `width`, `height`


## Encodings

1. [Encoding](https://encoding.spec.whatwg.org/): ![Done][done]
2. [Prescanning a byte stream to determine its encoding](https://html.spec.whatwg.org/multipage/parsing.html#prescan-a-byte-stream-to-determine-its-encoding): ![Done][done]


## URL

1. [URL](https://url.spec.whatwg.org/): ![Done][done]<br>
   1.1. [Parsing](https://url.spec.whatwg.org/#url-parsing): ![Done][done]<br>
   1.2. [Punycode](https://www.rfc-editor.org/info/rfc3492): ![Done][done]


## Unicode

1. [http://www.unicode.org/](http://www.unicode.org/): ![Done][done]<br>
   1.1. [Normalization forms](https://www.unicode.org/reports/tr15/): ![Done][done]<br>
   1.2. [Unicode IDNA Compatibility Processing](http://www.unicode.org/reports/tr46/): ![Done][done]


## Layout

1. Building a rendering tree: we're at this stage right now.
