# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

import wave
import numpy as np
import cv2
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

def convert_mp3_to_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    temp_wav = NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

def get_waveform_data(wav_path):
    wav_file = wave.open(wav_path, "r")
    frames = wav_file.getnframes()
    framerate = wav_file.getframerate()
    duration = frames / float(framerate)
    audio_data = wav_file.readframes(frames)
    waveform = np.frombuffer(audio_data, dtype=np.int16)
    wav_file.close()
    return waveform, duration

def create_waveform_image(waveform, duration, img_width=800, img_height=200):
    # 创建一个空白的黑色图像 (背景)
    img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    mid_y = img_height//2
    step = len(waveform)//img_width
    max_value = np.max(np.abs(waveform))

    color = (0, 255, 0)

    for i in range(img_width):
        index = i*step
        if index < len(waveform):
            y_value = int((float(waveform[index])/float(max_value))*(mid_y-1))
            # 画填充线
            cv2.line(img, (i, mid_y-y_value), (i, mid_y), color, 1)
            cv2.line(img, (i, mid_y), (i, mid_y+y_value), color, 1)

    return img


def save_waveform_image(img, output_path="Z:/temporaries/tst_wav/iamge-2.png"):
    # 使用 OpenCV 保存图片
    cv2.imwrite(output_path, img)
    print "波形图已保存为 {}".format(output_path)


def main(mp3_path):
    wav_path = convert_mp3_to_wav(mp3_path)
    waveform, duration = get_waveform_data(wav_path)

    # 创建波形图
    img = create_waveform_image(waveform, duration)

    # 保存波形图为图片文件
    save_waveform_image(img)

def main2(wav_path):
    waveform, duration = get_waveform_data(wav_path)

    # 创建波形图
    img = create_waveform_image(waveform, duration)

    # 保存波形图为图片文件
    save_waveform_image(img)



if __name__ == "__main__":
    mp3_path = "Z:/temporaries/tst_wav/755114__yellowtree__snare-roomsmashedv2.wav"  # 替换为你的音频文件路径
    main2(mp3_path)
    print get_waveform_data(mp3_path)

