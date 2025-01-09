# coding:utf-8
import re

import html

from urllib import quote

import requests

GOOGLE_TRANSLATE_URL = 'https://translate.google.com/?hl=en&sl={from_language}&tl={to_language}&text={text}&op=translate'


def translate(text, from_language="auto", to_language="auto"):
    text = quote(text)
    url = GOOGLE_TRANSLATE_URL.format(
        **dict(
            text=text,
            from_language=from_language,
            to_language=to_language
        )
    )
    print url
    response = requests.get(url)
    data = response.text
    print data
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""

    return html.unescape(result[0])


print translate('test', 'en', 'zh-CN')
