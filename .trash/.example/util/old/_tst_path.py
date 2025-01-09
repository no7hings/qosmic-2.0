# coding:utf-8
import lxbasic.storage as bsc_storage

p = "L:\FTP\qihe\to_diezhi\shl\20210511\1x\shengbei\shengbei"
print repr(p)

print bsc_storage.StgPathMapper.map_to_linux(bsc_storage.StgPathOpt(p).__str__())


# p_0 = p
#
# p_0_r = repr(p)
#
# lis = []
#
# for i in p:
#     i_r = repr(i)
#     i_c = len(i_r)
#     if i_c == 3:
#         lis.append(i)
#     else:
#         if i_c == 4:
#             if i_r == "'\\\\'":
#                 lis.append('/')
#             else:
#                 lis.append('/' + i_r[-2])
#         else:
#             hex_str = '0x' + i_r[3:-1]
#             lis.append('/' + str(int(oct(int(hex_str, 16)))))
#             # print len(), i_r
#
# print ''.join(lis)


