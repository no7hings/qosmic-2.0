# coding:utf-8


class MayaProcess(object):
    @classmethod
    def generate_command(cls, option):
        # windows
        cmds = [
            'rez-env qsm_dcc_main maya-2019 usd-20.11',
            (
                r'-- mayabatch -command '
                r'"python('
                r'\"import lxsession.commands as ssn_commands;'
                r'ssn_commands.execute_option_hook(option=\\\"{hook_option}\\\")\")"'
            ).format(
                hook_option='option_hook_key=dcc-process/maya-process&' + option
            )
        ]
        return ' '.join(cmds)

        # import lxbasic.storage as bsc_storage
        # c = bsc_storage.PkgContextNew(
        #     ' '.join(['lxdcc', 'maya', 'maya@2019.2', 'usd', 'mtoa@4.2.1.1'])
        # ).get_command(
        #     args_execute=[
        #         (
        #             r'-- mayabatch -command '
        #             r'"python('
        #             r'\"importlib=__import__(\\\"importlib\\\");'
        #             r'ssn_commands=importlib.import_module(\\\"lxsession.commands\\\");'
        #             r'ssn_commands.execute_option_hook(option=\\\"{hook_option}\\\")\")"'
        #         ).format(
        #             hook_option='option_hook_key="dcc-process/maya-process"&'+option
        #         )
        #     ],
        # )
        # return c


class PythonProcess(object):
    @classmethod
    def generate_command(cls, option):
        import lxbasic.resource as bsc_resource

        import lxbasic.storage as bsc_storage

        c = bsc_storage.PkgContextNew(
            ' '.join(['lxdcc', 'usd'])
        ).get_command(
            args_execute=[
                r'-- qsm-python {process_file} "{option}"'.format(
                    process_file=bsc_resource.ExtendResource.get('python-process/usd-script.py'), option=option
                )
            ],
        )
        return c
