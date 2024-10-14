# coding:utf-8


class MayaTimeunit:
    TIMEUNIT_TO_FPS_DICT = {
        '12fps': 12,
        'game': 14,
        '16fps': 16,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60
    }

    FPS_TO_TIMEUNIT_DICT = {v: k for k, v in TIMEUNIT_TO_FPS_DICT.items()}

    @classmethod
    def fps_to_timeunit(cls, fps):
        if fps in cls.FPS_TO_TIMEUNIT_DICT:
            return cls.FPS_TO_TIMEUNIT_DICT[fps]
        return '{}fps'.format(fps)

    @classmethod
    def timeunit_to_fps(cls, timeunit):
        if timeunit in cls.TIMEUNIT_TO_FPS_DICT:
            return cls.TIMEUNIT_TO_FPS_DICT[timeunit]
        return int(timeunit[:-3])
