# coding:utf-8


p = '/test/a/b/test'
pathsep = '/'
_ = p.split(pathsep)
if len(_) > 4:
    print '{0}{2}...{2}{1}'.format(pathsep.join(_[:2]), pathsep.join(_[-2:]), pathsep)
else:
    print p
