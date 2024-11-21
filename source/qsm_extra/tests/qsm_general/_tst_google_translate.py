# coding:utf-8
import requests
import urllib

# 定义翻译参数
text = "Water Balloon"
source_language = "en"
target_language = "zh-CN"

# 构造 URL
url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format(
    source_language, target_language, urllib.quote(text.encode("utf-8"))
)

# 发送请求
response = requests.get(url)
if response.status_code == 200:
    result = response.json()
    translated_text = result[0][0][0]
    print translated_text
else:
    print("Error:", response.status_code)

