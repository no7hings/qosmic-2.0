# coding:utf-8
import qsm_general.dotfile as gnl_dotfile


ma = gnl_dotfile.MayaAscii(
    'Z:/projects/QSM_TST/source/shots/A001_002/A001_002_001/user.shared/cfx.cfx_cloth/main/maya/scenes/A001_002_001.cfx.cfx_cloth.main.v001.ma'
)

print ma.get_reference_dict()
