# coding:utf-8
import lxbasic.pinyin as bsc_pinyin


print bsc_pinyin.Text.split_any_to_texts(
    '测试'
)


print bsc_pinyin.Text.split_any_to_words(
    '测试'
)

print bsc_pinyin.Text.find_first_chr(
    '测试'
)

print bsc_pinyin.Text.find_first_chr(
    '0测试'
)
