# coding:utf-8
import lxkatana

lxkatana.set_reload()

from Katana import KatanaFile

import lxkatana.scripts as ktn_scripts


for i in [
    '_Wsp/InstanceColorMap',
    #
    # '_Wsp_Usr/GeometrySpace',

]:
    i_f = '/data/e/workspace/lynxi/script/python/.setup/katana/Macros/{}.yml'.format(i)
    i_m = ktn_scripts.ScpMacro(i_f)
    i_m.build()
    i_m.save()
