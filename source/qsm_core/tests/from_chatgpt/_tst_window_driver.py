# coding:utf-8
import ctypes
import os


def get_full_mapped_path(drive_letter):
    """
    获取指定盘符映射的完整路径，包括本地磁盘路径或网络路径。

    :param drive_letter: 盘符（如 "Z:"）
    :return: 完整的本地路径或网络路径
    """
    # 确保盘符格式正确
    if not drive_letter.endswith(":"):
        drive_letter += ":"

    # 检查盘符是否已映射到本地路径
    # if os.path.exists(drive_letter):
    #     # 如果是本地路径，直接返回盘符
    #     return drive_letter

    # 如果是网络映射驱动器，则使用 WNetGetConnection 获取网络路径
    remote_name = ctypes.create_unicode_buffer(260)
    buffer_size = ctypes.c_ulong(ctypes.sizeof(remote_name))

    # 调用 WNetGetConnectionW 获取网络路径
    result = ctypes.windll.mpr.WNetGetConnectionW(
        ctypes.c_wchar_p(drive_letter),
        remote_name,
        ctypes.byref(buffer_size)
    )

    if result == 0:  # NO_ERROR
        return remote_name.value
    else:
        raise ctypes.WinError(result)


# 示例使用
try:
    mapped_path = get_full_mapped_path("Z:")
    print(u"The full mapped path for Z: is: {}".format(mapped_path))  # 确保所有字符串为 Unicode
except Exception as e:
    # 将异常转换为字符串，并显式编码为 UTF-8
    print(u"Error: {}".format(unicode(e).encode("utf-8")))
