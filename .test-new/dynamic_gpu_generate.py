# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class DynamicGpuCacheGenerate(object):
    @classmethod
    def gpu_frame_export(cls, location, file_path, start_frame, end_frame, frame_step=1, with_material=False):
        cmds.loadPlugin('gpuCache', quiet=1)
        if cmds.objExists(location):
            directory_path = os.path.dirname(file_path)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            cmds.gpuCache(
                location,
                startTime=start_frame, endTime=end_frame,
                optimize=1, optimizationThreshold=40000,
                writeMaterials=with_material,
                dataFormat='ogawa',
                directory=directory_path,
                fileName=file_name
            )

    @classmethod
    def gpu_export(cls, location, file_path, start_frame, end_frame, with_material=False):
        frame_range = range(start_frame, end_frame+1)
        seq_range = range(end_frame-start_frame+1)
        for i_seq in seq_range:
            i_frame = frame_range[i_seq]
            i_frame_seq = i_seq+1
            i_gpu_file_path = ('.'+str(i_frame_seq).zfill(4)).join(os.path.splitext(file_path))
            cls.gpu_frame_export(location, i_gpu_file_path, i_frame, i_frame, with_material)

    @classmethod
    def gpu_import(cls, location, file_path, start_frame, end_frame, frame_step=1):
        cmds.loadPlugin('gpuCache', quiet=1)

        nodes = []

        frame_count = end_frame - start_frame+1
        parent_path = '|'.join(location.split('|')[:-1])
        name = location.split('|')[-1]
        # main
        cmds.createNode('transform', name=name, parent=parent_path, skipSelect=1)

        cmds.addAttr(location, longName='start_frame', attributeType='long', keyable=1)
        cmds.setAttr(location+'.start_frame', 1, lock=1)
        cmds.addAttr(location, longName='end_frame', attributeType='long', keyable=1)
        cmds.setAttr(location+'.end_frame', frame_count, lock=1)
        cmds.addAttr(location, longName='frame', attributeType='long', keyable=1)
        cmds.addAttr(location, longName='time', attributeType='long', keyable=1)
        cmds.connectAttr('time1.outTime', location+'.time')
        cmds.addAttr(location, longName='speed', attributeType='double', min=1, max=100, keyable=1)
        cmds.setAttr(location+'.speed', 1)
        cmds.addAttr(location, longName='offset', attributeType='long', min=-frame_count, max=frame_count, keyable=1)

        cmds.addAttr(location, longName='gpu', attributeType='bool', keyable=1)
        cmds.setAttr(location+'.gpu', 1)
        # expression
        eps_name = '{}_eps'.format(name)

        eps_script = (
            '{0}.frame='
            'abs(({0}.time+{0}.end_frame+{0}.offset+floor({0}.time/{0}.end_frame)*2)'
            '%({0}.end_frame+1))%{0}.end_frame*{0}.speed+1;\r\n'
        ).format(
            location
        )

        eps_path = cmds.expression(
            name=eps_name, string=eps_script, object=location, alwaysEvaluate=1, unitConversion=1
        )

        cmds.setAttr(location+'.frame', lock=1)
        time_name = '{}_tmc'.format(name)
        cmds.rename('timeToUnitConversion1', time_name)
        nodes.extend([eps_path, time_name])
        # gpu
        for i_seq in range(frame_count):
            i_frame_seq = i_seq+1
            i_seq_str = str(i_seq).zfill(4)
            i_time_range = range(i_frame_seq, i_frame_seq+2)

            i_gpu_file_path = ('.'+str(i_frame_seq).zfill(4)).join(os.path.splitext(file_path))

            i_gpu_name = '{}_{}_gpu'.format(name, i_seq_str)
            i_gpu_path = '{}|{}'.format(location, i_gpu_name)
            cmds.createNode('gpuCache', name=i_gpu_name, parent=location, skipSelect=1)
            cmds.setAttr(i_gpu_path+'.cacheFileName', i_gpu_file_path, type='string')
            cmds.setAttr(i_gpu_path+'.visibility', keyable=1)
            nodes.append(i_gpu_path)

            i_mtp_name = '{}_{}_mtp'.format(name, i_seq_str)
            i_mtp_path = i_mtp_name
            cmds.createNode('multiplyDivide', name=i_mtp_name, skipSelect=1)
            cmds.connectAttr(location+'.gpu', i_mtp_path+'.input1Y')
            cmds.connectAttr(i_mtp_path+'.outputY', i_gpu_path+'.visibility')
            nodes.append(i_mtp_path)

            i_frm_name = '{}_{}_anc'.format(name, i_seq_str)
            i_frm_path = i_frm_name
            cmds.createNode('animCurveUU', name=i_frm_path, skipSelect=1)
            cmds.connectAttr(location+'.frame', i_frm_path+'.input')
            cmds.connectAttr(i_frm_path+'.output', i_mtp_path+'.input2X')
            cmds.connectAttr(i_frm_path+'.output', i_mtp_path+'.input2Y')
            cmds.setAttr(i_frm_path+'.preInfinity', 3)
            cmds.setAttr(i_frm_path+'.postInfinity', 3)
            nodes.append(i_frm_path)

            i_boolean = i_frame_seq == frame_count

            for j_time in i_time_range:
                j_value = 0
                if j_time == i_frame_seq:
                    j_value = 1

                cmds.setDrivenKeyframe(
                    i_mtp_path+'.input2X', currentDriver=location+'.frame', value=j_value,
                    driverValue=j_time, outTangentType='step')

            cmds.setDrivenKeyframe(
                i_mtp_path+'.input2X', currentDriver=location+'.frame',
                driverValue=0, value=0, outTangentType='step'
            )
            cmds.setDrivenKeyframe(
                i_mtp_path+'.input2X', currentDriver=location+'.frame',
                driverValue=frame_count, value=0, outTangentType='step'
            )
            if i_boolean:
                cmds.setDrivenKeyframe(
                    i_mtp_path+'.input2X', currentDriver=location+'.frame',
                    driverValue=0, value=1, outTangentType='step'
                )
                cmds.setDrivenKeyframe(
                    i_mtp_path+'.input2X', currentDriver=location+'.frame',
                    driverValue=1, value=0, outTangentType='step'
                )
                cmds.setDrivenKeyframe(
                    i_mtp_path+'.input2X', currentDriver=location+'.frame',
                    driverValue=frame_count, value=1, outTangentType='step'
                )
        # container
        ctn_name = '{}_dgc'.format(name)
        cmds.container(type='dagContainer', name=ctn_name)
        cmds.setAttr(ctn_name+'.blackBox', 1, lock=1)
        cmds.setAttr(ctn_name+'.iconName', 'out_gpuCache.png', type='string')
        cmds.setAttr(ctn_name+'.hiddenInOutliner', 1)
        cmds.container(ctn_name, edit=1, force=1, addNode=nodes)
        cmds.parent(ctn_name, location)
        cmds.setAttr(ctn_name+'.hiddenInOutliner', 1)


if __name__ == '__main__':
    # DynamicGpuCacheGenerate.gpu_export(
    #     '|master', 'E:/myworkspace/test-root/dynamic_gpu_export/b/test.abc', 1, 24
    # )
    DynamicGpuCacheGenerate.gpu_import(
        '|test', 'E:/myworkspace/test-root/dynamic_gpu_export/b/test.abc', 1, 24
    )
