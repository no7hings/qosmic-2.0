# coding:utf-8
import os

import subprocess


class ImageConvert(object):
    BIN_PATH = '/apps/pg/prod/htoa/5.3.0/platform-linux/houdini-18.0.460/scripts/bin'
    def __init__(self):
        os.environ['PATH'] += os.pathsep + self.BIN_PATH
        cmd = 'oiiotool "{}"'.format('--help')

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print p.stdout.readlines()


if __name__ == '__main__':
    ImageConvert()

