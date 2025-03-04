# coding:utf-8
import lxbasic.scan as bsc_scan

print(
    bsc_scan.ScanGlob.glob_files(
        '//DEV/map_x/episodes/TST//*'
    )
)

print(
    bsc_scan.ScanGlob.glob('//DEV/map_x/episodes/TST')
)
