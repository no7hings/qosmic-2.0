# coding:utf-8
# coding:utf-8
import qsm_general.dotfile as qsm_gnl_dotfile


xml = qsm_gnl_dotfile.PremiereXml(
    'Z:/temporaries/premiere_xml_test/test_scene.xml'
)

print(xml.get_fps())
print(xml.get_videos())
