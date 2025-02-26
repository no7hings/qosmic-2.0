# coding:utf-8
import pkgutil as _pkgutil

import lxbasic.log as _log_core

CRYPTO_FLAG = False

_module = _pkgutil.find_loader('cryptography')

if _module:
    CRYPTO_FLAG = True

    _log_core.Log.trace_method_result(
        'cryptography', 'load successful'
    )

    # noinspection PyUnresolvedReferences
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    # noinspection PyUnresolvedReferences
    from cryptography.hazmat.backends import default_backend
    # noinspection PyUnresolvedReferences
    from cryptography.hazmat.primitives import padding, hashes
