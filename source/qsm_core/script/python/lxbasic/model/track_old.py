# coding=utf-8
import collections

import copy

import math
import os.path

import sys

import bisect

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

from . import coord as _coord


class TrackModel(object):
    KEYS = [
        'key',
        'clip_start', 'clip_end',
        'start', 'speed',
        'source_start', 'source_end',
        'pre_cycle', 'post_cycle',
        'layer_index'
    ]

    COPY_KEYS = [
        '_key',
        '_clip_start', '_clip_end',
        '_speed', '_start', '_count',
        '_source_start', '_source_end',
        '_pre_cycle', '_post_cycle',
        # variant for scale
        '_scale_start', '_scale_end', '_scale_offset',
        # variant for blend
        '_pre_blend', '_post_blend',
        '_layer_index',
        '_is_bypass', '_is_trash',
        '_motion_json', '_motion_name',
        #
        '_valid_frames', '_valid_frame_ranges',
    ]

    MAIN_KEYS = [
        'key',
        'clip_start', 'clip_end',
        'start', 'speed', 'count',
        'source_start', 'source_end',
        'pre_cycle', 'post_cycle',
        'scale_start', 'scale_end', 'scale_offset',
        'pre_blend', 'post_blend',
        'layer_index',
        'is_bypass', 'is_trash',
        'motion_json',
    ]

    def setup(
        self,
        key,
        clip_start=1, clip_end=None,
        start=None, speed=None, count=None,
        source_start=1, source_end=24,
        pre_cycle=0, post_cycle=1,
        scale_start=None, scale_end=None, scale_offset=None,
        pre_blend=4, post_blend=4,
        layer_index=0,
        is_bypass=0, is_trash=0,
        motion_json='',
        **kwargs
    ):
        self._key = key

        self._speed = speed if speed is not None else 1.0

        self._source_start = int(source_start)
        self._source_end = int(source_end)

        self._pre_cycle = int(pre_cycle)
        self._post_cycle = int(post_cycle)

        self._clip_start = int(clip_start)
        self._start = int(start) if start is not None else self._clip_start

        self._clip_end = int(clip_end) if clip_end is not None else self._start+self.basic_post_count-1
        self._count = count if count is not None else self.clip_count

        self._scale_start = scale_start if scale_start is not None else self._clip_start
        self._scale_end = scale_end if scale_end is not None else self._clip_end
        self._scale_offset = scale_offset if scale_offset is not None else self.compute_scale_offset()

        self._pre_blend = pre_blend
        self._post_blend = post_blend

        self._valid_frames = []
        self._valid_frame_ranges = []

        self._layer_index = int(layer_index)

        self._is_bypass = is_bypass
        self._is_trash = is_trash

        self._motion_json = motion_json
        if self._motion_json:
            self._motion_name = os.path.basename(self._motion_json)
        else:
            self._motion_name = self._key

        self._kwargs = kwargs

    @classmethod
    def compute_end(cls, start, source_start, source_end, cycle, speed=1.0):
        return start+int(((source_end-source_start+1)*cycle)/speed)-1

    @staticmethod
    def _find_missing_frame_ranges(frames):
        if not frames:
            return []

        frames = sorted(frames)
        result = []
        start = frames[0]
        end = frames[-1]

        full_range = set(range(start, end+1))

        missing_nums = sorted(full_range-set(frames))

        if not missing_nums:
            return result

        missing_start = missing_nums[0]
        missing_end = missing_nums[0]

        for i in range(1, len(missing_nums)):
            if missing_nums[i] == missing_end+1:
                missing_end = missing_nums[i]
            else:
                if missing_start == missing_end:
                    result.append((missing_start, missing_start))
                else:
                    result.append((missing_start, missing_end))

                missing_start = missing_nums[i]
                missing_end = missing_nums[i]

        if missing_start == missing_end:
            result.append((missing_start, missing_start))
        else:
            result.append((missing_start, missing_end))

        return result

    @staticmethod
    def _find_frame_ranges(frames):
        if not frames:
            return []

        frames = sorted(frames)
        result = []
        start = frames[0]
        end = frames[0]

        for i in range(1, len(frames)):
            if frames[i] == end+1:
                end = frames[i]
            else:
                if start == end:
                    result.append((start, start))
                else:
                    result.append((start, end))
                start = frames[i]
                end = frames[i]

        if start == end:
            result.append((start, start))
        else:
            result.append((start, end))

        return result

    def __init__(self, model_stage):
        self._track_model_stage = model_stage

        self.setup(
            key='untitled',
            clip_start=1, clip_end=None,
            start=None, speed=None, count=None,
            source_start=1, source_end=24,
            pre_cycle=0, post_cycle=1,
            scale_start=None, scale_end=None, scale_offset=None,
            pre_blend=4, post_blend=4,
            layer_index=0,
            is_bypass=0
        )

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__, self._key
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def __eq__(self, other):
        for i in self.COPY_KEYS:
            if self.__dict__[i] != other.__dict__[i]:
                return False
        return True

    def __ne__(self, other):
        for i in self.COPY_KEYS:
            if self.__dict__[i] != other.__dict__[i]:
                return True
        return False

    def to_string(self):
        return bsc_content.ToString(
            collections.OrderedDict(
                [
                    (x, self.__dict__['_'+x]) for x in self.MAIN_KEYS
                ]
            )
        ).generate()

    def to_dict(self):
        return collections.OrderedDict(
            [
                (x, self.__dict__['_'+x]) for x in self.MAIN_KEYS
            ]
        )

    def copy(self):
        _ = self.__class__(self._track_model_stage)
        for i in self.COPY_KEYS:
            i_value = self.__dict__[i]
            if isinstance(i_value, (list, dict)):
                _.__dict__[i] = copy.copy(i_value)
            else:
                _.__dict__[i] = i_value
        return _

    def apply_valid_frames(self, frames):
        self._valid_frames = frames
        self._valid_frame_ranges = self._find_frame_ranges(frames)

    def get_frame_range_index(self, frame_range):
        if frame_range in self._valid_frame_ranges:
            return self._valid_frame_ranges.index(frame_range)

    @property
    def valid_frames(self):
        return self._valid_frames

    @property
    def valid_frame_ranges(self):
        return self._valid_frame_ranges

    @property
    def key(self):
        return self._key

    @property
    def rgb(self):
        return bsc_core.BscTextOpt(self._key).to_hash_rgb(s_p=(15, 35), v_p=(75, 95))

    @property
    def layer_index(self):
        return self._layer_index

    @layer_index.setter
    def layer_index(self, index):
        if index != self._layer_index:
            self._layer_index = index

    @property
    def is_bypass(self):
        return self._is_bypass

    @is_bypass.setter
    def is_bypass(self, boolean):
        self._is_bypass = boolean

    def set_bypass(self, value):
        self._is_bypass = int(value)

    @property
    def is_trash(self):
        return self._is_trash

    def set_trash(self, value):
        self._is_trash = int(value)

    def swap_bypass(self):
        self._is_bypass = int(not bool(self._is_bypass))
        return self._is_bypass

    def swap_trash(self):
        self._is_trash = int(not bool(self._is_trash))

    @property
    def speed_rcp(self):
        return 1.0/self._speed

    @property
    def scale(self):
        return 1.0/self._speed

    @property
    def start(self):
        return self._start

    @property
    def start_offset(self):
        return self._start-self._clip_start

    @property
    def speed(self):
        return self._speed

    @property
    def count(self):
        return self._count

    @property
    def count_offset(self):
        return self._count-self.clip_count

    @property
    def clip_start(self):
        return self._clip_start

    def get_valid_start(self):
        _ = self.valid_frame_ranges
        if _:
            return _[0][0]

    def get_valid_end(self):
        _ = self.valid_frame_ranges
        if _:
            return _[-1][1]

    @clip_start.setter
    def clip_start(self, value):
        if value != self._clip_start:
            self._clip_start = int(value)

    def update_scale_offset(self):
        self._scale_offset = self.compute_scale_offset()

    def compute_scale_offset(self):
        return self.start_offset+self.count_offset

    def move_by_clip_start(self, value):
        if value != self._clip_start:
            # start_offset and clip_count is not change mark first
            start_offset = self.start_offset
            count = self.clip_count

            self._clip_start = int(value)

            self._start = self._clip_start+start_offset

            self._clip_end = int(self._clip_start+count-1)

    def trim_by_clip_start(self, value, auto_cycle=False):
        # start < end-1
        coord = min(value, self.clip_end-1)
        self.clip_start = coord
        if auto_cycle is True:
            add = int(math.ceil(float(self.start_offset)/float(self.source_count)))
            # must >= 0
            add = max(0, add)
            self.pre_cycle = add
        self.update_scale_offset()
        return self.clip_start

    def trim_by_clip_count(self, value, auto_cycle=False):
        # count > 1
        count = max(value, 1)
        if auto_cycle is True:
            start_offset = self.start_offset
            add = int(math.ceil(float((count-start_offset))/float(self.source_count)))
            # must >= 1
            add = max(1, add)
            # add start offset
            count = add*self.source_count+start_offset
            self.post_cycle = add

        self.clip_count = count
        self.update_scale_offset()
        return self.clip_count

    def scale_by_clip_start(self, value):
        # start < end-1
        start = min(int(value), self.clip_end-1)
        count = self._clip_end-start+1

        start_offset = self.start_offset
        scale_count = self.scale_count
        # update variants
        self._start = start+start_offset
        self._clip_start = start
        self._count = count-start_offset+self._scale_offset

        scale = float(self._count)/float(scale_count)
        self._speed = 1.0/scale
        return self.clip_start

    def scale_by_clip_count(self, value):
        # count > 1
        count = max(int(value), 1)

        start_offset = self.start_offset
        scale_count = self.scale_count
        # update variants
        self._clip_end = self._clip_start+count-1
        self._count = count-start_offset+self._scale_offset

        scale = float(self._count)/float(scale_count)
        self._speed = 1.0/scale
        return self.clip_count

    @property
    def scale_count(self):
        return self._scale_end-self._scale_start+1

    @property
    def clip_end(self):
        return self._clip_end

    @clip_end.setter
    def clip_end(self, value):
        if value != self._clip_end:
            self._clip_end = int(value)

    @property
    def clip_count(self):
        return self._clip_end-self._clip_start+1

    @clip_count.setter
    def clip_count(self, value):
        if value < 0:
            return
        if value != self.clip_count:
            self._clip_end = self._clip_start+int(value)-1

    @property
    def start_trim(self):
        offset = self.start_offset
        if offset < 0:
            return -offset
        return 0

    @property
    def basic_end_offset(self):
        return self.clip_end-self.basic_end

    @property
    def basic_end_trim(self):
        offset = self.basic_end_offset
        if offset < 0:
            return -offset
        return 0

    # source
    @property
    def source_count(self):
        return self._source_end-self._source_start+1

    @property
    def scale_source_count(self):
        return self.source_count*self.scale

    @property
    def source_pre_count(self):
        return int(self.source_count*self._pre_cycle)

    @property
    def source_post_count(self):
        return int(self.source_count*self._post_cycle)

    @property
    def source_offset(self):
        return self._start-self._source_start

    # basic
    @property
    def basic_pre_count(self):
        return int((self.source_count*self._pre_cycle)/self._speed)

    @property
    def basic_post_count(self):
        return int((self.source_count*self._post_cycle)/self._speed)

    @property
    def basic_start(self):
        return self._start-self.basic_pre_count

    @property
    def basic_end(self):
        return self._start+self.basic_post_count-1

    @property
    def basic_start_offset_to_start(self):
        # offset for start
        return -self.basic_pre_count-self._clip_start+self._start

    @property
    def basic_end_offset_to_start(self):
        # offset for start
        return self.basic_post_count-self._clip_start+self._start

    @property
    def input(self):
        return 0

    @property
    def output_basic_frame(self):
        return max(min(self.input, self.basic_start), self.basic_end)

    @property
    def output_clip_frame(self):
        return max(min(self.output_basic_frame, self.clip_start), self.clip_end)

    @property
    def frames(self):
        return list(range(self._clip_start, self._clip_end+1))

    @property
    def source_start(self):
        return self._source_start

    @property
    def source_end(self):
        return self._source_end

    @property
    def pre_cycle(self):
        return self._pre_cycle

    @pre_cycle.setter
    def pre_cycle(self, value):
        self._pre_cycle = max(value, 0)

    @property
    def post_cycle(self):
        return self._post_cycle

    @post_cycle.setter
    def post_cycle(self, value):
        self._post_cycle = max(value, 1)
        self._scale_end = self._clip_end
        self._count = self.clip_count

    # scale
    @property
    def scale_start(self):
        return self._scale_start

    @property
    def scale_end(self):
        return self._scale_end

    # blend
    @property
    def pre_blend(self):
        return self._pre_blend

    def set_pre_blend(self, value):
        self._pre_blend = max(min(value, 24), 1)

    @property
    def post_blend(self):
        return self._post_blend

    def set_post_blend(self, value):
        self._post_blend = max(min(value, 24), 1)

    def compute_timetrack_args(self):
        bsc_x = self.compute_basic_x_at(self._clip_start)
        bsc_y = self.compute_basic_y_at(self._layer_index)
        bsc_w = self.compute_basic_w_by(self.clip_count)
        bsc_h = TrackModelStage.LAYER_BASIC_UNIT
        return bsc_x, bsc_y, bsc_w, bsc_h

    def compute_clip_start_loc(self, x):
        return self._track_model_stage._time_coord_model.compute_unit_index_loc(x)

    def compute_clip_count_by(self, w):
        return self._track_model_stage._time_coord_model.compute_unit_count_by(w)

    def compute_basic_x_at(self, clip_start):
        return self._track_model_stage._time_coord_model.compute_basic_coord_at(clip_start)

    def compute_basic_y_at(self, layer_index):
        return self._track_model_stage._layer_coord_model.compute_basic_coord_at(layer_index)

    def compute_basic_w_by(self, clip_count):
        return self._track_model_stage._time_coord_model.compute_basic_size_by(clip_count)

    def compute_layer_index_loc(self, y):
        return self._track_model_stage._layer_coord_model.compute_unit_index_loc(y)

    def compute_w_by_count(self, count):
        return self._track_model_stage._time_coord_model.compute_size_by_count(count)

    def to_hash(self):
        return bsc_core.BscHash.to_hash_key({x: self.__dict__['_'+x] for x in self.MAIN_KEYS})

    def get(self, key):
        return self.__dict__['_'+key]

    def offset_to(self, frame):
        pass


class TrackWidget(object):
    def __init__(self, *args, **kwargs):
        self._track_model = None
        self._last_track_model = None


class TrackModelGroup(object):
    def __init__(self, track_model_list):
        self._track_model_list = track_model_list

    def __str__(self):
        return str(self._track_model_list)

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def track_models(self):
        return self._track_model_list

    def sort(self):
        dict_ = dict()
        for i_track_model in self._track_model_list:
            i_clip_start = i_track_model.clip_start
            i_layer_index = i_track_model.layer_index
            dict_.setdefault((i_clip_start, i_layer_index), []).append(i_track_model)

        keys = dict_.keys()

        keys.sort()
        self._track_model_list = []
        for i_key in keys:
            i_track_models = dict_[i_key]
            for j_track_model in i_track_models:
                self._track_model_list.append(j_track_model)

    def apply_timeframe(self, timeframe):
        clip_start_first = 0
        for i_idx, i_track_model in enumerate(self._track_model_list):
            i_clip_start = i_track_model.clip_start
            if i_idx == 0:
                i_track_model.move_by_clip_start(timeframe)
                clip_start_first = i_clip_start
            else:
                i_offset = i_clip_start-clip_start_first
                i_track_model.move_by_clip_start(timeframe+i_offset)

    def apply_layer_index(self, layer_index):
        layer_index_first = 0
        for i_idx, i_track_model in enumerate(self._track_model_list):
            i_layer_index = i_track_model.layer_index
            if i_idx == 0:
                layer_index_first = i_layer_index
                i_track_model.layer_index = layer_index
            else:
                i_offset = i_layer_index-layer_index_first
                i_track_model.layer_index = layer_index+i_offset


class TrackModelStage(object):
    TIME_BASIC_UNIT = 100
    LAYER_BASIC_UNIT = 40

    @classmethod
    def _find_closest_frame(cls, frames, target):
        pos = bisect.bisect_left(frames, target)
        if pos == 0:
            return frames[0]
        if pos == len(frames):
            return frames[-1]

        before = frames[pos-1]
        after = frames[pos]
        if after-target < target-before:
            return after
        return before

    @classmethod
    def _layer_prc(cls, all_frames, models):
        dict_0 = {}
        for i_model in models:
            i_clip_end = i_model.clip_end
            dict_0.setdefault(i_clip_end, []).append(i_model)

        clip_end_list = dict_0.keys()
        clip_end_list.sort()
        clip_end_list.reverse()

        for i_clip_end in clip_end_list:
            i_models = dict_0[i_clip_end]
            for j_model in i_models:
                i_frames = j_model.frames
                i_valid_frames = list(set(i_frames)-set(all_frames))
                # must sort
                i_valid_frames.sort()
                j_model.apply_valid_frames(i_valid_frames)
                all_frames.extend(i_frames)
        return all_frames

    def __init__(self):
        self._track_widget_dict = {}

        self._time_coord_model = _coord.CoordModel()
        self._time_coord_model.setup(self.TIME_BASIC_UNIT)
        self._time_coord_model.update(0, 1.0, self.TIME_BASIC_UNIT)

        self._layer_coord_model = _coord.CoordModel()
        self._layer_coord_model.setup(self.LAYER_BASIC_UNIT)
        self._layer_coord_model.update(0, 1.0, self.LAYER_BASIC_UNIT)

        self._all_frames = []
        self._ordered_track_model_dict = collections.OrderedDict()

        self._track_start = 1
        self._track_end = 24

    def __str__(self):
        return bsc_content.ToString(
            self._track_widget_dict
        ).generate()

    @property
    def track_start(self):
        return self._track_start

    @property
    def track_end(self):
        return self._track_end

    @property
    def track_count(self):
        return self._track_end-self._track_start+1

    @property
    def missing_frame_ranges(self):
        return TrackModel._find_missing_frame_ranges(self._all_frames)

    @property
    def valid_frame_range_dict(self):
        return self._ordered_track_model_dict

    def is_exists(self, key):
        return key in self._track_widget_dict

    def create_one(
        self,
        widget,
        **kwargs
    ):
        track_model = TrackModel(self)
        track_model.setup(
            **kwargs
        )
        if widget is None:
            widget = TrackWidget()

        widget._track_model = track_model
        widget._last_track_model = track_model.copy()
        self.register(widget)
        return track_model

    def create_node_fnc(self, **kwargs):
        track_model = TrackModel(self)
        track_model.setup(**kwargs)
        return track_model

    def create_group_fnc(self, track_args_list):
        track_models = []
        for i_track_args in track_args_list:
            if isinstance(i_track_args, dict):
                track_models.append(self.create_node_fnc(**i_track_args))
            elif isinstance(i_track_args, TrackModel):
                track_models.append(i_track_args)
        return TrackModelGroup(track_models)

    def delete_one(self, track_model):
        self._track_widget_dict.pop(track_model.key)

    def step_coord_loc(self, x, y):
        return (
            self._time_coord_model.step_coord_loc(x),
            # self._layer_coord_model.step_coord_loc(y),
            y
        )

    def step_x_loc(self, x):
        return self._time_coord_model.step_coord_loc(x)

    def step_y_loc(self, y):
        return self._layer_coord_model.step_coord_loc(y)

    def compute_timeframe(self, x):
        return self._time_coord_model.compute_unit_index_loc_(x)

    def compute_layer_index(self, y):
        return self._layer_coord_model.compute_unit_index_loc_(y)

    def compute_start_x(self):
        return self._time_coord_model.compute_unit_coord_at(self._track_start)

    def compute_start_x_at(self, frame):
        return self._time_coord_model.compute_unit_coord_at(frame)

    def compute_width(self):
        return self._time_coord_model.compute_size_by_count(self.track_count)

    def compute_width_for(self, count):
        return self._time_coord_model.compute_size_by_count(count)

    def register(self, widget):
        self._track_widget_dict[widget._track_model.key] = widget
        self.update()

    def update(self):
        self._all_frames = []
        self._ordered_track_model_dict.clear()
        if not self._track_widget_dict:
            return
        sys.stdout.write('stage is change.\n')
        clip_start_list = []
        clip_end_list = []

        # get data by layer index
        dict_0 = {}
        for k, v in self._track_widget_dict.items():
            i_model = v._track_model
            if i_model.is_bypass > 0:
                i_model.apply_valid_frames([])
                continue
            elif i_model.is_trash > 0:
                i_model.apply_valid_frames([])
                continue

            i_layer_index = i_model._layer_index

            clip_start_list.append(i_model.clip_start)
            clip_end_list.append(i_model.clip_end)

            dict_0.setdefault(i_layer_index, []).append(i_model)

        layer_index_list = dict_0.keys()
        layer_index_list.sort()
        layer_index_list.reverse()

        # update valid frames
        for i_layer_index in layer_index_list:
            i_models = dict_0[i_layer_index]
            self._layer_prc(self._all_frames, i_models)

        dict_1 = {}
        for k, v in self._track_widget_dict.items():
            i_model = v._track_model
            i_frame_ranges = i_model.valid_frame_ranges
            for j in i_frame_ranges:
                dict_1[j] = i_model

        missing_frame_ranges = TrackModel._find_missing_frame_ranges(self._all_frames)
        if missing_frame_ranges:
            for i in missing_frame_ranges:
                dict_1[i] = None

        keys_1 = dict_1.keys()
        keys_1.sort()
        for i_key in keys_1:
            self._ordered_track_model_dict[i_key] = dict_1[i_key]

        if clip_start_list:
            self._track_start = min(clip_start_list)
        else:
            self._track_start = 1
        if clip_end_list:
            self._track_end = max(clip_end_list)
        else:
            self._track_end = 24

    def get_one_node(self, key):
        return self._track_widget_dict.get(key)

    def get_one(self, key):
        _ = self._track_widget_dict.get(key)
        if _:
            return _._track_model

    def get_all_nodes(self):
        return self._track_widget_dict.values()

    def get_all_models(self):
        return [x._track_model for x in self._track_widget_dict.values()]

    def get_all_layer_names(self):
        return [x._track_model.key for x in self._track_widget_dict.values()]

    def generate_travel(self):
        return TrackStageTravel(self._ordered_track_model_dict)

    def restore(self):
        self._track_widget_dict.clear()

        self._all_frames = []
        self._ordered_track_model_dict.clear()

    def to_hash(self):
        return bsc_core.BscHash.to_hash_key(
            {k: v._track_model.to_hash() for k, v in self._track_widget_dict.items()}
        )

    def compute_max_layer_index(self):
        return max(x.layer_index for x in self.get_all_models())

    def find_next_key(self, name):
        if name not in self._track_widget_dict:
            return name
        else:
            count = 1
            new_name = '{}_copy'.format(name)
            while new_name in self._track_widget_dict:
                new_name = '{}_copy{}'.format(name, count)
                count += 1

            if new_name not in self._track_widget_dict:
                return new_name


class TrackStageTravel(object):
    def __init__(self, ordered_track_model_dict):
        self._ordered_track_model_dict = ordered_track_model_dict
        self._index = 0
        self._index_minimum = 0
        self._index_maximum = len(self._ordered_track_model_dict)-1
        self._frame_range_dict = {}
        self._track_model_index_dict = {}
        for idx, (k, v) in enumerate(self._ordered_track_model_dict.items()):
            self._frame_range_dict[idx] = k
            self._track_model_index_dict[idx] = v

        self._track_model_current = None

    def current_data(self):
        return self._frame_range_dict[self._index], self._track_model_index_dict[self._index]

    def pre_data(self):
        if self._index > self._index_minimum:
            return self._frame_range_dict[self._index-1], self._track_model_index_dict[self._index-1]

    def pre_model(self):
        if self._index > self._index_minimum:
            return self._track_model_index_dict[self._index-1]

    def pre_key(self):
        track_model = self.pre_model()
        if track_model:
            return track_model.key

    def pre_pre_model(self):
        if self._index > self._index_minimum+1:
            return self._track_model_index_dict[self._index-2]

    def pre_pre_data(self):
        if self._index > self._index_minimum+1:
            return self._frame_range_dict[self._index-2], self._track_model_index_dict[self._index-2]

    def pre_pre_key(self):
        track_model = self.pre_pre_model()
        if track_model:
            return track_model.key

    def next_data(self):
        if self._index < self._index_maximum:
            return self._frame_range_dict[self._index+1], self._track_model_index_dict[self._index+1]

    def next_model(self):
        if self._index < self._index_maximum:
            return self._track_model_index_dict[self._index+1]

    def next_key(self):
        track_model = self.next_model()
        if track_model:
            return track_model.key

    def next_next_model(self):
        if self._index < self._index_maximum-1:
            return self._track_model_index_dict[self._index+2]

    def next_next_key(self):
        track_model = self.next_next_model()
        if track_model:
            return track_model.key

    def next_is_valid(self):
        if self._index < self._index_maximum:
            return self._track_model_index_dict[self._index+1] is not None
        return True

    def next(self):
        self._index += 1

    def is_valid(self):
        return self._index <= self._index_maximum

    def is_start(self):
        return self._index == 0

    def is_end(self):
        return self._index == self._index_maximum
