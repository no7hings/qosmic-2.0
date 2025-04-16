# coding:utf-8
import qsm_general.core as c

print(c.MayaBin.generate_dict())

# c.MayaBin.open_file(
#     'C:/Program Files/Autodesk/Maya2020/bin/maya.exe', 'X:/QSM_TST/A002/A002_001/动画/通过文件/A002_001_001.ma'
# )
c.MayaBin.open_file_use_rez(
    '2024', 'X:/QSM_TST/A002/A002_001/动画/通过文件/A002_001_001.ma'
)
