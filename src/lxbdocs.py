
import os
import sys
import re
from shutil import copyfile, rmtree

from jinja2 import Environment, FileSystemLoader
import mistune
import lexbor
import time

class Docs:
    nav_begin = 1

    def __init__(self, source_path, build_to, theme_path, module_name = None, out_file_type = 'html'):
        if '--url-with-ext' in sys.argv:
            self.url_with_ext = True
        else:
            self.url_with_ext = False

        if '--release' in sys.argv:
            self.is_release = True
        else:
            self.is_release = False

        self.default_theme_name = "main.html"
        self.extension = out_file_type

        self.source_path = os.path.normpath(source_path)
        self.build_path = os.path.normpath(build_to)
        self.theme_path = os.path.normpath(theme_path)

        sys.path.insert(0, theme_path)

        if module_name != None:
            module = __import__(module_name)
            class_ = getattr(module, "Theme")
            self.module = class_
        else:
            self.module = None

        self.markdown_render = lexbor.DocsRender(escape=False)
        self.markdown_render.conv = self

        self.markdown = mistune.Markdown(renderer = self.markdown_render)

        self.jinja2_env = Environment(
            loader = FileSystemLoader(theme_path, encoding='utf-8')
        )

    def make(self):
        rmtree(self.build_path, ignore_errors = True)
        os.makedirs(self.build_path)

        self.make_data_struct()
        self.build_create_dirs()
        self.build_create_files()

    def make_data_struct(self):
        dirs = []
        files = []
        maps = {}
        root_path = self.source_path
        theme_path = self.theme_path

        rel_path = re.compile("^%s/(.+)" % root_path)

        for root, subdirs, subfiles in os.walk(root_path):
            subfiles = [f for f in subfiles if not f[0] == '.' and not f[0] == '_']
            subdirs[:] = [d for d in subdirs if not d[0] == '.' and not d[0] == '_']

            for sdir in subdirs:
                ret = rel_path.match("%s/%s" % (root, sdir))
                dirs.append(ret.group(1))

            for sfile in subfiles:
                ret = rel_path.match("%s/%s" % (root, sfile))
                files.append(ret.group(1))

                extension = os.path.splitext(files[-1])[1]

                if extension.lower() == '.md':
                    maps[ files[-1][:-3] ] = self.load_md_params(files[-1])

        self.dirs = dirs
        self.files = files
        self.maps = maps

        files = []
        rel_path = re.compile("^%s/(.+)" % theme_path)

        for root, subdirs, subfiles in os.walk(theme_path):
            subfiles = [f for f in subfiles if not f[0] == '.' and not f[0] == '_']
            subdirs[:] = [d for d in subdirs if not d[0] == '.' and not d[0] == '_']

            for sfile in subfiles:
                ret = rel_path.match("%s/%s" % (root, sfile))
                files.append(ret.group(1))

        self.themes = files

    def load_md_params(self, file_path):
        params = {}

        src_full_path = "%s/%s" % (self.source_path, file_path)
        pr_w = re.compile("^\[([^\]]+)\]:\s*<>\s*[\"']([^\)]+)[\"']")
        pr_a = re.compile("^\[([^\]]+)\]:\s*([^\s]+)")
        fh = open(src_full_path)

        for line in fh:
            ret_w = pr_w.match(line)
            ret_a = pr_a.match(line)

            if ret_w != None:
                params[ret_w.group(1)] = ret_w.group(2)
                continue

            if ret_a != None:
                params[ret_a.group(1)] = ret_a.group(2)
                continue

            break

        fh.close()

        return params

    def build_create_files(self):
        maps = self.maps

        for file_path in self.files:
            src_full_path = "%s/%s" % (self.source_path, file_path)

            extension = os.path.splitext(src_full_path)[1]
            build_full_path = "%s/%s" % (self.build_path, file_path)

            if extension.lower() != '.md':
                copyfile(src_full_path, build_full_path)
                continue

            params = maps[file_path[:-3]]
            fh = open(src_full_path)

            if 'theme' in params:
                md = self.convert(file_path, fh.read(), params['theme'])
            else:
                md = self.convert(file_path, fh.read(), self.default_theme_name)

            fh.close()

            build_full_path = os.path.splitext(build_full_path)[0]
            build_full_path = "%s.%s" % (build_full_path, self.extension)

            fh = open(build_full_path, 'w')
            md = fh.write(md)
            fh.close()

    def build_create_dirs(self):
        if not os.path.exists(self.build_path):
            os.makedirs(self.build_path)

        for directory in self.dirs:
            full_path = "%s/%s" % (self.build_path, directory)

            if not os.path.exists(full_path):
                os.makedirs(full_path)

    def convert(self, file_path, md, theme_path):
        self.markdown_render.clean_headers()
        self.markdown_render.project_title = lexbor.name_convert(file_path)

        params = self.maps[file_path[:-3]]
        refs_max = int(params['refs_deep_max']) + 1 if 'refs_deep_max' in params else 4
        main_class = params['main_class'] if 'main_class' in params else ''
        md_html = self.markdown(md)
        refs_html = self.create_refs(1, refs_max)
        template = self.jinja2_env.get_template(theme_path)

        args = {
            'conv': self,
            'body': md_html,
            'refs': refs_html,
            'nav': self.create_nav(file_path),
            'title': self.create_title(file_path),
            'navigation': None,
            'module': self.module,
            'src_path': file_path,
            'time': time.time(),
            'main_class': main_class
        }

        if self.module != None:
            args = self.module.render(self, file_path, theme_path, args)

        return template.render(**args)

    def create_title(self, file_path):
        params = self.maps[file_path[:-3]]

        if 'title' in params:
            return "%s: %s" % (self.get_param('title'), params['title'])

        if 'name' in params:
            return "%s: %s" % (self.get_param('title'), params['name'])

        return self.get_param('title')

    def create_refs(self, from_level, to_level):
        html_headers = []
        headers = self.markdown_render.headers

        if len(headers) == 0:
            return ""

        first_entry = headers[0]
        entry = first_entry
        prev_entry = first_entry

        html_headers.append('<ul class="nav-level-%s">' % (first_entry[0]))
        html_headers.append('<li><a href="#%s">%s</a>' % (first_entry[1], first_entry[2]))

        for idx in range(1, len(headers)):
            entry = headers[idx]

            if entry[0] < from_level or entry[0] >= to_level:
                continue

            if entry[0] > prev_entry[0]:
                html_headers.append('<ul class="nav-level-%s">' % (entry[0]))
                html_headers.append('<li><a href="#%s">%s</a>' % (entry[1], entry[2]))
            elif entry[0] < prev_entry[0]:
                for cidx in range(0, prev_entry[0] - entry[0]):
                    html_headers.append('</ul>')

                html_headers.append('<li><a href="#%s">%s</a>' % (entry[1], entry[2]))
            else:
                html_headers.append('<li><a href="#%s">%s</a>' % (entry[1], entry[2]))

            prev_entry = entry

        if first_entry != entry and first_entry[0] < entry[0]:
            for cidx in range(0, prev_entry[0] - entry[0]):
                html_headers.append('</ul>')

        html_headers.append('</ul>')

        return "\n".join(html_headers)

    def create_refs_level(self, html_headers, level, max_level):
        if level == max_level:
            return

        headers = self.markdown_render.headers

        if len(headers[level]) == 0:
            return self.create_refs_level(html_headers, level + 1, max_level)

        html_headers.append('<ul class="nav-level-%s">' % (level))

        for entry in headers[level]:
            html_headers.append('<li><a href="#%s">%s</a>' % (entry[0], entry[1]))
            self.create_refs_level(html_headers, level + 1, max_level)
            html_headers.append('</li>')

        html_headers.append('</ul>')

    def create_nav(self, current_path):
        ret = []
        maps = self.maps
        clean_path = os.path.normpath(current_path[:-3]) # -3 = *.md
        paths = clean_path.split('/')

        ret.append('<ul>')

        for idx in range(self.get_param('nav_begin'), len(paths)):
            path = "/".join(paths[0:idx + 1])
            ret.append('<li>')

            params = maps[path] if path in maps else {}

            if params and 'name' in params:
                name = params['name']
            else:
                name = paths[idx]

            if len(paths) - 1 == idx:
                ret.append(name)
            elif path in maps:
                ret.append('<a href="%s">%s</a>' % (self.make_url(path), name))
            else:
                ret.append(name)

            ret.append('</li>')
            ret.append('<li class="nav-spliter">/</li>')

        ret.pop()
        ret.append('</ul>')

        return "".join(ret)

    def make_url(self, path):
        base_url = self.base_url()
        extension = os.path.splitext(path)[1]

        if path == '/':
            return os.path.normpath("%s/" % (base_url))

        if extension == '':
            url = "%s/%s" % (base_url, path)
            cur_path = "%s/%s.md" % (self.source_path, path)
        else:
            if extension.lower() == '.md':
                url = "%s/%s" % (base_url, path[:-3])
                cur_path = "%s/%s" % (self.source_path, path)
            else:
                url = "%s/%s" % (base_url, path)
                cur_path = "%s/%s" % (self.source_path, path)

        if os.path.isfile(cur_path) == False:
            raise Exception("File not found: %s" % (cur_path))

        if extension == '' or extension.lower() == '.md':
            if self.is_release == False or self.get_param("url_with_ext"):
                url = "%s.html" % (os.path.normpath(url))
            else:
                url = "%s/" % (os.path.normpath(url))

        return url

    def base_url(self):
        if self.is_release == False:
            return os.path.abspath(self.build_path)

        base_url = self.get_param("base_url")

        if self.get_param("base_url") != None:
            return base_url

        return ""

    def get_param(self, name):
        if self.module != None and hasattr(self.module, name) :
            return getattr(self.module, name)

        if hasattr(self, name):
            return getattr(self, name)

        return None


if __name__ == "__main__":
    docs = Docs("lexbor-site/src", "lexbor-site/build", "lexbor-site/theme", "module")
    docs.make()
