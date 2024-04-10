# coding:utf-8
import math


class DccMeshFaceVertexIndicesOpt(object):
    # print DccMeshFaceVertexIndicesOpt(
    #     [0, 1, 5, 4, 1, 2, 6, 5, 2, 3, 7, 6, 4, 5, 9, 8, 5, 6, 10, 9, 6, 7, 11, 10, 8, 9, 13, 12, 9, 10, 14, 13, 10, 11, 15, 14]
    # ).reverse_by_counts(
    #     [4, 4, 4, 4, 4, 4, 4, 4, 4]
    # )
    # print DccMeshFaceVertexIndicesOpt(
    #     [0, 1, 5, 4, 1, 2, 6, 5, 2, 3, 7, 6, 4, 5, 9, 8, 5, 6, 10, 9, 6, 7, 11, 10, 8, 9, 13, 12, 9, 10, 14, 13, 10, 11, 15, 14]
    # ).reverse_by_start_indices(
    #     [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
    # )
    def __init__(self, face_vertex_indices):
        self._raw = face_vertex_indices

    def reverse_by_counts(self, counts):
        lis = []
        vertex_index_start = 0
        for i_count in counts:
            vertex_index_end = vertex_index_start+i_count
            for j in range(vertex_index_end-vertex_index_start):
                lis.append(self._raw[vertex_index_end-j-1])
            #
            vertex_index_start += i_count
        return lis

    def reverse_by_start_indices(self, start_vertex_indices):
        lis = []
        for i in range(len(start_vertex_indices)):
            if i > 0:
                vertex_index_start = start_vertex_indices[i-1]
                vertex_index_end = start_vertex_indices[i]
                for j in range(vertex_index_end-vertex_index_start):
                    lis.append(self._raw[vertex_index_end-j-1])
        return lis


class DccMeshFaceShellOpt(object):
    def __init__(self, vertex_counts, vertex_indices):
        self.__vertex_counts, self.__vertex_indices = vertex_counts, vertex_indices

    @classmethod
    def _get_connected_face_indices(cls, face_to_vertex_dict, vertex_to_face_dict, face_index):
        return set(j for i in face_to_vertex_dict[face_index] for j in vertex_to_face_dict[i])

    @classmethod
    def _generate_face_and_vertex_query_dict(cls, vertex_counts, vertex_indices):
        face_to_vertex_dict = {}
        vertex_to_face_dict = {}
        vertex_index_start = 0
        for i_face_index, i_vertex_count in enumerate(vertex_counts):
            vertex_index_end = vertex_index_start+i_vertex_count
            for j in range(vertex_index_end-vertex_index_start):
                j_vertex_index = vertex_indices[vertex_index_start+j]
                vertex_to_face_dict.setdefault(j_vertex_index, []).append(i_face_index)
                face_to_vertex_dict.setdefault(i_face_index, []).append(j_vertex_index)
            #
            vertex_index_start += i_vertex_count
        return face_to_vertex_dict, vertex_to_face_dict

    @classmethod
    def generate_shell_dict_from_face_vertices(cls, vertex_counts, vertex_indices):
        # StgFileOpt(
        #     '/data/f/shell_id_test/input.json'
        # ).set_write([vertex_counts, vertex_indices])
        face_to_vertex_dict, vertex_to_face_dict = cls._generate_face_and_vertex_query_dict(
            vertex_counts, vertex_indices
        )
        #
        _face_count = len(vertex_counts)
        #
        all_face_indices = set(range(_face_count))
        #
        _cur_shell_index = 0
        #
        shell_to_face_dict = {}
        #
        _less_face_indices = set(range(_face_count))
        _cur_search_face_indices = set()
        _cur_shell_face_indices = set()
        c = 0
        while _less_face_indices:
            if c > _face_count:
                break
            #
            if _less_face_indices == all_face_indices:
                _cur_search_face_indices = cls._get_connected_face_indices(face_to_vertex_dict, vertex_to_face_dict, 0)
                _cur_shell_face_indices = set()
                _cur_shell_face_indices.update(_cur_search_face_indices)

            _less_face_indices -= _cur_search_face_indices
            #
            cur_connected_face_indices = set()
            [
                cur_connected_face_indices.update(
                    cls._get_connected_face_indices(face_to_vertex_dict, vertex_to_face_dict, i)
                ) for i in _cur_search_face_indices
            ]

            cur_int = cur_connected_face_indices&_cur_shell_face_indices
            cur_dif = cur_connected_face_indices-_cur_shell_face_indices
            if cur_int:
                if cur_dif:
                    _cur_shell_face_indices.update(cur_dif)
                    _cur_search_face_indices = cur_dif
                else:
                    shell_to_face_dict[_cur_shell_index] = _cur_shell_face_indices
                    if _less_face_indices:
                        _cur_shell_index += 1
                        #
                        _cur_face_index = min(_less_face_indices)
                        _cur_search_face_indices = cls._get_connected_face_indices(
                            face_to_vertex_dict, vertex_to_face_dict, _cur_face_index
                            )
                        _cur_shell_face_indices = set()
                        _cur_shell_face_indices.update(_cur_search_face_indices)
            #
            c += 1
        return {i: k for k, v in shell_to_face_dict.items() for i in v}

    def generate(self):
        return self.generate_shell_dict_from_face_vertices(
            self.__vertex_counts, self.__vertex_indices
        )


class CameraMtd(object):
    # noinspection PyUnusedLocal
    @classmethod
    def compute_front_transformation(cls, geometry_args, angle, mode=0, bottom=False):
        (x, y, z), (c_x, c_y, c_z), (w, h, d) = geometry_args

        if mode == 1:
            s = max(w, h)
        else:
            s = max(w, h)

        z_1 = s/math.tan(math.radians(angle))

        if bottom is True:
            t_x, t_y, t_z = (c_x, c_y+(s-h)/2, z_1-c_z)
        else:
            t_x, t_y, t_z = (c_x, c_y, z_1-c_z)

        r_x, r_y, r_z = 0, 0, 0
        s_x, s_y, s_z = 1, 1, 1
        return (t_x, t_y, t_z), (r_x, r_y, r_z), (s_x, s_y, s_z)

    # this function is for the old call
    get_front_transformation = compute_front_transformation

    @classmethod
    def compute_project_transformation(cls, size, scale_percent, margin_percent, camera_fov, camera_screen_mode, render_resolution):
        # s = 1, x = y = -0
        # s = .5, x = y = -.25
        # s = .25, x = y = -.375
        # x = y = -(0.5 - s/2)
        # a/b=tan(camera_fov/2)
        b = (size/2)/math.tan(math.radians(camera_fov/2))
        x, y = 1, 1
        w, h = render_resolution
        if camera_screen_mode == 'horizontal':
            x, y = 1, h/w
        elif camera_screen_mode == 'vertical':
            x, y = w/h, 1
        s_s = min(x, y)
        s = scale_percent*s_s
        t_x, t_y, t_z = -(0.5*x-s/2)+margin_percent, -(0.5*y-s/2)+margin_percent, -b
        s_x, s_y, s_z = s, s, s
        return (t_x, t_y, t_z), (s_x, s_y, s_z)


class RectLayoutOpt(object):
    class Directions(object):
        class Direction(int):
            def __str__(self):
                if self == 0:
                    return 'Directions.AlignW'
                else:
                    return 'Directions.AlignH'

            def swap(self):
                if self == 0:
                    return self.__class__(1)
                else:
                    return self.__class__(0)

            def is_align_w(self):
                return self == 0

            def is_align_h(self):
                return self == 1

        AlignW = Direction(0)
        AlignH = Direction(1)

    class Coord(object):
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __str__(self):
            return '{}(x={}, y={})'.format(
                self.__class__.__name__,
                self.x, self.y,
            )

        def __repr__(self):
            return self.__str__()

    class AbsRect(object):
        def _init_rect_(self, x, y, w, h):
            self.x, self.y, self.w, self.h = x, y, w, h

            self.__spacing = 0

        @property
        def spacing(self):
            return self.__spacing

        @spacing.setter
        def spacing(self, v):
            self.__spacing = v

        @property
        def args(self):
            return self.x, self.y, self.w, self.h

        @property
        def exact_args(self):
            return self.x, self.y, self.w-self.__spacing, self.h-self.__spacing

        @property
        def exact_rect(self):
            return self.__class__(
                self.x, self.y, self.w-self.__spacing, self.h-self.__spacing
            )

        @property
        def top_left(self):
            return RectLayoutOpt.Coord(self.x, self.y)

        @top_left.setter
        def top_left(self, coord):
            self.x, self.y = coord.x, coord.y

        @property
        def top_right(self):
            return RectLayoutOpt.Coord(self.x+self.w, self.y)

        @top_right.setter
        def top_right(self, coord):
            self.x, self.y = coord.x-self.w, coord.y

        @property
        def bottom_left(self):
            return RectLayoutOpt.Coord(self.x, self.y+self.h)

        @bottom_left.setter
        def bottom_left(self, coord):
            self.x, self.y = coord.x, coord.y-self.h

        @property
        def bottom_right(self):
            return RectLayoutOpt.Coord(self.x+self.w, self.y+self.h)

        @bottom_right.setter
        def bottom_right(self, coord):
            self.x, self.y = coord.x-self.w, coord.y-self.h

        @property
        def center(self):
            return RectLayoutOpt.Coord(self.x+self.w/2, self.y+self.h/2)

        @center.setter
        def center(self, coord):
            self.x, self.y = coord.x-self.w/2, coord.y-self.h/2

        def update_range(self, coord):
            c = self.bottom_right
            # update width and height
            if c.x < coord.x:
                self.w = coord.x-self.x
            if c.y < coord.y:
                self.h = coord.y-self.y

        def get_is_valid(self):
            return None not in [self.w, self.h]

    class AreaRect(AbsRect):
        def __init__(self, layout, direction, x, y, w, h):
            self.__layout = layout
            self.__direction = direction

            self._init_rect_(x, y, w, h)

            self.__space_direction_cur = self.__direction
            self.__space_rect_cur = None
            self.__piece_rect_cur = None

            self.__top_left_cur = None

            self.__area_fill_rect = None

        def __str__(self):
            return '{}(x={}, y={}, w={}, h={})'.format(
                self.__class__.__name__,
                self.x, self.y, self.w, self.h
            )

        def __repr__(self):
            return self.__str__()

        @property
        def piece_rect(self):
            return self.__piece_rect_cur

        @property
        def space_rect(self):
            return self.__space_rect_cur

        @property
        def area_fill_rect(self):
            return self.__area_fill_rect

        @property
        def space_direction(self):
            return self.__space_direction_cur

        def start(self):
            # align w
            if self.h is None:
                rect = self.__layout.take_one_as_h_maximum()
                if rect:
                    # update h first
                    self.h = rect.h
                    # layout rect
                    rect.top_left = self.top_left
                    # update fill rect
                    self.__area_fill_rect = RectLayoutOpt.Rect(x=self.x, y=self.y, w=0, h=0)
                    self.__area_fill_rect.update_range(rect.bottom_right)
                    # try next
                    space_rect_pre = self
                    # find second rect
                    c_r = rect.top_right
                    #
                    self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                        area=self, direction=self.__direction.swap(),
                        x=c_r.x, y=c_r.y, w=space_rect_pre.w-rect.w, h=rect.h,
                        parent=None
                    )
                    # self.__space_rect_cur.spacing = self.spacing
                    self.next_by_space(self.__space_rect_cur, 'layout start')
            # align h
            elif self.w is None:
                # first rect, layout align h take maximum width one
                rect = self.__layout.take_one_as_w_maximum()
                if rect:
                    # update w first
                    self.w = rect.w
                    # layout rect
                    rect.top_left = self.top_left
                    # update fill rect
                    self.__area_fill_rect = RectLayoutOpt.Rect(x=self.x, y=self.y, w=0, h=0)
                    # self.__area_fill_rect.spacing = self.spacing
                    self.__area_fill_rect.update_range(rect.bottom_right)
                    # try next
                    space_rect_pre = self
                    c_r = rect.bottom_left
                    # find second rect
                    self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                        area=self, direction=self.__direction.swap(),
                        x=c_r.x, y=c_r.y, w=rect.w, h=space_rect_pre.h-rect.h,
                        parent=None,
                    )
                    # self.__space_rect_cur.spacing = self.spacing
                    self.next_by_space(self.__space_rect_cur, 'layout start')

        # noinspection PyUnusedLocal
        def next_by_space_and_rect(self, space_rect, rect, scheme=None):
            if self.__space_rect_cur is not None:
                # layout rect
                rect.top_left = self.__space_rect_cur.top_left
                rect.set_space(space_rect)
                self.__area_fill_rect.update_range(rect.bottom_right)
                # generate piece
                piece = space_rect.parent
                c_r = rect.bottom_right
                c_a = self.bottom_right
                if piece is None:
                    if self.__direction.is_align_w():
                        self.__piece_rect_cur = RectLayoutOpt.SpaceRect(
                            area=self, direction=self.__direction.swap(),
                            x=rect.x, y=rect.y, w=rect.w, h=self.h,
                            parent=None
                        )
                        # self.__piece_rect_cur.spacing = self.spacing
                        if c_r.x >= c_a.x and c_r.y >= c_a.y:
                            self.next_area()
                        else:
                            if c_r.y >= c_a.y:
                                self.next_piece()
                            else:
                                c_r_0 = rect.bottom_left
                                self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                                    area=self, direction=self.__piece_rect_cur.direction,
                                    x=c_r_0.x, y=c_r_0.y, w=rect.w, h=c_a.y-c_r_0.y,
                                    parent=self.__piece_rect_cur
                                )
                                # self.__space_rect_cur.spacing = self.spacing
                                self.next_by_space(self.__space_rect_cur, 'new piece')
                    elif self.__direction.is_align_h():
                        self.__piece_rect_cur = RectLayoutOpt.SpaceRect(
                            area=self, direction=self.__direction.swap(),
                            x=rect.x, y=rect.y, w=self.w, h=rect.h,
                            parent=None
                        )
                        # self.__piece_rect_cur.spacing = self.spacing
                        if c_r.x >= c_a.x and c_r.y >= c_a.y:
                            self.next_area()
                        else:
                            if c_r.x >= c_a.x:
                                self.next_piece()
                            else:
                                c_r_0 = rect.top_right
                                self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                                    area=self, direction=self.__piece_rect_cur.direction.swap(),
                                    x=c_r_0.x, y=c_r_0.y, w=c_a.x-c_r.x, h=rect.h,
                                    parent=self.__piece_rect_cur
                                )
                                # self.__space_rect_cur.spacing = self.spacing
                                self.next_by_space(self.__space_rect_cur, 'new piece')
                else:
                    c_p = piece.bottom_right
                    if self.__direction.is_align_w():
                        if c_r.x >= c_p.x and c_r.y >= c_p.y:
                            self.next_piece()
                        else:
                            c_r_0 = rect.bottom_left
                            self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                                area=self, direction=piece.direction,
                                x=c_r_0.x, y=c_r_0.y, w=piece.w, h=c_a.y-c_r_0.y,
                                parent=piece
                            )
                            # self.__space_rect_cur.spacing = self.spacing
                            self.next_by_space(self.__space_rect_cur, 'new space')
                    elif self.__direction.is_align_h():
                        if c_r.x >= c_p.x and c_r.y >= c_p.y:
                            self.next_piece()
                        else:
                            c_r_0 = rect.top_right
                            self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                                area=self, direction=piece.direction,
                                x=c_r_0.x, y=c_r_0.y, w=c_a.x-c_r_0.x, h=piece.h,
                                parent=piece
                            )
                            # self.__space_rect_cur.spacing = self.spacing
                            self.next_by_space(self.__space_rect_cur, 'new space')

        def next_area(self):
            self.__layout.next()

        def next_piece(self):
            c_a = self.bottom_right
            c_f = self.__area_fill_rect.bottom_right
            if self.__direction.is_align_w():
                self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                    area=self, direction=self.__direction.swap(),
                    x=c_f.x, y=self.y, w=c_a.x-c_f.x, h=self.h,
                    parent=None
                )
                # self.__space_rect_cur.spacing = self.spacing
                self.next_by_space(self.__space_rect_cur, 'next piece')
            elif self.__direction.is_align_h():
                self.__space_rect_cur = RectLayoutOpt.SpaceRect(
                    area=self, direction=self.__direction.swap(),
                    x=self.x, y=c_f.y, w=self.w, h=c_a.y-c_f.y,
                    parent=None
                )
                # self.__space_rect_cur.spacing = self.spacing
                self.next_by_space(self.__space_rect_cur, 'next piece')

        def next_by_space(self, space_rect, scheme=None):
            if self.__layout.get_is_finished() is False:
                rect_next = self.__layout.take_one_by_space_rect(
                    space_rect,
                )
                # found
                if rect_next is not None:
                    self.next_by_space_and_rect(space_rect, rect_next, scheme)
                # not found
                else:
                    # is a piece
                    if space_rect.parent is None:
                        self.next_area()
                    else:
                        self.next_piece()

        @property
        def layout(self):
            return self.__layout

        @property
        def direction(self):
            return self.__direction

    class SpaceRect(AbsRect):
        def __init__(self, area, direction, x, y, w, h, parent=None):
            self._init_rect_(x, y, w, h)
            self.__area = area
            self.__direction = direction
            self.__parent = parent

        def __str__(self):
            return '{}(x={}, y={}, w={}, h={})'.format(
                self.__class__.__name__,
                self.x, self.y, self.w, self.h
            )

        def __repr__(self):
            return self.__str__()

        @property
        def parent(self):
            return self.__parent

        @property
        def ancestors(self):
            def rcs_fnc_(n_):
                _p = n_.parent
                if _p is not None:
                    list_.append(_p)
                    rcs_fnc_(_p)

            list_ = []
            rcs_fnc_(self)
            return list_

        @property
        def area(self):
            return self.__area

        @property
        def direction(self):
            return self.__direction

        def update_space_by_rect(self, rect):
            if self.__direction.is_align_w():
                self.h = rect.h
            elif self.__direction.is_align_h():
                self.w = rect.w

    class Rect(AbsRect):
        def __init__(self, x, y, w, h, index=0):
            self._init_rect_(x, y, w, h)
            self.__index = index

            self.__space = None

        def set_space(self, space):
            self.__space = space

        @property
        def index(self):
            return self.__index

        @property
        def space(self):
            return self.__space

        def __str__(self):
            return '{}(x={}, y={}, w={}, h={}, index={})'.format(
                self.__class__.__name__,
                self.x, self.y, self.w, self.h,
                self.index
            )

        def __repr__(self):
            return self.__str__()

    def __init__(self, xywh_array, spacing=0):
        """
        rect_arg: ((x, y), (w, h))
        """
        self.__x, self.__y = 0, 0

        self.__spacing = spacing
        self.__rects = []
        self.__w_dict = {}
        self.__h_dict = {}
        for i_index, (i_x, i_y, i_w, i_h) in enumerate(xywh_array):
            i_w_, i_h_ = i_w+spacing, i_h+spacing
            i_rect = self.Rect(i_x, i_y, i_w_, i_h_, i_index)
            i_rect.spacing = spacing
            self.__rects.append(i_rect)
            self.__w_dict.setdefault(i_w_, []).append(i_rect)
            self.__h_dict.setdefault(i_h_, []).append(i_rect)

        self.__rects_layout = []

        self.__area_rect_cur = None

    @staticmethod
    def find_w_maximum(rects, w_maximum):
        if len(rects) > 1:
            w_dict = {}
            for i_index, i_rect in enumerate(rects):
                w_dict.setdefault(i_rect.w, []).append(i_index)

            ws = [i for i in w_dict.keys() if i <= w_maximum]
            if ws:
                w_maximum = max(ws)
                return rects[w_dict[w_maximum][0]]
        else:
            rect = rects[0]
            if rect.w <= w_maximum:
                return rect

    def take_one_as_w_maximum_with_hs(self, dict_h, hs, w_maximum):
        rects = []
        [rects.extend(dict_h[i]) for i in hs]
        rect = self.find_w_maximum(rects, w_maximum)
        if rect is not None:
            self.take_rect(rect)
            return rect

    def take_one_as_h_maximum_with_ws(self, dict_w, ws, h_maximum):
        rects = []
        [rects.extend(dict_w[i]) for i in ws]
        rect = self.find_h_maximum(rects, h_maximum)
        if rect is not None:
            self.take_rect(rect)
            return rect

    @staticmethod
    def find_h_maximum(rects, h_maximum):
        if len(rects) > 1:
            h_dict = {}
            for i_index, i_rect in enumerate(rects):
                h_dict.setdefault(i_rect.h, []).append(i_index)

            hs = [i for i in h_dict.keys() if i <= h_maximum]
            if hs:
                h_maximum = max(hs)
                return rects[h_dict[h_maximum][0]]
        else:
            rect = rects[0]
            if rect.h <= h_maximum:
                return rect

    @property
    def spacing(self):
        return self.__spacing

    @property
    def area_rect(self):
        return self.__area_rect_cur

    @property
    def layout_rect(self):
        if self.__area_rect_cur is not None:
            c_r = self.__area_rect_cur.bottom_right
            rect = self.Rect(
                self.__x, self.__y, c_r.x-self.__x, c_r.y-self.__y
            )
            rect.spacing = self.spacing
            return rect

    def take_one_as_w_maximum(self):
        if self.__w_dict:
            w = max(self.__w_dict.keys())
            rects_w = self.__w_dict[w]
            # find the maximum height one
            rect = self.find_h_maximum(rects_w, float('inf'))
            rects_w.remove(rect)
            if not rects_w:
                self.__w_dict.pop(w)

            self.__rects.remove(rect)
            self.__rects_layout.append(rect)

            h = rect.h
            rects_h = self.__h_dict[h]
            rects_h.remove(rect)
            if not rects_h:
                self.__h_dict.pop(h)
            return rect

    def take_one_as_h_maximum(self):
        if self.__h_dict:
            h = max(self.__h_dict.keys())
            rects_h = self.__h_dict[h]
            # find the maximum width one
            rect = self.find_w_maximum(rects_h, float('inf'))
            rects_h.remove(rect)
            if not rects_h:
                self.__h_dict.pop(h)

            self.__rects.remove(rect)
            self.__rects_layout.append(rect)

            w = rect.w
            rects_w = self.__w_dict[w]
            rects_w.remove(rect)
            if not rects_w:
                self.__w_dict.pop(w)
            return rect

    def take_rect(self, rect):
        w, h = rect.w, rect.h
        rects_w = self.__w_dict[w]
        rects_w.remove(rect)
        if not rects_w:
            self.__w_dict.pop(w)

        self.__rects.remove(rect)
        self.__rects_layout.append(rect)

        rects_h = self.__h_dict[h]
        rects_h.remove(rect)
        if not rects_h:
            self.__h_dict.pop(h)

    def take_one_by_space_rect(self, space_rect):
        direction = space_rect.direction
        w_maximum, h_maximum = space_rect.w, space_rect.h
        # step 3
        # find all height minimum then space, and find the width max one
        if direction.is_align_w():
            dict_h = self.__h_dict
            if dict_h:
                h_minimum = min(dict_h.keys())
                if h_minimum <= h_maximum:
                    hs = [i for i in dict_h.keys() if i <= h_maximum]
                    hs.sort()
                    hs.reverse()
                    # find maximum w
                    return self.take_one_as_w_maximum_with_hs(dict_h, hs, w_maximum)
        # find all width minimum then space, and find the high max one
        elif direction.is_align_h():
            dict_w = self.__w_dict
            if dict_w:
                w_minimum = min(dict_w.keys())
                if w_minimum <= w_maximum:
                    ws = [i for i in dict_w.keys() if i <= w_maximum]
                    ws.sort()
                    ws.reverse()
                    # find maximum h
                    return self.take_one_as_h_maximum_with_ws(dict_w, ws, h_maximum)

    def take_one_by_space(self, space):
        direction = space.direction
        # step 3
        # find all height minimum then space, and find the width max one
        if direction.is_align_w():
            h_maximum = space.h
            dict_h = self.__h_dict
            if dict_h:
                h_minimum = min(dict_h.keys())
                if h_minimum <= h_maximum:
                    hs = [i for i in dict_h.keys() if i <= h_maximum]
                    hs.sort()
                    hs.reverse()
                    # find maximum w
                    w_maximum = space.w
                    return self.take_one_as_w_maximum_with_hs(dict_h, hs, w_maximum)
        # find all width minimum then space, and find the high max one
        elif direction.is_align_h():
            w_maximum = space.w
            dict_w = self.__w_dict
            if dict_w:
                w_minimum = min(dict_w.keys())
                if w_minimum <= w_maximum:
                    ws = [i for i in dict_w.keys() if i <= w_maximum]
                    ws.sort()
                    ws.reverse()
                    # find maximum h
                    h_maximum = space.h
                    return self.take_one_as_h_maximum_with_ws(dict_w, ws, h_maximum)

    def get_is_finished(self):
        return not self.__rects

    def get_layout_rects(self):
        return self.__rects_layout

    def generate(self):
        # noinspection PyBroadException
        try:
            self.next()
        except Exception:
            import traceback
            traceback.print_exc()
        return self.get_layout_rects()

    def next(self):
        if self.get_is_finished() is False:
            if self.__area_rect_cur is None:
                # do step 1, take maximum width rect and put into origin
                w_maximum, h_maximum = max(self.__w_dict.keys()), max(self.__h_dict.keys())
                # use width
                if w_maximum >= h_maximum:
                    rect = self.take_one_as_w_maximum()
                    if rect:
                        # layout rect
                        rect.top_left = self.Coord(self.__x, self.__y)

                        c_r = rect.bottom_left

                        self.__area_rect_cur = self.AreaRect(
                            layout=self,
                            direction=self.Directions.AlignW,
                            x=c_r.x, y=c_r.y, w=rect.w, h=None
                        )
                        # self.__area_rect_cur.spacing = self.spacing
                        self.__area_rect_cur.start()
                # use height
                else:
                    rect = self.take_one_as_h_maximum()
                    if rect is not None:
                        # layout rect
                        rect.top_left = self.Coord(self.__x, self.__y)

                        c_r = rect.top_right

                        self.__area_rect_cur = self.AreaRect(
                            layout=self,
                            direction=self.Directions.AlignH,
                            x=c_r.x, y=c_r.y, w=None, h=rect.h
                        )
                        # self.__area_rect_cur.spacing = self.spacing
                        self.__area_rect_cur.start()
            # swap area
            else:
                # to align height
                if self.__area_rect_cur.direction.is_align_w():
                    area_rect_pre = self.__area_rect_cur
                    c_a = area_rect_pre.bottom_right

                    self.__area_rect_cur = self.AreaRect(
                        layout=self,
                        direction=self.Directions.AlignH,
                        x=c_a.x, y=self.__y, w=None, h=c_a.y-self.__y
                    )
                    # self.__area_rect_cur.spacing = self.spacing
                    self.__area_rect_cur.start()
                elif self.__area_rect_cur.direction.is_align_h():
                    area_rect_pre = self.__area_rect_cur

                    c_a = area_rect_pre.bottom_right

                    self.__area_rect_cur = self.AreaRect(
                        layout=self,
                        direction=self.Directions.AlignW,
                        x=self.__x, y=c_a.y, w=c_a.x-self.__x, h=None
                    )
                    # self.__area_rect_cur.spacing = self.spacing
                    self.__area_rect_cur.start()
