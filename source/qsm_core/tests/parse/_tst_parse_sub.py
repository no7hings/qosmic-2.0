# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.BscStgParseOpt(
    '{root_source}/{project}/source/assets/{role}/{asset}'
)

print p.generate_combination_variants(
    dict(root_source='X:', project=['QSM_TST'], asset=['sam', 'lily'])
)
