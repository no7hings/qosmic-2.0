# coding:utf-8
import re

import six

import lxbasic.pinyin as bsc_pinyin


# def split_words_and_chars(string_list):
#     result = []
#     for string in string_list:
#         print isinstance(string, six.text_type)
#         words_chars = re.findall(ur'[\w]+|[\u4e00-\u9fff]+', string.decode('utf-8'))
#         result.extend(words_chars)
#     return result
#
# # 示例用法
string_list = [u'hello_你好_世界！', u'Python_3.8版本发布了。']
# result = split_words_and_chars([s.encode('utf-8') for s in string_list])
# print(result)

for i in string_list:
    print bsc_pinyin.Text.to_to_prettify(i)



# a = ['Hello', u'你好', '世界', 'Python', '3.8', '版本发布了']
#
# for i in bsc_pinyin.Texts.split_any_to_words_extra(a):
#     print i
