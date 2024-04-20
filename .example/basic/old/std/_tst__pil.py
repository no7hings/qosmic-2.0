# coding:utf-8
from PIL import Image

from PySide2 import QtGui


i = Image.open('/production/library/resource/all/3d_asset/parking_meter_ujpkaadfa/v0001/image/preview.png')


def align8to32(bytes, width, mode):
    """
    converts each scanline of data from 8 bit to 32 bit aligned
    """

    bits_per_pixel = {"1": 1, "L": 8, "P": 8}[mode]

    # calculate bytes per line and the extra padding if needed
    bits_per_line = bits_per_pixel * width
    full_bytes_per_line, remaining_bits_per_line = divmod(bits_per_line, 8)
    bytes_per_line = full_bytes_per_line + (1 if remaining_bits_per_line else 0)

    extra_padding = -bytes_per_line % 4

    # already 32 bit aligned by luck
    if not extra_padding:
        return bytes

    new_data = []
    for i in range(len(bytes) // bytes_per_line):
        new_data.append(
            bytes[i * bytes_per_line : (i + 1) * bytes_per_line]
            + b"\x00" * extra_padding
        )
    return b"".join(new_data)


def _toqclass_helper(im):
    data = None
    colortable = None
    im = Image.open(im)

    if im.mode == "1":
        format = QtGui.QImage.Format_Mono
    elif im.mode == "L":
        format = QtGui.QImage.Format_Indexed8
        colortable = []
        for i in range(256):
            colortable.append(QtGui.qRgb(i, i, i))
    elif im.mode == "P":
        format = QtGui.QImage.Format_Indexed8
        colortable = []
        palette = im.getpalette()
        for i in range(0, len(palette), 3):
            colortable.append(QtGui.qRgb(*palette[i : i + 3]))
    elif im.mode == "RGB":
        data = im.tobytes("raw", "BGRX")
        format = QtGui.QImage.Format_RGB32
    elif im.mode == "RGBA":
        try:
            data = im.tobytes("raw", "BGRA")
        except SystemError:
            # workaround for earlier versions
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        format = QtGui.QImage.Format_ARGB32
    else:
        raise ValueError("unsupported image mode %r" % im.mode)

    __data = data or align8to32(im.tobytes(), im.size[0], im.mode)
    return {"data": __data, "im": im, "format": format, "colortable": colortable}
