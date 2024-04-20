# coding:utf-8
import re

# Example usage
input_string = "/3d_plant/tree"
print re.sub(r'/(\d+)([^/]+)', lambda x: '/_{}{}'.format(x.group(1), x.group(2)), input_string)

print re.sub(r'/(\d+)([^/]+)', lambda x: '/_{}{}'.format(x.group(1), x.group(2)), "/_3d_plant/tree")
