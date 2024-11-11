# coding:utf-8
import qsm_general.wsp_task as c

task_session = c.TaskParse.generate_task_session_by_resource_source_scene_src(
    'Z:/projects/QSM_TST/source/shots/A001_001/A001_001_001/user.shared/cfx.cfx/main/maya/scenes/A001_001_001.cfx.cfx.main.v001.ma'
)

print task_session.get_file_for(
    'shot-release-shit_animation_scene-file'
)
