# coding:utf-8
import sys

import os

import math

import numpy as np

from .wrap import *

from . import base as _base


class Image(object):
    def __init__(self, image_path):
        self._image_path = image_path

    def get_average_rgb_array(self, num_blocks_x=2, num_blocks_y=2):
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


class ImageConcat(object):
    def __init__(self, input_image_paths, output_image_path):
        self._input_image_paths = input_image_paths
        self._output_image_path = output_image_path
    
    @classmethod
    def resize_and_crop(cls, image, max_size=512):
        height, width = image.shape[:2]

        size = min(height, width)

        top = (height-size)//2
        left = (width-size)//2

        cropped_image = image[top:top+size, left:left+size]

        if size > max_size:
            cropped_image = cv2.resize(cropped_image, (max_size, max_size))

        if cropped_image.shape[2] != 3:
            cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2RGB)

        cropped_image = cropped_image.astype(np.uint8)

        return cropped_image
    
    @classmethod
    def create_auto_grid(cls, images, max_size=512):
        num_images = len(images)

        grid_size = int(math.floor(math.sqrt(num_images)))

        total_cells = grid_size*grid_size

        blank_image = np.ones((max_size//grid_size, max_size//grid_size, 3), dtype=np.uint8)*0

        cropped_images = [cls.resize_and_crop(img, max_size//grid_size) for img in images]

        while len(cropped_images) < total_cells:
            cropped_images.append(blank_image)

        rows = []
        for i in range(0, total_cells, grid_size):
            row_images = cropped_images[i:i+grid_size]

            row_images = [cv2.resize(img, (max_size, max_size)) for img in row_images]

            rows.append(cv2.hconcat(row_images))

        cv_img = cv2.vconcat(rows)

        cv_img = cv2.resize(cv_img, (max_size, max_size))

        return cv_img

    def create(self):
        images = [cv2.imread(x) for x in self._input_image_paths]
        return self.create_auto_grid(images)

    def execute(self):
        cv_img = self.create()

        _base.CvUtil.save_image(cv_img, self._output_image_path)

    def show_result(self):
        cv_img = self.create()

        cv2.imshow('Auto Grid', cv_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
