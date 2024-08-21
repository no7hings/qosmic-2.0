# coding:utf-8
from __future__ import division

import sys

import os

import six

import re

import subprocess

from . import base as _base


class BscFfmpeg(object):
    """
ffmpeg version 7.0.1-essentials_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-zlib --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-sdl2 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libgme --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libtheora --enable-libvo-amrwbenc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-librubberband
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
Universal media converter
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Getting help:
    -h      -- print basic options
    -h long -- print more options
    -h full -- print all options (including all format and codec specific options, very long)
    -h type=name -- print all options for the named decoder/encoder/demuxer/muxer/filter/bsf/protocol
    See man ffmpeg for detailed description of the options.

Per-stream options can be followed by :<stream_spec> to apply that option to specific streams only. <stream_spec> can be a stream index, or v/a/s for video/audio/subtitle (see manual for full syntax).

Print help / information / capabilities:
-L                  show license
-h <topic>          show help
-version            show version
-muxers             show available muxers
-demuxers           show available demuxers
-devices            show available devices
-decoders           show available decoders
-encoders           show available encoders
-filters            show available filters
-pix_fmts           show available pixel formats
-layouts            show standard channel layouts
-sample_fmts        show available audio sample formats

Advanced information / capabilities:
-? <topic>          show help
-help <topic>       show help
--help <topic>      show help
-buildconf          show build configuration
-formats            show available formats
-codecs             show available codecs
-bsfs               show available bit stream filters
-protocols          show available protocols
-dispositions       show available stream dispositions
-colors             show available color names
-sources <device>   list sources of the input device
-sinks <device>     list sinks of the output device
-hwaccels           show available HW acceleration methods

Global options (affect whole program instead of just one file):
-v <loglevel>       set logging level
-y                  overwrite output files
-n                  never overwrite output files
-stats              print progress report during encoding

Advanced global options:
-loglevel <loglevel>  set logging level
-report             generate a report
-max_alloc <bytes>  set maximum size of a single allocated block
-cpuflags <flags>   force specific cpu flags
-cpucount <count>   force specific cpu count
-hide_banner <hide_banner>  do not show program banner
-ignore_unknown     Ignore unknown stream types
-copy_unknown       Copy unknown stream types
-recast_media       allow recasting stream type in order to force a decoder of different media type
-benchmark          add timings for benchmarking
-benchmark_all      add timings for each task
-progress <url>     write program-readable progress information
-stdin              enable or disable interaction on standard input
-timelimit <limit>  set max runtime in seconds in CPU user time
-dump               dump each input packet
-hex                when dumping packets, also dump the payload
-frame_drop_threshold <>  frame drop threshold
-copyts             copy timestamps
-start_at_zero      shift input timestamps to start at 0 when using copyts
-copytb <mode>      copy input stream time base when stream copying
-dts_delta_threshold <threshold>  timestamp discontinuity delta threshold
-dts_error_threshold <threshold>  timestamp error delta threshold
-xerror <error>     exit on error
-abort_on <flags>   abort on the specified condition flags
-filter_threads     number of non-complex filter threads
-filter_complex <graph_description>  create a complex filtergraph
-filter_complex_threads  number of threads for -filter_complex
-lavfi <graph_description>  create a complex filtergraph
-filter_complex_script <filename>  deprecated, use -/filter_complex instead
-auto_conversion_filters  enable automatic conversion filters globally
-stats_period <time>  set the period at which ffmpeg updates stats and -progress output
-debug_ts           print timestamp debugging info
-max_error_rate <maximum error rate>  ratio of decoding errors (0.0: no errors, 1.0: 100% errors) above which ffmpeg returns an error instead of success.
-vstats             dump video coding statistics to file
-vstats_file <file>  dump video coding statistics to file
-vstats_version     Version of the vstats format to use.
-sdp_file <file>    specify a file in which to print sdp information
-vaapi_device <device>  set VAAPI hardware device (DirectX adapter index, DRM path or X11 display name)
-qsv_device <device>  set QSV hardware device (DirectX adapter index, DRM path or X11 display name)
-init_hw_device <args>  initialise hardware device
-filter_hw_device <device>  set hardware device used when filtering
-adrift_threshold <threshold>  deprecated, does nothing
-qphist             deprecated, does nothing
-vsync <>           set video sync method globally; deprecated, use -fps_mode

Per-file options (input and output):
-f <fmt>            force container format (auto-detected otherwise)
-t <duration>       stop transcoding after specified duration
-to <time_stop>     stop transcoding after specified time is reached
-ss <time_off>      start transcoding at specified time

Advanced per-file options (input and output):
-bitexact           bitexact mode
-thread_queue_size  set the maximum number of queued packets from the demuxer


Advanced per-file options (input-only):
-sseof <time_off>   set the start time offset relative to EOF
-seek_timestamp     enable/disable seeking by timestamp with -ss
-accurate_seek      enable/disable accurate seeking with -ss
-isync <sync ref>   Indicate the input index for sync reference
-itsoffset <time_off>  set the input ts offset
-re <>              read input at native frame rate; equivalent to -readrate 1
-readrate <speed>   read input at specified rate
-readrate_initial_burst <seconds>  The initial amount of input to burst read before imposing any readrate
-dump_attachment[:<spec>] <filename>  extract an attachment into a file
-stream_loop <loop count>  set number of times input stream shall be looped
-find_stream_info   read and decode the streams to fill missing information with heuristics

Per-file options (output-only):
-metadata[:<spec>] <key=value>  add metadata

Advanced per-file options (output-only):
-map <[-]input_file_id[:stream_specifier][,sync_file_id[:stream_specifier]]>  set input stream mapping
-map_metadata[:<spec>] <outfile[,metadata]:infile[,metadata]>  set metadata information of outfile from infile
-map_chapters <input_file_index>  set chapters mapping
-fs <limit_size>    set the limit file size in bytes
-timestamp <time>   set the recording timestamp ('now' to set the current time)
-program[:<spec>] <title=string:st=number...>  add program with specified streams
-stream_group[:<spec>] <id=number:st=number...>  add stream group with specified streams and group type-specific arguments
-dframes <number>   set the number of data frames to output
-target <type>      specify target file type ("vcd", "svcd", "dvd", "dv" or "dv50" with optional prefixes "pal-", "ntsc-" or "film-")
-shortest           finish encoding within shortest input
-shortest_buf_duration  maximum buffering duration (in seconds) for the -shortest option
-qscale <q>         use fixed quality scale (VBR)
-profile <profile>  set profile
-attach <filename>  add an attachment to the output file
-muxdelay <seconds>  set the maximum demux-decode delay
-muxpreload <seconds>  set the initial demux-decode delay
-fpre <filename>    set options from indicated preset file

Per-stream options:
-c[:<stream_spec>] <codec>  select encoder/decoder ('copy' to copy stream without reencoding)
-filter[:<stream_spec>] <filter_graph>  apply specified filters to audio/video

Advanced per-stream options:
-codec[:<stream_spec>] <codec>  alias for -c (select encoder/decoder)
-pre[:<stream_spec>] <preset>  preset name
-itsscale[:<stream_spec>] <scale>  set the input ts scale
-apad[:<stream_spec>] <>  audio pad
-copyinkf[:<stream_spec>]  copy initial non-keyframes
-copypriorss[:<stream_spec>]  copy or discard frames before start time
-frames[:<stream_spec>] <number>  set the number of frames to output
-tag[:<stream_spec>] <fourcc/tag>  force codec tag/fourcc
-q[:<stream_spec>] <q>  use fixed quality scale (VBR)
-filter_script[:<stream_spec>] <filename>  deprecated, use -/filter
-reinit_filter[:<stream_spec>] <>  reinit filtergraph on input parameter changes
-discard[:<stream_spec>] <>  discard
-disposition[:<stream_spec>] <>  disposition
-bits_per_raw_sample[:<stream_spec>] <number>  set the number of bits per raw sample
-stats_enc_pre[:<stream_spec>]  write encoding stats before encoding
-stats_enc_post[:<stream_spec>]  write encoding stats after encoding
-stats_mux_pre[:<stream_spec>]  write packets stats before muxing
-stats_enc_pre_fmt[:<stream_spec>]  format of the stats written with -stats_enc_pre
-stats_enc_post_fmt[:<stream_spec>]  format of the stats written with -stats_enc_post
-stats_mux_pre_fmt[:<stream_spec>]  format of the stats written with -stats_mux_pre
-autorotate[:<stream_spec>]  automatically insert correct rotate filters
-autoscale[:<stream_spec>]  automatically insert a scale filter at the end of the filter graph
-time_base[:<stream_spec>] <ratio>  set the desired time base hint for output stream (1:24, 1:48000 or 0.04166, 2.0833e-5)
-enc_time_base[:<stream_spec>] <ratio>  set the desired time base for the encoder (1:24, 1:48000 or 0.04166, 2.0833e-5). two special values are defined - 0 = use frame rate (video) or sample rate (audio),-1 = match source time base
-bsf[:<stream_spec>] <bitstream_filters>  A comma-separated list of bitstream filters
-max_muxing_queue_size[:<stream_spec>] <packets>  maximum number of packets that can be buffered while waiting for all streams to initialize
-muxing_queue_data_threshold[:<stream_spec>] <bytes>  set the threshold after which max_muxing_queue_size is taken into account

Video options:
-r[:<stream_spec>] <rate>  override input framerate/convert to given output framerate (Hz value, fraction or abbreviation)
-aspect[:<stream_spec>] <aspect>  set aspect ratio (4:3, 16:9 or 1.3333, 1.7777)
-vn                 disable video
-vcodec <codec>     alias for -c:v (select encoder/decoder for video streams)
-vf <filter_graph>  alias for -filter:v (apply filters to video streams)
-b <bitrate>        video bitrate (please use -b:v)

Advanced Video options:
-vframes <number>   set the number of video frames to output
-fpsmax[:<stream_spec>] <rate>  set max frame rate (Hz value, fraction or abbreviation)
-pix_fmt[:<stream_spec>] <format>  set pixel format
-display_rotation[:<stream_spec>] <angle>  set pure counter-clockwise rotation in degrees for stream(s)
-display_hflip[:<stream_spec>]  set display horizontal flip for stream(s) (overrides any display rotation if it is not set)
-display_vflip[:<stream_spec>]  set display vertical flip for stream(s) (overrides any display rotation if it is not set)
-rc_override[:<stream_spec>] <override>  rate control override for specific intervals
-timecode <hh:mm:ss[:;.]ff>  set initial TimeCode value.
-pass[:<stream_spec>] <n>  select the pass number (1 to 3)
-passlogfile[:<stream_spec>] <prefix>  select two pass log file name prefix
-vstats             dump video coding statistics to file
-vstats             dump video coding statistics to file
-vstats_file <file>  dump video coding statistics to file
-vstats_version     Version of the vstats format to use.
-intra_matrix[:<stream_spec>] <matrix>  specify intra matrix coeffs
-inter_matrix[:<stream_spec>] <matrix>  specify inter matrix coeffs
-chroma_intra_matrix[:<stream_spec>] <matrix>  specify intra matrix coeffs
-vtag <fourcc/tag>  force video tag/fourcc
-fps_mode[:<stream_spec>]  set framerate mode for matching video streams; overrides vsync
-force_fps[:<stream_spec>]  force the selected framerate, disable the best supported framerate selection
-force_fps[:<stream_spec>]  force the selected framerate, disable the best supported framerate selection
-streamid <streamIndex:value>  set the value of an outfile streamid
-force_key_frames[:<stream_spec>] <timestamps>  force key frames at specified timestamps
-hwaccel[:<stream_spec>] <hwaccel name>  use HW accelerated decoding
-hwaccel_device[:<stream_spec>] <devicename>  select a device for HW acceleration
-hwaccel_output_format[:<stream_spec>] <format>  select output format used with HW accelerated decoding
-fix_sub_duration_heartbeat[:<stream_spec>]  set this video output stream to be a heartbeat stream for fix_sub_duration, according to which subtitles should be split at random access points
-vpre <preset>      set the video options to the indicated preset
-top[:<stream_spec>] <>  deprecated, use the setfield video filter
-qphist             deprecated, does nothing

Audio options:
-aq <quality>       set audio quality (codec-specific)
-ar[:<stream_spec>] <rate>  set audio sampling rate (in Hz)
-ac[:<stream_spec>] <channels>  set number of audio channels
-an                 disable audio
-acodec <codec>     alias for -c:a (select encoder/decoder for audio streams)
-ab <bitrate>       alias for -b:a (select bitrate for audio streams)
-af <filter_graph>  alias for -filter:a (apply filters to audio streams)

Advanced Audio options:
-aframes <number>   set the number of audio frames to output
-atag <fourcc/tag>  force audio tag/fourcc
-sample_fmt[:<stream_spec>] <format>  set sample format
-channel_layout[:<stream_spec>] <layout>  set channel layout
-ch_layout[:<stream_spec>] <layout>  set channel layout
-guess_layout_max[:<stream_spec>]  set the maximum number of channels to try to guess the channel layout
-apre <preset>      set the audio options to the indicated preset

Subtitle options:
-sn                 disable subtitle
-scodec <codec>     alias for -c:s (select encoder/decoder for subtitle streams)

Advanced Subtitle options:
-stag <fourcc/tag>  force subtitle tag/fourcc
-fix_sub_duration[:<stream_spec>]  fix subtitles duration
-canvas_size[:<stream_spec>] <size>  set canvas size (WxH or abbreviation)
-spre <preset>      set the subtitle options to the indicated preset

Data stream options:
-dcodec <codec>     alias for -c:d (select encoder/decoder for data streams)
-dn                 disable data
    """

    CODING_MAP = dict(
        MPEG4='mpeg4',
        H264='libx264'
    )

    @classmethod
    def get_ffmpeg_source(cls):
        return 'Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin/ffmpeg.exe'

    @classmethod
    def get_ffprobe_source(cls):
        return 'Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin/ffprobe.exe'

    @classmethod
    def generate_video_coding_convert_cmd_script(cls, **kwargs):
        """
        ffmpeg -i input.mp4 -c:v libx264 -r 30 -c:a aac output.mp4
        """
        fps, frame_count = cls.get_frame_args(kwargs['input'])
        kwargs['fps'] = fps
        coding = kwargs.pop('coding') or 'MPEG4'
        kwargs['coding'] = cls.CODING_MAP[coding]
        cmd_args = [
            cls.get_ffmpeg_source(),
            r'-r {fps}',
            r'-i "{input}"',
            r'-vf "fps={fps}"',
            r'-c:v {coding}',
            r'-pix_fmt yuv420p',
            r'-b:v 8000k',
            r'-c:a aac',
            r'-y',
            r'"{output}"'
        ]
        return ' '.join(cmd_args).format(**kwargs)

    @classmethod
    def generate_image_concat_cmd_script(cls, **kwargs):
        """
    cmd = BscFfmpeg.generate_image_concat_cmd_script(
        input='/data/e/workspace/lynxi/test/maya/software-render/render/09/test/image/cam_full_body.####.jpg',
        output='/data/e/workspace/lynxi/test/maya/software-render/render/09/test/cam_full_body.mov',
        fps=24
    )

    BscProcess.execute_with_result(
        cmd
    )
        """
        start_frame = kwargs.pop('start_frame')
        end_frame = kwargs.pop('end_frame')
        coding = kwargs.pop('coding') or 'MPEG4'
        kwargs['coding'] = cls.CODING_MAP[coding]
        return (
            '{bin}'
            ' -v error'
            # input fps
            ' -f concat -safe 0 -r {fps} -i "{input}"'
            # output fps
            ' -vf "fps={fps}"'
            # video coding
            ' -c:v {coding}'
            # color coding
            ' -pix_fmt yuv420p'
            # video bit
            ' -b:v 8000k'
            # override
            ' -y'
            ' "{output}"'
        ).format(
            bin=cls.get_ffmpeg_source(),
            input=cls._create_image_concat_file_list(
                kwargs.pop('input'),
                start_frame=start_frame,
                end_frame=end_frame,
                frame_step=kwargs.get('frame_step')
            ),
            **kwargs
        )

    @classmethod
    def _create_image_concat_file_list(cls, input_file_path, start_frame, end_frame, frame_step):
        data = map(
            lambda x: 'file \'{}\''.format(x),
            cls._completion_image_file_list(input_file_path, start_frame, end_frame, frame_step)
        )
        cache_directory_path = os.path.dirname(input_file_path)
        cache_name_base = os.path.splitext(os.path.basename(input_file_path))[0].replace(
            '####', '{}-{}'.format(start_frame, end_frame)
        )
        cache_f = '{}/{}.files'.format(cache_directory_path, cache_name_base)
        with open(cache_f, 'w') as f:
            f.write('\n'.join(data))
        return cache_f

    @classmethod
    def generate_video_concat_cmd_script(cls, **kwargs):
        input_ = kwargs.pop('input')
        kwargs['input'] = cls._create_video_concat_file_list(input_, kwargs.get('output'))
        return (
            '{bin}'
            ' -f concat -safe 0 -i "{input}"'
            ' -c:v copy'
            ' -y'
            ' "{output}"'
        ).format(
            bin=cls.get_ffmpeg_source(),
            **kwargs
        )

    @classmethod
    def _completion_image_file_list(cls, file_path, start_frame, end_frame, frame_step):
        list_ = []
        directory_path = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        s = re.findall('#', file_name)
        s_c = len(s)
        f_name_cur = None
        if isinstance(frame_step, int):
            for i in range(start_frame, end_frame+1):
                i_f_name = file_name.replace('#'*s_c, str(i).zfill(s_c))
                i_f = '{}/{}'.format(directory_path, i_f_name)
                if os.path.isfile(i_f):
                    if (i-1) % frame_step == 0:
                        f_name_cur = i_f_name
                        list_.append(i_f_name)
                    else:
                        if f_name_cur is not None:
                            list_.append(f_name_cur)
                else:
                    if f_name_cur is not None:
                        list_.append(f_name_cur)
        else:
            for i in range(start_frame, end_frame+1):
                i_f_name = file_name.replace('#'*s_c, str(i).zfill(s_c))
                i_f = '{}/{}'.format(directory_path, i_f_name)
                if os.path.isfile(i_f):
                    f_name_cur = i_f_name
                    list_.append(i_f_name)
                else:
                    if f_name_cur is not None:
                        list_.append(f_name_cur)
        return list_

    @classmethod
    def _create_video_concat_file_list(cls, input_video_paths, output_video_path):
        data = map(
            lambda x: 'file \'{}\''.format(x), input_video_paths
        )
        cache_directory_path = os.path.dirname(output_video_path)
        cache_name_base = os.path.splitext(os.path.basename(output_video_path))[0]
        cache_f = '{}/{}.files'.format(cache_directory_path, cache_name_base)
        with open(cache_f, 'w') as f:
            f.write('\n'.join(data))
        return cache_f

    @classmethod
    def auto_unicode(cls, path):
        if not isinstance(path, six.text_type):
            return path.decode('utf-8')
        return path

    @staticmethod
    def auto_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @classmethod
    def get_frame_args(cls, video_path):
        cmd_args = [
            cls.get_ffprobe_source(),
            '-v error',
            '-select_streams',
            'v:0',
            '-show_entries',
            'stream=r_frame_rate,duration',
            '-of',
            'default=nokey=1:noprint_wrappers=1',
        ]

        cmd_script = '{} "{}"'.format(' '.join(cmd_args), video_path)

        result = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()

        if result.returncode != 0:
            print("Error: ", stderr)
            return None

        lines = stdout.strip().split('\n')
        if len(lines) < 2:
            print("Error: Could not retrieve frame rate and duration.")
            return None

        frame_rate_str = lines[0]
        duration_str = lines[1]

        frame_rate = eval(frame_rate_str)
        if duration_str == 'N/A':
            duration = 0
        else:
            duration = float(duration_str)

        frame_count = int(frame_rate*duration)

        return frame_rate, frame_count

    @classmethod
    def extract_frame(cls, video_path, image_path, frame_index):
        """
Y:/deploy/rez-packages/external/ffmpeg/6.0/platform-windows/bin/ffmpeg.exe -i Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov -vf select=eq(n\,0) -vsync vfr -q:v 2 -y Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.jpg
        """
        try:
            cmd_args = [
                cls.get_ffmpeg_source(),
                r'-i "{}"'.format(video_path),
                r'-vf',
                r'select=eq(n\,{})'.format(frame_index),
                '-vsync vfr', '-q:v 2', '-y',
                '"{}"'.format(image_path)
            ]
            cmd_script = ' '.join(cmd_args)
            subprocess.check_call(cmd_script)
            sys.stdout.write('frame extract to: "{}"\n'.format(image_path))
        except subprocess.CalledProcessError:
            import traceback

            traceback.print_exc()

    @classmethod
    def extract_all_frames(cls, video_path, image_format, width_maximum=None):
        directory_path = os.path.dirname(video_path)
        base = os.path.basename(video_path)
        name_base, ext = os.path.splitext(base)
        image_directory_path = '{}/{}.images'.format(directory_path, name_base)
        image_file_path = '{}/image.%04d.{}'.format(image_directory_path, image_format)
        _base.BscStorage.create_directory(image_directory_path)
        frame_args = cls.get_frame_args(video_path)
        if frame_args:
            cmd_args = [
                cls.get_ffmpeg_source(),
                '-i', video_path,
            ]

            if isinstance(width_maximum, int):
                cmd_args.extend(
                    [
                        '-vf', 'scale={}:-1'.format(width_maximum),
                    ]
                )

            cmd_args.extend(
                [
                    '-vsync vfr', '-q:v 2', '-y',
                    '{}/image.%04d.{}'.format(
                        image_directory_path,
                        image_format
                    )
                ]
            )
            cmd_script = ' '.join(cmd_args)
            subprocess.check_call(cmd_script)
            return image_file_path
