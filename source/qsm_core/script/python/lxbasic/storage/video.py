# coding:utf-8
import os.path

from lxbasic.core import base as bsc_cor_base

from lxbasic.core import process as bsc_cor_process

from lxbasic.core import execute as bsc_cor_execute

from . import base as bsc_stg_base

from . import extend as bsc_stg_extend


class VdoFileOpt(object):
    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def path(self):
        return self._file_path

    def get_thumbnail_file_path(self, ext='.jpg'):
        return bsc_stg_extend.StgTmpThumbnailMtd.get_file_path_(self._file_path, ext=ext)

    def generate_thumbnail(self, width=128, ext='.jpg', block=False):
        thumbnail_file_path = self.get_thumbnail_file_path(ext=ext)
        if os.path.exists(self._file_path):
            if os.path.exists(thumbnail_file_path) is False:
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    bsc_cor_execute.ExcBaseMtd.ffmpeg(),
                    u'-i "{}"'.format(self.path),
                    '-vf scale={}:-1'.format(width),
                    '-vframes 1',
                    '"{}"'.format(thumbnail_file_path)
                ]
                #
                if block is True:
                    bsc_cor_process.PrcBaseMtd.execute_with_result(
                        ' '.join(cmd_args)
                    )
                else:
                    bsc_cor_process.PrcBaseMtd.set_run(
                        ' '.join(cmd_args)
                    )
        return thumbnail_file_path

    def generate_thumbnail_create_args(self, width=128, ext='.jpg'):
        thumbnail_file_path = self.get_thumbnail_file_path(ext=ext)
        if os.path.exists(thumbnail_file_path) is False:
            if os.path.exists(self._file_path):
                directory_path = os.path.dirname(thumbnail_file_path)
                if os.path.exists(directory_path) is False:
                    os.makedirs(directory_path)
                #
                cmd_args = [
                    bsc_cor_execute.ExcBaseMtd.ffmpeg(),
                    u'-i "{}"'.format(self.path),
                    '-vf scale={}:-1'.format(width),
                    '-vframes 1',
                    '-n',
                    '"{}"'.format(thumbnail_file_path)
                ]
                return thumbnail_file_path, ' '.join(cmd_args)
        return thumbnail_file_path, None

    def convert_to(self):
        pass

    def set_mov_create_from(self, image_file_path, width=1024, fps=24, block=False):
        if bsc_stg_base.StgPathMtd(self._file_path).get_is_exists() is False:
            cmd_args = [
                bsc_cor_execute.ExcBaseMtd.ffmpeg(),
                '-i "{}"'.format(image_file_path),
                '-r {}'.format(fps),
                '-f mov',
                '-vf scale={}:-1'.format(width),
                '-vcodec h264',
                '-n',
                '"{}"'.format(self.path)
            ]
            cmd = ' '.join(cmd_args)
            if block is True:
                bsc_cor_process.PrcBaseMtd.execute_with_result(
                    cmd
                )
            else:
                bsc_cor_process.PrcBaseMtd.set_run(
                    cmd
                )

    def set_create_from(self, image_file_path, start_frame=0):
        cmd = '/opt/rv/bin/rvio "{image_file}" -overlay frameburn .4 1.0 30.0 -dlut "{lut_directory}" -o "{movie_file}" -comment "{user}" -outparams timecode={start_frame}'.format(
            **dict(
                movie_file=self._file_path,
                image_file=image_file_path,
                lut_directory='/l/packages/pg/third_party/ocio/aces/1.0.3/baked/maya/sRGB_for_ACEScg_Maya.csp',
                start_frame=start_frame,
                user=bsc_cor_base.SysBaseMtd.get_user_name()
            )
        )
        bsc_cor_process.PrcBaseMtd.execute_with_result(
            cmd
        )

    def get_size(self):
        cmd_args = [
            bsc_cor_execute.ExcBaseMtd.ffmpeg(),
            u'-i "{}"'.format(self.path),
        ]
        cmd = ' '.join(cmd_args)
        bsc_cor_process.PrcBaseMtd.execute_with_result(
            cmd
        )


class VdoRvioOpt(object):
    """
    Usage: RV movie and image sequence viewer

      One File:                   rv foo.jpg
      This Directory:             rv .
      Other Directory:            rv /path/to/dir
      Image Sequence w/Audio:     rv [ in.#.tif in.wav ]
      Stereo w/Audio:             rv [ left.#.tif right.#.tif in.wav ]
      Stereo Movies:              rv [ left.mov right.mov ]
      Stereo Movie (from rvio):   rv stereo.mov
      Cuts Sequenced:             rv cut1.mov cut2.#.exr cut3.mov
      Stereo Cuts Sequenced:      rv [ l1.mov r1.mov ] [ l2.mov r2.mov ]
      Forced Anamorphic:          rv [ -pa 2.0 fullaperture.#.dpx ]
      Compare:                    rv -wipe a.exr b.exr
      Difference:                 rv -diff a.exr b.exr
      Slap Comp Over:             rv -over a.exr b.exr
      Tile Images:                rv -tile *.jpg
      Cache + Play Movie:         rv -l -play foo.mov
      Cache Images to Examine:    rv -c big.#.exr
      Fullscreen on 2nd monitor:  rv -fullscreen -screen 1
      Select Source View:         rv [ in.exr -select view right ]
      Select Source Layer:        rv [ in.exr -select layer light1.diffuse ]       (single-view source)
      Select Source Layer:        rv [ in.exr -select layer left,light1.diffuse ]  (multi-view source)
      Select Source Channel:      rv [ in.exr -select channel R ]                  (single-view, single-layer source)
      Select Source Channel:      rv [ in.exr -select channel left,Diffuse,R ]     (multi-view, multi-layer source)

    Image Sequence Numbering

      Frames 1 to 100 no padding:     image.1-100@.jpg
      Frames 1 to 100 padding 4:      image.1-100#.jpg -or- image.1-100@@@@.jpg
      Frames 1 to 100 padding 5:      image.1-100@@@@@.jpg
      Frames -100 to -200 padding 4:  image.-100--200#jpg
      printf style padding 4:         image.%04d.jpg
      printf style w/range:           image.%04d.jpg 1-100
      printf no padding w/range:      image.%d.jpg 1-100
      Complicated no pad 1 to 100:    image_887f1-100@_982.tif
      Stereo pair (left,right):       image.#.%V.tif
      Stereo pair (L,R):              image.#.%v.tif
      All Frames, padding 4:          image.#.jpg
      All Frames in Sequence:         image.*.jpg
      All Frames in Directory:        /path/to/directory
      All Frames in current dir:      .

    Per-source arguments (inside [ and ] restricts to that source only)

    -pa %f                  Per-source pixel aspect ratio
    -ro %d                  Per-source range offset
    -rs %d                  Per-source range start
    -fps %f                 Per-source or global fps
    -ao %f                  Per-source audio offset in seconds
    -so %f                  Per-source stereo relative eye offset
    -rso %f                 Per-source stereo right eye offset
    -volume %f              Per-source or global audio volume (default=1)
    -fcdl %S                Per-source file CDL
    -lcdl %S                Per-source look CDL
    -flut %S                Per-source file LUT
    -llut %S                Per-source look LUT
    -pclut %S               Per-source pre-cache software LUT
    -cmap %S                Per-source channel mapping (channel names, separated by ',')
    -select %S %S           Per-source view/layer/channel selection
    -crop %d %d %d %d       Per-source crop (xmin, ymin, xmax, ymax)
    -uncrop %d %d %d %d     Per-source uncrop (width, height, xoffset, yoffset)
    -in %d                  Per-source cut-in frame
    -out %d                 Per-source cut-out frame
    -noMovieAudio           Disable source movie's baked-in audio
    -inparams ...           Source specific input parameters

     ...                    Input sequence patterns, images, movies, or directories
    -c                      Use region frame cache
    -l                      Use look-ahead cache
    -nc                     Use no caching
    -s %f                   Image scale reduction
    -ns                     Nuke style sequence notation (deprecated and ignored -- no longer needed)
    -noRanges               No separate frame ranges (i.e. 1-10 will be considered a file)
    -sessionType %S         Session type (sequence, stack) (deprecated, use -view)
    -stereo %S              Stereo mode (hardware, checker, scanline, anaglyph, lumanaglyph, left, right, pair, mirror, hsqueezed, vsqueezed)
    -stereoSwap %d          Swap left and right eyes stereo display (0 == no, 1 == yes, default=0)
    -vsync %d               Video Sync (1 = on, 0 = off, default = 0)
    -comp %S                Composite mode (over, add, difference, replace, topmost)
    -layout %S              Layout mode (packed, row, column, manual)
    -over                   Same as -comp over -view defaultStack
    -diff                   Same as -comp difference -view defaultStack
    -replace                Same as -comp replace -view defaultStack
    -topmost                Same as -comp topmost -view defaultStack
    -layer                  Same as -comp topmost -view defaultStack, with strict frame ranges
    -tile                   Same as -layout packed -view defaultLayout
    -wipe                   Same as -over with wipes enabled
    -view %S                Start with a particular view
    -noSequence             Don't contract files into sequences
    -inferSequence          Infer sequences from one file
    -autoRetime %d          Automatically retime conflicting media fps in sequences and stacks (1 = on, 0 = off, default = 1)
    -rthreads %d            Number of reader threads (default=1)
    -fullscreen             Start in fullscreen mode
    -present                Start in presentation mode (using presentation device)
    -presentAudio %d        Use presentation audio device in presentation mode (1 = on, 0 = off)
    -presentDevice %S       Presentation mode device
    -presentVideoFormat %S  Presentation mode override video format (device specific)
    -presentDataFormat %S   Presentation mode override data format (device specific)
    -screen %d              Start on screen (0, 1, 2, ...)
    -noBorders              No window manager decorations
    -geometry %d %d [%d %d] Start geometry X, Y, W, H
    -fitMedia               Fit the window to the first media shown
    -init %S                Override init script
    -nofloat                Turn off floating point by default
    -maxbits %d             Maximum default bit depth (default=32)
    -gamma %f               Set display gamma (default=1)
    -sRGB                   Display using linear -> sRGB conversion
    -rec709                 Display using linear -> Rec 709 conversion
    -dlut %S                Apply display LUT
    -brightness %f          Set display relative brightness in stops (default=0)
    -resampleMethod %S      Resampling method (area, linear, cubic, nearest, default=area)
    -eval %S                Evaluate Mu expression at every session start
    -pyeval %S              Evaluate Python expression at every session start
    -nomb                   Hide menu bar on start up
    -play                   Play on startup
    -playMode %d            Playback mode (0=Context dependent, 1=Play all frames, 2=Realtime, default=0)
    -loopMode %d            Playback loop mode (0=Loop, 1=Play Once, 2=Ping-Pong, default=0)
    -cli                    Mu command line interface
    -vram %f                VRAM usage limit in Mb, default = 64.000000
    -cram %f                Max region cache RAM usage in Gb, (13Gb available, default 0.2Gb)
    -lram %f                Max look-ahead cache RAM usage in Gb, (13Gb available, default 0.2Gb)
    -noPBO                  Prevent use of GL PBOs for pixel transfer
    -prefetch               Prefetch images for rendering
    -useAppleClientStorage  Use APPLE_client_storage extension
    -useThreadedUpload      Use threading for texture uploading/downloading if possible
    -bwait %f               Max buffer wait time in cached seconds, default 5.0
    -lookback %f            Percentage of the lookahead cache reserved for frames behind the playhead, default 25
    -yuv                    Assume YUV hardware conversion
    -noaudio                Turn off audio
    -audiofs %d             Use fixed audio frame size (results are hardware dependant ... try 512)
    -audioCachePacket %d    Audio cache packet size in samples (default=2048)
    -audioMinCache %f       Audio cache min size in seconds (default=0.300000)
    -audioMaxCache %f       Audio cache max size in seconds (default=0.600000)
    -audioModule %S         Use specific audio module
    -audioDevice %S         Use specific audio device
    -audioRate %f           Use specific output audio rate (default=ask hardware)
    -audioPrecision %d      Use specific output audio precision (default=16)
    -audioNice %d           Close audio device when not playing (may cause problems on some hardware) default=0
    -audioNoLock %d         Do not use hardware audio/video syncronization (use software instead, default=1)
    -audioPreRoll %d        Preroll audio on device open (Linux only; default=1)
    -audioGlobalOffset %f   Global audio offset in seconds
    -audioDeviceLatency %f  Audio device latency compensation in milliseconds
    -bg %S                  Background pattern (default=black, white, grey18, grey50, checker, crosshatch)
    -formats                Show all supported image and movie formats
    -apple                  Use Quicktime and NSImage libraries (on OS X)
    -cinalt                 Use alternate Cineon/DPX readers
    -exrcpus %d             EXR thread count (default=0)
    -exrRGBA                EXR Always read as RGBA (default=false)
    -exrInherit             EXR guess channel inheritance (default=false)
    -exrNoOneChannel        EXR never use one channel planar images (default=false)
    -exrIOMethod %d [%d]    EXR I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=1) and optional chunk size (default=61440)
    -exrReadWindowIsDisplayWindow
                            EXR read window is display window (default=false)
    -exrReadWindow %d       EXR Read Window Method (0=Data, 1=Display, 2=Union, 3=Data inside Display, default=3)
    -jpegRGBA               Make JPEG four channel RGBA on read (default=no, use RGB or YUV)
    -jpegIOMethod %d [%d]   JPEG I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=1) and optional chunk size (default=61440)
    -cinpixel %S            Cineon pixel storage (default=RGB8_PLANAR)
    -cinchroma              Use Cineon chromaticity values (for default reader only)
    -cinIOMethod %d [%d]    Cineon I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -dpxpixel %S            DPX pixel storage (default=RGB8_PLANAR)
    -dpxchroma              Use DPX chromaticity values (for default reader only)
    -dpxIOMethod %d [%d]    DPX I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -tgaIOMethod %d [%d]    TARGA I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -tiffIOMethod %d [%d]   TIFF I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -lic %S                 Use specific license file
    -noPrefs                Ignore preferences
    -resetPrefs             Reset preferences to default values
    -qtcss %S               Use QT style sheet for UI
    -qtstyle %S             Use QT style
    -qtdesktop %d           QT desktop aware, default=1 (on)
    -xl                     Aggressively absorb screen space for large media
    -mouse %d               Force tablet/stylus events to be treated as a mouse events, default=0 (off)
    -network                Start networking
    -networkPort %d         Port for networking
    -networkHost %S         Alternate host/address for incoming connections
    -networkTag %S          Tag to mark automatically saved port file
    -networkConnect %S [%d] Start networking and connect to host at port
    -networkPerm %d         Default network connection permission (0=Ask, 1=Allow, 2=Deny, default=0)
    -reuse %d               Try to re-use the current session for incoming URLs (1 = reuse session, 0 = new session, default = 1)
    -nopackages             Don't load any packages at startup (for debugging)
    -encodeURL              Encode the command line as an rvlink URL, print, and exit
    -bakeURL                Fully bake the command line as an rvlink URL, print, and exit
    -sendEvent ...          Send external events e.g. -sendEvent 'name' 'content'
    -flags ...              Arbitrary flags (flag, or 'name=value') for use in Mu code
    -debug ...              Debug category
    -version                Show RV version number
    -strictlicense          Exit rather than consume an rv license if no rvsolo licenses are available
    -prefsPath %S           Alternate path to preferences directory
    -scheduler %S           Thread scheduling policy (may require root)
    -priorities %d %d       Set display and audio thread priorities (may require root)
    #
    Usage: RVIO (hardware version) movie and image sequence conversion and creation
      Make Movie:           rvio in.#.tif -o out.mov
      Convert Image:        rvio in.tif -o out.jpg
      Convert Image Seq.:   rvio in.#.tif -o out.#.jpg
      Movie With Audio:     rvio [ in.#.tif in.wav ] -o out.mov
      Movie With LUT:       rvio [ -llut log2film.csp in.#.dpx ] -o out.mov
      Rip Movie Range #1:   rvio in.mov -t 1000-1200 -o out.mov
      Rip Movie Range #2:   rvio in.mov -t 1000-1200 -o out.#.jpg
      Rip Movie Audio:      rvio in.mov -o out.wav
      Conform Image:        rvio in.tif -outres 512 512 -o out.tif
      Resize Image:         rvio in.#.tif -scale 0.25 -o out.#.jpg
      Resize/Stretch:       rvio in.#.tif -resize 640 480 -o out.#.jpg
      Resize Keep Aspect:   rvio in.#.tif -resize 1920 0 -o out.#.jpg
      Resize Keep Aspt #2:  rvio in.#.tif -resize 0 1080 -o out.#.jpg
      Sequence:             rvio cut1.#.tif cut2.mov cut3.1-100#.dpx -o out.mov
      Per-Source Arg:       rvio [ -pa 2.0 -fps 30 cut1.#.dpx ] cut2.mov -o out.mov
      Stereo Movie File:    rvio [ left.mov right.mov ] -outstereo separate -o out.mov
      Stereo Anaglyph:      rvio [ left.mov right.mov ] -outstereo anaglyph -o out.mov
      Log Cin/DPX to Movie: rvio -inlog -outsrgb in.#.cin -o out.mov
      Output Log Cin/DPX:   rvio -outlog in.#.exr -o out.#.dpx
      OpenEXR 16 Bit Out:   rvio in.#.dpx -outhalf -o out.#.exr
      OpenEXR to 8 Bit:     rvio in.#.exr -out8 -o out.#.tif
      OpenEXR B44 4:2:0:    rvio in.#.exr -outhalf -yryby 1 2 2 -codec B44 -o out.#.exr
      OpenEXR B44A 4:2:0:   rvio in.#.exr -outhalf -yrybya 1 2 2 1 -codec B44A -o out.#.exr
      OpenEXR DWAA 4:2:0:   rvio in.#.exr -outhalf -yryby 1 2 2 -quality 45 -codec DWAA -o out.#.exr
      OpenEXR DWAB 4:2:0:   rvio in.#.exr -outhalf -yrybya 1 2 2 1 -quality 45 -codec DWAB -o out.#.exr
      ACES from PD DPX:     rvio in.#.dpx -inlog -outhalf -outaces out.#.aces
      ACES from JPEG:       rvio in.#.jpg -insrgb -outhalf -outaces out.#.aces
      Chng White to D75:    rvio in.#.exr -outillum D75 -outhalf -o out.#.exr
      Chng White to D75 #2: rvio in.#.exr -outwhite 0.29902 0.31485 -outhalf -o out.#.exr
      TIFF 32 Bit Float:    rvio in.#.tif -outformat 32 float -o out.#.tif
      Anamorphic Unsqueeze: rvio [ -pa 2.0 in_2k_full_ap.#.dpx ] -outres 2048 1556/2 -o out_2k.mov
      Camera JPEG to EXR:   rvio -insrgb IMG1234.jpg -o out.exr
      Letterbox HD in 1.33: rvio [ -uncrop 1920 1444 0 182 in1080.#.dpx ] -outres 640 480 -o out.mov
      Crop 2.35 of Full Ap: rvio [ -crop 0 342 2047 1213 inFullAp.#.dpx ] -o out.mov
      Multiple CPUs:        rvio -v -rthreads 3 in.#.dpx -o out.mov
      Test Throughput:      rvio -v in.#.dpx -o out.null

    Advanced EXR/ACES Header Attributes Usage:
      Multiple -outparam values can be used.
      Type names: f, i, s, sv        -- float, int, string, string vector [N values]
                  v2i, v2f, v3i, v3f -- 2D and 3D int and float vectors [2 or 3 values required]
                  b2i, b2f           -- 2D box float and int [4 values required]
                  c                  -- chromaticities [8 values required]
      Passthrough syntax:   -outparams passthrough=REGEX
      Attr creation syntax: -outparams NAME:TYPE=VALUE0[,VALUE1,...]"
      EXIF attrs:           rvio exif.jpg -insrgb -o out.exr -outparams "passthrough=.*EXIF.*"
      Create float attr:    rvio in.exr -o out.exr -outparams pi:f=3.14
      Create v2i attr:      rvio in.exr -o out.exr -outparams myV2iAttr:v2i=1,2
      Create string attr:   rvio in.exr -o out.exr -outparams "myAttr:s=HELLO WORLD"
      Chromaticies (XYZ):   rvio XYZ.tiff -o out.exr -outparams chromaticities:c=1,0,0,1,0,0,.333333,.3333333
      No Color Adaptation:  rvio in.exr -o out.aces -outaces -outillum D65REC709

    Example Leader/Overlay Usage:
              simpleslate: side-text Field1=Value1 Field2=Value2 ...
              watermark: text opacity
              frameburn: opacity grey font-point-size
              bug: file.tif opacity height
              matte: aspect-ratio opacity

      Movie w/Slate:        rvio in.#.jpg -o out.mov -leader simpleslate "FilmCo" \
                                 "Artist=Jane Q. Artiste" "Shot=S01" "Show=BlockBuster" \
                                 "Comments=You said it was too blue so I made it red"
      Movie w/Watermark:    rvio in.#.jpg -o out.mov -overlay watermark "FilmCo Eyes Only" .25
      Movie w/Frame Burn:   rvio in.#.jpg -o out.mov -overlay frameburn .4 1.0 30.0
      Movie w/Bug:          rvio in.#.jpg -o out.mov -overlay bug logo.tif 0.4 128 15 100
      Movie w/Matte:        rvio in.#.jpg -o out.mov -overlay matte 2.35 0.8
      Multiple:             rvio ... -leader ... -overlay ... -overlay ...

    Image Sequence Numbering

      Frames 1 to 100 no padding:     image.1-100@.jpg
      Frames 1 to 100 padding 4:      image.1-100#.jpg -or- image.1-100@@@@.jpg
      Frames 1 to 100 padding 5:      image.1-100@@@@@.jpg
      Frames -100 to -200 padding 4:  image.-100--200#jpg
      printf style padding 4:         image.%04d.jpg
      printf style w/range:           image.%04d.jpg 1-100
      printf no padding w/range:      image.%d.jpg 1-100
      Complicated no pad 1 to 100:    image_887f1-100@_982.tif
      Stereo pair (left,right):       image.#.%V.tif
      Stereo pair (L,R):              image.#.%v.tif
      All Frames, padding 4:          image.#.jpg
      All Frames in Sequence:         image.*.jpg
      All Frames in Directory:        /path/to/directory
      All Frames in current dir:      .

    Per-source arguments (inside [ and ] restricts to that source only)

    -pa %f                  Per-source pixel aspect ratio
    -ro %d                  Per-source range offset
    -rs %d                  Per-source range start
    -fps %f                 Per-source or global fps
    -ao %f                  Per-source audio offset in seconds
    -so %f                  Per-source stereo relative eye offset
    -rso %f                 Per-source stereo right eye offset
    -volume %f              Per-source or global audio volume (default=1)
    -fcdl %S                Per-source file CDL
    -lcdl %S                Per-source look CDL
    -flut %S                Per-source file LUT
    -llut %S                Per-source look LUT
    -pclut %S               Per-source pre-cache software LUT
    -cmap %S                Per-source channel mapping (channel names, separated by ',')
    -select %S %S           Per-source view/layer/channel selection
    -crop %d %d %d %d       Per-source crop (xmin, ymin, xmax, ymax)
    -uncrop %d %d %d %d     Per-source uncrop (width, height, xoffset, yoffset)
    -in %d                  Per-source cut-in frame
    -out %d                 Per-source cut-out frame
    -noMovieAudio           Disable source movie's baked-in audio
    -inparams ...           Source specific input parameters

    Global arguments

     ...                    Input sequence patterns, images, movies, or directories
    -o %S                   Output sequence or image
    -t %S                   Output time range (default=input time range)
    -tio                    Output time range from view's in/out points
    -v                      Verbose messages
    -vv                     Really Verbose messages
    -q                      Best quality color conversions (not necessary, slower)
    -ns                     Nuke-style sequences (deprecated and ignored -- no longer needed)
    -noRanges               No separate frame ranges (i.e. 1-10 will be considered a file)
    -rthreads %d            Number of reader/render threads (default=1)
    -wthreads %d            Number of writer threads (limited support for this)
    -view %S                View to render (default=defaultSequence or current view in rv file)
    -noSequence             Don't contract files into sequences
    -formats                Show all supported image and movie formats
    -leader ...             Insert leader/slate (can use multiple time)
    -leaderframes %d        Number of leader frames (default=1)
    -overlay ...            Visual overlay(s) (can use multiple times)
    -inlog                  Convert input to linear space via Cineon Log->Lin
    -inlogc                 Convert input to linear space via ARRI LogC->Lin
    -inredlog               Convert input to linear space via Red Log->Lin
    -inredlogfilm           Convert input to linear space via Red Log Film->Lin
    -insrgb                 Convert input to linear space from sRGB space
    -in709                  Convert input to linear space from Rec-709 space
    -ingamma %f             Convert input using gamma correction
    -filegamma %f           Convert input using gamma correction to linear space
    -inchannelmap ...       map input channels
    -inpremult              premultiply alpha and color
    -inunpremult            un-premultiply alpha and color
    -exposure %f            Apply relative exposure change (in stops)
    -scale %f               Scale input image geometry
    -resize %d [%d]         Resize input image geometry to exact size on input
    -dlut %S                Apply display LUT
    -flip                   Flip image (flip vertical) (keep orientation flags the same)
    -flop                   Flop image (flip horizontal) (keep orientation flags the same)
    -yryby %d %d %d         Y RY BY sub-sampled planar output
    -yrybya %d %d %d %d     Y RY BY A sub-sampled planar output
    -yuv %d %d %d           Y U V sub-sampled planar output
    -outparams ...          Codec specific output parameters
    -outchannelmap ...      map output channels
    -outrgb                 same as -outchannelmap R G B
    -outpremult             premultiply alpha and color
    -outunpremult           un-premultiply alpha and color
    -outlog                 Convert output to log space via Cineon Lin->Log
    -outsrgb                Convert output to sRGB ColorSpace
    -out709                 Convert output to Rec-709 ColorSpace
    -outlogc                Convert output to Arri LogC ColorSpace
    -outlogcEI %d           Use Arri LogC curve values for this Exposure Index value (default 800)
    -outredlog              Convert output to Red Log ColorSpace
    -outredlogfilm          Convert output to Red Log Film ColorSpace
    -outgamma %f            Apply gamma to output
    -outstereo ...          Output stereo (checker, scanline, anaglyph, left, right, pair, mirror, hsqueezed, vsqueezed, default=separate)
    -outformat %d %S        Output bits and format (e.g. 16 float -or- 8 int)
    -outhalf                Same as -outformat 16 float
    -out8                   Same as -outformat 8 int
    -outres %d %d           Output resolution
    -outfps %f              Output FPS
    -outaces                Output ACES gamut (converts pixels to ACES)
    -outwhite %f %f         Output white CIE 1931 chromaticity x, y
    -outillum %S            Output standard illuminant name (A-C, D50, D55, D65, D65REC709, D75 E, F[1-12])
    -codec %S               Output codec (varies with file format)
    -audiocodec %S          Output audio codec (varies with file format)
    -audiorate %f           Output audio sample rate (default 48000)
    -audiochannels %d       Output audio channels (default 2)
    -quality %f             Output codec quality 0.0 -> 1.0 (100000 for DWAA/DWAB) (varies w/format and codec default=0.9)
    -outpa %S               Output pixel aspect ratio (e.g. 1.33 or 16:9, etc. metadata only) default=1:1
    -comment %S             Ouput comment (movie files, default="")
    -copyright %S           Ouput copyright (movie files, default="")
    -lic %S                 Use specific license file
    -debug ...              Debug category
    -version                Show RVIO version number
    -iomethod %d [%d]       I/O Method (overrides all) (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=-1) and optional chunk size (default=61440)
    -exrcpus %d             EXR thread count (default=12)
    -exrRGBA                EXR Always read as RGBA (default=false)
    -exrInherit             EXR guess channel inheritance (default=false)
    -exrNoOneChannel        EXR never use one channel planar images (default=false)
    -exrIOMethod %d [%d]    EXR I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -exrReadWindowIsDisplayWindow
                            EXR read window is display window (default=false)
    -exrReadWindow %d       EXR Read Window Method (0=Data, 1=Display, 2=Union, 3=Data inside Display, default=1)
    -jpegRGBA               Make JPEG four channel RGBA on read (default=no, use RGB or YUV)
    -jpegIOMethod %d [%d]   JPEG I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -cinpixel %S            Cineon pixel storage (default=A2_BGR10)
    -cinchroma              Use Cineon chromaticity values (for default reader only)
    -cinIOMethod %d [%d]    Cineon I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -dpxpixel %S            DPX pixel storage (default=A2_BGR10)
    -dpxchroma              Use DPX chromaticity values (for default reader only)
    -dpxIOMethod %d [%d]    DPX I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -tgaIOMethod %d [%d]    TARGA I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -tiffIOMethod %d [%d]   TIFF I/O Method (0=standard, 1=buffered, 2=unbuffered, 3=MemoryMap, 4=AsyncBuffered, 5=AsyncUnbuffered, default=2) and optional chunk size (default=61440)
    -init %S                Override init script
    -err-to-out             Output errors to standard output (instead of standard error)
    -strictlicense          Exit rather than consume an rv license if no rvio licenses are available
    -flags ...              Arbitrary flags (flag, or 'name=value') for Mu
    """
    OPTION = dict(
        input='',
        output='',
        quality=1.0,
        width=2048,
        lut_directory='/l/packages/pg/third_party/ocio/aces/1.0.3/baked/maya/sRGB_for_ACEScg_Maya.csp',
        comment='test',
        start_frame=1001,
    )

    def __init__(self, option):
        self._option = {}
        self._option.update(self.OPTION)
        self._option.update(option)

    def test(self):
        cmd_args = [
            '/opt/rv/bin/rvio',
            '{image_file}',
            '-vv',
            '-overlay frameburn .4 1.0 30.0',
            '-dlut "{lut_directory}"',
            '-o "{movie_file}"',
            '-comment "{comment}"',
            '-outparams timecode={start_frame}',
            '-quality {quality}',
            # maximum = 2048?
            # '-resize {width}x0'
        ]
        bsc_cor_process.PrcBaseMtd.execute_with_result(
            ' '.join(cmd_args).format(**self._option)
        )

    def set_convert_to_vedio(self):
        cmd_args = [
            '/opt/rv/bin/rvio',
            '{input}',
            '-vv',
            '-overlay frameburn .4 1.0 30.0',
            '-dlut "{lut_directory}"',
            '-o "{output}"',
            '-comment "{comment}"',
            '-outparams timecode={start_frame}',
            '-quality {quality}',
        ]
        bsc_cor_process.PrcBaseMtd.execute_with_result(
            ' '.join(cmd_args).format(**self._option)
        )

    def set_image_convert_to_vedio(self):
        cmd_args = [
            '/opt/rv/bin/rvio',
            '{input}',
            '-vv',
            '-overlay frameburn .4 1.0 30.0',
            # '-dlut "{lut_directory}"',
            '-o "{output}"',
            '-outparams comment="{comment}"',
            '-quality {quality}',
            '-copyright "©2013-2022 Papergames. All rights reserved."'
        ]
        bsc_cor_process.PrcBaseMtd.execute_with_result(
            ' '.join(cmd_args).format(**self._option)
        )
