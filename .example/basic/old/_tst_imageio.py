# coding:utf-8
import lxbasic.core as bsc_core


def test():
    file_path_src = '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/test.roughness.jpg'
    file_path_tgt = '/l/resource/library/texture/all/surface/rough_concrete_ogioE0/v0001/texture/test/test.roughness.exr'
    option = dict(
        input=file_path_src,
        output=file_path_tgt,
    )
    cmd_args = [
        bsc_core.ExcBaseMtd.oiiotool(),
        u'-i "{input}"',
        # '--ch R,G,B,A=1.0',
        u'-o "{output}"',
    ]
    bsc_core.PrcBaseMtd.execute_with_result(
        ' '.join(cmd_args).format(**option)
    )


if __name__ == '__main__':
    test()

