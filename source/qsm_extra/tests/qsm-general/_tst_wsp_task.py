# coding:utf-8
import lnx_wotrix.core as c


task_parse = c.TaskParse()

print(task_parse)

task_parse = c.TaskParse()

print(task_parse)


task_session = c.TaskParse.generate_task_session_by_resource_source_scene_src(
    'maya', 'Z:/projects/QSM_TST/source/shots/A001_001/A001_001_001/user.shared/cfx.cfx/main/maya/scenes/A001_001_001.cfx.cfx.main.v001.ma'
)


print(
    task_session.get_file_or_dir_for(
        'shot-disorder-animation-scene-file'
    )
)
