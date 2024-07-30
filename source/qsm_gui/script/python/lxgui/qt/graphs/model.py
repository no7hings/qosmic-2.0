# coding=utf-8
import copy
import sys

import lxbasic.core as bsc_core


class CoordModel(object):
    def __init__(self):
        self._unit_current_index = 0

        self._unit_basic_size = 48
        self._unit_size = 48

        self._unit_offset_index = 0
        self._unit_offset_coord = 0

        self._unit_count = 0
        self._unit_index_minimum, self._unit_index_maximum = 0, 1

        self._draw_offset = -1

        self._scale = 1.0
        self._translate = 0

    def update(self, translate, scale, size):
        self._translate = translate
        self._scale = scale

        self._unit_size = self._unit_basic_size*scale

        self._unit_offset_coord = translate % self._unit_size

        self._unit_offset_index = self._index_loc(translate)

        self._unit_count = int(size/self._unit_size)+2

        self._unit_index_minimum, self._unit_index_maximum = (
            -self._unit_offset_index, self._unit_count-self._unit_offset_index
        )

    @classmethod
    def index_loc(cls, coord, unit_size):
        if coord >= 0:
            return int(coord/unit_size)
        return int(coord/unit_size)-1

    def _index_loc(self, coord):
        if coord >= 0:
            return int(coord/self._unit_size)
        return int(coord/self._unit_size)-1

    def compute_unit_index_loc(self, coord):
        return self._index_loc(coord-self._translate+self._unit_size/2)

    def compute_unit_count_by(self, size):
        return int(size/self._unit_size)

    def compute_coord_at(self, index):
        return int(
            index*self._unit_size+self._unit_offset_coord
        )

    def compute_unit_coord_at(self, index):
        return index*self._unit_size+self._translate

    def compute_offset_at(self, index):
        return int(
            (index+self._unit_offset_index)*self._unit_size+self._unit_offset_coord
        )

    def compute_draw_index_at(self, idx):
        return idx-self._unit_offset_index+self._draw_offset

    def compute_draw_coord_at(self, idx):
        return (idx*self._unit_size)+(self._draw_offset*self._unit_size)+self._unit_offset_coord

    def compute_basic_index_loc(self, coord):
        return self.index_loc(coord, self._unit_basic_size)

    def compute_size_by_count(self, count):
        return int(count*self._unit_size)

    def compute_basic_size_by(self, count):
        return int(count*self._unit_basic_size)

    def compute_basic_coord_at(self, index):
        return int(
            index*self._unit_basic_size
        )

    def step_coord_loc(self, coord):
        return int(
            self._index_loc(coord)*self._unit_size+self._unit_offset_coord
        )

    @property
    def unit_size(self):
        return self._unit_size

    @property
    def unit_offset(self):
        return self._unit_offset_coord

    @property
    def unit_count(self):
        return self._unit_count

    @property
    def unit_index_offset(self):
        return self._unit_offset_index


class TrackModel(object):
    COPY_KEYS = [
        '_key',
        '_speed',
        '_start',
        '_source_start', '_source_end',
        '_pre_cycle', '_post_cycle',
        '_clip_start', '_clip_end',
        '_pre_blend', '_post_blend',
        '_valid_frames',
        '_layer_index'
    ]

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
                    result.append(start)
                else:
                    result.append((start, end))
                start = frames[i]
                end = frames[i]

        if start == end:
            result.append(start)
        else:
            result.append((start, end))

        return result

    def __init__(self, stage_model):
        self._stage_model = stage_model

        self.setup('untitled', 1, 1, 24, 0, 1, 0)

    def __str__(self):
        return '{}(key={}, time={}-{}, layer={})'.format(
            self.__class__.__name__, self._key, self._clip_start, self._clip_end, self._layer_index
        )

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

    def setup(self, key, start, source_start, source_end, pre_cycle, post_cycle, layer_index):
        self._key = key

        self._speed = 1.0

        self._start = int(start)

        self._source_start = int(source_start)
        self._source_end = int(source_end)

        self._pre_cycle = int(pre_cycle)
        self._post_cycle = int(post_cycle)

        self._clip_start = self._start
        self._clip_end = self._start+self.basic_post_count-1

        self._pre_blend = -4
        self._post_blend = -4

        self._valid_frames = []

        self._layer_index = int(layer_index)

    def apply_valid_frames(self, frames):
        self._valid_frames = frames

    @property
    def valid_frame_ranges(self):
        return self._find_frame_ranges(self._valid_frames)

    @property
    def key(self):
        return self._key

    @property
    def rgb(self):
        return bsc_core.RawTextOpt(self._key).to_rgb_1(s_p=(25, 35), v_p=(85, 95))

    @property
    def layer_index(self):
        return self._layer_index

    @layer_index.setter
    def layer_index(self, index):
        if index != self._layer_index:
            self._layer_index = index

    def copy(self):
        _ = self.__class__(self._stage_model)
        for i in self.COPY_KEYS:
            i_value = self.__dict__[i]
            if isinstance(i_value, (list, dict)):
                _.__dict__[i] = copy.copy(i_value)
            else:
                _.__dict__[i] = i_value
        return _

    @property
    def speed(self):
        return self._speed

    @property
    def source_count(self):
        return self._source_end-self._source_start+1

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if value != self._start:
            # start_offset and clip_count is not change mark first
            offset = self.start_offset
            count = self.clip_count

            self._start = int(value)
            # update clip start and end, count is not change
            self._clip_start = self._start-offset
            self._clip_end = self._clip_start+count-1

    @property
    def clip_start(self):
        return self._clip_start

    @clip_start.setter
    def clip_start(self, value):
        if value != self._clip_start:
            self._clip_start = int(value)

    def offset_by_clip_start(self, value):
        if value != self._clip_start:
            # start_offset and clip_count is not change mark first
            offset = self.start_offset
            count = self.clip_count

            self._clip_start = int(value)

            self._start = self._clip_start+offset
            self._clip_end = int(self._clip_start+count-1)

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
    def start_offset(self):
        return self._start-self._clip_start

    @property
    def start_trim(self):
        offset = self.start_offset
        if offset < 0:
            return -offset
        return 0

    @property
    def end_offset(self):
        return self.clip_end-self.basic_end

    @property
    def basic_end_trim(self):
        offset = self.end_offset
        if offset < 0:
            return -offset
        return 0

    @property
    def basic_pre_count(self):
        return int((self.source_count*self._pre_cycle)/self._speed)

    @property
    def basic_post_count(self):
        return int((self.source_count*self._post_cycle)/self._speed)

    @property
    def basic_start_offset(self):
        return -self.basic_pre_count-self._clip_start+self._start

    @property
    def basic_end_offset(self):
        # offset for start
        return self.basic_post_count-self._clip_start+self._start

    @property
    def basic_start(self):
        return self._start-self.basic_pre_count

    @property
    def basic_end(self):
        return self._start+self.basic_post_count-1

    @property
    def pre_blend(self):
        return self._pre_blend

    @property
    def post_blend(self):
        return self._post_blend

    @property
    def frames(self):
        return list(range(self._clip_start, self._clip_end+1))

    def compute_timetrack_args(self):
        bsc_x = self.compute_basic_x_at(self._clip_start)
        bsc_y = self.compute_basic_y_at(self._layer_index)
        bsc_w = self.compute_basic_w_by(self.clip_count)
        bsc_h = TrackStageModel.LAYER_BASIC_UNIT
        return bsc_x, bsc_y, bsc_w, bsc_h

    def compute_clip_start_loc(self, x):
        return self._stage_model._time_coord_model.compute_unit_index_loc(x)

    def compute_clip_count_by(self, w):
        return self._stage_model._time_coord_model.compute_unit_count_by(w)

    def compute_basic_x_at(self, clip_start):
        return self._stage_model._time_coord_model.compute_basic_coord_at(clip_start)

    def compute_basic_y_at(self, layer_index):
        return self._stage_model._layer_coord_model.compute_basic_coord_at(layer_index)

    def compute_basic_w_by(self, clip_count):
        return self._stage_model._time_coord_model.compute_basic_size_by(clip_count)

    def compute_layer_index_loc(self, y):
        return self._stage_model._layer_coord_model.compute_unit_index_loc(y)

    def compute_w_by_count(self, count):
        return self._stage_model._time_coord_model.compute_size_by_count(count)


class TrackStageModel(object):
    TIME_BASIC_UNIT = 100
    LAYER_BASIC_UNIT = 48

    def __init__(self):
        self._track_dict = {}

        self._time_coord_model = CoordModel()
        self._time_coord_model.update(0, 1.0, self.TIME_BASIC_UNIT)

        self._layer_coord_model = CoordModel()
        self._layer_coord_model.update(0, 1.0, self.LAYER_BASIC_UNIT)

        self._track_start = 1
        self._track_end = 2

    @property
    def track_start(self):
        return self._track_start

    @property
    def track_end(self):
        return self._track_end
    
    @property
    def track_count(self):
        return self._track_end-self._track_start+1

    def create_one(self, widget, key, start, source_start, source_end, pre_cycle, post_cycle, layer_index):
        model = TrackModel(self)
        model.setup(key, start, source_start, source_end, pre_cycle, post_cycle, layer_index)
        widget._track_model = model
        widget._track_last_model = model.copy()
        self.register(widget)
        return model

    def step_coord_loc(self, x, y):
        return self._time_coord_model.step_coord_loc(x), self._layer_coord_model.step_coord_loc(y)

    def compute_start_x(self):
        return self._time_coord_model.compute_unit_coord_at(self._track_start)

    def compute_start_x_at(self, frame):
        return self._time_coord_model.compute_unit_coord_at(frame)

    def compute_width(self):
        return self._time_coord_model.compute_size_by_count(self.track_count)

    def compute_width_for(self, count):
        return self._time_coord_model.compute_size_by_count(count)

    def register(self, widget):
        self._track_dict[widget._track_model.key] = widget
        self.update()
        
    def update(self):
        frame_stack = []
        sys.stdout.write('update stage.\n')
        clip_start_list = []
        clip_end_list = []

        dict_0 = {}
        for k, v in self._track_dict.items():
            i_model = v._track_model
            i_layer_index = i_model._layer_index

            clip_start_list.append(i_model.clip_start)
            clip_end_list.append(i_model.clip_end)

            dict_0.setdefault(i_layer_index, []).append(i_model)

        layer_index_list = dict_0.keys()
        layer_index_list.sort()
        layer_index_list.reverse()

        for i_layer_index in layer_index_list:
            i_models = dict_0[i_layer_index]
            self._same_layer_process(frame_stack, i_models)

        self._track_start = min(clip_start_list)
        self._track_end = max(clip_end_list)

    def get_all(self):
        return [x._track_model for x in self._track_dict.values()]

    @classmethod
    def _same_layer_process(cls, frame_stack, models):
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
                i_valid_frames = list(set(i_frames)-set(frame_stack))
                i_valid_frames.sort()
                j_model.apply_valid_frames(i_valid_frames)
                frame_stack.extend(i_frames)
        return frame_stack

