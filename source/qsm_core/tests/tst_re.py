# coding:utf-8
import re

path = '|unit_assembly_dgc|region_2_AR|region_2_AR_NS:region_2_GRP|region_2_AR_NS:crate_grp|region_2_AR_NS:crate_grpShape'
path2 = '|__UNIT_ASSEMBLY__|test_gpu_assembly:unit_assembly_dgc|test_gpu_assembly:region_2_AR|test_gpu_assembly:region_2_AR_NS:region_2_GRP|test_gpu_assembly:region_2_AR_NS:crate_grp|test_gpu_assembly:region_2_AR_NS:crate_grpShape'

m = re.search(
    r'(\|.*{name})(\|.*{name}_NS.*:.*).*'.format(name='region_2_AR'), path2
)

print m.group(1)

namespace = path.split('|')[-1].split(':')[-2]

print namespace
