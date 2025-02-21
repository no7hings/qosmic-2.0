# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QTextBrowser

class HtmlFormatter:
    COLORS = {
        'default': 'color: white;',  # 默认白色
        'red': 'color: red;',        # 红色
        'green': 'color: green;',    # 绿色
        'yellow': 'color: yellow;',  # 黄色
    }

    def __init__(self, indent_size=2):
        self.indent_size = indent_size
        self.lines = []
        self.add_html_structure()
        self.current_line = ""
        self.current_indent = 0  # 当前缩进级别

    def add_html_structure(self):
        self.lines.append("<html>")
        self.lines.append("  <body>")
        self.lines.append("    <style>.no_wrap{white-space:nowrap;}</style>")
        self.lines.append("    <style>.no_wrap_and_center{white-space:nowrap;text-align: center;}</style>")

    def new_line(self, text, indent=0, color='default', same_line=False):
        """
        Add a line of text with specified indentation and color.
        :param text: The content of the line (plain text).
        :param indent: The level of indentation (using non-breaking spaces).
        :param color: The color to apply (red, green, yellow, or default).
        :param same_line: If True, append text to the current line instead of starting a new line.
        """
        if not isinstance(text, unicode):
            text = unicode(text, 'utf-8')

        # 计算当前行的缩进
        indent_spaces = '&nbsp;' * (indent * self.indent_size)

        # 如果是同一行追加文本
        if same_line:
            color_style = self.COLORS.get(color, self.COLORS['default'])
            self.current_line += u'&nbsp;'.join([u'<span style="%s">%s</span>' % (color_style, text)])  # 追加到当前行
        else:
            if self.current_line:
                # 添加当前行并换行
                self.lines.append(u'%s%s<br>' % (indent_spaces, self.current_line))
            color_style = self.COLORS.get(color, self.COLORS['default'])
            self.current_line = u'%s<span style="%s">%s</span>' % (indent_spaces, color_style, text)  # 新起一行

    def finalize_line(self):
        """Finalize the current line to ensure it gets added to the output."""
        if self.current_line:
            self.lines.append(self.current_line + '<br>')
            self.current_line = ""

    def to_html(self):
        """
        Returns the formatted XML as an HTML string.
        """
        self.finalize_line()  # 确保当前行被添加到输出
        self.lines.append("  </body>")
        self.lines.append("</html>")
        return u'\n'.join(self.lines)  # 返回完整的 HTML

# PyQt5 应用程序以在 QTextBrowser 中显示输出
app = QApplication([])

# 创建并显示 QTextBrowser
browser = QTextBrowser()

# 使用示例：
formatter = HtmlFormatter()

# 添加行并在同一行中追加不同颜色的文本
formatter.new_line('X:/QSM_TST/Assets/scn/test_assembly/Maya/Final/test_assembly.ma', indent=0)
formatter.new_line(u'网格', indent=1)
formatter.new_line(u'通过', indent=1, color='red', same_line=True)  # 在同一行追加红色文本
formatter.new_line(u'网格计数', indent=1)  # 确保缩进一致
formatter.new_line(u'三角面数', indent=2)
formatter.new_line(u'通过', indent=3)
formatter.new_line(u'三角面数（单位面积）', indent=2)
formatter.new_line(u'通过', indent=3)
formatter.new_line(u'模型数（所有）', indent=2)
formatter.new_line(u'通过', indent=3)
formatter.new_line(u'模型数（可见）', indent=2)
formatter.new_line(u'通过', indent=3)
formatter.new_line(u'非缓存（GPU）面数百分比', indent=2)
formatter.new_line(u'警告', indent=3, color='red', same_line=True)  # 在同一行追加红色文本
formatter.new_line(u'非缓存（GPU）面数百分比为100%，超过了预设的25%。', indent=4, color='red', same_line=True)

# 将格式化的 HTML 设置到 QTextBrowser
browser.setHtml(formatter.to_html())

# 显示 QTextBrowser
browser.show()

# 运行 PyQt 应用程序
app.exec_()
