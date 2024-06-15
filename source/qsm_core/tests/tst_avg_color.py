# coding:utf-8
import cv2
import numpy as np

# 读取图像
image = cv2.imread('E:/myworkspace/qosmic-2.0/source/qsm_resource/resources/icons/application/maya.png')

# 检查图像是否成功读取
if image is None:
    print('Error: unable to load image')
else:
    # 获取图像的高度和宽度
    height, width = image.shape[:2]

    # 设定分块的数量（这里分成4x4的块）
    num_blocks_x = 4
    num_blocks_y = 4

    # 计算每个块的宽度和高度
    block_width = width//num_blocks_x
    block_height = height//num_blocks_y

    # 存储每个块的平均颜色
    avg_colors = []

    # 循环遍历每个块
    for i in range(num_blocks_y):
        for j in range(num_blocks_x):
            # 计算当前块的左上角和右下角的坐标
            x_start = j*block_width
            y_start = i*block_height
            x_end = x_start+block_width
            y_end = y_start+block_height

            # 获取当前块
            block = image[y_start:y_end, x_start:x_end]

            # 计算当前块的平均颜色
            avg_color = cv2.mean(block)

            # 检查图像是否有alpha通道
            if len(image.shape) == 2 or image.shape[2] == 3:
                # 如果没有alpha通道
                avg_color = avg_color[:3]

            # 存储平均颜色
            avg_colors.append(avg_color)

    # 打印所有块的平均颜色
    for idx, color in enumerate(avg_colors):
        print("Block {} average color (B, G, R): {}".format(idx+1, color))
