# coding:utf-8
import os

from .wrap import *


class CvUtil:
    @classmethod
    def save_image(cls, cv_img, file_path):
        # create directory first
        directory_path = os.path.dirname(file_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        file_path = file_path.encode('mbcs')
        cv2.imwrite(file_path, cv_img)
