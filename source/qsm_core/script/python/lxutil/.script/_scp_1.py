# coding:utf-8
import os

import json

import yaml


def set_json_convert_to_yaml(file_paths):
    for j in file_paths:
        base, ext = os.path.splitext(j)
        with open(j) as j_r:
            v = json.load(j_r)
            y_tmp = base + '.tmp.yml'
            # with open(y_tmp, 'w') as y_tmp_w:
            #     yaml.dump(
            #         v, y_tmp_w,
            #         indent=4,
            #         default_flow_style=False,
            #         width=480,
            #         # default_style='',
            #         canonical=False
            #     )
            y = base + '.yml'
            with open(y_tmp) as y_tmp_r:
                v = yaml.load(y_tmp_r)
                with open(y, 'w') as y_w:
                    yaml.dump(
                        v, y_w,
                        indent=4,
                        default_flow_style=False,
                        default_style=None,
                        canonical=False
                    )


set_json_convert_to_yaml(
    []
)
