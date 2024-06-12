# coding:utf-8
import six

import re

import pypinyin

import itertools


class Text(object):
    @staticmethod
    def split_any_to_words(text):
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return re.findall(six.u(r'[\w]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))

    @staticmethod
    def split_any_to_words_extra(text):
        lst = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[\w]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            lst.append(i_c)
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                lst.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
        return lst


class Texts(object):
    @classmethod
    def split_any_to_words(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_words, texts)))

    @classmethod
    def split_any_to_words_extra(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_words_extra, texts)))
