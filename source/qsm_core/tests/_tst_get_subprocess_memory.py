# coding:utf-8
import lxbasic.sprc as bsc_sprc


# b = bsc_core.BscSubprocess.get_memory_usage(10052)
# print bsc_core.BscInteger.to_prettify_as_file_size(b)

# print bsc_core.BscSubprocess.get_cpu_usage(10052)

print bsc_sprc.SprcDag.get_descendant_args(
    2172
)
