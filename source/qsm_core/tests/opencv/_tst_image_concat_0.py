# coding:utf-8
import cv2

import numpy as np

import math

# 读取四张图片
img1 = cv2.imread('Z:/temporaries/image_concat_test/max.png')
img2 = cv2.imread('Z:/temporaries/image_concat_test/max.png')
img3 = cv2.imread('Z:/temporaries/image_concat_test/snook.png')
img4 = cv2.imread('Z:/temporaries/image_concat_test/snook.png')


def resize_and_crop(image, max_size=512):
    # 获取图片的高度和宽度
    height, width = image.shape[:2]

    # 计算裁剪的大小
    size = min(height, width)

    # 计算裁剪区域的起始位置，使裁剪为正方形
    top = (height-size)//2
    left = (width-size)//2

    # 裁剪中心部分并得到正方形图像
    cropped_image = image[top:top+size, left:left+size]

    # 缩放图片到最大尺寸 512x512
    if size > max_size:
        cropped_image = cv2.resize(cropped_image, (max_size, max_size))

    # 强制转换为3通道RGB并确保数据类型一致
    if cropped_image.shape[2] != 3:
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2RGB)

    # 确保所有图像的数据类型是 uint8
    cropped_image = cropped_image.astype(np.uint8)

    return cropped_image


def create_auto_grid(images, max_size=512):
    num_images = len(images)

    # 计算网格的行数和列数
    grid_size = math.ceil(math.sqrt(num_images))  # 计算网格的维度
    grid_rows = grid_size
    grid_cols = grid_size
    print(grid_size)

    print(math.floor(math.sqrt(num_images)), math.ceil(math.sqrt(num_images)))

    if num_images <= 3:
        grid_rows = grid_cols = 1
    elif num_images <= 8:
        grid_rows = grid_cols = 2
    elif num_images <= 15:
        grid_rows = grid_cols = 3
    elif num_images <= 24:
        grid_rows = grid_cols = 4
    elif num_images <= 35:
        grid_rows = grid_cols = 5
    else:
        grid_rows = grid_cols = 6

    # 计算总格子的数量
    total_cells = grid_rows*grid_cols

    # 生成一个空白图像来填充空白位置 (这里使用白色填充)
    blank_image = np.ones((max_size, max_size, 3), dtype=np.uint8)*255

    # 裁剪并缩放每张图片，并强制转换为3通道图像
    cropped_images = [resize_and_crop(img, max_size) for img in images]

    # 如果图片数量不足，填充空白图像
    while len(cropped_images) < total_cells:
        cropped_images.append(blank_image)

    # 将图片排列成网格
    rows = []
    for i in range(0, total_cells, grid_cols):
        row_images = cropped_images[i:i+grid_cols]

        # 确保每一行的图片大小一致
        row_images = [cv2.resize(img, (max_size, max_size)) for img in row_images]

        # 水平拼接每行
        rows.append(cv2.hconcat(row_images))

    # 垂直拼接所有行
    result = cv2.vconcat(rows)

    result = cv2.resize(result, (max_size, max_size))

    return result


# 将图片放入一个列表中
images = [
    img1,
    img2,
    img3,
    img4,
    img3,
    # img4,
    # img3,
    # img4,
    # img4,
]  # 你可以根据需要传入任意数量的图片

# 创建自动网格拼接图像
result = create_auto_grid(images)

# 显示结果
cv2.imshow('Auto Grid', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存结果
cv2.imwrite('output_auto_grid.jpg', result)

