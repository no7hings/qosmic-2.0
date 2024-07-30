# coding:utf-8
import re

from pypinyin import lazy_pinyin

def split_words_and_chars(string_list):
    result = []
    for string in string_list:
        words_chars = re.findall(ur'[\w]+|[\u4e00-\u9fff]+', string.decode('utf-8'))
        for wc in words_chars:
            if re.match(ur'[\u4e00-\u9fff]+', wc):
                result.extend(lazy_pinyin(wc))
            else:
                result.append(wc)
    return result


# 示例用法
string_list = [u'Hello, 你好，世界！', u'Python_3.8版本发布了。']
result = split_words_and_chars([s.encode('utf-8') for s in string_list])
print(result)
