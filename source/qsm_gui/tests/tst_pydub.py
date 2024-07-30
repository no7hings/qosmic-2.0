# coding:utf-8
import os

os.environ['PATH'] += ';Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin'

from pydub import utils


print utils.which('ffmpeg')
