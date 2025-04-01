# coding:utf-8
from __future__ import division

import json

import os

import sys

import six

import re

import subprocess

import tempfile

from . import base as _base


class BscFfmpegVideo(object):
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

    class Coding:
        """
        Encoders:
         V..... = Video
         A..... = Audio
         S..... = Subtitle
         .F.... = Frame-level multithreading
         ..S... = Slice-level multithreading
         ...X.. = Codec is experimental
         ....B. = Supports draw_horiz_band
         .....D = Supports direct rendering method 1
         ------
         V....D a64multi             Multicolor charset for Commodore 64 (codec a64_multi)
         V....D a64multi5            Multicolor charset for Commodore 64, extended with 5th color (colram) (codec a64_multi5)
         V....D alias_pix            Alias/Wavefront PIX image
         V..... amv                  AMV Video
         V....D apng                 APNG (Animated Portable Network Graphics) image
         V....D asv1                 ASUS V1
         V....D asv2                 ASUS V2
         V....D libaom-av1           libaom AV1 (codec av1)
         V....D av1_nvenc            NVIDIA NVENC av1 encoder (codec av1)
         V..... av1_qsv              AV1 (Intel Quick Sync Video acceleration) (codec av1)
         V....D av1_amf              AMD AMF AV1 encoder (codec av1)
         V....D av1_vaapi            AV1 (VAAPI) (codec av1)
         V....D avrp                 Avid 1:1 10-bit RGB Packer
         V..X.D avui                 Avid Meridien Uncompressed
         VF...D bitpacked            Bitpacked
         V....D bmp                  BMP (Windows and OS/2 bitmap)
         VF...D cfhd                 GoPro CineForm HD
         V....D cinepak              Cinepak
         V....D cljr                 Cirrus Logic AccuPak
         V.S..D vc2                  SMPTE VC-2 (codec dirac)
         VFS..D dnxhd                VC3/DNxHD
         V....D dpx                  DPX (Digital Picture Exchange) image
         VFS..D dvvideo              DV (Digital Video)
         VFS..D dxv                  Resolume DXV
         VF...D exr                  OpenEXR image
         V.S..D ffv1                 FFmpeg video codec #1
         VF...D ffvhuff              Huffyuv FFmpeg variant
         V....D fits                 Flexible Image Transport System
         V....D flashsv              Flash Screen Video
         V....D flashsv2             Flash Screen Video Version 2
         V..... flv                  FLV / Sorenson Spark / Sorenson H.263 (Flash Video) (codec flv1)
         V....D gif                  GIF (Graphics Interchange Format)
         V..... h261                 H.261
         V..... h263                 H.263 / H.263-1996
         V.S... h263p                H.263+ / H.263-1998 / H.263 version 2
         V....D libx264              libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (codec h264)
         V....D libx264rgb           libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 RGB (codec h264)
         V....D h264_amf             AMD AMF H.264 Encoder (codec h264)
         V....D h264_mf              H264 via MediaFoundation (codec h264)
         V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
         V..... h264_qsv             H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (Intel Quick Sync Video acceleration) (codec h264)
         V....D h264_vaapi           H.264/AVC (VAAPI) (codec h264)
         VF...D hdr                  HDR (Radiance RGBE format) image
         V....D libx265              libx265 H.265 / HEVC (codec hevc)
         V....D hevc_amf             AMD AMF HEVC encoder (codec hevc)
         V....D hevc_mf              HEVC via MediaFoundation (codec hevc)
         V....D hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
         V..... hevc_qsv             HEVC (Intel Quick Sync Video acceleration) (codec hevc)
         V....D hevc_vaapi           H.265/HEVC (VAAPI) (codec hevc)
         VF...D huffyuv              Huffyuv / HuffYUV
         VF...D jpeg2000             JPEG 2000
         VF.... libopenjpeg          OpenJPEG JPEG 2000 (codec jpeg2000)
         VF...D jpegls               JPEG-LS
         VF...D ljpeg                Lossless JPEG
         VFS..D magicyuv             MagicYUV video
         VFS... mjpeg                MJPEG (Motion JPEG)
         V..... mjpeg_qsv            MJPEG (Intel Quick Sync Video acceleration) (codec mjpeg)
         V....D mjpeg_vaapi          MJPEG (VAAPI) (codec mjpeg)
         V.S... mpeg1video           MPEG-1 video
         V.S... mpeg2video           MPEG-2 video
         V..... mpeg2_qsv            MPEG-2 video (Intel Quick Sync Video acceleration) (codec mpeg2video)
         V....D mpeg2_vaapi          MPEG-2 (VAAPI) (codec mpeg2video)
         V.S... mpeg4                MPEG-4 part 2
         V....D libxvid              libxvidcore MPEG-4 part 2 (codec mpeg4)
         V..... msmpeg4v2            MPEG-4 part 2 Microsoft variant version 2
         V..... msmpeg4              MPEG-4 part 2 Microsoft variant version 3 (codec msmpeg4v3)
         V....D msrle                Microsoft RLE
         V..... msvideo1             Microsoft Video-1
         V....D pam                  PAM (Portable AnyMap) image
         V....D pbm                  PBM (Portable BitMap) image
         V....D pcx                  PC Paintbrush PCX image
         V....D pfm                  PFM (Portable FloatMap) image
         V....D pgm                  PGM (Portable GrayMap) image
         V....D pgmyuv               PGMYUV (Portable GrayMap YUV) image
         V....D phm                  PHM (Portable HalfFloatMap) image
         VF...D png                  PNG (Portable Network Graphics) image
         V....D ppm                  PPM (Portable PixelMap) image
         VF...D prores               Apple ProRes
         VF...D prores_aw            Apple ProRes (codec prores)
         VFS... prores_ks            Apple ProRes (iCodec Pro) (codec prores)
         VF...D qoi                  QOI (Quite OK Image format) image
         V....D qtrle                QuickTime Animation (RLE) video
         V....D r10k                 AJA Kona 10-bit RGB Codec
         V....D r210                 Uncompressed RGB 10-bit
         VF...D rawvideo             raw video
         V....D roqvideo             id RoQ video (codec roq)
         V....D rpza                 QuickTime video (RPZA)
         V..... rv10                 RealVideo 1.0
         V..... rv20                 RealVideo 2.0
         V....D sgi                  SGI image
         V....D smc                  QuickTime Graphics (SMC)
         V....D snow                 Snow
         V..... speedhq              NewTek SpeedHQ
         V....D sunrast              Sun Rasterfile image
         V....D svq1                 Sorenson Vector Quantizer 1 / Sorenson Video 1 / SVQ1
         V....D targa                Truevision Targa image
         V....D libtheora            libtheora Theora (codec theora)
         VF...D tiff                 TIFF image
         VF...D utvideo              Ut Video
         VF...D v210                 Uncompressed 4:2:2 10-bit
         V....D v308                 Uncompressed packed 4:4:4
         V....D v408                 Uncompressed packed QT 4:4:4:4
         V....D v410                 Uncompressed 4:4:4 10-bit
         V.S..D vbn                  Vizrt Binary Image
         V..... vnull                null video
         V....D libvpx               libvpx VP8 (codec vp8)
         V....D vp8_vaapi            VP8 (VAAPI) (codec vp8)
         V....D libvpx-vp9           libvpx VP9 (codec vp9)
         V....D vp9_vaapi            VP9 (VAAPI) (codec vp9)
         V..... vp9_qsv              VP9 video (Intel Quick Sync Video acceleration) (codec vp9)
         VF...D wbmp                 WBMP (Wireless Application Protocol Bitmap) image
         V....D libwebp_anim         libwebp WebP image (codec webp)
         V....D libwebp              libwebp WebP image (codec webp)
         V..... wmv1                 Windows Media Video 7
         V..... wmv2                 Windows Media Video 8
         V..... wrapped_avframe      AVFrame to AVPacket passthrough
         V....D xbm                  XBM (X BitMap) image
         V....D xface                X-face image
         V....D xwd                  XWD (X Window Dump) image
         V....D y41p                 Uncompressed YUV 4:1:1 12-bit
         V....D yuv4                 Uncompressed packed 4:2:0
         VF...D zlib                 LCL (LossLess Codec Library) ZLIB
         V....D zmbv                 Zip Motion Blocks Video
         A....D aac                  AAC (Advanced Audio Coding)
         A....D aac_mf               AAC via MediaFoundation (codec aac)
         A....D ac3                  ATSC A/52A (AC-3)
         A....D ac3_fixed            ATSC A/52A (AC-3) (codec ac3)
         A....D ac3_mf               AC3 via MediaFoundation (codec ac3)
         A....D adpcm_adx            SEGA CRI ADX ADPCM
         A....D adpcm_argo           ADPCM Argonaut Games
         A....D g722                 G.722 ADPCM (codec adpcm_g722)
         A....D g726                 G.726 ADPCM (codec adpcm_g726)
         A....D g726le               G.726 little endian ADPCM ("right-justified") (codec adpcm_g726le)
         A....D adpcm_ima_alp        ADPCM IMA High Voltage Software ALP
         A....D adpcm_ima_amv        ADPCM IMA AMV
         A....D adpcm_ima_apm        ADPCM IMA Ubisoft APM
         A....D adpcm_ima_qt         ADPCM IMA QuickTime
         A....D adpcm_ima_ssi        ADPCM IMA Simon & Schuster Interactive
         A....D adpcm_ima_wav        ADPCM IMA WAV
         A....D adpcm_ima_ws         ADPCM IMA Westwood
         A....D adpcm_ms             ADPCM Microsoft
         A....D adpcm_swf            ADPCM Shockwave Flash
         A....D adpcm_yamaha         ADPCM Yamaha
         A....D alac                 ALAC (Apple Lossless Audio Codec)
         A....D libopencore_amrnb    OpenCORE AMR-NB (Adaptive Multi-Rate Narrow-Band) (codec amr_nb)
         A....D libvo_amrwbenc       Android VisualOn AMR-WB (Adaptive Multi-Rate Wide-Band) (codec amr_wb)
         A..... anull                null audio
         A....D aptx                 aptX (Audio Processing Technology for Bluetooth)
         A....D aptx_hd              aptX HD (Audio Processing Technology for Bluetooth)
         A....D comfortnoise         RFC 3389 comfort noise generator
         A....D dfpwm                DFPWM1a audio
         A..X.D dca                  DCA (DTS Coherent Acoustics) (codec dts)
         A....D eac3                 ATSC A/52 E-AC-3
         A....D flac                 FLAC (Free Lossless Audio Codec)
         A....D g723_1               G.723.1
         A....D libgsm               libgsm GSM (codec gsm)
         A....D libgsm_ms            libgsm GSM Microsoft variant (codec gsm_ms)
         A..X.D mlp                  MLP (Meridian Lossless Packing)
         A....D mp2                  MP2 (MPEG audio layer 2)
         A....D mp2fixed             MP2 fixed point (MPEG audio layer 2) (codec mp2)
         A....D libmp3lame           libmp3lame MP3 (MPEG audio layer 3) (codec mp3)
         A....D mp3_mf               MP3 via MediaFoundation (codec mp3)
         A....D nellymoser           Nellymoser Asao
         A..X.D opus                 Opus
         A....D libopus              libopus Opus (codec opus)
         A....D pcm_alaw             PCM A-law / G.711 A-law
         A....D pcm_bluray           PCM signed 16|20|24-bit big-endian for Blu-ray media
         A....D pcm_dvd              PCM signed 16|20|24-bit big-endian for DVD media
         A....D pcm_f32be            PCM 32-bit floating point big-endian
         A....D pcm_f32le            PCM 32-bit floating point little-endian
         A....D pcm_f64be            PCM 64-bit floating point big-endian
         A....D pcm_f64le            PCM 64-bit floating point little-endian
         A....D pcm_mulaw            PCM mu-law / G.711 mu-law
         A....D pcm_s16be            PCM signed 16-bit big-endian
         A....D pcm_s16be_planar     PCM signed 16-bit big-endian planar
         A....D pcm_s16le            PCM signed 16-bit little-endian
         A....D pcm_s16le_planar     PCM signed 16-bit little-endian planar
         A....D pcm_s24be            PCM signed 24-bit big-endian
         A....D pcm_s24daud          PCM D-Cinema audio signed 24-bit
         A....D pcm_s24le            PCM signed 24-bit little-endian
         A....D pcm_s24le_planar     PCM signed 24-bit little-endian planar
         A....D pcm_s32be            PCM signed 32-bit big-endian
         A....D pcm_s32le            PCM signed 32-bit little-endian
         A....D pcm_s32le_planar     PCM signed 32-bit little-endian planar
         A....D pcm_s64be            PCM signed 64-bit big-endian
         A....D pcm_s64le            PCM signed 64-bit little-endian
         A....D pcm_s8               PCM signed 8-bit
         A....D pcm_s8_planar        PCM signed 8-bit planar
         A....D pcm_u16be            PCM unsigned 16-bit big-endian
         A....D pcm_u16le            PCM unsigned 16-bit little-endian
         A....D pcm_u24be            PCM unsigned 24-bit big-endian
         A....D pcm_u24le            PCM unsigned 24-bit little-endian
         A....D pcm_u32be            PCM unsigned 32-bit big-endian
         A....D pcm_u32le            PCM unsigned 32-bit little-endian
         A....D pcm_u8               PCM unsigned 8-bit
         A....D pcm_vidc             PCM Archimedes VIDC
         A....D real_144             RealAudio 1.0 (14.4K) (codec ra_144)
         A....D roq_dpcm             id RoQ DPCM
         A..X.D s302m                SMPTE 302M
         A....D sbc                  SBC (low-complexity subband codec)
         A..X.D sonic                Sonic
         A..X.D sonicls              Sonic lossless
         A....D libspeex             libspeex Speex (codec speex)
         A..X.D truehd               TrueHD
         A....D tta                  TTA (True Audio)
         A..X.D vorbis               Vorbis
         A....D libvorbis            libvorbis (codec vorbis)
         A....D wavpack              WavPack
         A....D wmav1                Windows Media Audio 1
         A....D wmav2                Windows Media Audio 2
         S..... ssa                  ASS (Advanced SubStation Alpha) subtitle (codec ass)
         S..... ass                  ASS (Advanced SubStation Alpha) subtitle
         S..... dvbsub               DVB subtitles (codec dvb_subtitle)
         S..... dvdsub               DVD subtitles (codec dvd_subtitle)
         S..... mov_text             3GPP Timed Text subtitle
         S..... srt                  SubRip subtitle (codec subrip)
         S..... subrip               SubRip subtitle
         S..... text                 Raw text subtitle
         S..... ttml                 TTML subtitle
         S..... webvtt               WebVTT subtitle
         S..... xsub                 DivX subtitles (XSUB)
        """
        MPEG4 = 'mpeg4'
        H263 = 'h263p'
        H264 = 'libx264'
        H265 = 'libx265'
        H264_QSV = 'h264_qsv'

        TEST = 'prores_ks'

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
        coding = kwargs.pop('coding') or cls.Coding.MPEG4
        kwargs['coding'] = coding
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
    
    # image sequence
    @classmethod
    def generate_image_sequence_concat_cmd_script(cls, **kwargs):
        """
        cmd = BscFfmpegVideo.generate_image_sequence_concat_cmd_script(
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
        coding = kwargs.pop('coding') or cls.Coding.MPEG4

        kwargs['coding'] = coding
        fps = int(kwargs.pop('fps', 24))

        if coding == cls.Coding.H263:
            filter_string = '-vf "fps={fps},scale=trunc(iw/4)*4:trunc(ih/4)*4"'.format(fps=fps)
            coding_string = '-c:v {coding}'.format(coding=coding)
        elif coding == cls.Coding.H264:
            filter_string = '-vf "fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2"'.format(fps=fps)
            coding_string = '-c:v {coding}'.format(coding=coding)
        elif coding == cls.Coding.H265:
            filter_string = '-vf "fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2"'.format(fps=fps)
            coding_string = '-c:v {coding}'.format(coding=coding)
        elif coding == cls.Coding.H264_QSV:
            filter_string = '-vf "fps={fps}"'.format(fps=fps)
            coding_string = '-c:v {coding}'.format(coding=coding)
        else:
            filter_string = '-vf "fps={fps}"'.format(fps=fps)
            coding_string = '-c:v {coding}'.format(coding=coding)

        return (
            '{bin}'
            ' -v error'
            # input fps
            ' -f concat -safe 0 -r {fps} -i "{input}"'
            # output fps -vf "fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2"
            ' {filter_string}'
            # video coding
            ' {coding_string}'
            # color coding
            ' -pix_fmt yuv420p'
            # video bit
            ' -b:v 8000k'
            # fixme: disable bframe?
            ' -bf 0'
            # override
            ' -y'
            ' "{output}"'
        ).format(
            bin=cls.get_ffmpeg_source(),
            input=cls._create_image_sequence_concat_file_list(
                kwargs.pop('input'),
                start_frame=start_frame,
                end_frame=end_frame,
                frame_step=kwargs.get('frame_step'),
            ),
            filter_string=filter_string,
            coding_string=coding_string,
            fps=fps,
            **kwargs
        )

    @classmethod
    def _create_image_sequence_concat_file_list(cls, input_file_path, start_frame, end_frame, frame_step):
        data = map(
            lambda x: 'file \'{}\''.format(x),
            cls._completion_image_sequence_file_list(input_file_path, start_frame, end_frame, frame_step)
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
    def _completion_image_sequence_file_list(cls, file_path, start_frame, end_frame, frame_step):
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
    
    # video
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
        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        cmd_script = '{} "{}"'.format(' '.join(cmd_args), video_path)

        result = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()

        stdout = _base.ensure_unicode(stdout)

        if result.returncode != 0:
            sys.stderr.write(stderr+'\n')
            return None

        lines = stdout.strip().split('\n')
        if len(lines) < 2:
            sys.stderr.write("Error: Could not retrieve frame rate and duration.\n")
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

            cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
            cmd_script = ' '.join(cmd_args)
            s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            s_p.communicate()
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
            cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
            cmd_script = ' '.join(cmd_args)
            s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            s_p.communicate()
            return image_file_path

    @classmethod
    def create_compress(cls, video_path_src, video_path_dst, width_maximum=512, replace=False):
        """
ffmpeg -i input.mp4 -vf "scale=-1:128" -r 24 -vcodec libx264 -crf 28 -preset ultrafast output.mp4
        """
        video_path_src = _base.ensure_unicode(video_path_src)
        video_path_dst = _base.ensure_unicode(video_path_dst)

        if os.path.isfile(video_path_dst) is True:
            if replace is False:
                return

        # create directory first
        directory_path = os.path.dirname(video_path_dst)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        cmd_args = [
            cls.get_ffmpeg_source(),
            six.u(r'-i "{}"').format(video_path_src),
            r'-v error',
            r'-vf',
            r'"scale=trunc({}/2)*2:trunc(ow/a/2)*2"'.format(width_maximum),
            '-r 24', '-vcodec libx264', '-crf 28', '-preset ultrafast', '-y',
            six.u('"{}"').format(video_path_dst)
        ]
        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        cmd_script = ' '.join(cmd_args)
        subprocess.check_call(cmd_script)

    @classmethod
    def concat_by_image_sequence(
        cls,
        image_sequence, video_path, 
        start_frame, end_frame, 
        frame_step=None,
        fps=24, 
        coding='libx264', replace=False
    ):

        video_path = _base.ensure_unicode(video_path)

        if os.path.isfile(video_path) is True:
            if replace is False:
                return

        if coding == cls.Coding.H263:
            filter_string = '"scale=trunc(iw/4)*4:trunc(ih/4)*4"'.format(fps=fps)
        elif coding == cls.Coding.H264:
            filter_string = '"scale=trunc(iw/2)*2:trunc(ih/2)*2"'.format(fps=fps)
        elif coding == cls.Coding.H265:
            filter_string = '"scale=trunc(iw/2)*2:trunc(ih/2)*2"'.format(fps=fps)
        elif coding == cls.Coding.H264_QSV:
            filter_string = '""'.format(fps=fps)
        else:
            filter_string = '""'.format(fps=fps)

        cmd_args = [
            cls.get_ffmpeg_source(),
            '-v', 'error',
            '-f', 'concat',
            '-safe', '0',
            '-r', str(fps),
            '-i', cls._create_image_sequence_concat_file_list(
                image_sequence,
                start_frame=start_frame,
                end_frame=end_frame,
                frame_step=frame_step,
            ),
            '-vsync', 'cfr',
            '-vf', filter_string,
            '-c:v', coding,
            '-pix_fmt', 'yuv420p',
            '-b:v', '8000k',
            # fixme: disable bframe?
            '-bf', '0',
            '-y',
            video_path,
        ]

        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        cmd_script = ' '.join(cmd_args)
        s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        s_p.communicate()

    @classmethod
    def concat_by_images(cls, output_video, image_paths, fps=24, coding='libx264', replace=False):
        output_video = _base.ensure_unicode(output_video)

        if os.path.isfile(output_video) is True:
            if replace is False:
                return

        # create directory first
        directory_path = os.path.dirname(output_video)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        fd, file_list = tempfile.mkstemp(suffix='.concat.files')
        # create file list
        with os.fdopen(fd, 'w') as f:
            for i_image_path in image_paths:
                f.write('file \'{}\'\n'.format(os.path.abspath(i_image_path)))

        cmd_args = [
            cls.get_ffmpeg_source(),
            '-f', 'concat',
            '-safe', '0',
            '-i', file_list,
            '-r', str(fps),
            '-v', 'error',
            '-vf', '"scale=\'min(1024,iw)\':-2:force_original_aspect_ratio=decrease, pad=1024:ceil(ih/2)*2:(ow-iw)/2:(oh-ih)/2"',
            '-c:v', coding,
            '-pix_fmt', 'yuv420p',
            '-b:v', '8000k',
            '-bf', '0',
            '-y',
            output_video
        ]

        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        cmd_script = ' '.join(cmd_args)
        s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        s_p.communicate()

    @classmethod
    def concat_by_videos(cls, output_video, videos, fps=None, coding='libx264', replace=False):
        if os.path.isfile(output_video) and not replace:
            return

        # create directory first
        directory_path = os.path.dirname(output_video)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        first_video = videos[0]
        cmd_args = [
            cls.get_ffprobe_source(),
            '-i', first_video,
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-of', 'csv=p=0'
        ]
        process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError("Error getting video properties: {}".format(stderr))

        width, height, fps_first = stdout.strip().split(',')
        if fps is None:
            fps = eval(fps_first)

        fd, file_list = tempfile.mkstemp(suffix='.concat.files')
        with os.fdopen(fd, 'w') as f:
            for i_video in videos:
                i_video_path_tmp = tempfile.mktemp(suffix='.mov')

                i_cmd_args = [
                    cls.get_ffmpeg_source(),
                    '-i', i_video,
                    '-vf', 'scale={}:{}'.format(width, height),
                    '-r', str(fps),
                    '-c:v', coding,
                    '-pix_fmt', 'yuv420p',
                    '-y', i_video_path_tmp
                ]

                i_prc = subprocess.Popen(i_cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                i_prc.communicate()
                if i_prc.returncode != 0:
                    raise RuntimeError("Error adjusting video: {}".format(i_video))

                f.write("file '{}'\n".format(i_video_path_tmp))

        cmd_args = [
            cls.get_ffmpeg_source(),
            '-f', 'concat',
            '-safe', '0',
            '-i', file_list,
            '-c', 'copy',
            '-y',
            output_video
        ]

        concat_process = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        concat_process.communicate()

        if concat_process.returncode != 0:
            raise RuntimeError("Error concatenating videos")

        os.remove(file_list)

    @classmethod
    def get_codec(cls, video_path):
        video_path = _base.ensure_unicode(video_path)

        cmd_args = [
            cls.get_ffprobe_source(),
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name",
            "-of", "json",
            video_path
        ]

        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        result = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = result.communicate()

        if result.returncode != 0:
            sys.stderr.write(stderr+'\n')
            return None

        output = json.loads(stdout)
        if "streams" in output and len(output["streams"]) > 0:
            return output["streams"][0].get("codec_name")

    @classmethod
    def convert_webp(cls, file_path_0, file_path1):
        # ffmpeg -i input_image.webp output_image.png
        cmd_args = [
            cls.get_ffmpeg_source(),
            '-i', file_path_0, file_path1
        ]

        cmd_args = [_base.ensure_mbcs(x) for x in cmd_args]
        cmd_script = ' '.join(cmd_args)
        s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        s_p.communicate()
