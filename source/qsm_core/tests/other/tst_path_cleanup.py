# coding:utf-8
import lxbasic.core as bsc_core

print(
    bsc_core.BscStorage.clear_pathsep_to(
        bsc_core.ensure_unicode('//nas1/玄机动作库')
    )
)
