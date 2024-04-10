# coding:utf-8
import os

import lxbasic.dcc.core as bsc_dcc_core

file_path = os.path.dirname(__file__)

c = bsc_dcc_core.HoudiniSetupCreator(file_path)

main_menu_xml_file = c.create_main_menu_xml()
print main_menu_xml_file

# shutil.copy2(
#     main_menu_xml_file,
#     '/data/e/myworkspace/td/lynxi/script/python/.setup/houdini/MainMenuCommon.xml'
# )
