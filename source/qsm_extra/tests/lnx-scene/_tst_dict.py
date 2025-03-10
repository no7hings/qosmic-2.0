# coding:utf-8
import json

import lnx_scene.gui.graph.base as b

f = 'E:/myworkspace/qosmic-2.0/source/qsm_extra/tests/lnx-scene/_tst_node.json'
with open(f) as j:
    json_str = j.read()

dict_ = json.loads(json_str)
