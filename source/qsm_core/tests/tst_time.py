# coding:utf-8
import lxbasic.core as bsc_core

import ctypes

import uuid

lib = ctypes.windll.rpcrt4


b = ctypes.create_string_buffer(16)

_UuidCreate = getattr(lib, 'UuidCreateSequential', getattr(lib, 'UuidCreate', None))
_UuidCreate(b)

bytes_ = b.raw

int_ = long(('%02x'*16) % tuple(map(ord, bytes_)), 16)

hex_ = '%032x' % int_

print hex_

# print bsc_core.RawIntegerOpt(100).set_encode_to_36()
#
# print bsc_core.RawIntegerOpt(100).set_encode_to_36()

# for i in range(10):
#     print str(uuid.uuid1()).upper()


