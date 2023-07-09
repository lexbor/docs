[name]: Roadmap
[theme]: document.html

## Roadmap

This section lists the most important modules involved in creating a browser
engine.  The list will grow over time.

Specific list items appear in their respective sections (`DOM`, `HTML`, etc.)
in order of their implementation.

### Legend

* ![Done][done]: There is no need to return to this item.  Done is done.

* ![In Progress][progress]: Continually in development; can already be used.

* If status is not given, the work hasn't started yet.

[done]: img/done.svg
[progress]: img/in_progress.svg


### DOM

1. [DOM Interfaces](https://dom.spec.whatwg.org/#node-trees):
   ![In Progress][progress]
2. [DOM Events](https://dom.spec.whatwg.org/#events)


### HTML

1. [HTML Parser](https://html.spec.whatwg.org/multipage/parsing.html#parsing):
   ![Done][done]
2. [HTML Interfaces](https://html.spec.whatwg.org/multipage/semantics.html#semantics):
   ![In Progress][progress]
3. [Custom Elements](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-elements)
4. [Queuing a mutation record](https://dom.spec.whatwg.org/#queueing-a-mutation-record)


### CSS

1. [Syntax](https://drafts.csswg.org/css-syntax-3/):
   ![Done][done]

2. [Grammar](https://drafts.csswg.org/css-values-4/#component-combinators):
   Need compact and fast CSS property parsing code

3. [Namespaces](https://drafts.csswg.org/css-namespaces-3/)

4. [Selectors](https://drafts.csswg.org/selectors-4/):
   ![Done][done]

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


### Fonts, OpenType

1. [Font/OpenType](https://docs.microsoft.com/ru-ru/typography/opentype/spec/)
   1.1. [Parsing OpenType font files](https://docs.microsoft.com/ru-ru/typography/opentype/spec/otff)
   1.2. Calculating font metrics for glyphs in HTML layout: `baseline`,
        `ascender`, `descender`, `line-gap`, `x-height`, `cap-height`,
        `width`, `height`


### Encodings

1. [Encoding](https://encoding.spec.whatwg.org/):
   ![Done][done]

2. [Prescanning a byte stream to determine its encoding](https://html.spec.whatwg.org/multipage/parsing.html#prescan-a-byte-stream-to-determine-its-encoding):
   ![Done][done]


### URL

1. [URL](https://url.spec.whatwg.org/)
   1.1. [Parsing](https://url.spec.whatwg.org/#url-parsing)

   1.2. [Punycode](http://www.unicode.org/reports/tr46/)


### Unicode

1. [http://www.unicode.org/](http://www.unicode.org/)

   1.1. [Normalization forms](https://www.unicode.org/reports/tr15/)


### Layout

1. Building a rendering tree
