# coding:utf-8
import sys

from .wrap import *


class Image(object):
    def __init__(self, image_path):
        self._image_path = image_path

    def get_average_rgbs(self, num_blocks_x=2, num_blocks_y=2):
        image = cv2.imread(self._image_path)
        if image is None:
            sys.stderr.write('Error: unable to load image\n')
            return []
        else:
            height, width = image.shape[:2]

            block_width = width//num_blocks_x
            block_height = height//num_blocks_y

            avg_rgb_lst = []

            for i in range(num_blocks_y):
                for j in range(num_blocks_x):
                    i_start_x = j*block_width
                    i_start_y = i*block_height
                    i_end_x = i_start_x+block_width
                    i_end_y = i_start_y+block_height

                    i_block = image[i_start_y:i_end_y, i_start_x:i_end_x]

                    i_avg_rgb = cv2.mean(i_block)

                    if len(image.shape) == 2 or image.shape[2] == 3:
                        i_avg_rgb = i_avg_rgb[:3]
                    avg_rgb_lst.append(i_avg_rgb)
            return avg_rgb_lst
