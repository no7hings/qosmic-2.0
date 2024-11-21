# coding:utf-8
import lxbasic.storage as bsc_storage

import qsm_general.dotfile as d

data = d.MayaMelPreset.generate_template_for('nCloth')

bsc_storage.StgFileOpt(
    'E:/myworkspace/qosmic-2.0/source/qsm_extra/configures/node_preset/nCloth.yml'
).set_write(data)
