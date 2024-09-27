# coding:utf-8
import wave
import numpy as np
import cv2


def get_waveform_data(wav_path):
    wav_file = wave.open(wav_path, 'r')
    # with wave.open(wav_path, 'r') as wav_file:
    n_channels = wav_file.getnchannels()   # 声道数
    framerate = wav_file.getframerate()    # 采样率
    n_frames = wav_file.getnframes()       # 总帧数
    duration = n_frames / float(framerate) # 音频时长

    # 读取音频数据
    waveform_data = wav_file.readframes(n_frames)

    # 根据样本宽度处理不同格式
    samp_width = wav_file.getsampwidth()  # 每个样本的字节数
    if samp_width == 1:
        dtype = np.uint8  # 8-bit PCM
        waveform = np.frombuffer(waveform_data, dtype=dtype)
    elif samp_width == 2:
        dtype = np.int16  # 16-bit PCM
        waveform = np.frombuffer(waveform_data, dtype=dtype)
    elif samp_width == 3:
        # 处理 24-bit PCM，每个样本3字节
        waveform = np.frombuffer(waveform_data, dtype=np.uint8)
        waveform = convert_24bit_to_32bit(waveform)
    else:
        raise ValueError("Unsupported sample width: {}".format(samp_width))

    # 如果是立体声（2声道），则需要进行 reshape
    if n_channels == 2:
        waveform = waveform.reshape(-1, 2)

    return waveform, framerate, duration, n_channels

def convert_24bit_to_32bit(waveform):
    """
    将 24-bit PCM 样本转换为 32-bit 整数数组
    """
    # 每个样本3字节，因此需要将每3个字节组合成一个32位整数
    n_samples = len(waveform) // 3
    output = np.zeros(n_samples, dtype=np.int32)

    for i in range(n_samples):
        # 将三个字节组成一个24位整数（加符号扩展到32位）
        sample = waveform[i * 3:i * 3 + 3]
        value = int(sample[0]) | (int(sample[1]) << 8) | (int(sample[2]) << 16)

        # 处理符号位，如果第24位为1，则负值
        if value & 0x800000:  # 0x800000 是24位数最高位的掩码
            value -= 0x1000000  # 符号扩展到32位负数

        output[i] = value

    return output

def split_channels(waveform, n_channels):
    if n_channels == 2:
        # 立体声（两个声道）
        left_channel = waveform[:, 0]
        right_channel = waveform[:, 1]
        return left_channel, right_channel
    else:
        # 单声道
        return waveform, None

def draw_waveform(waveform, img_width, img_height, color):
    img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255
    mid_y = img_height // 2
    max_value = np.max(np.abs(waveform))
    step = len(waveform) // img_width

    for i in range(img_width):
        index = i * step
        if index < len(waveform):
            y_value = int((float(waveform[index]) / float(max_value)) * (mid_y - 1))
            cv2.line(img, (i, mid_y - y_value), (i, mid_y + y_value), color, 1)

    return img

def draw_stereo_waveform(left_channel, right_channel, img_width, img_height):
    left_color = (255, 0, 0)   # 蓝色
    right_color = (0, 0, 255)  # 红色
    img = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255

    # 绘制左声道
    left_waveform_img = draw_waveform(left_channel, img_width, img_height // 2, left_color)
    img[:img_height // 2, :] = left_waveform_img

    # 绘制右声道
    if right_channel is not None:
        right_waveform_img = draw_waveform(right_channel, img_width, img_height // 2, right_color)
        img[img_height // 2:, :] = right_waveform_img

    return img


def draw_waveform_combined(waveform, img_width, img_height):
    img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    mid_y = img_height // 2
    max_value = np.max(np.abs(waveform))
    step = len(waveform) // img_width

    for i in range(img_width):
        index = i * step
        if index < len(waveform):
            y_value = int((float(waveform[index]) / float(max_value)) * (mid_y - 1))
            # 绘制左声道（假设在负半轴）
            cv2.line(img, (i, mid_y), (i, mid_y - y_value), (255, 0, 0), 1)  # 左声道（蓝色）
            # 绘制右声道（假设在正半轴）
            if index + 1 < len(waveform):
                right_value = int((float(waveform[index + 1]) / float(max_value)) * (mid_y - 1))
                cv2.line(img, (i, mid_y), (i, mid_y + right_value), (0, 0, 255), 1)  # 右声道（红色）

    return img


def save_waveform_image(img, output_path):
    cv2.imwrite(output_path, img)


def main(wav_path, output_path):
    waveform, framerate, duration, n_channels = get_waveform_data(wav_path)

    if n_channels == 2:
        left_channel = waveform[:, 0]
        right_channel = waveform[:, 1]
        # 合并为单个波形数据
        combined_waveform = np.empty((len(left_channel)+len(right_channel),), dtype=np.int32)
        combined_waveform[0::2] = left_channel
        combined_waveform[1::2] = right_channel
    else:
        combined_waveform = waveform

    img_height = 256  # 固定高度
    img_width = int(len(combined_waveform)/256)

    waveform_img = draw_waveform_combined(combined_waveform, img_width, img_height)
    save_waveform_image(waveform_img, output_path)


if __name__ == '__main__':
    # 示例调用
    wav_path = 'Z:/temporaries/tst_wav/754770__hewnmarrow__drum-beat-001-fx-006.wav'
    output_path = 'Z:/temporaries/tst_wav/test.png'
    main(wav_path, output_path)
