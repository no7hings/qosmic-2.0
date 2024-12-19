# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    import lxresolver.core as rsv_core

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if bsc_storage.StgFile.get_is_exists(any_scene_file_path) is True:
            resolver = rsv_core.RsvBase.generate_root()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                render_frames = hook_option_opt.get('render_frames')
                render_frame_step = int(hook_option_opt.get('render_frame_step'))
                if render_frame_step > 1:
                    render_frame_range = bsc_core.BscTextOpt(render_frames).to_frame_range()
                    render_frames_ = bsc_core.BscFrameRange.get(
                        render_frame_range, render_frame_step
                    )
                    hook_option_opt.set(
                        'render_frames', ','.join(map(str, render_frames_))
                    )
                    hook_option_opt.set(
                        'render_frame_step', 1
                    )
                #
                cache_workspace = hook_option_opt.get('cache_workspace')
                if cache_workspace == rsv_scene_properties.get('workspaces.release'):
                    hook_option_opt.set('cache_use_output_enable', 0)
                elif cache_workspace == rsv_scene_properties.get('workspaces.temporary'):
                    hook_option_opt.set('cache_use_output_enable', 1)
                #
                usd_effect_components = hook_option_opt.get(
                    'usd_effect_components'
                )
                if usd_effect_components:
                    hook_option_opt.set(
                        'usd_effect_components', ','.join(usd_effect_components)
                    )
                else:
                    hook_option_opt.set(
                        'usd_effect_components', ''
                    )
                # todo, replace to new fnc
                cmd_pattern = 'rez-env python pg_tools -- python /l/packages/pg/prod/pg_production_lib/9.9.9/lib/production/efx/vendor_collect/send_efx_render.py send_render_job --proj="{project}" --shot="{shot}" --task="{task}" --output={cache_use_output_enable} --layer=1 --upload_sg={user_upload_shotgun_enable} --user="{user}" --frame="{render_frames}" --ele="{usd_effect_components}"'
                #
                cmd = cmd_pattern.format(
                    **hook_option_opt.value
                )
                # print cmd
                bsc_core.BscProcess.execute_with_result(
                    cmd
                )
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
