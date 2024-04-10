# coding:utf-8
import six

from .... import core as bsc_core

from .... import storage as bsc_storage

from ... import abstracts as bsc_etr_abstracts


class EtrRv(bsc_etr_abstracts.AbsEtrRv):
    @classmethod
    def open_file(cls, file_path):
        bsc_core.PrcBaseMtd.set_run_with_result_use_thread(
            'rez-env pgrv -- rv "{}"'.format(file_path)
        )

    @classmethod
    def convert_to_mov(cls, **kwargs):
        default_kwargs = dict(
            input='',
            output='',
            quality=1.0,
            width=2048,
            lut_directory='/job/PLE/bundle/thirdparty/aces/1.2/baked/maya/sRGB_for_ACEScg_Maya.csp',
            comment='test',
            start_frame=1001,
        )
        cmd_args = [
            'rez-env pgrv',
            '--',
            '/opt/rv/bin/rvio',
            '{input}',
            '-vv',
            '-o "{output}"',
            '-outparams comment="{comment}"',
            '-quality {quality}',
            '-copyright "©2013-2022 Papergames. All rights reserved."'
        ]
        if 'input' in kwargs:
            input_ = kwargs['input']
            if input_:
                _ = []
                if isinstance(input_, (tuple, list)):
                    if input_[0].endswith('.exr'):
                        cmd_args.extend(
                            [
                                '-dlut "{lut_directory}"',
                            ]
                        )
                    #
                    if '####' in input_[0]:
                        cmd_args.extend(
                            [
                                '-overlay frameburn .4 1.0 30.0',
                            ]
                        )
                    #
                    default_kwargs['input'] = ' '.join(map(lambda x: '"{}"'.format(x), input_))
                elif isinstance(input_, six.string_types):
                    if input_.endswith('.exr'):
                        cmd_args.extend(
                            ['-dlut "{lut_directory}"']
                        )

                    #
                    if '####' in input_:
                        cmd_args.extend(
                            [
                                '-overlay frameburn .4 1.0 30.0',
                            ]
                        )
                    #
                    default_kwargs['input'] = '"{}"'.format(input_)
        #
        output = kwargs['output']
        output_opt = bsc_storage.StgFileOpt(output)
        output_opt.create_directory()
        default_kwargs['output'] = output
        bsc_core.PrcBaseMtd.execute_with_result(
            ' '.join(cmd_args).format(**default_kwargs)
        )


class EtrUsd(bsc_etr_abstracts.AbsEtrUsd):
    @classmethod
    def registry_set(cls, file_path):
        # noinspection PyUnresolvedReferences
        import prod_tools.set_dressing.record_set_registry as record_set_registry

        record_set_registry.run(file_path)
