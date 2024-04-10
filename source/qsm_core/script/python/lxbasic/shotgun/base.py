# coding:utf-8
import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class StgBase(object):
    CONNECTION = None

    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_resource.RscExtendConfigure.get_as_content('shotgun/main')
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @classmethod
    def generate_connection(cls):
        from shotgun_api3 import shotgun

        c = cls._generate_content()

        # noinspection PyBroadException
        try:
            _ = shotgun.Shotgun(
                c.get('connection.url'),
                c.get('connection.script'),
                c.get('connection.code'),
                ca_certs=bsc_storage.StgPathMapper.map_to_current(
                    c.get('connection.ca_certs')
                )
            )
            return _
        except Exception:
            bsc_core.ExceptionMtd.print_stack()
            return None

    @staticmethod
    def get_shot_frame_range(project_name, shot_name):
        # noinspection PyUnresolvedReferences
        import sgtk

        bundle = sgtk.platform.current_engine()
        if bundle:
            sg = bundle.shotgun
            shot = sg.find_one(
                'Shot', [
                    ['code', 'is', shot_name]
                ],
                ['sg_cut_in', 'sg_cut_out']
            )
            return shot.get('sg_cut_in'), shot.get('sg_cut_out')

    @staticmethod
    def get_project_resolution(project_name):
        # noinspection PyUnresolvedReferences
        import sgtk

        bundle = sgtk.platform.current_engine()
        if bundle:
            sg = bundle.shotgun
            project = sg.find_one(
                'Project',
                [
                    ['name', 'is', project_name]
                ],
                ['sg_resolution']
            )
            _ = project.get('sg_resolution')
            if _:
                return [int(i) for i in _.split('*')]


if __name__ == '__main__':
    cn = StgBase.generate_connection()
    print cn

