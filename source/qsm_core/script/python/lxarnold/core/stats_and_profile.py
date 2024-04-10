# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.core as bsc_core


class StatsFileOpt(object):
    def __init__(self, obj):
        self._obj = obj

        self._content = ctt_core.Content(
            value=self._obj.path
        )

    # memory
    def get_capacity_memory_byte(self):
        return self._content.get(
            'CPU info.memory capacity.bytes'
        )

    def get_peak_memory_byte(self):
        return self._content.get(
            'render 0000.peak CPU memory used.bytes'
        )

    def get_peak_memory_gb(self):
        b = self.get_peak_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    def get_peak_memory_byte_(self):
        lis = []
        ks = self._content.get_keys(
            'render 0000.peak CPU memory used.*.bytes'
        )
        vs = []
        for i_k in ks:
            i_n = ' '.join(i_k.split('.')[-2:])
            i_v = self._content.get(i_k)
            vs.append(i_v)
            lis.append(
                (i_n, i_v, i_v)
            )
        return lis

    def get_geometry_face_count(self):
        return self._content.get(
            'render 0000.geometric elements.subdiv patches.elements'
        )

    def get_geometry_mesh_face_count(self):
        keys = [
            'render 0000.triangle tessellation.polymesh.count',
            'render 0000.triangle tessellation.subdivs.count',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    def get_mesh_max_subdiv_iteration(self):
        ks = [
            ('render 0000.triangle tessellation.subdivs.adaptive.count', 4),
            ('render 0000.triangle tessellation.subdivs.iterations 3+.count', 3),
            ('render 0000.triangle tessellation.subdivs.iterations 2.count', 2),
            ('render 0000.triangle tessellation.subdivs.iterations 1.count', 1),

        ]
        for k, v in ks:
            if self._content.get(k):
                return v
        return 0

    def get_startup_memory_byte(self):
        keys = [
            'render 0000.peak CPU memory used.at startup.bytes',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    def get_startup_memory_gb(self):
        b = self.get_startup_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    def get_geometry_memory_byte(self):
        keys = [
            'render 0000.peak CPU memory used.geometry.bytes',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    def get_geometry_memory_gb(self):
        b = self.get_geometry_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    def get_mesh_memory_byte(self):
        keys = [
            'render 0000.peak CPU memory used.geometry.polymesh.bytes',
            'render 0000.peak CPU memory used.geometry.subdivs.bytes',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    def get_mesh_memory_gb(self):
        b = self.get_mesh_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    def get_curve_memory_byte(self):
        keys = [
            'render 0000.peak CPU memory used.geometry.curves.bytes',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    #
    def get_curve_memory_gb(self):
        b = self.get_curve_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    def get_texture_memory_byte(self):
        keys = [
            'render 0000.peak CPU memory used.texture cache.bytes',
        ]
        vs = [self._content.get(i) or 0 for i in keys]
        return sum(vs)

    def get_texture_memory_gb(self):
        b = self.get_texture_memory_byte()
        if b:
            return bsc_core.RawIntegerMtd.byte_to_gb(
                b
            )

    # time
    def get_render_microsecond_(self):
        ks = self._content.get_keys('*.microseconds')
        for i in ks:
            print i, self._content.get(i)

    def get_microsecond(self):
        return self._content.get(
            'render 0000.frame time.microseconds'
        )

    def get_hours(self):
        ms = self.get_microsecond()
        if ms:
            return bsc_core.RawIntegerMtd.microsecond_to_hours(ms)

    def get_startup_microsecond(self):
        return self._content.get(
            'render 0000.scene creation time.microseconds'
        )

    def get_startup_hours(self):
        ms = self.get_startup_microsecond()
        if ms:
            return bsc_core.RawIntegerMtd.microsecond_to_hours(ms)

    def _test_(self):
        print self.get_warnings()

    def get_warnings(self):
        lis = []
        _ = self._content.get('render 0000.number of warnings by type') or {}
        for k, v in _.items():
            lis.append('{}, {};'.format(k, v))
        return lis


class ProfileFileOpt(object):
    def __init__(self, obj):
        self._obj = obj

        self._content = ctt_core.Content(
            value=self._obj.path
        )

    def _test_(self):
        pass
