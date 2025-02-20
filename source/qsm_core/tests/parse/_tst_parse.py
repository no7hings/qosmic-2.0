# coding:utf-8
import lxbasic.core as bsc_core

p = bsc_core.BscStgParseOpt(
    'X:/QSM_TST/A001{epi_IGN}/A001_001{seq_IGN}/动画/通过文件/A001_001_001.ma'
)

print(p.find_matches())

p = bsc_core.BscStgParseOpt(
    'X:/QSM_TST/{episode}/A001_001{seq_IGN}/动画/通过文件/A001_001_001.ma'
)

print(p.find_matches())
