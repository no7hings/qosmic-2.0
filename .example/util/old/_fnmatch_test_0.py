# coding:utf-8
import fnmatch

print fnmatch.filter(['@/a_0/a_0@', '@/a_0/b_0@', '@/a_0/a_0/a_0@'], '@/a_0/*[!@]')
