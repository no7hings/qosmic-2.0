# coding:utf-8
import six

import re

import pypinyin

import itertools


class Text(object):
    @staticmethod
    def split_any_to_texts(text):
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')
        return re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))

    @classmethod
    def split_any_to_words(cls, text):
        list_ = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            # is chinese
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                list_.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
            else:
                list_.append(i_c)
        return list_

    @classmethod
    def to_prettify(cls, text):
        return six.u(' ').join(
            map(lambda x: x.capitalize(), cls.split_any_to_texts(text))
        )

    @staticmethod
    def split_any_to_words_extra(text):
        list_ = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            list_.append(i_c)
            # is chinese
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                # to pinyin
                list_.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
        return list_

    @classmethod
    def to_pinyin_name(cls, text):
        list_ = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                list_.append('_'.join(map(lambda x: str(x).lower(), pypinyin.lazy_pinyin(i_c))))
            else:
                list_.append(i_c)
        return '_'.join(list_)

    @classmethod
    def to_pinyin_map(cls, text):
        dict_ = {}
        list_ = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            list_.append(i_c)
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                i_pinyin = ''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c)))
                dict_[i_pinyin] = i_c
        return list_, dict_

    @classmethod
    def find_first_chr(cls, text):
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))

        if chars:
            c = chars[0]
            if re.match(six.u(r'[\u4e00-\u9fff]+'), c):
                return pypinyin.lazy_pinyin(c)[0][0].lower()
            return c[0].lower()

    @classmethod
    def cleanup(cls, text):
        list_ = []
        # to string
        if isinstance(text, six.text_type):
            text = text.encode('utf-8')

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text.decode('utf-8'))
        for i_c in chars:
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                pass
            else:
                list_.append(i_c)
        return '_'.join(list_)


class Texts(object):
    @classmethod
    def split_any_to_texts(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_texts, texts)))

    @classmethod
    def split_any_to_words_extra(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_words_extra, texts)))
