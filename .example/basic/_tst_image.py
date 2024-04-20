# coding:utf-8
import lxbasic.storage as bsc_storage

t = bsc_storage.ImgOiioOptForTexture(
    '/data/e/workspace/lynxi/test/texture/mossy_ground_umkkfcolw.ao.tx'
)

print t.get_is_linear()
