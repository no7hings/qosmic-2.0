# coding:utf-8
import cv2
import os

# 图片文件夹路径和文件名模板
image_folder = 'C:/Users/nothings/.qosmic/temporary/2024_0628/C8AF519E-350B-11EF-9A8F-4074E0DA267B'
video_name = 'C:/Users/nothings/.qosmic/temporary/2024_0628/C8AF519E-350B-11EF-9A8F-4074E0DA267B/video-8.mov'

# 获取图片文件夹中的所有图片文件名并按顺序排序
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort()

# 获取第一张图片的宽高信息
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, channels = frame.shape

# 定义视频编码器并创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用H.264编码器
video = cv2.VideoWriter(video_name, fourcc, 30, (width, height))

# 遍历图片并将其写入视频对象
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

# 释放VideoWriter对象并关闭所有窗口
video.release()
cv2.destroyAllWindows()
