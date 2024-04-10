# coding:utf-8
import collections

import fnmatch

import parse

import re

import hashlib

import struct

import uuid

import os

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage


class _Uuid(object):
    BASIC = '4908BDB4-911F-3DCE-904E-96E4792E75F1'

    @classmethod
    def get_new(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def generate_by_hash_value(cls, hash_value):
        return str(uuid.uuid3(uuid.UUID(_Uuid.BASIC), str(hash_value))).upper()

    @classmethod
    def get_by_string(cls, string):
        return str(uuid.uuid3(uuid.UUID(_Uuid.BASIC), str(string))).upper()

    @classmethod
    def get_by_file(cls, file_path):
        if os.path.isfile(file_path):
            timestamp = os.stat(file_path).st_mtime
            return str(
                uuid.uuid3(uuid.UUID(_Uuid.BASIC), 'file="{}"; timestamp={}; version=2.0'.format(file_path, timestamp))
                ).upper()
        return str(uuid.uuid3(uuid.UUID(_Uuid.BASIC), str('file="{}"'.format(file_path)))).upper()


class _Hash(object):
    @classmethod
    def get_pack_format(cls, max_value):
        o = 'q'
        if max_value < 128:
            o = 'b'
        elif max_value < 32768:
            o = 'h'
        elif max_value < 4294967296:
            o = 'i'
        return o

    @classmethod
    def get_hash_value(cls, raw, as_unique_id=False):
        raw_str = str(raw)
        pack_array = [ord(i) for i in raw_str]
        s = hashlib.md5(
            struct.pack('%s%s'%(len(pack_array), cls.get_pack_format(max(pack_array))), *pack_array)
        ).hexdigest()
        if as_unique_id is True:
            return _Uuid.generate_by_hash_value(s)
        return s.upper()


class _LinePattern(object):
    @classmethod
    def to_fnmatch_pattern(cls, variant):
        if variant is not None:
            re_pattern = re.compile(r'[{](.*?)[}]', re.S)
            #
            keys = re.findall(re_pattern, variant)
            s = variant
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return variant

    def __init__(self, parse_pattern):
        self._pattern_parse = parse_pattern
        self._pattern_fnmatch = self.to_fnmatch_pattern(self._pattern_parse)

    def get_parse_pattern(self):
        return self._pattern_parse

    parse_pattern = property(get_parse_pattern)

    def get_fnmatch_pattern(self):
        return self._pattern_fnmatch

    fnmatch_pattern = property(get_fnmatch_pattern)


class _AbsDotFile(object):
    SEP = '\n'
    LINE_PATTERN_CLS = None

    @classmethod
    def _to_lines(cls, raw, sep):
        return [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    @classmethod
    def _generate_match_args(cls, pattern, lines):
        if lines:
            list_ = []
            pattern_0 = cls.LINE_PATTERN_CLS(pattern)
            lines = fnmatch.filter(
                lines, pattern_0.fnmatch_pattern
            )
            for l_line in lines:
                i_p = parse.parse(
                    pattern_0.parse_pattern, l_line, case_sensitive=True
                )
                if i_p:
                    i_variants = i_p.named
                    list_.append((l_line, i_variants))
            return list_
        return []

    def __init__(self, file_path):
        self._file_path = file_path
        self._update_lines()

    def _update_lines(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = self.SEP
                self._lines = self._to_lines(raw, sep)

    def get_file_path(self):
        return self._file_path

    file_path = property(get_file_path)

    def get_lines(self):
        return self._lines

    lines = property(get_lines)


class DotXgenOpt(_AbsDotFile):
    SEP = '\n\n'
    LINE_PATTERN_CLS = _LinePattern

    FILE_REFERENCE_DICT = {
        'Palette': ['xgDataPath', 'xgProjectPath'],
        'Description': ['xgDataPath', 'xgProjectPath']
    }

    def __init__(self, file_path):
        super(DotXgenOpt, self).__init__(file_path)

    def _generate_node_args(self):
        list_ = []
        bsc_log.Log.trace_method_result(
            'file parse is started', 'file="{}"'.format(
                self._file_path
            )
        )
        pattern_0 = self.LINE_PATTERN_CLS('{obj_type}\n{port_lines}\n')
        lines = fnmatch.filter(
            self.lines, pattern_0.fnmatch_pattern
        )
        for i_line in lines:
            p = parse.parse(
                pattern_0.parse_pattern, i_line
            )
            if p:
                variant = p.named
                list_.append((i_line, variant))
        bsc_log.Log.trace_method_result(
            'file parse is completed', 'file="{}"'.format(
                self._file_path
            )
        )
        return list_

    @classmethod
    def _generate_obj_port_dict(cls, raw):
        dict_ = {}
        sep = '\n'
        _ = cls._to_lines(raw, sep)
        for i in _:
            __ = i.strip().split('\t')
            port_name, port_raw, port_type = __[0], __[-1], None
            dict_[port_name] = port_type, port_raw
        return dict_

    def _get_file_paths(self):
        list_ = []
        obj_raws = self._generate_node_args()
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            if i_obj_type in self.FILE_REFERENCE_DICT:
                i_port_dict = self._generate_obj_port_dict(i_variants['port_lines'])
                i_obj_name = i_port_dict['name'][-1]
                #
                i_port_names = self.FILE_REFERENCE_DICT[i_obj_type]
                for j_port_name in i_port_names:
                    if j_port_name in i_port_dict:
                        j_port_type, j_port_raw = i_port_dict[j_port_name]
                        raw = dict(
                            obj_type=i_obj_type,
                            obj_name=i_obj_name,
                            port_name=j_port_name,
                            port_type=j_port_type,
                            port_raw=j_port_raw,
                            line_index=self.lines.index(i_line),
                            line=i_line,
                        )
                        list_.append(raw)
        return list_

    def get_file_paths(self):
        return self._get_file_paths()

    def set_repair(self):
        list_ = []
        project_directory_path = self.get_project_directory_path()
        project_directory_path = bsc_storage.StgPathOpt(
            project_directory_path
        ).get_path()
        _ = self.get_file_paths()
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgDataPath':
                i_raw = i['port_raw']
                if i_raw.startswith('${PROJECT}'):
                    i_new_raw = i_raw.replace('${PROJECT}', project_directory_path)
                    #
                    if i_raw != i_new_raw:
                        i_line_index = i['line_index']
                        i_line = i['line']
                        i_new_line = i_line.replace(i_raw, i_new_raw)
                        list_.append(
                            (i_line_index, i_new_line)
                        )
                        bsc_log.Log.trace_method_result(
                            'xgen collection directory repair',
                            'directory="{}" >> "{}"'.format(
                                i_raw, i_new_raw
                            )
                        )

        for i_line_index, i_line in list_:
            self.lines[i_line_index] = i_line

    def get_project_directory_path(self):
        obj_raws = self._generate_node_args()
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            if i_obj_type == 'Palette':
                i_port_dict = self._generate_obj_port_dict(i_variants['port_lines'])
                j_port_type, j_port_raw = i_port_dict['xgProjectPath']
                return j_port_raw

    def repath_collection_directory_to(self, xgen_collection_directory_path_tgt, xgen_collection_name):
        _ = self.get_file_paths()
        list_ = []
        bsc_log.Log.trace_method_result(
            'xgen collection directory repath is started',
            'directory="{}"'.format(
                xgen_collection_directory_path_tgt
            )
        )
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgDataPath':
                i_raw = i['port_raw']
                i_raw = bsc_storage.StgPathOpt(
                    i_raw
                ).get_path()
                #
                i_obj_type = i['obj_type']
                i_obj_name = i['obj_name']
                if i_obj_type == 'Description':
                    i_new_raw = '{}/{}/'.format(xgen_collection_directory_path_tgt, xgen_collection_name)
                else:
                    i_new_raw = '{}/{}'.format(xgen_collection_directory_path_tgt, xgen_collection_name)
                #
                if i_raw != i_new_raw:
                    i_line_index = i['line_index']
                    i_line = i['line']
                    i_new_line = i_line.replace(i_raw, i_new_raw)
                    #
                    list_.append(
                        (i_line_index, i_new_line)
                    )
                    bsc_log.Log.trace_method_result(
                        'xgen collection directory repath',
                        'obj="{}"'.format(
                            i_obj_name
                        )
                    )
                    bsc_log.Log.trace_method_result(
                        'xgen collection directory repath',
                        'directory="{}" >> "{}"'.format(
                            i_raw, i_new_raw
                        )
                    )
        #
        for i_line_index, i_line in list_:
            self.lines[i_line_index] = i_line
        #
        bsc_log.Log.trace_method_result(
            'xgen collection directory repath is completed',
            'directory="{}"'.format(
                xgen_collection_directory_path_tgt
            )
        )

    def repath_project_directory_to(self, xgen_project_directory_path_tgt):
        _ = self.get_file_paths()
        list_ = []
        bsc_log.Log.trace_method_result(
            'xgen project directory repath is started',
            'directory="{}"'.format(
                xgen_project_directory_path_tgt
            )
        )
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgProjectPath':
                i_raw = i['port_raw']
                i_raw = bsc_storage.StgPathOpt(
                    i_raw
                ).get_path()
                #
                i_obj_name = i['obj_name']
                #
                i_new_raw = xgen_project_directory_path_tgt
                #
                if i_raw != i_new_raw:
                    i_line_index = i['line_index']
                    i_line = i['line']
                    i_new_line = i_line.replace(i_raw, i_new_raw)
                    list_.append(
                        (i_line_index, i_new_line)
                    )
                    bsc_log.Log.trace_method_result(
                        'xgen project directory repath',
                        'obj="{}"'.format(
                            i_obj_name
                        )
                    )
                    bsc_log.Log.trace_method_result(
                        'xgen project directory repath',
                        'directory="{}" >> "{}"'.format(
                            i_raw, i_new_raw
                        )
                    )
        #
        for i_line_index, i_line in list_:
            self.lines[i_line_index] = i_line
        #
        bsc_log.Log.trace_method_result(
            'xgen project directory repath is completed',
            'directory="{}"'.format(
                xgen_project_directory_path_tgt
            )
        )

    def get_description_properties(self):
        d = ctt_core.Dict()
        bsc_log.Log.trace_method_result(
            'file parse is started', 'file="{}"'.format(
                self._file_path
            )
        )
        obj_raws = self._generate_node_args()
        enable = False
        cur_description_name = None
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            i_port_dict = self._generate_obj_port_dict(i_variants['port_lines'])
            #
            if i_obj_type == 'Description':
                enable = True
                cur_description_name = i_port_dict['name'][-1]
            elif i_obj_type.startswith('Patches'):
                enable = False
            #
            i_key = cur_description_name
            if i_obj_type != 'Description':
                if cur_description_name is not None:
                    i_key = '{}.{}'.format(cur_description_name, i_obj_type)
                else:
                    i_key = i_obj_type
            #
            if enable is True:
                if '\t' not in i_obj_type:
                    for j_port_name, (j_port_type, j_port_raw) in i_port_dict.items():
                        j_key = '{}.{}'.format(i_key, j_port_name)
                        # print j_key, j_port_raw
                        d.set(j_key, j_port_raw)
                else:
                    pass
                    j_key = '{}.extra'.format(cur_description_name)
                    d.add_element(j_key, i_obj_type)
                    # print i_obj_type
        return d

    def get_collection_data_directory_path(self):
        pass

    def set_save(self):
        bsc_storage.StgFileOpt(self.file_path).set_write(
            ''.join(self.lines)
        )


class DotMaOptOld(_AbsDotFile):
    SEP = ';\n'
    LINE_PATTERN_CLS = _LinePattern

    FILE_REFERENCE_DICT = {
        'file': 'ftn',
        'reference': 'fn[0]',
        'xgmPalette': 'xfn',
        'xgmDescription': None,
        'gpuCache': 'cfn',
        'AlembicNode': 'fn',
        #
        'aiImage': 'filename',
        'aiMaterialx': 'filename',
        'aiVolume': 'filename',
        'aiStandIn': 'dso',
    }

    def __init__(self, file_path):
        super(DotMaOptOld, self).__init__(file_path)

    def get_references_file_paths(self):
        list_ = []
        pattern = self.LINE_PATTERN_CLS(
            'file -rdi {a} -ns "{namespace}" -rfn "{obj}"{b}-typ{c}"{file_type}"{d}"{file}"{r}'
        )
        lines = fnmatch.filter(
            self.lines, pattern.fnmatch_pattern
        )
        for i_line in lines:
            p = parse.parse(
                pattern.parse_pattern, i_line
            )
            if p:
                file_path = p.named['file']
                list_.append(file_path)
        return list_

    def _generate_node_args(self):
        list_ = []
        pattern_0 = self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}"{r}')
        lines = fnmatch.filter(
            self.lines, pattern_0.fnmatch_pattern
        )
        for i_line in lines:
            p = parse.parse(
                pattern_0.parse_pattern, i_line
            )
            if p:
                variants = p.named
                list_.append((i_line, variants))
        #
        return list_

    def _generate_obj_port_dict(self, line):
        dict_ = {}
        index = self.lines.index(line)
        #
        is_end = False
        p_index = index+2
        p_maximum = 10000
        c = 0
        while is_end is False:
            p_line = self.lines[p_index]
            is_port_s = self._get_is_port_(p_line)
            if is_port_s:
                # check max raw size
                p_line_size = len(p_line)
                if p_line_size < 1000:
                    port_raw = self._get_obj_port_raw_(p_line)
                    if port_raw is not None:
                        port_variant = port_raw
                        port_name, port_type, port_raw = port_variant['port_name'], port_variant['port_type'], \
                            port_variant['port_raw']
                        dict_[port_name] = port_type, port_raw
                else:
                    print 'error: line [{}...] is to large({})'.format(p_line[:50], p_line_size)
            else:
                is_end = True
            if c == p_maximum:
                is_end = True
            p_index += 1
            c += 1
        return dict_

    @classmethod
    def _get_is_port_(cls, line):
        pattern_0 = cls.LINE_PATTERN_CLS('{l}setAttr{r}')
        results = fnmatch.filter(
            [line], pattern_0.fnmatch_pattern
        )
        if results:
            return True
        #
        pattern_1 = cls.LINE_PATTERN_CLS('{l}addAttr{r}')
        results = fnmatch.filter(
            [line], pattern_1.fnmatch_pattern
        )
        if results:
            return True
        return False

    @classmethod
    def _get_obj_port_raw_(cls, line):
        pattern_0 = cls.LINE_PATTERN_CLS('{l}setAttr ".{port_name}" -type "{port_type}"{m}"{port_raw}";{r}')
        results = fnmatch.filter(
            [line], pattern_0.fnmatch_pattern
        )
        if results:
            p = parse.parse(
                pattern_0.parse_pattern, line
            )
            if p:
                variant = p.named
                return variant
        pattern_1 = cls.LINE_PATTERN_CLS('{l}setAttr ".{port_name}" {port_raw};{r}')
        results = fnmatch.filter(
            [line], pattern_1.fnmatch_pattern
        )
        if results:
            p = parse.parse(
                pattern_1.parse_pattern, line
            )
            if p:
                variant = p.named
                variant['port_type'] = None
                return variant
        pattern_2 = cls.LINE_PATTERN_CLS('{l}addAttr {m0} -ln "{port_name}" -dt "{port_type}";{r}')
        results = fnmatch.filter(
            [line], pattern_2.fnmatch_pattern
        )
        if results:
            p = parse.parse(
                pattern_2.parse_pattern, line
            )
            if p:
                variant = p.named
                variant['port_raw'] = None
                return variant

    @classmethod
    def _get_obj_uuid_raw_(cls, line):
        pattern = cls.LINE_PATTERN_CLS('{l}rename -uuid "{raw}"{r}')
        results = fnmatch.filter(
            [line], pattern.fnmatch_pattern
        )
        if results:
            result = results[0]
            p = parse.parse(
                pattern.parse_pattern, result
            )
            print p

    def _test_(self):
        self._get_file_paths()

    def _get_file_paths(self):
        list_ = []
        obj_raws = self._generate_node_args()
        print 'start file-path: "{}"'.format(self.file_path)
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            i_obj_name = i_variants['obj_name']
            if i_obj_type in self.FILE_REFERENCE_DICT:
                i_port_name = self.FILE_REFERENCE_DICT[i_obj_type]
                if i_port_name is not None:
                    # print 'start obj: "{}"'.format(obj_name)
                    port_raws = self._generate_obj_port_dict(i_line)
                    if i_port_name in port_raws:
                        i_port_type, i_port_raw = port_raws[i_port_name]
                        raw = dict(
                            obj_type=i_obj_type,
                            obj_name=i_obj_name,
                            port_name=i_port_name,
                            port_type=i_port_type,
                            port_raw=i_port_raw
                        )
                        if i_obj_type == 'file':
                            i_file_path = i_port_raw
                            i_file_base = os.path.basename(i_file_path)
                            # sequence
                            if 'ufe' in port_raws:
                                _, i_sequence = port_raws['ufe']
                                if i_sequence == 'yes':
                                    i_results = re.findall(r'[0-9]{3,4}', i_file_base)
                                    if i_results:
                                        i_file_path = i_file_path.replace(i_results[-1], '<f>')
                                        raw['port_raw'] = i_file_path
                            # udim
                            if 'uvt' in port_raws:
                                _, is_udim = port_raws['uvt']
                                if is_udim == '3':
                                    i_results = re.findall(r'[0-9][0-9][0-9][0-9]', i_file_base)
                                    if i_results:
                                        i_file_path = i_file_path.replace(i_results[-1], '<udim>')
                                        raw['port_raw'] = i_file_path
                        #
                        list_.append(raw)
                    # print 'end obj: "{}"'.format(obj_name)
        print 'end file-path: "{}"'.format(self.file_path)
        return list_

    def get_file_paths(self):
        return self._get_file_paths()


class DotMtlxOptOld(_AbsDotFile):
    SEP = '\n'
    LINE_PATTERN_CLS = _LinePattern
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, file_path):
        super(DotMtlxOptOld, self).__init__(file_path)

    def _get_material_assign_matches(self):
        return self._generate_match_args(
            pattern='{l}<materialassign name="material_assign__{geometry_type}__{index}" material="{material}" geom="{geometry}" />{r}',
            lines=self.lines
        )

    def _get_property_set_assign_matches(self):
        return self._generate_match_args(
            pattern='{l}<propertysetassign name="{assign_name}" propertyset="{property_set_name}" geom="{geometry}" />{r}',
            lines=self.lines
        )

    # noinspection PyUnusedLocal
    def _get_property_set_raw_(self, property_set_name):
        matches = self._generate_match_args(
            pattern='{l}<propertyset name="%s">{r}'%property_set_name,
            lines=self._lines
        )
        if matches:
            line, properties = matches[-1]
            index = self._lines.index(line)

            index += 1

            property_line = self._lines[index]
            pattern = '{l}<property >{r}'
            print property_line

    def get_material_assign_raws(self):
        return self._get_material_assign_matches()

    # noinspection PyNoneFunctionAssignment,PyUnusedLocal
    def get_geometries_properties(self):
        list_ = []
        material_assign_raws = self._get_material_assign_matches()
        for material_assign_raw in material_assign_raws:
            geometry_properties = self.PROPERTIES_CLS(self, {})
            line, properties = material_assign_raw
            geometry_properties.set('type', properties['geometry_type'])
            geometry_properties.set('path', properties['geometry'])
            geometry_properties.set('material', properties['material'])
            list_.append(geometry_properties)
        property_set_assign_raws = self._get_property_set_assign_matches()
        for property_set_assign_raw in property_set_assign_raws:
            line, properties = property_set_assign_raw
            property_set_name = properties['property_set_name']
            property_set_raw = self._get_property_set_raw_(property_set_name)
        return list_


class DotOslOptOld(_AbsDotFile):
    SEP = '\n'
    LINE_PATTERN_CLS = _LinePattern
    PROPERTIES_CLS = ctt_core.Properties

    def __init__(self, file_path):
        super(DotOslOptOld, self).__init__(file_path)

    def _get_shader_start_line_(self):
        _ = self._generate_match_args(
            pattern='shader {shader_name}({extra}',
            lines=self.lines
        )
        print _

    def get_port_args(self):
        print self._generate_match_args(
            pattern='',
            lines=self.lines
        )


class DotMtlxOpt(_AbsDotFile):
    SEP = '\n'

    def __init__(self, file_path):
        super(DotMtlxOpt, self).__init__(file_path)

        self._set_run_()

    def _set_run_(self):
        self._generate_geometry_paths()
        self._generate_texture_paths()

    def _generate_geometry_paths(self):
        self._geometry_paths = []
        if self._lines:
            parse_pattern = '{extra_0}<materialassign name="{assign_name}" material="{material_name}" geom="{geometry_path}" />{extra_1}'
            filter_pattern = '*<materialassign name="*" material="*" geom="*" />*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for result in results:
                    p = parse.parse(
                        parse_pattern, result
                    )
                    if p:
                        path = p['geometry_path']
                        if not path.endswith('/procedural_curves'):
                            self._geometry_paths.append(path)

    def _generate_texture_paths(self):
        self._texture_paths = []
        if self._lines:
            parse_pattern = '{extra_0}<input name="filename" type="string" value="{texture_path}" />{extra_1}'
            filter_pattern = '*<input name="filename" type="string" value="*" />*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for result in results:
                    p = parse.parse(
                        parse_pattern, result
                    )
                    if p:
                        texture_path = p['texture_path']
                        if texture_path not in self._texture_paths:
                            self._texture_paths.append(p['texture_path'])

    @property
    def geometry_paths(self):
        return self._geometry_paths

    @property
    def texture_paths(self):
        return self._texture_paths


class DotMaMeshMtd(object):
    @classmethod
    def get_edge_vertices(cls, ports):
        all_port_names = ports.keys()
        vertex_indices = []
        #
        port_paths = []
        if 'ed[0]' in ports:
            port_paths = ['fc[0]']
        port_paths += fnmatch.filter(
            all_port_names, 'ed?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_edge_vertices_update_(data, vertex_indices)
        return vertex_indices

    @classmethod
    def _set_edge_vertices_update_(cls, data, vertex_indices):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            _ = i.split(' ')
            for j in _:
                vertex_index = int(j)
                vertex_indices.append(vertex_index)

    @classmethod
    def get_face_vertices(cls, ports):
        edge_vertex_indices = cls.get_edge_vertices(ports)
        #
        all_port_names = ports.keys()
        face_edge_indices = []
        #
        face_vertex_counts = []
        face_vertex_indices = []
        #
        port_paths = []
        if 'fc[0]' in ports:
            port_paths = ['fc[0]']
        port_paths += fnmatch.filter(
            all_port_names, 'fc?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_face_vertices_update_(
                    data, face_vertex_counts, face_vertex_indices, face_edge_indices, edge_vertex_indices
                    )
        # print 'edge_vertex_indices =', edge_vertex_indices
        # print 'face_edge_indices =', face_edge_indices
        # print 'face_vertex_indices =', face_vertex_indices
        return face_vertex_counts, face_vertex_indices

    @classmethod
    def _set_face_vertices_update_(
        cls, data, face_vertex_counts, face_vertex_indices, face_edge_indices, edge_vertex_indices
    ):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            if i.startswith('f'):
                _ = i.split(' ')
                count = int(_[1])
                face_vertex_counts.append(count)
                for j in _[2:]:
                    edge_index = int(j)
                    if edge_index >= 0:
                        vertex_index = edge_vertex_indices[edge_index*3]
                    else:
                        vertex_index = edge_vertex_indices[(abs(edge_index)-1)*3+1]
                    #
                    face_vertex_indices.append(vertex_index)
                    #
                    face_edge_indices.append(edge_index)

    @classmethod
    def get_points(cls, ports):
        all_port_names = ports.keys()
        points = []
        port_paths = fnmatch.filter(
            all_port_names, 'vt?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_points_update_(data, points)
        return points

    @classmethod
    def _set_points_update_(cls, data, points):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            _ = i.split(' ')
            for j in _:
                points.append(float(j))


class DotMaOpt(_AbsDotFile):
    SEP = ';\n'
    LINE_PATTERN_CLS = _LinePattern
    FILE_REFERENCE_DICT = {
        'file': 'ftn',
        'reference': 'fn[0]',
        'xgmPalette': 'xfn',
        'xgmDescription': None,
        'gpuCache': 'cfn',
        'AlembicNode': 'fn',
        #
        'aiImage': 'filename',
        'aiMaterialx': 'filename',
        'aiVolume': 'filename',
        'aiStandIn': 'dso',
    }

    @classmethod
    def _filter_nodes(cls, objs, root, obj_types):
        dict_ = collections.OrderedDict()
        for obj_path, obj_properties in objs.items():
            obj_type = obj_properties['obj_type']
            #
            if obj_path.startswith('{}/'.format(root)) is False:
                continue
            #
            if obj_type not in obj_types:
                continue
            #
            dict_[obj_path] = obj_properties
        return dict_

    def __init__(self, file_path):
        super(DotMaOpt, self).__init__(file_path)
        self._file_lines = self._get_file_lines()
        self._obj_lines = self._get_node_lines()

    def get_references_file_paths(self):
        list_ = []
        pattern = self.LINE_PATTERN_CLS(
            'file -rdi {a} -ns "{namespace}" -rfn "{obj}"{b}-typ{c}"{file_type}"{d}"{file}"{r}'
        )
        lines = fnmatch.filter(
            self.lines, pattern.fnmatch_pattern
        )
        for line in lines:
            p = parse.parse(
                pattern.parse_pattern, line
            )
            if p:
                file_path = p.named['file']
                list_.append(file_path)
        return list_

    def _get_node_path(self, obj_parent_name, obj_name):
        def _rcs_fnc(obj_name_):
            _obj_name = obj_name_
            _obj_parent_name = '*'
            if obj_name_ is not None:
                if '|' in obj_name_:
                    _ = obj_name_.split('|')
                    _obj_name = _[-1]
                    if len(_) > 3:
                        _obj_parent_name = '|'.join(_[:-1])
                    else:
                        _obj_parent_name = _[1]
                #
                _match_pattern_0 = matcher_0.parse_pattern.format(
                    **dict(obj_name=_obj_name, obj_parent_name=_obj_parent_name)
                )
                _result_0 = fnmatch.filter(
                    self._lines, _match_pattern_0
                )
                if _result_0:
                    _p_0 = parse.parse(
                        matcher_0.parse_pattern, _result_0[0]
                    )
                    if _p_0:
                        path_args.append(_p_0['obj_name'])
                        _rcs_fnc(_p_0['obj_parent_name'])
                else:
                    _match_pattern_1 = matcher_1.parse_pattern.format(**dict(obj_name=_obj_name))
                    _result_1 = fnmatch.filter(self._lines, _match_pattern_1)
                    if _result_1:
                        _p_1 = parse.parse(
                            matcher_1.parse_pattern, _result_1[0]
                        )
                        if _p_1:
                            path_args.append(_p_1['obj_name'])

        path_args = [obj_name]
        matcher_0 = self.LINE_PATTERN_CLS('createNode transform -n "{obj_name}" -p "{obj_parent_name}";\n')
        matcher_1 = self.LINE_PATTERN_CLS('createNode transform -n "{obj_name}";\n')
        #
        _rcs_fnc(obj_parent_name)
        #
        path_args.reverse()
        return '/'+'/'.join(path_args)

    def _get_node_by_path(self, obj_path):
        _ = obj_path.split('/')
        obj_name = _[-1]
        for matcher in [
            self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_name}";\n'),
            self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}";\n')
        ]:
            pattern = matcher.parse_pattern.format(
                **dict(obj_type='*', obj_name=obj_name, obj_parent_name='*')
            )
            results = fnmatch.filter(
                self._obj_lines, pattern
            )
            if results:
                line = results[0]
                p = parse.parse(
                    matcher.parse_pattern, line
                )
                if p:
                    variants = p.named
                    properties = collections.OrderedDict()
                    properties['line'] = line
                    properties['obj_type'] = variants['obj_type']
                    properties['obj_name'] = variants['obj_name']
                    return properties

    def _get_file_lines(self):
        return fnmatch.filter(
            self._lines, '*file -rdi *;\n'
        ) or []

    def _get_node_lines(self):
        return fnmatch.filter(
            self._lines, 'createNode *;\n'
        ) or []

    def _get_node_children(self, obj_path):
        dict_ = collections.OrderedDict()
        obj = self._get_node_by_path(obj_path)
        if obj:
            _ = obj_path.split('/')
            obj_name_ = _[-1]
            obj_path_ = obj_path.replace('/', '|')
            for matcher in [
                self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_name}";\n'),
                self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_path}";\n')
            ]:
                pattern = matcher.parse_pattern.format(
                    **dict(
                        obj_type='*',
                        obj_name='*',
                        obj_parent_name=obj_name_,
                        obj_parent_path=obj_path_
                    )
                )
                results = fnmatch.filter(
                    self._obj_lines, pattern
                )
                if results:
                    for line in results:
                        p = parse.parse(
                            matcher.parse_pattern, line
                        )
                        if p:
                            variants = p.named
                            i_obj_name = variants['obj_name']
                            i_obj_type = variants['obj_type']
                            i_obj_path = '{}/{}'.format(obj_path, i_obj_name)
                            properties = collections.OrderedDict()
                            properties['line'] = line
                            properties['obj_type'] = i_obj_type
                            properties['obj_name'] = i_obj_name
                            #
                            # print '<obj-create> "{}"'.format(i_obj_path)
                            dict_[i_obj_path] = properties
        return dict_

    def _get_obj_descendants(self, obj_path):
        def rcs_fnc_(obj_path_):
            _child_objs = self._get_node_children(obj_path_)
            for _obj_path, _obj_properties in _child_objs.items():
                dict_[_obj_path] = _obj_properties
                rcs_fnc_(_obj_path)

        #
        dict_ = collections.OrderedDict()
        obj = self._get_node_by_path(obj_path)
        if obj:
            rcs_fnc_(obj_path)
        return dict_

    def generate_node_args(self):
        dict_ = collections.OrderedDict()
        #
        obj_matcher = self.LINE_PATTERN_CLS('createNode {obj_type} -n "{obj_name}";\n')
        lines = fnmatch.filter(
            self._lines, obj_matcher.fnmatch_pattern
        )
        for i_line in lines:
            i_properties = collections.OrderedDict()
            p = parse.parse(
                obj_matcher.parse_pattern, i_line
            )
            if p:
                i_line_index = self._lines.index(i_line)
                i_unique_id = self._get_uuid_by_line(self._lines[i_line_index+1])
                i_variants = p.named
                i_name_ptn = self.LINE_PATTERN_CLS(
                    '{obj_name}" -p "{obj_parent_name}'
                )
                i_obj_type = i_variants['obj_type']
                i_obj_name = i_variants['obj_name']
                i_obj_path = i_obj_name
                i_obj_parent_name = None
                if fnmatch.filter(
                    [i_obj_name], i_name_ptn.fnmatch_pattern
                ):
                    i_name_p = parse.parse(
                        i_name_ptn.parse_pattern, i_obj_name
                    )
                    if i_name_p:
                        i_name_variants = i_name_p.named
                        i_obj_name = i_name_variants['obj_name']
                        i_obj_parent_name = i_name_variants['obj_parent_name']

                if i_obj_type in ['transform', 'mesh']:
                    i_obj_path = self._get_node_path(i_obj_parent_name, i_obj_name)

                i_properties['line'] = i_line
                i_properties['obj_type'] = i_obj_type
                i_properties['obj_name'] = i_obj_name
                i_properties['unique_id'] = i_unique_id
                dict_[i_obj_path] = i_properties

        return dict_

    def get_node_paths(self):
        _ = self.generate_node_args()
        return _.keys()

    def _get_uuid_by_line(self, line):
        pattern = self.LINE_PATTERN_CLS('{l}rename -uid "{unique_id}";\n')
        results = fnmatch.filter(
            [line], pattern.fnmatch_pattern
        )
        if results:
            result = results[0]
            p = parse.parse(
                pattern.parse_pattern, result
            )
            if p:
                variants = p.named
                return variants['unique_id']

    # noinspection PyUnusedLocal
    def _get_obj_port_lines_(self, obj_properties):
        line = obj_properties['line']
        dict_ = collections.OrderedDict()
        obj_line_index = self._obj_lines.index(line)
        start_index = self._lines.index(line)
        if (obj_line_index+1) < len(self._obj_lines):
            next_line = self._obj_lines[obj_line_index+1]
        else:
            next_line = 'select -ne :time1;\n'
        #
        end_index = self._lines.index(next_line)
        return self._lines[start_index+2:end_index]

    # noinspection PyUnusedLocal
    def _get_obj_ports_(self, obj_path, obj_properties):
        dict_ = collections.OrderedDict()
        lines = self._get_obj_port_lines_(obj_properties)
        for line in lines:
            raw = self._get_port_properties_at_line_(line)
            if isinstance(raw, dict):
                port_path = raw.get('port_path')
                data_type = raw.get('data_type')
                data = raw.get('data')
                #
                properties = collections.OrderedDict()
                properties['date_type'] = data_type
                properties['data'] = data
                if data_type == 'array':
                    properties['size'] = int(raw.get('size'))
                dict_[port_path] = properties
                # print '<port-create> "{}"'.format('{}.{}'.format(obj_path, port_path))
        return dict_

    def _get_obj_is_io_(self, obj_properties):
        lines = self._get_obj_port_lines_(obj_properties)
        return fnmatch.filter(lines, '\tsetAttr ".io" yes;\n') != []

    def _get_port_properties_at_line_(self, line):
        matchers = [
            (self.LINE_PATTERN_CLS('\tsetAttr -ch {capacity} ".{port_path}" -type "{data_type}" \n\t\t{data};\n'), None,
             None),
            (self.LINE_PATTERN_CLS('\tsetAttr -s {size} -ch {capacity} ".{port_path}";\n'), 'array', None),
            (self.LINE_PATTERN_CLS(
                '\tsetAttr -s {size} -ch {capacity} ".{port_path}" -type "{data_type}" \n\t\t{data};\n'
                ), 'array', None),
            (self.LINE_PATTERN_CLS('\tsetAttr -s {size} -ch {capacity} ".{port_path}"\n\t\t{data};\n'), 'array', None),
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}" -type "{data_type}" \n\t\t{data};\n'), None, None),
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}"\n\t\t{data};\n'), None, None),
            #
            (self.LINE_PATTERN_CLS('\tsetAttr -s {size} ".{port_path}" {data};\n'), 'array', None),
            (self.LINE_PATTERN_CLS('\tsetAttr -s {size} ".{port_path}";\n'), 'array', None),
            #
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}" yes;\n'), 'bool', True),
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}" no;\n'), 'bool', False),
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}" -type "{data_type}" "{data}";\n'), None, None),
            (self.LINE_PATTERN_CLS('\tsetAttr ".{port_path}" {data};\n'), None, None),
        ]
        for i in matchers:
            matcher, data_type, data = i
            results = fnmatch.filter(
                [line], matcher.fnmatch_pattern
            )
            if results:
                p = parse.parse(
                    matcher.parse_pattern, line
                )
                if p:
                    variants = p.named
                    if data_type is not None:
                        variants['data_type'] = data_type
                    if data is not None:
                        variants['data'] = data
                    return variants

    def get_mesh_info(self, root):
        dict_ = collections.OrderedDict()
        if root is not None:
            objs = self._get_obj_descendants(root)
            if objs:
                mesh_objs = self._filter_nodes(objs, root=root, obj_types=['mesh'])
                if mesh_objs:
                    maximum = len(mesh_objs)
                    mesh_dict = collections.OrderedDict()
                    dict_['mesh'] = mesh_dict

                    with bsc_log.LogProcessContext.create(maximum, 'mesh-info-read') as l_p:
                        for seq, (obj_path, obj_properties) in enumerate(mesh_objs.items()):
                            l_p.do_update()
                            #
                            if self._get_obj_is_io_(obj_properties) is True:
                                continue
                            #
                            obj_orig_path = '{}Orig'.format(obj_path)
                            if obj_orig_path in mesh_objs:
                                obj_properties = mesh_objs[obj_orig_path]
                            #
                            ports = self._get_obj_ports_(obj_path, obj_properties)
                            #
                            face_vertex_counts, face_vertex_indices = DotMaMeshMtd.get_face_vertices(ports)
                            face_count = len(face_vertex_counts)
                            face_vertices_uuid = _Hash.get_hash_value(
                                (face_vertex_counts, face_vertex_indices), as_unique_id=True
                            )
                            #
                            points = DotMaMeshMtd.get_points(ports)
                            point_count = len(points)
                            points_uuid = _Hash.get_hash_value(
                                points, as_unique_id=True
                            )
                            #
                            info = collections.OrderedDict()
                            mesh_dict[obj_path] = info
                            info['face-vertices-uuid'] = face_vertices_uuid
                            info['face-count'] = face_count
                            #
                            info['points-uuid'] = points_uuid
                            info['point-count'] = point_count
            else:
                print 'root is not exists'
        return dict_

    def get_reference_file_paths(self, auto_convert=True):
        list_ = []
        for line in self._file_lines:
            for matcher in [
                self.LINE_PATTERN_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" -typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -typ "{file_type}" "{file_path}";\n'
                ),
                #
                self.LINE_PATTERN_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" -typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_PATTERN_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -typ "{file_type}" "{file_path}";\n'
                ),
            ]:
                results = fnmatch.filter(
                    [line], matcher.fnmatch_pattern
                )
                if results:
                    result = results[0]
                    p = parse.parse(
                        matcher.parse_pattern, result
                    )
                    if p:
                        variants = p.named
                        file_path = variants.get('file_path')
                        if auto_convert is True:
                            file_path = bsc_storage.StgPathMapper.map_to_current(file_path)
                        list_.append(file_path)
                        break
        return list_


class DotAssOpt(_AbsDotFile):
    LINE_PATTERN_CLS = _LinePattern

    def __init__(self, file_path):
        super(DotAssOpt, self).__init__(file_path)

    def do_file_path_convert_to_env(self):
        self._texture_paths = []
        replace_lis = []
        if self._lines:
            matcher = self.LINE_PATTERN_CLS(
                '{l}filename "{file_path}"\n'
            )
            results = fnmatch.filter(
                self._lines, matcher.fnmatch_pattern
            )
            if results:
                for i_line in results:
                    i_p = parse.parse(
                        matcher.parse_pattern, i_line
                    )
                    if i_p:
                        i_variants = i_p.named
                        i_file_path = i_variants['file_path']

                        i_file_path_new = bsc_storage.StgEnvPathMapper.map_to_env(
                            i_file_path, pattern='[KEY]'
                        )
                        #
                        if i_file_path_new is not None:
                            i_new_line = i_line.replace(i_file_path, i_file_path_new)

                            replace_lis.append(
                                (i_line, i_new_line, i_file_path, i_file_path_new)
                            )
        #
        for i_line, i_new_line, i_file_path, i_file_path_new in replace_lis:
            index = self._lines.index(i_line)
            self._lines[index] = i_new_line
            bsc_log.Log.trace_method_result(
                'dot-ass path-convert',
                'file="{}" >> "{}"'.format(i_file_path, i_file_path_new)
            )

        bsc_storage.StgFileOpt(self._file_path).set_write(''.join(self._lines))

    def get_is_from_maya(self):
        if self._lines:
            if len(self._lines) >= 3:
                _ = self._lines[2]
                if fnmatch.filter([_], '### host app: MtoA *'):
                    return True
        return False

    def get_is_from_katana(self):
        if self._lines:
            if len(self._lines) >= 3:
                _ = self._lines[2]
                if fnmatch.filter([_], '### host app: KtoA *'):
                    return True
        return False

    def get_file_paths(self):
        ms = self._generate_match_args('{l}filename "{texture_path}"{r}', self._lines)
        if ms:
            return [i[1]['texture_path'] for i in ms]
        return []


class DotUsdaOpt(_AbsDotFile):
    SEP = '\n'
    LINE_PATTERN_CLS = _LinePattern

    def __init__(self, file_path):
        super(DotUsdaOpt, self).__init__(file_path)

    def get_frame_range(self):
        m_0 = self.LINE_PATTERN_CLS('    startTimeCode = {value}\n')
        m_1 = self.LINE_PATTERN_CLS('    endTimeCode = {value}\n')
        results_0 = fnmatch.filter(
            self._lines, m_0.fnmatch_pattern
        )
        start_frame = 0
        if results_0:
            p_0 = parse.parse(
                m_0.parse_pattern, results_0[0]
            )
            if p_0:
                start_frame = int(p_0['value'])

        results_1 = fnmatch.filter(
            self._lines, m_1.fnmatch_pattern
        )
        end_frame = 0
        if results_1:
            p_1 = parse.parse(
                m_1.parse_pattern, results_1[0]
            )
            if p_1:
                end_frame = int(p_1['value'])
        return start_frame, end_frame
