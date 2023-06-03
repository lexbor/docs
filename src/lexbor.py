
import copy, re
import mistune
from mistune import Renderer, InlineGrammar, InlineLexer

class DocsRender(Renderer):
    link_rel_reg = re.compile("^(:?[a-zA-Z]+:|\/|#)")
    link_to_class = re.compile('\s*<a\s+href="\s*#class-([^"]+)"></a>\s*$')

    def clean_headers(self):
        self.headers = []

    def table_cell(self, content, **flags):
        res = []
        args = []
        gtr = self.link_to_class.search(content)

        if gtr != None:
            class_arg = ' class="%s"' % gtr.group(1)
        else:
            class_arg = ''
    
        content = self.link_to_class.sub('', content)

        if flags['align'] != None:
            args.append(' style="text-align: %s"' % flags['align'])

        if flags['header'] == True:
            res.append('<th%s>%s</th>' % (class_arg, content))
        else:
            res.append('<td%s' % class_arg)
            res.append(''.join(args))
            res.append('>%s</td>' % content)

        return ''.join(res)

    def header(self, text, level, raw):
        name = name_convert("%s" % (text))

        if level >= 1 and level <= 6:
            self.headers.append([level, name, text])

        return '<h%s>%s<a class="anchor" aria-hidden="true" id="%s" href="#%s">#</a></h%s>' % (level, text, name, name, level)

    def image(self, src, title, alt_text):
        rg = self.link_rel_reg.match(src)

        if rg == None:
            src = self.conv.make_url(src)

        return super().image(src, title, alt_text)

    def link(self, link, title, content):
        rg = self.link_rel_reg.match(link)

        if rg == None:
            link = self.conv.make_url(link)

        return super().link(link, title, content)

    def block_code(self, code, lang):
        ch = CHigh()
        data = ch.lines(code)
        text = ch.convert(code, data)

        if lang == None:
            return '\n<pre class="code highlight"><code>%s</code></pre>\n' % \
                mistune.escape(code)

        if lang.lower() == 'c-api-function':
            return '\n<pre class="code highlight"><code class="api-function">%s</code></pre>\n' % \
                text

        elif lang.lower() == 'c-api-enum':
            return '\n<pre class="code highlight"><code class="api-enum">%s</code></pre>\n' % \
               text

        elif lang.lower() == 'c-api-struct':
            return '\n<pre class="code highlight"><code class="api-struct">%s</code></pre>\n' % \
                text

        elif lang.lower() == 'c':
            return '\n<pre class="code highlight"><code>%s</code></pre>\n' % \
                text

        return '\n<pre class="code"><code>%s</code></pre>\n' % \
            mistune.escape(code)

def name_convert(name):
    return re.sub(r"[^a-zA-Z0-9_]", "_", name).lower()

class CHigh():
    functions = re.compile("([a-zA-Z0-9_]+)\s*\(([^\)]*?)\)", re.MULTILINE)
    args_var = re.compile("([a-zA-Z0-9_&\s]+)", re.MULTILINE)
    text = re.compile('("(?:[^"]|\\.)*")', re.MULTILINE)
    numbers = re.compile('([0-9]+|\.[0-9]+|[0-9]+\.[0-9]+)')
    def_var = re.compile("([a-zA-Z0-9_][a-zA-Z0-9_\s]+)(?:\s+\**|\**\s+|\*+|\s+)([a-zA-Z0-9_\[\]]+)\s*(?:;|,|=[^=])", re.MULTILINE)
    def_functions = re.compile("\s*([a-zA-Z0-9_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z0-9_]+)\s*\(([^\)]*?)\)", re.MULTILINE)
    def_functions_args = re.compile("([a-zA-Z0-9_][a-zA-Z0-9\]\[_*&\s]+)(?:,|$)", re.MULTILINE)
    def_type = re.compile("([a-zA-Z0-9_\s]+)(?:\s+\**|\**\s+|\*+|\s+)([a-zA-Z0-9_]+)", re.MULTILINE)
    comment = re.compile("(/\*([^*]|\*+[^/])*\*+/)", re.MULTILINE)
    mpath = re.compile("(?:[a-zA-Z0-9_])(?:\s*(?:->|\.)\s*([a-zA-Z0-9_]+))*", re.MULTILINE)

    types_list = set((
        'size_t', 'ssize_t', 'off_t', 'wchar_t', 'ptrdiff_t', 'sig_atomic_t', 'fpos_t',
        'clock_t', 'time_t', 'va_list', 'jmp_buf', 'FILE', 'DIR', 'div_t', 'ldiv_t',
        'mbstate_t', 'wctrans_t', 'wint_t', 'wctype_t',
        '_Bool', '_Complex', 'int8_t', 'int16_t', 'int32_t', 'int64_t', 'uint8_t',
        'uint16_t', 'uint32_t', 'uint64_t', 'int_least8_t', 'int_least16_t',
        'int_least32_t', 'int_least64_t', 'uint_least8_t', 'uint_least16_t',
        'uint_least32_t', 'uint_least64_t', 'int_fast8_t', 'int_fast16_t', 'int_fast32_t',
        'int_fast64_t', 'uint_fast8_t', 'uint_fast16_t', 'uint_fast32_t', 'uint_fast64_t',
        'intptr_t', 'uintptr_t', 'intmax_t', 'uintmax_t',
        'clockid_t', 'cpu_set_t', 'cpumask_t', 'dev_t', 'gid_t', 'id_t', 'ino_t', 'key_t',
        'mode_t', 'nfds_t', 'pid_t', 'rlim_t', 'sig_t', 'sighandler_t', 'siginfo_t',
        'sigset_t', 'sigval_t', 'socklen_t', 'timer_t', 'uid_t'))

    std_types_list = set(('bool', 'int', 'long', 'float', 'short', 'double',
        'char', 'unsigned', 'signed', 'void'))

    std_list = set(('asm', 'auto', 'break', 'case', 'const', 'continue',
        'default', 'do', 'else', 'enum', 'extern', 'for', 'goto',
        'if', 'register', 'restricted', 'return', 'sizeof',
        'static', 'struct', 'switch', 'typedef', 'union',
        'volatile', 'while', 'inline', '_inline', '__inline', 'naked', 
        'restrict', 'thread', 'typename'))

    std_list_bn = set(('true', 'false', 'NULL'))

    std_macros_list = set(('EXIT_SUCCESS', 'EXIT_FAILURE'))

    def __init__(self):
        self.types = re.compile('(^|<|>|[^\S_])(%s)($|<|>|[^\S_])' % '|'.join(self.types_list))
        self.std_types = re.compile('(^|<|>|[^\S_])(%s)($|<|>|[^\S_])' % '|'.join(self.std_types_list))
        self.std = re.compile('(^|<|>|[^\S_])(%s)($|<|>|[^\S_])' % '|'.join(self.std_list))
        self.std_bn = re.compile('(^|<|>|[^\S_])(%s)($|<|>|[^\S_])' % '|'.join(self.std_list_bn))
        self.std_macros = re.compile('(^|<|>|[^\S_])(%s)($|<|>|[^\S_])' % '|'.join(self.std_macros_list))

    def make(self, code):
        pass

    def append(self, name, start, stop, result):
        if start not in result['start']:
            result['start'][start] = {}

        if name not in result['start'][start]:
            result['start'][start][name] = {}

        if stop not in result['stop']:
            result['stop'][stop] = {}

        if name not in result['stop'][stop]:
            result['stop'][stop][name] = start

    def lines(self, code, offset = 0):
        result = {'start': {}, 'stop': {}}

        for match in self.text.finditer(code):
            self.append('text', match.span(1)[0] + offset, match.span(1)[1] + offset, result)

        for match in self.def_functions.finditer(code):
            self.append('def_function_type', match.span(1)[0] + offset, match.span(1)[1] + offset, result)
            self.append('def_function_name', match.span(2)[0] + offset, match.span(2)[1] + offset, result)

            self.parse_args(match.group(3), result, match.span(3)[0] + offset)

        for match in self.functions.finditer(code):
            self.append('function_name', match.span(1)[0] + offset, match.span(1)[1] + offset, result)

            if match.group(1).lower() == 'if':
                self.lines(match.group(2), match.span(2)[0] + offset)
            else:
                self.parse_args(match.group(2), result, match.span(2)[0] + offset)

        for match in self.def_var.finditer(code):
            self.append('def_type', match.span(1)[0] + offset, match.span(1)[1] + offset, result)
            self.append('var', match.span(2)[0] + offset, match.span(2)[1] + offset, result)

        for match in self.numbers.finditer(code):
            self.append('number', match.span(1)[0] + offset, match.span(1)[1] + offset, result)

        for match in self.comment.finditer(code):
            self.append('comment', match.span(1)[0] + offset, match.span(1)[1] + offset, result)

        for match in self.mpath.finditer(code):
            self.append('mpath', match.span(1)[0] + offset, match.span(1)[1] + offset, result)

        return result

    def parse_args(self, args_line, result, offset):
        for match in self.def_functions_args.finditer(args_line):
            arg = self.def_type.match(match.group(1))

            if arg != None:
                self.append('def_type', arg.span(1)[0] + match.span(1)[0] + offset, arg.span(1)[1] + match.span(1)[0] + offset, result)
                self.append('var', arg.span(2)[0] + match.span(1)[0] + offset, arg.span(2)[1] + match.span(1)[0] + offset, result)
            else:
                arg = self.args_var.match(match.group(1))

                if arg != None:
                    self.append('var', arg.span(1)[0] + match.span(1)[0] + offset, arg.span(1)[1] + match.span(1)[0] + offset, result)

    def ns_types(self, text):
        text = self.types.sub('\\1<span class="type">\\2</span>\\3', text)
        text = self.std_types.sub('\\1<span class="std-type">\\2</span>\\3', text)
        text = self.std.sub('\\1<span class="std">\\2</span>\\3', text)
        text = self.std_bn.sub('\\1<span class="std-bn">\\2</span>\\3', text)
        text = self.std_macros.sub('\\1<span class="std-macros">\\2</span>\\3', text)

        return text

    def convert(self, code, data):
        result = []

        for idx in range(0, len(code)):
            if idx in data['start']:
                if 'text'in data['start'][idx]:
                    result.append('<span class="text">')
                elif 'comment'in data['start'][idx]:
                    result.append('<span class="comment">')
                elif 'number'in data['start'][idx]:
                    result.append('<span class="number">')
                elif 'def_function_type'in data['start'][idx]:
                    result.append('<span class="defftype">')
                elif 'def_function_name'in data['start'][idx]:
                    result.append('<span class="deffname">')
                elif 'def_type'in data['start'][idx]:
                    result.append('<span class="deftype">')
                elif 'function_name'in data['start'][idx]:
                    result.append('<span class="ffname">')
                elif 'var'in data['start'][idx]:
                    result.append('<span class="var">')
                elif 'mpath'in data['start'][idx]:
                    result.append('<span class="mpath">')

            if idx in data['stop']:
                result.append('</span>')

            if code[idx] == '<':
                result.append('&lt;')
            elif code[idx] == '&':
                result.append('&#38;')
            else:
                result.append(code[idx])

        return self.ns_types(''.join(result))

if __name__ == "__main__":
    code = """#include <lexbor/html/parser.h>

int
main(int argc, const char *argv[])
{
    lxb_status_t status;
    const lxb_char_t *tag_name;
    lxb_html_document_t *document;

    static const lxb_char_t html[] = "<div>Work fine!</div>";
    size_t html_len = sizeof(html) - 1;

    document = lxb_html_document_create();
    if (document == NULL) {
        exit(EXIT_FAILURE);
    }

    status = lxb_html_document_parse(document, html, html_len);
    if (status != LXB_STATUS_OK) {
        exit(EXIT_FAILURE);
    }

    tag_name = lxb_tag_name_by_id(lxb_html_document_tag_heap(document),
                                  lxb_dom_interface_node(document->body)->tag_id, NULL);

    printf("Element tag name: %s\n", tag_name);

    lxb_html_document_destroy(document);

    return EXIT_SUCCESS;
}
"""

    ch = CHigh()
    data = ch.lines(code)
    text = ch.convert(code, data)

    print(text)
