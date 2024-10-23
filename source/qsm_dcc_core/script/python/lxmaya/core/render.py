# coding:utf-8
# maya
from .wrap import *


class Option(object):
    ATTR_MAPPER = {}
    NODES = []

    @classmethod
    def set(cls, key, value):
        if key in cls.ATTR_MAPPER:
            attr = cls.ATTR_MAPPER[key]
            type_name = cmds.getAttr(attr, type=1)
            if type_name == 'string':
                cmds.setAttr(attr, value, type='string')
            else:
                cmds.setAttr(attr, value)

    @classmethod
    def get(cls, key):
        if key in cls.ATTR_MAPPER:
            return cmds.getAttr(cls.ATTR_MAPPER[key])

    @classmethod
    def to_dict(cls):
        dict_ = {}
        for i_node in cls.NODES:
            i_dict = {}

            for j_key in cmds.listAttr(
                i_node, read=1, write=1, inUse=1, multi=1
            ) or []:
                j_atr = '{}.{}'.format(i_node, j_key)
                j_value = cmds.getAttr(j_atr)
                i_dict[j_key] = j_value
            dict_[i_node] = i_dict
        return dict_

    @classmethod
    def load_dict(cls, dict_):
        for i_node, i_dict in dict_.items():
            for j_key, j_value in i_dict.items():
                j_atr = '{}.{}'.format(i_node, j_key)
                j_type_name = cmds.getAttr(j_atr, type=1)
                if j_value is None:
                    continue
                if j_type_name == 'string':
                    cmds.setAttr(j_atr, j_value, type='string')
                else:
                    cmds.setAttr(j_atr, j_value)


class RenderOption(Option):
    ATTR_MAPPER = dict(
        renderer='defaultRenderGlobals.currentRenderer',
        output_file_p='defaultRenderGlobals.imageFilePrefix',
        #
        start_frame='defaultRenderGlobals.startFrame',
        end_frame='defaultRenderGlobals.endFrame',
        frame_step='defaultRenderGlobals.byFrameStep',
        #
        image_format='defaultRenderGlobals.imfPluginKey',
        #
        image_width='defaultResolution.width',
        image_height='defaultResolution.height',
    )

    NODES = [
        'defaultRenderGlobals',
        'defaultResolution',
    ]

    @classmethod
    def set_frame_enable(cls):
        cmds.setAttr('defaultRenderGlobals.animation', 1)
        # etc. name.#.ext
        cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
        cmds.setAttr('defaultRenderGlobals.periodInExt', 1)
        cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
        # etc. name.####.ext
        cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)

    @classmethod
    def set_image_size(cls, image_width, image_height, dpi=72):
        cls.set('image_width', image_width)
        cls.set('image_height', image_height)
        #
        cmds.setAttr('defaultResolution.pixelAspect', 1)
        cmds.setAttr('defaultResolution.deviceAspectRatio', float(image_width/image_height))
        cmds.setAttr('defaultResolution.dpi', dpi)


class SoftwareOption(Option):
    ATTR_MAPPER = dict(

    )
    NODES = [
        'defaultRenderQuality'
    ]


class SoftwareRender(object):
    """
Usage: Render [options] filename
       where "filename" is a Maya ASCII or a Maya binary file.

Common options:
  -help              Print help
  -test              Print Mel commands but do not execute them
  -verb              Print Mel commands before they are executed
  -keepMel           Keep the temporary Mel file
  -listRenderers     List all available renderers
  -renderer string   Use this specific renderer
  -r string          Same as -renderer
  -proj string       Use this Maya project to load the file
  -log string        Save output into the given file
  -rendersetuptemplate string Apply a render setup template to your scene before command line rendering.  Only templates exported via File > Export All in the Render Setup editor are supported.  Render setting presets and AOVs are imported from the template.  Render settings and AOVs are reloaded after the template if the -rsp and -rsa flags are used in conjunction with this flag.
  -rst string        Same as -rendersetuptemplate
  -rendersettingspreset string Apply the scene Render Settings from this template file before command line rendering.  This is equivalent to performing File > Import Scene Render Settings in the Render Setup editor, then batch rendering.
  -rsp string        Same as -rendersettingspreset
  -rendersettingsaov string Import the AOVs from this json file before command line rendering.
  -rsa string        Same as -rendersettingsaov

Specific options for renderer "sw": Maya software renderer

General purpose flags:
  -rd path                    Directory in which to store image files
  -im filename                Image file output name
  -fnc int                    File Name Convention: any of name, name.ext, ... See the
        Render Settings window to find available options. Use namec and
        namec.ext for Multi Frame Concatenated formats. As a shortcut,
        numbers 1, 2, ... can also be used
  -of string                  Output image file format. See the Render Settings window
        to find available formats

  -s float                    Starting frame for an animation sequence
  -e float                    End frame for an animation sequence
  -b float                    By frame (or step) for an animation sequence
  -skipExistingFrames boolean Skip frames that are already rendered (if true) or force rendering all frames (if false)
  -pad int                    Number of digits in the output image frame file name
        extension
  -rfs int                    Renumber Frame Start: number for the first image when
        renumbering frames
  -rfb int                    Renumber Frame By: step used for renumbering frames
  -se int                     Obsolete flag identical to -rfs. Used only for backward
        compatibility
  -be int                     Obsolete flag identical to -rfe. Used only for backward
        compatibility

  -cam name                   Specify which camera to be rendered
  -rgb boolean                Turn RGB output on or off
  -alpha boolean              Turn Alpha output on or off
  -depth boolean              Turn Depth output on or off
  -iip                        Ignore Image Planes turn off all image planes before
        rendering

  -x int                      Set X resolution of the final image
  -y int                      Set Y resolution of the final image
  -percentRes float           Renders the image using percent of the resolution
  -ard float                  Device aspect ratio for the rendered image
  -par float                  Pixel aspect ratio for the rendered image

More advanced flags:

Anti-aliasing quality:
  -eaa int                    The anti-aliasing quality of EAS (Abuffer). One of:
        highest(0), high(1), medium(2), low(3)
  -ss int                     Global number of shading samples per surface in a pixel
  -mss int                    Maximum number of adaptive shading samples per surface
        in a pixel
  -mvs int                    Number of motion blur visibility samples
  -mvm int                    Maximum number of motion blur visibility samples
  -pss int                    Number of particle visibility samples
  -vs int                     Global number of volume shading samples
  -ufil boolean               If true, use the multi-pixel filtering; otherwise use
        single pixel filtering
  -pft int                    When useFilter is true, identifies one of the following
        filters: box(0), triangle(2), gaussian(4), quadratic(5)
  -pfx float                  When useFilter is true, defines the X size of the filter
  -pfy float                  When useFilter is true, defines the Y size of the filter
  -rct float                  Red channel contrast threshold
  -gct float                  Green channel contrast threshold
  -bct float                  Blue channel contrast threshold
  -cct float                  Pixel coverage contrast threshold (default is 1.0/8.0)

Raytracing quality:
  -ert boolean                Enable ray tracing
  -rfl int                    Maximum ray-tracing reflection level
  -rfr int                    Maximum ray-tracing refraction level
  -sl int                     Maximum ray-tracing shadow ray depth

Field Options:
  -field boolean              Enable field rendering. When on, images are interlaced
  -pal                        When field rendering is enabled, render even field
        first (PAL)
  -ntsc                       When field rendering is enabled, render odd field
        first (NTSC)

Motion Blur:
  -mb boolean                 Motion blur on/off
  -mbf float                  Motion blur by frame
  -sa float                   Shutter angle for motion blur (1-360)
  -mb2d boolean               Motion blur 2D on/off
  -bll float                  2D motion blur blur length
  -bls float                  2D motion blur blur sharpness
  -smv int                    2D motion blur smooth value
  -smc boolean                2D motion blur smooth color on/off
  -kmv boolean                Keep motion vector for 2D motion blur on/off

Render Options:
  -ifg boolean                Use the film gate for rendering if false
  -edm boolean                Enable depth map usage
  -g float                    Gamma value
  -premul boolean             Premultiply color by the alpha value
  -premulthr float            When premultiply is on, defines the threshold used to
        determine whether to premultiply or not

Memory and Performance:
  -uf boolean                 Use the tessellation file cache
  -oi boolean                 Dynamically detects similarly tessellated surfaces
  -rut boolean                Reuse render geometry to generate depth maps
  -udb boolean                Use the displacement bounding box scale to optimize
        displacement-map performance
  -mm int                     Renderer maximum memory use (in Megabytes)

Render Layers and Passes:
  -rl boolean|name(s)         Render each render layer separately. Applicable to both legacy render layers and render setup. When used with render setup, a rs_ prefix is appended to the name of each folder created for each layer.
  -rp boolean|name(s)         Render passes separately. Only applicable to legacy render layers. 'all' will render all passes
  -rs boolean                 Obsolete flag. Used only for backward compatibility
  -sel boolean|name(s)        Selects which objects, groups and/or sets to render

Mel callbacks
  -preRender string           Mel code executed before rendering
  -postRender string          Mel code executed after rendering
  -preLayer string            Mel code executed before each render layer
  -postLayer string           Mel code executed after each render layer
  -preFrame string            Mel code executed before each frame
  -postFrame string           Mel code executed after each frame
  -pre string                 Obsolete flag
  -post string                Obsolete flag

Other:
  -rep boolean                Do not replace the rendered image if it already exists
  -reg int int int int        Set sub-region pixel boundary of the final image:
        left, right, bottom, top
  -n int                      Number of processors to use (0 indicates use all
        available)
  -mf boolean                 Append image file format to image name if true
  -sp boolean                 Generate shadow depth maps only
  -amt boolean                Abort renderer when encountered missing texture
  -ipr boolean                Create an IPR file
  -keepPreImage boolean       Keep the renderings prior to post-process around

*** Remember to put a space between option flags and their arguments. ***
Any boolean flag will take the following values as TRUE: on, yes, true, or 1.
Any boolean flag will take the following values as FALSE: off, no, false, or 0.

    e.g. -x 512 -y 512 -cam persp -im test -of jpg -mb on -sa 180 file

    """
    @classmethod
    def generate_command(cls, **kwargs):
        """
cmd = mya_core.SoftwareRender.get_command(
    scene='/data/e/workspace/lynxi/test/maya/software-render/test_3.ma',
    image_directory='/data/e/workspace/lynxi/test/maya/software-render/render/11',
    image_format='jpg',
    camera='cam_full_body',
    resolution='512x512',
    start_frame=1,
    end_frame=1,
    step=1,
    quality='low',
    pre_command='import easy.script.render as esy_scp_render; esy_scp_render.TtbRenderScript().load_white()'
)

print cmd
        """
        quality = kwargs['quality']
        sample_s = (
            ' -eaa {sample_level}'
            ' -ss {sample}'
            ' -mss {sample_max}'
        )
        filter_s = (
            # filter
            #   enable
            ' -ufil true'
            #   triangle
            ' -pft 2'
            #   filter width, height
            ' -pfx 2.0 -pfy 2.0'
        )
        ray_tracing_s = (
            # ray tracing
            #   enable
            ' -ert true'
            ' -rfl {reflection_ray}'
            ' -rfr {refraction_ray}'
            ' -sl {shadow_ray}'
        )
        if quality == 'low':
            render_settings_s = (sample_s+filter_s+ray_tracing_s).format(
                sample_level=3, sample=2, sample_max=2,
                reflection_ray=2, refraction_ray=2, shadow_ray=4
            )
        elif quality == 'medium':
            render_settings_s = (sample_s+filter_s+ray_tracing_s).format(
                sample_level=2, sample=4, sample_max=4,
                reflection_ray=2, refraction_ray=2, shadow_ray=8
            )
        elif quality == 'high':
            render_settings_s = (sample_s+filter_s+ray_tracing_s).format(
                sample_level=1, sample=8, sample_max=8,
                reflection_ray=2, refraction_ray=2, shadow_ray=12
            )
        else:
            raise RuntimeError()
        width, height = kwargs.pop('resolution').split('x')
        aspect_ratio = float(width)/float(height)
        if 'pre_command' in kwargs:
            pre_mel = r'python(\"{}\")'.format(kwargs.pop('pre_command'))
            render_settings_s += ' -preRender "{}"'.format(pre_mel)

        kwargs['render_settings'] = render_settings_s
        return (
            'Render'
            ' -r sw'
            ' -rd "{image_directory}"'
            ' -of "{image_format}"'
            ' -im "primary"'
            ' -fnc name.#.ext'
            ' -cam "{camera}"'
            ' -rt 0'
            ' -x {width} -y {height} -ard {aspect_ratio}'
            ' -s {start_frame} -e {end_frame} -b {frame_step} -pad 4'
            '{render_settings}'
            ' -g 2.2'
            ' "{scene}"'
        ).format(
            width=width, height=height, aspect_ratio=aspect_ratio,
            **kwargs
        )


class ArnoldRender(object):
    """
Usage: Render [options] filename
       where "filename" is a Maya ASCII or a Maya binary file.

Common options:
  -help              Print help
  -test              Print Mel commands but do not execute them
  -verb              Print Mel commands before they are executed
  -keepMel           Keep the temporary Mel file
  -listRenderers     List all available renderers
  -renderer string   Use this specific renderer
  -r string          Same as -renderer
  -proj string       Use this Maya project to load the file
  -log string        Save output into the given file
  -rendersetuptemplate string Apply a render setup template to your scene before command line rendering.  Only templates exported via File > Export All in the Render Setup editor are supported.  Render setting presets and AOVs are imported from the template.  Render settings and AOVs are reloaded after the template if the -rsp and -rsa flags are used in conjunction with this flag.
  -rst string        Same as -rendersetuptemplate
  -rendersettingspreset string Apply the scene Render Settings from this template file before command line rendering.  This is equivalent to performing File > Import Scene Render Settings in the Render Setup editor, then batch rendering.
  -rsp string        Same as -rendersettingspreset
  -rendersettingsaov string Import the AOVs from this json file before command line rendering.
  -rsa string        Same as -rendersettingsaov

Specific options for renderer "arnold": Arnold renderer

General purpose flags:
  -rd path                    Directory in which to store image files
  -im filename                Image file output name
  -rt int                     Render type (0 = render, 1 = export ass, 2 = export and kick)
  -lic boolean                Turn licensing on or off
  -of format                  Output image file format. See the Render Settings window to
        find available formats
  -fnc int                    File Name Convention: any of name, name.ext, ... See the
        Render Settings window to find available options. Use namec and
        namec.ext for Multi Frame Concatenated formats. As a shortcut,
        numbers 1, 2, ... can also be used

Frame numbering options
  -s float                    Starting frame for an animation sequence
  -e float                    End frame for an animation sequence
  -seq string                 Frame number sequence e.g "2 4 6..10"
  -b float                    By frame (or step) for an animation sequence
  -skipExistingFrames boolean Skip frames that are already rendered (if true) or force rendering all frames (if false)
  -pad int                    Number of digits in the output image frame file name
                    extension

Render Layers and Passes
  -rl boolean|name(s)         Render each render layer separately
  -rp boolean|name(s)         Render passes separately. 'all' will render all passes
  -sel boolean|name(s)        Selects which objects, groups and/or sets to render
  -l boolean|name(s)          Selects which display and render layers to render

Camera options
  -cam name                   Specify which camera to be rendered
  -rgb boolean                Turn RGB output on or off
  -alpha boolean              Turn Alpha output on or off
  -depth boolean              Turn Depth output on or off
  -iip                        Ignore Image Planes. Turn off all image planes before
                    rendering

Resolution options
  -x int                      Set X resolution of the final image
  -y int                      Set Y resolution of the final image
  -percentRes float           Renders the image using percent of the resolution
  -ard float                  Device aspect ratio for the rendered image
  -reg int                    Set render region

Samples options
  -ai:as int                  Set anti-aliasing samples
  -ai:hs int                  Set indirect diffuse samples
  -ai:gs int                  Set indirect specular samples
  -ai:rs int                  Set transmission samples
  -ai:bssrdfs int             Number of SSS Samples.

Sample Clamping
  -ai:cmpsv boolean           Enable sample clamping.
  -ai:aovsc boolean           Sample campling affects AOVs.
  -ai:aasc float              Sample max value.
  -ai:iasc float              Sample max value for indirect rays.

Depth options
  -ai:td int                  Set total depth.
  -ai:dif int                 Set indirect diffuse depth.
  -ai:glo int                 Set indirect specular depth.
  -ai:rfr int                 Set transmission depth.
  -ai:vol int                 Set volume GI depth.
  -ai:atd int                 Set auto-transparency depth.

Motion blur
  -ai:mben boolean            Enable motion blur.
  -ai:mbdf boolean            Enable object deformation motion blur.
  -ai:mbcen boolean           Enable camera motion blur.
  -ai:mbrt int                Position. (0 - Start On Frame, 1 - Center On Frame, 2 - End On Frame, 3 - Custom)
  -ai:mbfr float              Shutter Length.
  -ai:mbstart float           Motion Start.
  -ai:mbend float             Motion End.
  -ai:mbms int                Number of motion steps.

Lights
  -ai:llth float              Low light threshold value.
  -ai:ll int                  Light linking mode. (0 - None, 1 - Maya Light Links)
  -ai:sl int                  Shadow linking mode. (0 - None, 1 - Follows Light Linking, 2 - Maya Shadow Links)

Subdivision
  -ai:mxsb int                Maximum subdivision level.

Render Settings
  -ai:threads int             Set the number of threads.
  -ai:bscn int                Bucket Scanning. (0 - Top, 1 - Bottom, 2 - Left, 3 - Right, 4 - Random, 5 - Woven, 6 - Spiral, 7 - Hilbert)
  -ai:bsz int                 Bucket Size.
  -ai:bass boolean            Binary Ass Export.
  -ai:exbb boolean            Export Bounding box.
  -ai:aerr boolean            Abort on Error.
  -ai:alf boolean             Abort on License Fail.
  -ai:slc boolean             Skip License Check.
  -ai:device int              Render Device ( 0 - CPU , 1 - GPU )
  -ai:manGpuSel boolean        Turn on/off Manual GPU Selection
  -ai:gpu int                 Index of the GPU used for the render ( Works in conjunction with manGpuSel and can set a single GPU to render)
  -ai:enas boolean            Enable Adaptive Sampling.
  -ai:maxaa int               AA Samples Max.
  -ai:aath float              AA Adaptive Threshold.
  -ai:uopt string             User Options.
  -ai:port int                Set the Command Port for the Batch Progress Driver
  -ai:ofn string              Original file name.

Textures
  -ai:txamm boolean           Enable texture auto mipmap.
  -ai:txaun boolean           Accept untiled textures.
  -ai:txett boolean           Use existing tiled textures.
  -ai:txaum boolean           Accept unmipped textures.
  -ai:txat int                Auto tile size.
  -ai:txmm float              Maximum texture cache memory. (MB)
  -ai:txmof int               Maximum number of opened textures.
  -ai:txpfs boolean           Per file texture stats.
  -ai:txdb float              Deprecated parameter.
  -ai:txgb float              Deprecated parameter.

Feature Overrides
  -ai:foop boolean            Ignore operators.
  -ai:fotx boolean            Ignore textures.
  -ai:fosh boolean            Ignore shaders.
  -ai:foat boolean            Ignore atmosphere.
  -ai:folt boolean            Ignore lights.
  -ai:fosw boolean            Ignore shadows.
  -ai:fosd boolean            Ignore subdivision.
  -ai:fodp boolean            Ignore displacement.
  -ai:fobp boolean            Ignore bump.
  -ai:fosm boolean            Ignore smoothing.
  -ai:fomb boolean            Ignore motion blur.
  -ai:fosss boolean           Ignore SSS.
  -ai:fodof boolean           Ignore DOF.

Search Path
  -ai:sppg string             Plugins search path.
  -ai:sppr string             Procedurals search path.
  -ai:spsh string             Plugin search path.
  -ai:sptx string             Textures search path.

Log
  -ai:lfn string              Log filename.
  -ai:ltc boolean             Log to Console.
  -ai:ltf boolean             Log to File.
  -ai:lve int                 Verbosity level. (0 - Errors, 1 - Warnings, 2 - Info, 3 - Debug)
  -ai:lmw int                 Maximum number of warnings.
  -ai:mti boolean             MtoA Translation Info.
  -ai:ste boolean             Enable Stats.
  -ai:stf string              Stats Filename .
  -ai:stm int                 Stats Mode
  -ai:pfe boolean             Enable profile.
  -ai:pff string              Profile Filename.

Mel callbacks
  -preRender string           add Mel code executed before rendering
  -postRender string          add Mel code executed after rendering
  -preLayer string            add Mel code executed before each render layer
  -postLayer string           add Mel code executed after each render layer
  -preFrame string            add Mel code executed before each frame
  -postFrame string           add Mel code executed after each frame
  -insertPreRender string     insert Mel code executed before rendering
  -insertPostRender string    insert Mel code executed after rendering
  -insertPreLayer string      insert Mel code executed before each render layer
  -insertPostLayer string     insert Mel code executed after each render layer
  -insertPreFrame string      insert Mel code executed before each frame
  -insertPostFrame string     insert Mel code executed after each frame

 *** Remember to place a space between option flags and their arguments. ***
Any boolean flag will take the following values as TRUE: on, yes, true, or 1.
Any boolean flag will take the following values as FALSE: off, no, false, or 0.

    e.g. -s 1 -e 10 -x 512 -y 512 -cam persp -as 4 -hs 2 -dif 2 file.
    """
    @classmethod
    def generate_command(cls, **kwargs):
        quality = kwargs['quality']
        sample_s = (
            ' -ai:as {camera_samples}'
            ' -ai:hs {diffuse_samples}'
            ' -ai:gs {specular_samples}'
            ' -ai:rs {transmission_samples}'
            # unused flag
            # ' -ai:bssrdfs {sss_samples}'
        )
        ray_tracing_s = (
            ' -ai:td {total_depth}'
            ' -ai:dif {diffuse_depth}'
            ' -ai:glo {specular_depth}'
            ' -ai:rfr {transmission_depth}'
            ' -ai:vol {volume_depth}'
            ' -ai:atd {auto_transparency_depth}'
        )
        default_s = (
            ' -ai:aerr false'
            # verbosity level
            ' -ai:lve 3'
        )
        if quality == 'low':
            render_settings_s = (sample_s+ray_tracing_s+default_s).format(
                camera_samples=3,
                diffuse_samples=2,
                specular_samples=2,
                transmission_samples=2,
                volume_sampless=0,
                sss_samples=3,
                total_depth=14,
                diffuse_depth=2,
                specular_depth=3,
                transmission_depth=5,
                volume_depth=0,
            )
        elif quality == 'medium':
            render_settings_s = (sample_s+ray_tracing_s+default_s).format(
                camera_samples=6,
                diffuse_samples=2,
                specular_samples=2,
                transmission_samples=2,
                volume_sampless=0,
                sss_samples=3,
                total_depth=14,
                diffuse_depth=2,
                specular_depth=3,
                transmission_depth=5,
                volume_depth=0,
            )
        elif quality == 'high':
            render_settings_s = (sample_s+ray_tracing_s+default_s).format(
                camera_samples=9,
                diffuse_samples=2,
                specular_samples=3,
                transmission_samples=2,
                volume_sampless=0,
                sss_samples=4,
                total_depth=14,
                diffuse_depth=2,
                specular_depth=3,
                transmission_depth=8,
                volume_depth=0,
            )
        else:
            raise RuntimeError()

        width, height = kwargs.pop('resolution').split('x')
        aspect_ratio = float(width)/float(height)
        if 'pre_command' in kwargs:
            pre_mel = r'python(\"{}\")'.format(kwargs.pop('pre_command'))
            render_settings_s += ' -preRender "{}"'.format(pre_mel)
        kwargs['render_settings'] = render_settings_s
        return (
            'Render'
            ' -r arnold'
            ' -rd "{image_directory}"'
            ' -of "{image_format}"'
            ' -im "primary"'
            ' -fnc name.#.ext'
            ' -cam "{camera}"'
            ' -rt 0'
            ' -x {width} -y {height} -ard {aspect_ratio}'
            ' -s {start_frame} -e {end_frame} -b {frame_step} -pad 4'
            '{render_settings}'
            # ' -g 2.2'
            ' "{scene}"'
        ).format(
            width=width, height=height, aspect_ratio=aspect_ratio,
            **kwargs
        )
