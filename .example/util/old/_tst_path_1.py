# coding:utf-8
import lxbasic.core as bsc_core

# p = u"L:\FTP\qihe\to_diezhi\shl\20210511\1x\shengbei\shengbei"

p = u'L:\FTP\meirishijie\to_diezhi\20210526\石头文件\stone_path_B'


def _set_convert_(path):
    lis = []
    for i in path:
        i_r = repr(i)
        i_r_s = i_r.split("'")[1]
        i_r_s_c = len(i_r_s)
        if i_r_s_c == 1:
            lis.append(i)
        elif i_r_s_c == 2:
            if i_r_s == '\\\\':
                lis.append('/')
            else:
                lis.append('/' + i_r_s[-1])
        else:
            # hex
            if i_r_s.startswith('\\x'):
                hex_str = '0' + i_r_s[1:]
                lis.append('/' + str(int(oct(int(hex_str, 16)))))
            # unicode
            elif i_r_s.startswith('\\u'):
                lis.append(i_r_s)
    #
    return ''.join(lis).decode('unicode_escape')


print _set_convert_(p)
