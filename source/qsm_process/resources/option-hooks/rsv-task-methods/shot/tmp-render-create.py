# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFileMtd.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                #
                render_frames = hook_option_opt.get('render_frames')
                render_frame_step = int(hook_option_opt.get('render_frame_step'))
                if render_frame_step > 1:
                    render_frame_range = bsc_core.RawTextOpt(render_frames).to_frame_range()
                    render_frames_ = bsc_core.RawFrameRangeMtd.get(
                        render_frame_range, render_frame_step
                    )
                    hook_option_opt.set(
                        'render_frames', ','.join(map(str, render_frames_))
                    )
                    hook_option_opt.set(
                        'render_frame_step', 1
                    )
                #
                component_usd_file_path = get_component_usd_file(rsv_task, rsv_scene_properties)
                if bsc_storage.StgFileMtd.get_is_exists(component_usd_file_path) is True:
                    hook_option_opt.set(
                        'component_usd_file', component_usd_file_path
                    )
                    # todo, replace to new fnc
                    cmd_pattern = 'rez-env python pg_tools -- python /l/packages/pg/prod/pg_production_lib/9.9.9/lib/production/set/auto_set/submit_usd_render_job.py --usd="{component_usd_file}" --proj="{project}" --shot="{shot}" --step="{step}" --task="{task}" --shading="{render_look}" --user="{user}" --frames="{render_frames}" --stepby={render_frame_step} --motion={render_motion_enable} --instance={render_instance_enable} --bokeh={render_bokeh_enable} --bg={render_background_enable} --chunk={render_chunk} --aa={render_arnold_aa_sample} --publish={user_upload_shotgun_enable} --tech_review={user_tech_review_enable} --playlist=0 --description="prerender"'
                    cmd = cmd_pattern.format(
                        **hook_option_opt.value
                    )
                    # print cmd
                    bsc_core.PrcBaseMtd.execute_with_result(
                        cmd
                    )
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def get_component_usd_file(rsv_task, rsv_scene_properties):
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == rsv_scene_properties.get('workspaces.release'):
        keyword_0 = '{branch}-component-usd-file'
    elif workspace == rsv_scene_properties.get('workspaces.temporary'):
        keyword_0 = '{branch}-temporary-component-usd-file'
    else:
        raise TypeError()

    component_usd_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    component_usd_file_path = component_usd_file_rsv_unit.get_result(version=version)
    return component_usd_file_path


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
