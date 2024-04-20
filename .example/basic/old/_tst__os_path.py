# coding:utf-8
import lxbasic.storage as bsc_storage

scene_file_path = "\l\prod\cjd\publish\assets\prp\cjdj_fengche\rig\rigging\cjdj_fengche.rig.rigging.v003\maya\cjdj_fengche.ma"
print scene_file_path
print repr(scene_file_path)

print bsc_storage.StgPathOpt(
    scene_file_path
).get_path()


for i in '\a':
    print repr(i)


i_r_s = '\\x07'
hex_str = '0' + i_r_s[1:]

print str(int(oct(int(hex_str, 16))))
