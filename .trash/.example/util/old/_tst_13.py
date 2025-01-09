# coding:utf-8
import grp
import pwd
import os

stat_info = os.stat('/l/prod/shl/publish/assets/flg/tree_d/srf/surfacing/tree_d.srf.surfacing.v008/texture/Bark.tx')
uid = stat_info.st_uid
gid = stat_info.st_gid
print uid, gid

user = pwd.getpwuid(uid)[0]
group = grp.getgrgid(gid)[0]
print user, group
