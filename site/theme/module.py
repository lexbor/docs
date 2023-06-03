
import os
import sys
import re

class Theme:
    title = "Lexbor"
    nav_begin = 1
    url_with_ext = False
    base_url = ""

    def render(docs, md_path, theme_path, args):
        args['body'] = '<div class="markdown-body">%s</div>' % (args['body'])
        return args
