# coding:utf-8
import lxkatana

lxkatana.set_reload()

import collections

import lxkatana.dcc.objects as ktn_dcc_objects

n = ktn_dcc_objects.Node('Group3')

n.set_input_port_add('input')

n.set_output_port_add('output')

n.create_customize_attributes(
    collections.OrderedDict(
        [
            ('render_settings.camera_enable', False),
            (('path', 'render_settings.camera'), ''),
            ('render_settings.resolution_enable', False),
            ('render_settings.resolution', '512x512'),
            ('render_settings.frame_enable', False),
            ('render_settings.frame', 1),
            #
            ('arnold_render_settings.stats_file_enable', False),
            (('file', 'arnold_render_settings.stats_file'), ''),
            ('arnold_render_settings.profile_file_enable', False),
            (('file', 'arnold_render_settings.profile_file'), '')
        ]
    )
)
