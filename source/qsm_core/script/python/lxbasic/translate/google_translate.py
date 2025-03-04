# coding:utf-8
import requests

import urllib


class GoogleTranslate:

    class Languages:
        CHS = 'zh-CN'
        ENG = 'en'

    @classmethod
    def translate(cls, text, source_language, target_language):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format(
            source_language, target_language, urllib.quote(text.encode("utf-8"))
        )
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            translated_text = result[0][0][0]
            return translated_text

    @classmethod
    def eng_to_chs(cls, text):
        return cls.translate(
            text, cls.Languages.ENG, cls.Languages.CHS
        )

    @classmethod
    def chs_to_eng(cls, text):
        return cls.translate(
            text, cls.Languages.CHS, cls.Languages.ENG
        )
