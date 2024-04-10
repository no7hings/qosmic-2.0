# coding:utf-8
import os

import lxbasic.core as bsc_core

import lxbasic.texture as bsc_texture
# arnold
from .wrap import *

from . import base as and_cor_base


class AndImageOpt(object):
    @classmethod
    def _get_info(cls, file_path):
        _f = bsc_core.auto_encode(file_path)
        width, height = and_cor_base.AndImage.get_resolution(_f) or (0, 0)
        dic = dict(
            bit=cls._get_bit(_f) or 0,
            type=cls._get_type(_f),
            channel_count=and_cor_base.AndImage.get_channel_count(_f),
            width=width,
            height=height
        )
        return dic

    @staticmethod
    def _get_bit(file_path):
        return and_cor_base.AndImage.get_bit(file_path)

    @staticmethod
    def _get_type(file_path):
        return and_cor_base.AndImage.get_type(file_path)

    @staticmethod
    def _get_channel_count(file_path):
        return and_cor_base.AndImage.get_channel_count(file_path)

    @classmethod
    def _get_is_srgb(cls, file_path):
        return (
            cls._get_bit(file_path) <= 16
            and cls._get_type(file_path) in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)
        )

    @classmethod
    def _get_is_linear(cls, file_path):
        return not cls._get_is_srgb(file_path)

    @classmethod
    def _get_is_8_bit(cls, file_path):
        return cls._get_bit(file_path) <= 8

    @classmethod
    def _get_is_16_bit(cls, file_path):
        return cls._get_bit(file_path) <= 16

    def __init__(self, file_path):
        self._file_path = file_path
        if os.path.isfile(file_path):
            self._file_path = file_path
            self._info = self._get_info(
                self._file_path
            )
        else:
            raise OSError()

    def get_path(self):
        return self._file_path

    path = property(get_path)

    def get_size(self):
        return int(self._info['width']), int(self._info['height'])

    size = property(get_size)

    def get_bit(self):
        return self._info['bit']

    bit = property(get_bit)

    def get_type(self):
        return self._info['type']

    type = property(get_type)

    def get_channel_count(self):
        return self._info['channel_count']

    channel_count = property(get_channel_count)

    def get_is_8_bit(self):
        return self.bit <= 8

    def get_is_16_bit(self):
        return self.bit <= 16


class AndTextureOpt(AndImageOpt):
    """
    maketx -- convert images to tiled, MIP-mapped textures
    OpenImageIO-Arnold 2.2.1 http://www.openimageio.org
    Usage:  maketx [options] file...
        --help                   Print help message
        -v                       Verbose status messages
        -o %s                    Output filename
        --threads %d             Number of threads (default: #cores)
        -u                       Update mode
        --format %s              Specify output file format (default: guess from extension)
        --nchannels %d           Specify the number of output image channels.
        --chnames %s             Rename channels (comma-separated)
        -d %s                    Set the output data format to one of: uint8, sint8, uint16, sint16, half, float
        --tile %d %d             Specify tile size
        --separate               Use planarconfig separate (default: contiguous)
        --compression %s         Set the compression method (default = zip, if possible)
        --fovcot %f              Override the frame aspect ratio. Default is width/height.
        --wrap %s                Specify wrap mode (black, clamp, periodic, mirror)
        --swrap %s               Specific s wrap mode separately
        --twrap %s               Specific t wrap mode separately
        --resize                 Resize textures to power of 2 (default: no)
        --noresize               Do not resize textures to power of 2 (deprecated)
        --filter %s              Select filter for resizing (choices: box triangle gaussian sharp-gaussian catmull-rom blackman-harris sinc lanczos3 radial-lanczos3 nuke-lanczos6 mitchell bspline disk cubic keys simon rifman, default=box)
        --hicomp                 Compress HDR range before resize, expand after.
        --sharpen %f             Sharpen MIP levels (default = 0.0 = no)
        --nomipmap               Do not make multiple MIP-map levels
        --checknan               Check for NaN/Inf values (abort if found)
        --fixnan %s              Attempt to fix NaN/Inf values in the image (options: none, black, box3)
        --fullpixels             Set the 'full' image range to be the pixel data window
        --Mcamera %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the camera matrix
        --Mscreen %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f
                                 Set the screen matrix
        --prman-metadata         Add prman specific metadata
        --attrib %s %s           Sets metadata attribute (name, value)
        --sattrib %s %s          Sets string metadata attribute (name, value)
        --sansattrib             Write command line into Software & ImageHistory but remove --sattrib and --attrib options
        --constant-color-detect  Create 1-tile textures from constant color inputs
        --monochrome-detect      Create 1-channel textures from monochrome inputs
        --opaque-detect          Drop alpha channel that is always 1.0
        --no-compute-average     Don't compute and store average color
        --ignore-unassoc         Ignore unassociated alpha tags in input (don't autoconvert)
        --runstats               Print runtime statistics
        --mipimage %s            Specify an individual MIP level
    Basic modes (default is plain texture):
        --shadow                 Create shadow map
        --envlatl                Create lat/long environment map
        --lightprobe             Create lat/long environment map from a light probe
        --bumpslopes             Create a 6 channels bump-map with height, derivatives and square derivatives from an height or a normal map
        --bumpformat %s          Specify the interpretation of a 3-channel input image for --bumpslopes: "height", "normal" or "auto" (default).
    Color Management Options (OpenColorIO DISABLED)
        --colorconfig %s         Explicitly specify an OCIO configuration file
        --colorconvert %s %s     Apply a color space conversion to the image. If the output color space is not the same bit depth as input color space, it is your responsibility to set the data format to the proper bit depth using the -d option.  (choices: sRGB, linear)
        --unpremult              Unpremultiply before color conversion, then premultiply after the color conversion.  You'll probably want to use this flag if your image contains an alpha channel.
    Configuration Presets
        --prman                  Use PRMan-safe settings for tile size, planarconfig, and metadata.
        --oiio                   Use OIIO-optimized settings for tile size, planarconfig, metadata.
    Arnold Extensions
        --colorengine            Select the color processor engine to use: ocio or syncolor
                                 (default: ocio, available: ocio, syncolor)
        --colorconfig            For OCIO, set the OCIO config (leave empty to use OCIO
                                 environment variable).
                                 For synColor, use this flag twice to set the native and
                                 the custom catalog paths.
    """
    #
    TX_EXT = '.tx'

    def __init__(self, *args, **kwargs):
        super(AndTextureOpt, self).__init__(*args, **kwargs)

    @classmethod
    def get_method_for_color_space_as_aces(cls):
        return bsc_texture.TxrMethodForColorSpaceAsAces.generate_instance()

    @classmethod
    def get_method_for_color_space_as_tx_convert(cls):
        return bsc_texture.TxrMethodForColorSpaceAsTxConvert.generate_instance()

    def get_is_srgb(self):
        return (
            self._info['bit'] <= 16
            and self._info['type'] in (ai.AI_TYPE_BYTE, ai.AI_TYPE_INT, ai.AI_TYPE_UINT)
        )

    def get_is_linear(self):
        return not self.get_is_srgb()

    def get_color_space(self):
        if self.get_is_srgb():
            return bsc_core.BscColorSpaces.SRGB
        return bsc_core.BscColorSpaces.LINEAR

    def generate_path_as_tx(self, search_directory_path=None):
        file_path_src = self._file_path
        #
        name = os.path.basename(file_path_src)
        name_base, ext = os.path.splitext(name)
        directory_path = os.path.dirname(file_path_src)
        if search_directory_path:
            return '{}/{}{}'.format(search_directory_path, name_base, self.TX_EXT)
        return '{}/{}{}'.format(directory_path, name_base, self.TX_EXT)

    def create_unit_tx(
        self, color_space, use_aces, aces_file, aces_color_spaces, aces_render_color_space,
        search_directory_path=None, block=False
    ):
        cmd = self.generate_unit_tx_create_command(
            color_space,
            use_aces,
            aces_file,
            aces_color_spaces,
            aces_render_color_space,
            search_directory_path
        )
        #
        if block is True:
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd
            )
            return True
        else:
            return bsc_core.PrcBaseMtd.set_run(
                cmd
            )

    def generate_unit_tx_create_command(
        self, color_space_src, use_aces, aces_file, aces_color_spaces, aces_render_color_space,
        search_directory_path=None
    ):
        file_path_src = self._file_path
        cmd_args = [
            'maketx',
            '-v',
            '-u',
            '--unpremult',
            '--threads 2',
            '--oiio'
        ]
        if use_aces is True:
            if color_space_src in aces_color_spaces:
                if color_space_src != aces_render_color_space:
                    cmd_args += [
                        '--colorengine ocio',
                        '--colorconfig "{}"'.format(aces_file),
                        #
                        '--colorconvert "{}" "{}"'.format(color_space_src, aces_render_color_space),
                    ]
            else:
                raise TypeError(
                    'file="{}", aces color-space="{}" is not available'.format(
                        file_path_src, color_space_src
                    )
                )
        #
        if search_directory_path:
            file_path_src_tgt = self.generate_path_as_tx(
                search_directory_path
            )
            cmd_args += [
                '-o "{}"'.format(file_path_src_tgt)
            ]
        # etc. jpg to exr
        if self.get_is_srgb() and self.get_is_8_bit():
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa'
            ]
        #
        cmd_args += [
            '"{}"'.format(file_path_src)
        ]
        #
        return ' '.join(cmd_args)

    @classmethod
    def generate_format_convert_as_aces_command(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt):
        option = dict(
            file_src=bsc_core.auto_encode(file_path_src),
            file_tgt=bsc_core.auto_encode(file_path_tgt),
            color_space_src=color_space_src,
            color_space_tgt=color_space_tgt,
            format_tgt=os.path.splitext(file_path_tgt)[-1][1:],
            aces_file=cls.get_method_for_color_space_as_aces().get_ocio_file()
        )

        cmd_args = [
            'maketx',
            # verbose status messages
            '-v',
            # update mode
            '-u',
            # number of output image channels
            # '--nchannels {channel_count_src}',
            '--unpremult',
            '--threads 2',
            '--oiio',
            # do not mip map
            '--nomipmap',
            # color convert
            '--colorengine ocio',
            # '--colorconfig "{}"'.format('/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'),
            '--colorconvert "{color_space_src}" "{color_space_tgt}"',
            '--format {format_tgt}',
            '"{file_src}"',
            '-o "{file_tgt}"'
        ]
        cmd = ' '.join(cmd_args).format(**option)
        return cmd

    @classmethod
    def generate_create_exr_as_acescg_command(
        cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt, use_update_mode=True
    ):
        option = dict(
            file_src=bsc_core.auto_encode(file_path_src),
            file_tgt=bsc_core.auto_encode(file_path_tgt),
            color_space_src=color_space_src,
            color_space_tgt=color_space_tgt,
            format_tgt=os.path.splitext(file_path_tgt)[-1][1:],
            aces_file=cls.get_method_for_color_space_as_aces().get_ocio_file()
        )
        cmd_args = [
            'maketx',
            '"{file_src}"',
            '-o "{file_tgt}"',
            # verbose status messages
            '-v',
            '--unpremult',
            '--threads 2',
            '--oiio',
        ]
        # use update mode
        if use_update_mode is True:
            cmd_args += [
                '-u'
            ]
        # convert color
        if color_space_src != color_space_tgt:
            cmd_args += [
                '--colorengine ocio',
                '--colorconfig "{}"'.format(cls.get_method_for_color_space_as_aces().get_ocio_file()),
                '--colorconvert "{color_space_src}" "{color_space_tgt}"',
            ]
        # format args, etc. jpg to exr
        if cls._get_is_srgb(file_path_src) and cls._get_is_8_bit(file_path_src):
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa',
            ]
        else:
            cmd_args += [
                '--format exr',
            ]
        cmd = ' '.join(cmd_args).format(**option)
        return cmd

    # noinspection PyUnusedLocal
    @classmethod
    def generate_create_tx_as_acescg_command(
        cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt, use_update_mode=True
    ):
        cmd_args = [
            'maketx',
            '"{}"'.format(bsc_core.auto_encode(file_path_src)),
            '-o "{}"'.format(bsc_core.auto_encode(file_path_tgt)),
            '-v',
            '-u',
            '--unpremult',
            '--threads 4',
            '--oiio'
        ]
        # color space args
        if color_space_src != color_space_tgt:
            aces_color_spaces = cls.get_method_for_color_space_as_aces().get_all_color_spaces()
            if color_space_src in aces_color_spaces:
                cmd_args += [
                    '--colorengine ocio',
                    '--colorconfig "{}"'.format(cls.get_method_for_color_space_as_aces().get_ocio_file()),
                    '--colorconvert "{}" "{}"'.format(color_space_src, color_space_tgt),
                ]
            else:
                raise TypeError(
                    'file: "{}", aces color-space: "{}" is not available'.format(
                        file_path_src, color_space_src
                    )
                )
        # format args, etc. jpg to exr
        if cls._get_is_srgb(file_path_src) and cls._get_is_8_bit(file_path_src):
            cmd_args += [
                '--format exr',
                '-d half',
                '--compression dwaa'
            ]
        #
        return ' '.join(cmd_args)
