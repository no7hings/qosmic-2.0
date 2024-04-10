# coding:utf-8
import sys


def test_(option_opt):
    import time

    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    print option_opt

    _m = 10

    with bsc_log.LogProcessContext.create_as_bar(maximum=_m, label='test') as l_p:
        for _i in range(_m):
            time.sleep(.5)
            l_p.do_update()


def test(option_opt):
    import lxusd.scripts as usd_scripts

    # usd_scripts.ScpInstance.generate_instance_cache(
    #     '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/maya/scenes/usd/env_waterfall_003.usd',
    #     '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/clarisse/plants_038.fix.usd',
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg',
    #     'st',
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test_instance_color_map.usd',
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test_instance_color_map.json'
    # )

    usd_scripts.ScpInstance.generate_grow_cache(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/maya/scenes/usd/env_waterfall_004.usd',
        '/depts/lookdev/ld_qiuhua/texture/TexturesCom_NatureForests0050_M.jpg',
        'st',
        '/data/e/workspace/lynxi/test/maya/vertex-color/test_grow_color_map.usd'
    )


def cache_hierarchy_fnc(option_opt):
    import lxusd.core as usd_core

    location = option_opt.get('location')
    file_path = option_opt.get('file')
    stage_opt = usd_core.UsdStageOpt(file_path)
    return [location+i for i in stage_opt.get_all_obj_paths()]


def generate_grow_cache(option_opt):
    import lxusd.scripts as usd_scripts

    grow_usd_file_path = option_opt.get('grow_usd')
    image_file_path = option_opt.get('image')
    uv_map_name = option_opt.get('uv_map_name')
    cache_usd_file_path = option_opt.get('cache_usd')

    usd_scripts.ScpInstance.generate_grow_cache(
        grow_usd_file_path, image_file_path, uv_map_name, cache_usd_file_path
    )


def generate_instance_cache(option_opt):
    import lxusd.scripts as usd_scripts

    grow_usd_file_path = option_opt.get('grow_usd')
    instance_usd_file_path = option_opt.get('instance_usd')
    image_file_path = option_opt.get('image')
    uv_map_name = option_opt.get('uv_map_name')
    cache_usd_file_path = option_opt.get('cache_usd')
    cache_json_file_path = option_opt.get('cache_json')

    usd_scripts.ScpInstance.generate_instance_cache(
        grow_usd_file_path, instance_usd_file_path, image_file_path, uv_map_name,
        cache_usd_file_path, cache_json_file_path
    )


def transfer_clarisse_usd(option_opt):
    import lxusd.scripts as usd_scripts

    usd_file_path = option_opt.get('usd')
    use_usd = option_opt.get_as_boolean('use_usd')
    use_usda = option_opt.get_as_boolean('use_usda')

    cc = usd_scripts.UsdScpForClarisseCleanup(usd_file_path)
    cc.transfer()
    if use_usd is True:
        cc.save_as_usd()
    elif use_usda is True:
        cc.save_as_usda()


def main(argv):
    import lxbasic.core as bsc_core

    import lxusd.startup as usd_startup

    usd_startup.UsdSetup.build_environ()

    option = argv[1]
    option_opt = bsc_core.ArgDictStringOpt(option)
    key = option_opt.get('method')

    if key == 'test':
        test(option_opt)
    elif key == 'cache-hierarchy':
        cache_hierarchy_fnc(option_opt)
    elif key in {'generator-grow-cache'}:
        generate_grow_cache(option_opt)
    elif key in {'generator-instance-cache'}:
        generate_instance_cache(option_opt)
    elif key in {'transfer-clarisse-usd'}:
        transfer_clarisse_usd(option_opt)


if __name__ == '__main__':
    main(sys.argv)
