# coding:utf-8
import lxbasic.deadline as bsc_deadline

job = bsc_deadline.DdlJobQuery('60ffefd71a404114900dd35c')
tasks = job.get_tasks()
for task in tasks:
    task_contents = task.get_contents()
    for task_content in task_contents:
        arnold_stouts = bsc_deadline.DdlLog(task_content.raw).get_stouts(content=True)
        arnold_errors = bsc_deadline.DdlLogForArnold(arnold_stouts).get_errors()
        if arnold_errors:
            print task
            # print job.get_property('OutDir')
            # print job.get_property('Props.PlugInfo.ScriptModule')
            # print job.get_property('Props.PlugInfo.OutputNode')
            # print job.get_property('Props.PlugInfo.SceneFile')
            # print task
            # # print task.properties
            print task.get_property('Frames')
            # print task.get_property('Slave')
            # print task.get_property('Start')
            # print task.get_property('StartRen')
            # print task.get_property('Comp')
            print arnold_errors
            # arnold_warnings = bsc_deadline.DdlLogForArnold(arnold_stouts).get_warnings()
            # if arnold_warnings:
            #     print arnold_warnings
        # arnold_warning = bsc_deadline.DdlLogForArnold(arnold_stouts).get_warnings()
        # print arnold_warning
        # logs = task.get_logs()
        # for log in logs:
        #     print log.properties
