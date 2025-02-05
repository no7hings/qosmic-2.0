# coding:utf-8
import six


class HtmlFormatter:
    COLORS = {
        'default': 'color: white;',
        'red': 'color: #FF0033;',
        'green': 'color: #33FF77;',
        'yellow': 'color: #FFFF33;',
    }

    def __init__(self, indent_size=4):
        self.indent_size = indent_size
        self.lines = []
        self.add_html_structure()

    def add_html_structure(self):
        self.lines.append("<html>")
        self.lines.append("  <body>")
        self.lines.append("    <style>.no_wrap{white-space:nowrap;}</style>")
        self.lines.append("    <style>.no_wrap_and_center{white-space:nowrap;text-align: center;}</style>")

    def new_line(self, text, indent=0, color='default'):
        if not isinstance(text, six.text_type):
            text = six.text_type(text)

        # Add the line of text with HTML formatting
        indent_spaces = '&nbsp;' * (indent * self.indent_size)  # Using non-breaking spaces for indentation
        color_style = self.COLORS.get(color, self.COLORS['default'])
        formatted_line = u'%s<span style="%s">%s</span><br>' % (indent_spaces, color_style, text)
        self.lines.append(formatted_line)

    def append_line(self, text, color='default'):
        if not isinstance(text, six.text_type):
            text = six.text_type(text)

        # Add the line of text with HTML formatting
        color_style = self.COLORS.get(color, self.COLORS['default'])
        formatted_line = u'<span style="%s">%s</span><br>' % (color_style, text)

        self.lines[-1] = self.lines[-1][:-4]+formatted_line

    def to_html(self):

        self.lines.append("  </body>")
        self.lines.append("</html>")
        return u'\n'.join(self.lines)
