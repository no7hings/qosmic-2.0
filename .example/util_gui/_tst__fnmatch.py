# coding:utf-8
import fnmatch

print fnmatch.filter(
    ['ani', 'flo', 'rlo', 'abc', 'set'], '[afr][ln][io]'
)
