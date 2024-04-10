# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects


class FileCollection(object):
    def __init__(self, source_path, target_path):
        d = bsc_dcc_objects.StgDirectory(source_path)
        dds = d.get_descendants()
        dic = {}
        for dd in dds:
            fps = dd.get_child_file_paths()
            for fp in fps:
                # print fp
                sfp = fp[len(source_path):]
                # print sfp
                sf = bsc_dcc_objects.StgFile(sfp)
                if sfp.endswith('.tx'):
                    osfp = sf.get_orig_file('.tx')
                    if osfp is not None:
                        osf = bsc_dcc_objects.StgFile(osfp)
                        fn = osf.name
                        if fn in dic:
                            seq = dic[fn]
                            seq += 1
                            dic[fn] = seq
                            new_fn = '{}.v{}{}'.format(osf.base, str(seq).zfill(3), osf.ext)
                        else:
                            seq = 0
                            dic[fn] = seq
                            new_fn = fn
                        target_file_path = '{}/image/{}'.format(target_path, new_fn)
                        osf.copy_to_file(target_file_path)
                elif sfp.endswith('.abc'):
                    target_file_path = '{}/abc/{}'.format(target_path, sf.name)
                    sf.copy_to_file(target_file_path)


if __name__ == '__main__':
    print bsc_dcc_objects.StgFile(
        '/l/temp/td/dongchangbao/tx_convert_test/exr_1/jiguang_cloth_mask.1001.1001.tx'
    ).get_orig_file('.tx')
    # FileCollection(
    #     source_path='/data/package_temporary_bsnw_1',
    #     target_path='/data/package_temporary_bsnw_1_0',
    # )
