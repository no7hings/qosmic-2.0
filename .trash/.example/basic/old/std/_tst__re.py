# coding:utf-8
import re

k = 'y'

p = r'(.*)({})(.*)'.format(k.replace('*', '.*'))

m = re.search(
    p, 'python'
)

# print m.groups()


# path = '/l'
#
# print re.findall(
#     r'/(.*)', path
# )
#
# print not not re.findall(
#     r'(/)(.*)', path
# )

path = 'la:/'

print not not re.findall(
    r'^[a-zA-Z]:(.*)', path
)
