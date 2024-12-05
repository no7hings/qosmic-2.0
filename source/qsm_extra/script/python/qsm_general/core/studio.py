# coding:utf-8
import lxbasic.core as bsc_core


class Studio(object):
    PIP_DRIVER_MAP = dict(
        XSH='//10.33.4.90/pipeline-root',
        XHZ='//10.1.1.11/pipeline-root',
        XQD='//192.160.0.101/pipeline-root',
        DEV='//DONGCHANGBAO/pipeline-root'
    )

    PIP_DRIVER_MAP_R = {v: k for k, v in PIP_DRIVER_MAP.items()}

    @classmethod
    def get_current(cls):
        driver_source = bsc_core.BscStorage.get_driver_source(
            'Y:'
        )
        return cls.PIP_DRIVER_MAP_R.get(driver_source, 'UNKNOWN')
