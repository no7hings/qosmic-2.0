# coding:utf-8
import re

p_0 = r'[<](.*?)[>]'

a_0 = '<abc>'

print re.findall(re.compile(p_0, re.S), a_0)


p_1 = r'[<](.*^[\n].*)[>]'

a_1 = '<abc\nabc>'

print re.findall(re.compile(p_1, re.S), a_0)
print re.findall(re.compile(p_1, re.S), a_1)
