# coding:utf-8
import difflib

s = open('/data/f/houdini-test/right.txt.hip').readlines()

t = open('/data/f/houdini-test/error.txt.hip').readlines()


r = difflib.HtmlDiff().make_file(
    s,
    t
)

open('/data/f/houdini-test/result.html', 'w').write(r)
