# coding:utf-8
import re

# 原始字符串，需要前面加上 u 表示 Unicode 字符串
text = u'你好，世界! Hello, world! 你今天过得怎么样？'

# 使用正则表达式进行拆分，匹配标点符号和空格
# \W 匹配非字母数字字符，\s 匹配空白符
result = re.split(ur'[^\w\u4e00-\u9fff]+', text)

# 移除空字符串（由于多个连续的标点或空格）
result = [word for word in result if word]

print(result)