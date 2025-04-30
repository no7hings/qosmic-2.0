# coding:utf-8
import pkgutil as _pkgutil

AUDIO_FLAG = False

_module = _pkgutil.find_loader('pyaudio')

if _module:
    AUDIO_FLAG = True

    import lxbasic.log as _log_core

    _log_core.Log.trace_method_result(
        'pyaudio', 'load successful.'
    )

    # noinspection PyUnresolvedReferences
    import pyaudio
    # noinspection PyUnresolvedReferences
    import pydub
