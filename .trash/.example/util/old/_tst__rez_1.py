# coding:utf-8
import lxbasic.core as bsc_core

import rez.resolved_context as r_c

import rez.package_filter as r_f

f = r_f.PackageFilterList.singleton

r = r_c.ResolvedContext(
    ['maya_usd-0.6.0'],
    package_filter=f,
    package_paths=[
        "/l/packages/pg/prod",
        "/l/packages/pg/dept",
        "/l/packages/pg/third_party/app",
        "/l/packages/pg/third_party/plugin",
        "/l/packages/pg/third_party/ocio"
    ]
)

dict_ = r.to_dict()

print bsc_core.DictMtd.to_string_as_json_style(dict_)





