# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import numpy as np
import cv2
from pydub import AudioSegment

def get_waveform_data(wav_path):
    # 使用 pydub 加载音频文件
    audio = AudioSegment.from_file(wav_path)
    n_channels = audio.channels
    frame_rate = audio.frame_rate
    samples = np.array(audio.get_array_of_samples())

    # 如果是立体声，将样本分开
    if n_channels == 2:
        samples = samples.reshape((-1, 2))

    return samples, frame_rate, audio.duration_seconds, n_channels

def draw_waveform_combined(waveform, img_width, img_height, n_channels):
    img = np.ones((img_height, img_width, 3), dtype=np.uint8)*47
    mid_y = img_height // 2
    max_value = np.max(np.abs(waveform))
    step = len(waveform) // img_width

    for i in range(img_width):
        index = i * step
        if index < len(waveform):
            # 获取当前声道的样本值
            left_value = waveform[index, 0] if n_channels == 2 else waveform[index]
            y_value = int((float(left_value)/float(max_value))*(mid_y-1))
            cv2.line(img, (i, mid_y), (i, mid_y-y_value), (127, 255, 63), 1)  # 左声道（蓝色）

            if n_channels == 2 and index+1 < len(waveform):
                right_value = waveform[index, 1]
                right_y_value = int((float(right_value)/float(max_value))*(mid_y-1))
                cv2.line(img, (i, mid_y), (i, mid_y+right_y_value), (63, 127, 255), 1)  # 右声道（红色）

    return img


def save_waveform_image(img, output_path):
    cv2.imwrite(output_path, img)

def main(wav_path, output_path):
    waveform, frame_rate, duration, n_channels = get_waveform_data(wav_path)

    img_height = 256  # 固定高度
    img_width = int(len(waveform) / 256)  # 根据样本数计算宽度

    waveform_img = draw_waveform_combined(waveform, img_width, img_height, n_channels)
    save_waveform_image(waveform_img, output_path)


if __name__ == '__main__':
    # 示例调用
    wav_path = 'Z:/temporaries/tst_wav/test-1.mp3'
    output_path = 'Z:/temporaries/tst_wav/test-1.png'
    main(wav_path, output_path)
