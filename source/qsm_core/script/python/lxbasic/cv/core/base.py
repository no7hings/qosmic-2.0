# coding:utf-8
import os

from .wrap import *


class CvUtil:
    @classmethod
    def save_image(cls, cv_img, file_path):
        import lxbasic.core as bsc_core

        # create directory first
        directory_path = os.path.dirname(file_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        file_path = bsc_core.ensure_unicode(file_path)
        file_path = bsc_core.ensure_mbcs(file_path)
        cv2.imwrite(file_path, cv_img)
