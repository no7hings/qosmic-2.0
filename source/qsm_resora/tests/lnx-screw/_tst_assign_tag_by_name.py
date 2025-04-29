# coding:utf-8
import lxbasic.pinyin as bsc_pinyin

import lnx_screw.core as c

stage = c.Stage('resource_audio_11')

tag_map = stage.generate_tag_map('chs')

nodes = stage.find_all(stage.EntityTypes.Node)

for i in nodes:
    i_node_path = i.path
    i_name = i.gui_name_chs
    i_keys = bsc_pinyin.Text.split(i_name)
    for j_key in i_keys:
        if j_key in tag_map:
            j_tag_paths = tag_map[j_key]
            for k_tag_path in j_tag_paths:
                stage.create_node_tag_assign(
                    i_node_path, k_tag_path
                )
