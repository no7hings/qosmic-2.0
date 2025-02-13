# coding:utf-8
from __future__ import print_function

import shutil

import os

import qsm_general.core.houdini as h

file_path = os.path.dirname(__file__)

c = h.HoudiniStartupCreate(file_path)

main_menu_xml_file = c.create_main_menu_xml()
print(main_menu_xml_file)

shutil.copy2(
    main_menu_xml_file,
    'E:/myworkspace/qosmic-2.0/source/qsm_houdini_main/startup/houdini/MainMenuCommon.xml'
)
