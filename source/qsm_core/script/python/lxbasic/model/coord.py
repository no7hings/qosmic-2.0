# coding=utf-8


class CoordModel(object):
    @classmethod
    def index_loc(cls, coord, unit_size):
        if coord >= 0:
            return int(coord/unit_size)
        return int(coord/unit_size)-1

    def __init__(self):
        self._unit_current_index = 0

        self._unit_basic_size = 48
        self._unit_size = 48

        self._unit_offset_index = 0
        self._unit_offset_coord = 0

        self._unit_index_count = 0
        self._unit_index_minimum, self._unit_index_maximum = 0, 1

        self._draw_offset = -1

        self._scale = 1.0
        self._translate = 0

    def setup(self, basic_size):
        self._unit_basic_size = basic_size

    def update(self, translate, scale, size):
        self._translate = translate
        self._scale = scale

        self._unit_size = self._unit_basic_size*scale

        self._unit_offset_coord = translate%self._unit_size

        self._unit_offset_index = self._index_loc(translate)

        self._unit_index_count = int(size/self._unit_size)+2

        self._unit_index_minimum, self._unit_index_maximum = (
            -self._unit_offset_index, self._unit_index_count-self._unit_offset_index
        )

    def _index_loc(self, coord):
        if coord >= 0:
            return int(coord/self._unit_size)
        return int(coord/self._unit_size)-1

    def compute_unit_index_loc(self, coord):
        return self._index_loc(coord-self._translate+self._unit_size/2)

    def compute_unit_index_loc_(self, coord):
        return self._index_loc(coord-self._translate)

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
    def unit_index_count(self):
        return self._unit_index_count

    @property
    def unit_index_offset(self):
        return self._unit_offset_index

    @property
    def unit_index_range(self):
        return -self._unit_offset_index, (self._unit_index_count-self._unit_offset_index)-2
