# coding:utf-8
import lxbasic.core as bsc_core

import rez.resolved_context as r_c

import rez.package_filter as r_f

import rez.package_search as p_s

_, g = p_s.get_reverse_dependency_tree(
    'lxdcc_lib',
    depth=3,
    paths=[
        "/l/packages/pg/prod",
        "/l/packages/pg/dept",
        "/l/packages/pg/third_party/app",
        "/l/packages/pg/third_party/plugin",
        "/l/packages/pg/third_party/ocio"
    ]
)

# f = r_f.PackageFilterList.singleton
#
# # f.add_filter('no-local')
#
# r = r_c.ResolvedContext(
#     ['pgmaya', 'usd', 'lxdcc'],
#     package_filter=f,
#     package_paths=[
#         "/l/packages/pg/prod",
#         "/l/packages/pg/dept",
#         "/l/packages/pg/third_party/app",
#         "/l/packages/pg/third_party/plugin",
#         "/l/packages/pg/third_party/ocio"
#     ]
# )
#
# dict_ = r.to_dict()
#
# print bsc_core.DictMtd.to_string_as_json_style(dict_)
#
#
# g = r.graph()
#
path_dict = {}

for i in g.nodes():
    i_atr = g.node_attributes(i)
    if len(i_atr) > 3:
        i_key = i_atr[0][1]
    else:
        i_key = i
        # i_key = i_atr[0][1]
        if '-' in i_key:
            i_name, i_version = i_key.split('-')
            if '[' in i_version:
                if '[]' in i_version:
                    i_version_ = i_version[:-2]
                    i_path = '/{}/{}-(0)'.format(i_name, i_version_)
                else:
                    i_version_ = i_version.split('[')[0]
                    i_index = i_version.split('[')[-1][:-1]
                    i_path = '/{}/{}-({})'.format(i_name, i_version_, i_index)
            else:
                i_path = '/{}/{}'.format(i_name, i_version)
        else:
            i_path = '/{}'.format(i_key)

        # print i_path
        path_dict[i] = i_path
        print i_key, i_path


for i in g.edges():
    i_tgt, i_src = i
    i_src_path, i_tgt_path = path_dict[i_src], path_dict[i_tgt]
    print i_src_path, i_tgt_path



