#!/usr/bin/env python
# Derived from reverse-sandbox/sandbox_regex.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import logging as mosaic_logging
import logging.config as _boundary_import_logging_config
import logging as mosaic_logging
from policymosaic.regex_bytecode import mosaic_RegexParser as mosaic_RegexParser
mosaic_logging.config.fileConfig(_name_boundary.resource('logger.config'))
mosaic_logger = mosaic_logging.getLogger(__name__)

@_name_boundary.class_contract('Node', {'TYPE_JUMP_FORWARD': 'mosaic_TYPE_JUMP_FORWARD', 'TYPE_JUMP_BACKWARD': 'mosaic_TYPE_JUMP_BACKWARD', 'TYPE_CHARACTER': 'mosaic_TYPE_CHARACTER', 'TYPE_END': 'mosaic_TYPE_END', 'FLAG_WHITE': 'mosaic_FLAG_WHITE', 'FLAG_GREY': 'mosaic_FLAG_GREY', 'FLAG_BLACK': 'mosaic_FLAG_BLACK', 'name': 'mosaic_name', 'type': 'mosaic_type', 'value': 'mosaic_value', 'flag': 'mosaic_flag', 'set_name': 'mosaic_set_name', 'set_type_jump_forward': 'mosaic_set_type_jump_forward', 'set_type_jump_backward': 'mosaic_set_type_jump_backward', 'set_type_character': 'mosaic_set_type_character', 'set_type_end': 'mosaic_set_type_end', 'is_type_end': 'mosaic_is_type_end', 'is_type_jump': 'mosaic_is_type_jump', 'is_type_jump_backward': 'mosaic_is_type_jump_backward', 'is_type_jump_forward': 'mosaic_is_type_jump_forward', 'is_type_character': 'mosaic_is_type_character', 'set_value': 'mosaic_set_value', 'set_flag_white': 'mosaic_set_flag_white', 'set_flag_grey': 'mosaic_set_flag_grey', 'set_flag_black': 'mosaic_set_flag_black'})
class mosaic_Node:
    """Representation of a node inside a regex non-deterministic automaton

    The most important attribute is the node type, which may be any of
    the four macros TYPE_... below.
    """
    mosaic_TYPE_JUMP_FORWARD = 1
    mosaic_TYPE_JUMP_BACKWARD = 2
    mosaic_TYPE_CHARACTER = 3
    mosaic_TYPE_END = 4
    mosaic_FLAG_WHITE = 1
    mosaic_FLAG_GREY = 2
    mosaic_FLAG_BLACK = 3
    mosaic_name = ''
    mosaic_type = None
    mosaic_value = None
    mosaic_flag = 'white'

    @_name_boundary.callable_contract({'self': 'mosaic_self_b31fee9', 'name': 'mosaic_name_3f6bac4', 'type': 'mosaic_type_d417fbc', 'value': 'mosaic_value_c589cda'}, '__init__')
    def __init__(mosaic_self_b31fee9, mosaic_name_3f6bac4=None, mosaic_type_d417fbc=None, mosaic_value_c589cda=''):
        _name_boundary.attributes(mosaic_self_b31fee9)['name'] = mosaic_name_3f6bac4
        _name_boundary.attributes(mosaic_self_b31fee9)['type'] = mosaic_type_d417fbc
        _name_boundary.attributes(mosaic_self_b31fee9)['value'] = mosaic_value_c589cda
        _name_boundary.attributes(mosaic_self_b31fee9)['flag'] = _name_boundary.attributes(mosaic_self_b31fee9)['FLAG_WHITE']

    @_name_boundary.callable_contract({'self': 'mosaic_self_ce1b484', 'name': 'mosaic_name_befb48b'}, 'set_name')
    def mosaic_set_name(mosaic_self_ce1b484, mosaic_name_befb48b):
        _name_boundary.attributes(mosaic_self_ce1b484)['name'] = mosaic_name_befb48b

    @_name_boundary.callable_contract({'self': 'mosaic_self_19b3fcb'}, 'set_type_jump_forward')
    def mosaic_set_type_jump_forward(mosaic_self_19b3fcb):
        _name_boundary.attributes(mosaic_self_19b3fcb)['type'] = _name_boundary.attributes(mosaic_self_19b3fcb)['TYPE_JUMP_FORWARD']

    @_name_boundary.callable_contract({'self': 'mosaic_self_d340ae6'}, 'set_type_jump_backward')
    def mosaic_set_type_jump_backward(mosaic_self_d340ae6):
        _name_boundary.attributes(mosaic_self_d340ae6)['type'] = _name_boundary.attributes(mosaic_self_d340ae6)['TYPE_JUMP_BACKWARD']

    @_name_boundary.callable_contract({'self': 'mosaic_self_98b20f4'}, 'set_type_character')
    def mosaic_set_type_character(mosaic_self_98b20f4):
        _name_boundary.attributes(mosaic_self_98b20f4)['type'] = _name_boundary.attributes(mosaic_self_98b20f4)['TYPE_CHARACTER']

    @_name_boundary.callable_contract({'self': 'mosaic_self_8ac9db6'}, 'set_type_end')
    def mosaic_set_type_end(mosaic_self_8ac9db6):
        _name_boundary.attributes(mosaic_self_8ac9db6)['type'] = _name_boundary.attributes(mosaic_self_8ac9db6)['TYPE_END']

    @_name_boundary.callable_contract({'self': 'mosaic_self_7f569a0'}, 'is_type_end')
    def mosaic_is_type_end(mosaic_self_7f569a0):
        return _name_boundary.attributes(mosaic_self_7f569a0)['type'] == _name_boundary.attributes(mosaic_self_7f569a0)['TYPE_END']

    @_name_boundary.callable_contract({'self': 'mosaic_self_d958a84'}, 'is_type_jump')
    def mosaic_is_type_jump(mosaic_self_d958a84):
        return _name_boundary.attributes(mosaic_self_d958a84)['type'] == _name_boundary.attributes(mosaic_self_d958a84)['TYPE_JUMP_BACKWARD'] or _name_boundary.attributes(mosaic_self_d958a84)['type'] == _name_boundary.attributes(mosaic_self_d958a84)['TYPE_JUMP_FORWARD']

    @_name_boundary.callable_contract({'self': 'mosaic_self_c486ca9'}, 'is_type_jump_backward')
    def mosaic_is_type_jump_backward(mosaic_self_c486ca9):
        return _name_boundary.attributes(mosaic_self_c486ca9)['type'] == _name_boundary.attributes(mosaic_self_c486ca9)['TYPE_JUMP_BACKWARD']

    @_name_boundary.callable_contract({'self': 'mosaic_self_7ff1be2'}, 'is_type_jump_forward')
    def mosaic_is_type_jump_forward(mosaic_self_7ff1be2):
        return _name_boundary.attributes(mosaic_self_7ff1be2)['type'] == _name_boundary.attributes(mosaic_self_7ff1be2)['TYPE_JUMP_FORWARD']

    @_name_boundary.callable_contract({'self': 'mosaic_self_194a5fa'}, 'is_type_character')
    def mosaic_is_type_character(mosaic_self_194a5fa):
        return _name_boundary.attributes(mosaic_self_194a5fa)['type'] == _name_boundary.attributes(mosaic_self_194a5fa)['TYPE_CHARACTER']

    @_name_boundary.callable_contract({'self': 'mosaic_self_565d2c5', 'value': 'mosaic_value_805f0e6'}, 'set_value')
    def mosaic_set_value(mosaic_self_565d2c5, mosaic_value_805f0e6):
        _name_boundary.attributes(mosaic_self_565d2c5)['value'] = mosaic_value_805f0e6

    @_name_boundary.callable_contract({'self': 'mosaic_self_c097102'}, 'set_flag_white')
    def mosaic_set_flag_white(mosaic_self_c097102):
        _name_boundary.attributes(mosaic_self_c097102)['flag'] = _name_boundary.attributes(mosaic_self_c097102)['FLAG_WHITE']

    @_name_boundary.callable_contract({'self': 'mosaic_self_83c29c8'}, 'set_flag_grey')
    def mosaic_set_flag_grey(mosaic_self_83c29c8):
        _name_boundary.attributes(mosaic_self_83c29c8)['flag'] = _name_boundary.attributes(mosaic_self_83c29c8)['FLAG_GREY']

    @_name_boundary.callable_contract({'self': 'mosaic_self_8d838fe'}, 'set_flag_black')
    def mosaic_set_flag_black(mosaic_self_8d838fe):
        _name_boundary.attributes(mosaic_self_8d838fe)['flag'] = _name_boundary.attributes(mosaic_self_8d838fe)['FLAG_BLACK']

    @_name_boundary.callable_contract({'self': 'mosaic_self_ab430e1'}, '__str__')
    def __str__(mosaic_self_ab430e1):
        if _name_boundary.attributes(mosaic_self_ab430e1)['type'] == _name_boundary.attributes(mosaic_self_ab430e1)['TYPE_JUMP_BACKWARD']:
            return '(%s: jump backward)' % _name_boundary.attributes(mosaic_self_ab430e1)['name']
        elif _name_boundary.attributes(mosaic_self_ab430e1)['type'] == _name_boundary.attributes(mosaic_self_ab430e1)['TYPE_JUMP_FORWARD']:
            return '(%s: jump forward)' % _name_boundary.attributes(mosaic_self_ab430e1)['name']
        elif _name_boundary.attributes(mosaic_self_ab430e1)['type'] == _name_boundary.attributes(mosaic_self_ab430e1)['TYPE_END']:
            return '(%s: end)' % _name_boundary.attributes(mosaic_self_ab430e1)['name']
        else:
            return '(%s: %s)' % (_name_boundary.attributes(mosaic_self_ab430e1)['name'], _name_boundary.attributes(mosaic_self_ab430e1)['value'])

@_name_boundary.class_contract('Graph', {'graph_dict': 'mosaic_graph_dict', 'canon_graph_dict': 'mosaic_canon_graph_dict', 'node_list': 'mosaic_node_list', 'start_node': 'mosaic_start_node', 'end_states': 'mosaic_end_states', 'start_state': 'mosaic_start_state', 'regex': 'mosaic_regex', 'unified_regex': 'mosaic_unified_regex', 'add_node': 'mosaic_add_node', 'has_node': 'mosaic_has_node', 'update_node': 'mosaic_update_node', 'add_new_next_to_node': 'mosaic_add_new_next_to_node', 'get_node_for_idx': 'mosaic_get_node_for_idx', 'get_re_index_for_pos': 'mosaic_get_re_index_for_pos', 'fill_from_regex_list': 'mosaic_fill_from_regex_list', 'get_character_nodes': 'mosaic_get_character_nodes', 'find_node_type_jump': 'mosaic_find_node_type_jump', 'reduce': 'mosaic_reduce', 'get_edges': 'mosaic_get_edges', 'convert_to_canonical': 'mosaic_convert_to_canonical', 'need_use_plus': 'mosaic_need_use_plus', 'unify_two_strings': 'mosaic_unify_two_strings', 'unify_strings': 'mosaic_unify_strings', 'remove_state': 'mosaic_remove_state', 'simplify': 'mosaic_simplify', 'combine_start_end_nodes': 'mosaic_combine_start_end_nodes'})
class mosaic_Graph:
    """Representation of a regex NDA (Non-Deterministic Automaton)

    Use this class to convert a regex list of items into its canonical
    regular expression string.
    """
    mosaic_graph_dict = {}
    mosaic_canon_graph_dict = {}
    mosaic_node_list = []
    mosaic_start_node = None
    mosaic_end_states = []
    mosaic_start_state = 0
    mosaic_regex = []
    mosaic_unified_regex = ''

    @_name_boundary.callable_contract({'self': 'mosaic_self_89a8060'}, '__init__')
    def __init__(mosaic_self_89a8060):
        _name_boundary.attributes(mosaic_self_89a8060)['graph_dict'] = {}

    @_name_boundary.callable_contract({'self': 'mosaic_self_52eea2f', 'node': 'mosaic_node_aebe269', 'next_list': 'mosaic_next_list_d67c7c3'}, 'add_node')
    def mosaic_add_node(mosaic_self_52eea2f, mosaic_node_aebe269, mosaic_next_list_d67c7c3=None):
        _name_boundary.attributes(mosaic_self_52eea2f)['graph_dict'][mosaic_node_aebe269] = mosaic_next_list_d67c7c3

    @_name_boundary.callable_contract({'self': 'mosaic_self_6a19893', 'node': 'mosaic_node_dbfd31c'}, 'has_node')
    def mosaic_has_node(mosaic_self_6a19893, mosaic_node_dbfd31c):
        return mosaic_node_dbfd31c in graph_dict.keys()

    @_name_boundary.callable_contract({'self': 'mosaic_self_89e67fa', 'node': 'mosaic_node_b26712e', 'next_list': 'mosaic_next_list_a1699f8'}, 'update_node')
    def mosaic_update_node(mosaic_self_89e67fa, mosaic_node_b26712e, mosaic_next_list_a1699f8):
        _name_boundary.attributes(mosaic_self_89e67fa)['graph_dict'][mosaic_node_b26712e] = mosaic_next_list_a1699f8

    @_name_boundary.callable_contract({'self': 'mosaic_self_efac1de', 'node': 'mosaic_node_8cc4205', 'next': 'mosaic_next_921a821'}, 'add_new_next_to_node')
    def mosaic_add_new_next_to_node(mosaic_self_efac1de, mosaic_node_8cc4205, mosaic_next_921a821):
        _name_boundary.attributes(mosaic_self_efac1de)['graph_dict'][mosaic_node_8cc4205].append(mosaic_next_921a821)

    @_name_boundary.callable_contract({'self': 'mosaic_self_db9b948'}, '__str__')
    def __str__(mosaic_self_db9b948):
        mosaic_max_08adc22 = -1
        for mosaic_node_312bae0 in _name_boundary.attributes(mosaic_self_db9b948)['graph_dict'].keys():
            if mosaic_max_08adc22 < int(_name_boundary.attributes(mosaic_node_312bae0)['name']):
                mosaic_max_08adc22 = int(_name_boundary.attributes(mosaic_node_312bae0)['name'])
        mosaic_graph_list_c7fd183 = [None] * (mosaic_max_08adc22 + 1)
        for mosaic_node_312bae0 in _name_boundary.attributes(mosaic_self_db9b948)['graph_dict'].keys():
            mosaic_actual_string_f3c53c9 = str(mosaic_node_312bae0) + ':'
            for mosaic_next_node_64c9021 in _name_boundary.attributes(mosaic_self_db9b948)['graph_dict'][mosaic_node_312bae0]:
                mosaic_actual_string_f3c53c9 += ' ' + str(mosaic_next_node_64c9021)
            mosaic_graph_list_c7fd183[int(_name_boundary.attributes(mosaic_node_312bae0)['name'])] = mosaic_actual_string_f3c53c9
        mosaic_ret_string_ad699cb = '\n-- Node graph --\n'
        for mosaic_s_3b1e3bb in mosaic_graph_list_c7fd183:
            if mosaic_s_3b1e3bb:
                mosaic_ret_string_ad699cb += mosaic_s_3b1e3bb + '\n'
        mosaic_ret_string_ad699cb += '\n-- Canonical graph --\n'
        for mosaic_state_0deb599 in _name_boundary.attributes(mosaic_self_db9b948)['canon_graph_dict'].keys():
            if mosaic_state_0deb599 == _name_boundary.attributes(mosaic_self_db9b948)['start_state']:
                mosaic_ret_string_ad699cb += '> '
            elif mosaic_state_0deb599 in _name_boundary.attributes(mosaic_self_db9b948)['end_states']:
                mosaic_ret_string_ad699cb += '# '
            else:
                mosaic_ret_string_ad699cb += '  '
            mosaic_ret_string_ad699cb += '%d: %s\n' % (mosaic_state_0deb599, _name_boundary.attributes(mosaic_self_db9b948)['canon_graph_dict'][mosaic_state_0deb599])
        mosaic_ret_string_ad699cb += '\n'
        return mosaic_ret_string_ad699cb

    @_name_boundary.callable_contract({'self': 'mosaic_self_a95765e', 'idx': 'mosaic_idx_5dadae9'}, 'get_node_for_idx')
    def mosaic_get_node_for_idx(mosaic_self_a95765e, mosaic_idx_5dadae9):
        if mosaic_idx_5dadae9 >= len(_name_boundary.attributes(mosaic_self_a95765e)['node_list']):
            return None
        return _name_boundary.attributes(mosaic_self_a95765e)['node_list'][mosaic_idx_5dadae9]

    @_name_boundary.callable_contract({'self': 'mosaic_self_ebb4507', 'regex_list': 'mosaic_regex_list_2fcdf2a', 'pos': 'mosaic_pos_8537485'}, 'get_re_index_for_pos')
    def mosaic_get_re_index_for_pos(mosaic_self_ebb4507, mosaic_regex_list_2fcdf2a, mosaic_pos_8537485):
        for mosaic_idx_02a932f, mosaic_item_00e03c9 in enumerate(mosaic_regex_list_2fcdf2a):
            if mosaic_item_00e03c9['pos'] == mosaic_pos_8537485:
                return mosaic_idx_02a932f
        for mosaic_idx_02a932f, mosaic_item_00e03c9 in enumerate(mosaic_regex_list_2fcdf2a):
            if mosaic_item_00e03c9['pos'] - 1 == mosaic_pos_8537485:
                return mosaic_idx_02a932f
        return -1

    @_name_boundary.callable_contract({'self': 'mosaic_self_4aa6f09', 'regex_list': 'mosaic_regex_list_3afe41e'}, 'fill_from_regex_list')
    def mosaic_fill_from_regex_list(mosaic_self_4aa6f09, mosaic_regex_list_3afe41e):
        _name_boundary.attributes(mosaic_self_4aa6f09)['node_list'] = []
        for mosaic_idx_985e2d9, mosaic_item_db9d1f6 in enumerate(mosaic_regex_list_3afe41e):
            mosaic_node_0832588 = mosaic_Node(name='%s' % mosaic_idx_985e2d9)
            if mosaic_item_db9d1f6['type'] == 'jump_backward':
                _name_boundary.attributes(mosaic_node_0832588)['set_type_jump_backward']()
            elif mosaic_item_db9d1f6['type'] == 'jump_forward':
                _name_boundary.attributes(mosaic_node_0832588)['set_type_jump_forward']()
            elif mosaic_item_db9d1f6['type'] == 'end':
                _name_boundary.attributes(mosaic_node_0832588)['set_type_end']()
            else:
                _name_boundary.attributes(mosaic_node_0832588)['set_type_character']()
                _name_boundary.attributes(mosaic_node_0832588)['set_value'](mosaic_item_db9d1f6['value'])
            _name_boundary.attributes(mosaic_self_4aa6f09)['node_list'].append(mosaic_node_0832588)
        _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'] = {}
        for mosaic_idx_985e2d9, mosaic_node_0832588 in enumerate(_name_boundary.attributes(mosaic_self_4aa6f09)['node_list']):
            if _name_boundary.attributes(mosaic_node_0832588)['is_type_end']():
                _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = []
            elif _name_boundary.attributes(mosaic_node_0832588)['is_type_character']():
                mosaic_next_5f07294 = _name_boundary.attributes(mosaic_self_4aa6f09)['get_node_for_idx'](mosaic_idx_985e2d9 + 1)
                if mosaic_next_5f07294:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = [mosaic_next_5f07294]
                else:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = []
            elif _name_boundary.attributes(mosaic_node_0832588)['is_type_jump_backward']():
                mosaic_next_idx_b2c1498 = _name_boundary.attributes(mosaic_self_4aa6f09)['get_re_index_for_pos'](mosaic_regex_list_3afe41e, mosaic_regex_list_3afe41e[mosaic_idx_985e2d9]['value'])
                mosaic_next_5f07294 = _name_boundary.attributes(mosaic_self_4aa6f09)['get_node_for_idx'](mosaic_next_idx_b2c1498)
                if mosaic_next_5f07294:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = [mosaic_next_5f07294]
                else:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = []
            elif _name_boundary.attributes(mosaic_node_0832588)['is_type_jump_forward']():
                mosaic_next_idx1_8072bab = mosaic_idx_985e2d9 + 1
                mosaic_next_idx2_6c1d162 = _name_boundary.attributes(mosaic_self_4aa6f09)['get_re_index_for_pos'](mosaic_regex_list_3afe41e, mosaic_regex_list_3afe41e[mosaic_idx_985e2d9]['value'])
                mosaic_next1_b624dd1 = _name_boundary.attributes(mosaic_self_4aa6f09)['get_node_for_idx'](mosaic_next_idx1_8072bab)
                mosaic_next2_e421aef = _name_boundary.attributes(mosaic_self_4aa6f09)['get_node_for_idx'](mosaic_next_idx2_6c1d162)
                _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588] = []
                if mosaic_next1_b624dd1:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588].append(mosaic_next1_b624dd1)
                if mosaic_next2_e421aef:
                    _name_boundary.attributes(mosaic_self_4aa6f09)['graph_dict'][mosaic_node_0832588].append(mosaic_next2_e421aef)

    @_name_boundary.callable_contract({'self': 'mosaic_self_f6217a2', 'node': 'mosaic_node_d6c061e'}, 'get_character_nodes')
    def mosaic_get_character_nodes(mosaic_self_f6217a2, mosaic_node_d6c061e):
        mosaic_node_list_cfb7283 = []
        for mosaic_next_ed91d4b in _name_boundary.attributes(mosaic_self_f6217a2)['graph_dict'][mosaic_node_d6c061e]:
            if _name_boundary.attributes(mosaic_next_ed91d4b)['is_type_character']() or _name_boundary.attributes(mosaic_next_ed91d4b)['is_type_end']():
                mosaic_node_list_cfb7283.append(mosaic_next_ed91d4b)
            else:
                mosaic_node_list_cfb7283 = list(set(mosaic_node_list_cfb7283).union(_name_boundary.attributes(mosaic_self_f6217a2)['get_character_nodes'](mosaic_next_ed91d4b)))
        return mosaic_node_list_cfb7283

    @_name_boundary.callable_contract({'self': 'mosaic_self_c5ee984', 'current_node': 'mosaic_current_node_7535954', 'node': 'mosaic_node_b778893', 'backup_dict': 'mosaic_backup_dict_e8e2036'}, 'find_node_type_jump')
    def mosaic_find_node_type_jump(mosaic_self_c5ee984, mosaic_current_node_7535954, mosaic_node_b778893, mosaic_backup_dict_e8e2036):
        if not _name_boundary.attributes(mosaic_current_node_7535954)['is_type_jump']():
            return False
        if mosaic_current_node_7535954 == mosaic_node_b778893:
            return True
        if not _name_boundary.attributes(mosaic_self_c5ee984)['graph_dict'][mosaic_current_node_7535954]:
            return False
        for mosaic_next_node_2b7a2da in mosaic_backup_dict_e8e2036[mosaic_current_node_7535954]:
            if _name_boundary.attributes(mosaic_self_c5ee984)['find_node_type_jump'](mosaic_next_node_2b7a2da, mosaic_node_b778893, mosaic_backup_dict_e8e2036):
                return True
        return False

    @_name_boundary.callable_contract({'self': 'mosaic_self_1f2cd23'}, 'reduce')
    def mosaic_reduce(mosaic_self_1f2cd23):
        mosaic_star_node_9f9ac1b = None
        for mosaic_node_95a8a96 in _name_boundary.attributes(mosaic_self_1f2cd23)['graph_dict'].keys():
            if _name_boundary.attributes(mosaic_node_95a8a96)['is_type_character']():
                _name_boundary.attributes(mosaic_self_1f2cd23)['graph_dict'][mosaic_node_95a8a96] = _name_boundary.attributes(mosaic_self_1f2cd23)['get_character_nodes'](mosaic_node_95a8a96)
            if _name_boundary.attributes(mosaic_node_95a8a96)['name'] == '0':
                mosaic_start_node_becdf88 = mosaic_node_95a8a96
        mosaic_old_dict_90f94f2 = dict(_name_boundary.attributes(mosaic_self_1f2cd23)['graph_dict'])
        mosaic_backup_dict_6b7781a = dict(_name_boundary.attributes(mosaic_self_1f2cd23)['graph_dict'])
        for mosaic_node_95a8a96 in mosaic_old_dict_90f94f2.keys():
            if _name_boundary.attributes(mosaic_node_95a8a96)['is_type_jump']():
                if _name_boundary.attributes(mosaic_self_1f2cd23)['find_node_type_jump'](mosaic_start_node_becdf88, mosaic_node_95a8a96, mosaic_backup_dict_6b7781a):
                    continue
                del _name_boundary.attributes(mosaic_self_1f2cd23)['graph_dict'][mosaic_node_95a8a96]

    @_name_boundary.callable_contract({'self': 'mosaic_self_66bad9a', 'node': 'mosaic_node_0fbc3d8'}, 'get_edges')
    def mosaic_get_edges(mosaic_self_66bad9a, mosaic_node_0fbc3d8):
        mosaic_edges_20218b1 = []
        mosaic_is_end_state_28d4c1f = False
        for mosaic_next_5c8cd5e in _name_boundary.attributes(mosaic_self_66bad9a)['graph_dict'][mosaic_node_0fbc3d8]:
            if _name_boundary.attributes(mosaic_next_5c8cd5e)['is_type_end']():
                mosaic_is_end_state_28d4c1f = True
            else:
                mosaic_edges_20218b1.append((_name_boundary.attributes(mosaic_next_5c8cd5e)['value'], int(_name_boundary.attributes(mosaic_next_5c8cd5e)['name'])))
        return (mosaic_is_end_state_28d4c1f, mosaic_edges_20218b1)

    @_name_boundary.callable_contract({'self': 'mosaic_self_8c735aa'}, 'convert_to_canonical')
    def mosaic_convert_to_canonical(mosaic_self_8c735aa):
        _name_boundary.attributes(mosaic_self_8c735aa)['end_states'] = []
        for mosaic_node_ae27cd5 in _name_boundary.attributes(mosaic_self_8c735aa)['graph_dict'].keys():
            if _name_boundary.attributes(mosaic_node_ae27cd5)['is_type_end']():
                continue
            mosaic_state_idx_f5b6d40 = int(_name_boundary.attributes(mosaic_node_ae27cd5)['name'])
            mosaic_is_end_state_8089ffc, _name_boundary.attributes(mosaic_self_8c735aa)['canon_graph_dict'][mosaic_state_idx_f5b6d40] = _name_boundary.attributes(mosaic_self_8c735aa)['get_edges'](mosaic_node_ae27cd5)
            if mosaic_is_end_state_8089ffc == True:
                _name_boundary.attributes(mosaic_self_8c735aa)['end_states'].append(mosaic_state_idx_f5b6d40)
        for mosaic_node_ae27cd5 in _name_boundary.attributes(mosaic_self_8c735aa)['graph_dict'].keys():
            if _name_boundary.attributes(mosaic_node_ae27cd5)['name'] == '0':
                _name_boundary.attributes(mosaic_self_8c735aa)['start_state'] = -1
                _name_boundary.attributes(mosaic_self_8c735aa)['canon_graph_dict'][-1] = [(_name_boundary.attributes(mosaic_node_ae27cd5)['value'], 0)]
        mosaic_logger.debug(_name_boundary.attributes(mosaic_self_8c735aa)['canon_graph_dict'])
        mosaic_logger.debug('end_states:')
        mosaic_logger.debug(_name_boundary.attributes(mosaic_self_8c735aa)['end_states'])
        mosaic_logger.debug('start_state:')
        mosaic_logger.debug(_name_boundary.attributes(mosaic_self_8c735aa)['start_state'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_52ec204', 'initial_string': 'mosaic_initial_string_5efb42b', 'string_to_add': 'mosaic_string_to_add_6911441'}, 'need_use_plus')
    def mosaic_need_use_plus(mosaic_self_52ec204, mosaic_initial_string_5efb42b, mosaic_string_to_add_6911441):
        if not mosaic_string_to_add_6911441.endswith('*'):
            return False
        if mosaic_string_to_add_6911441.startswith('(') and mosaic_string_to_add_6911441[-2:-1] == ')':
            mosaic_actual_part_ce004e5 = mosaic_string_to_add_6911441[1:-2]
        else:
            mosaic_actual_part_ce004e5 = mosaic_string_to_add_6911441[:-1]
        if mosaic_initial_string_5efb42b.endswith(mosaic_actual_part_ce004e5):
            return True
        if mosaic_initial_string_5efb42b.endswith(mosaic_string_to_add_6911441):
            return True
        return False

    @_name_boundary.callable_contract({'self': 'mosaic_self_bd7ee17', 's1': 'mosaic_s1_52973d0', 's2': 'mosaic_s2_f798827'}, 'unify_two_strings')
    def mosaic_unify_two_strings(mosaic_self_bd7ee17, mosaic_s1_52973d0, mosaic_s2_f798827):
        mosaic_lcss_b3ef9c2 = ''
        for mosaic_i_fb4aeb9 in range(1, len(mosaic_s1_52973d0) + 1):
            if mosaic_s2_f798827.find(mosaic_s1_52973d0[:mosaic_i_fb4aeb9], 0, mosaic_i_fb4aeb9) != -1:
                mosaic_lcss_b3ef9c2 = mosaic_s1_52973d0[:mosaic_i_fb4aeb9]
        if mosaic_lcss_b3ef9c2:
            mosaic_s1_52973d0 = mosaic_s1_52973d0[len(mosaic_lcss_b3ef9c2):]
            mosaic_s2_f798827 = mosaic_s2_f798827[len(mosaic_lcss_b3ef9c2):]
        mosaic_lces_4f2c589 = ''
        for mosaic_i_fb4aeb9 in range(1, len(mosaic_s1_52973d0) + 1):
            if mosaic_s2_f798827.find(mosaic_s1_52973d0[-mosaic_i_fb4aeb9:], len(mosaic_s2_f798827) - mosaic_i_fb4aeb9, len(mosaic_s2_f798827)) != -1:
                mosaic_lces_4f2c589 = mosaic_s1_52973d0[-mosaic_i_fb4aeb9:]
        if mosaic_lces_4f2c589:
            mosaic_s1_52973d0 = mosaic_s1_52973d0[:len(mosaic_s1_52973d0) - len(mosaic_lces_4f2c589)]
            mosaic_s2_f798827 = mosaic_s2_f798827[:len(mosaic_s2_f798827) - len(mosaic_lces_4f2c589)]
        if not mosaic_s1_52973d0 and (not mosaic_s2_f798827):
            return mosaic_lcss_b3ef9c2 + mosaic_lces_4f2c589
        if mosaic_s1_52973d0 and mosaic_s2_f798827:
            return mosaic_lcss_b3ef9c2 + '(' + mosaic_s1_52973d0 + '|' + mosaic_s2_f798827 + ')' + mosaic_lces_4f2c589
        if not mosaic_s2_f798827:
            mosaic_aux_edc8695 = mosaic_s1_52973d0
            mosaic_s1_52973d0 = mosaic_s2_f798827
            mosaic_s2_f798827 = mosaic_aux_edc8695
        if mosaic_s2_f798827[-1] == '+':
            mosaic_s2_f798827 = mosaic_s2_f798827[:-1] + '*'
        elif len(mosaic_s2_f798827) > 1:
            mosaic_s2_f798827 = '(' + mosaic_s2_f798827 + ')?'
        else:
            mosaic_s2_f798827 = mosaic_s2_f798827 + '?'
        return mosaic_lcss_b3ef9c2 + mosaic_s2_f798827 + mosaic_lces_4f2c589

    @_name_boundary.callable_contract({'self': 'mosaic_self_b85df0c', 'string_list': 'mosaic_string_list_9e519c4'}, 'unify_strings')
    def mosaic_unify_strings(mosaic_self_b85df0c, mosaic_string_list_9e519c4):
        mosaic_unified_e7c43a1 = ''
        if not mosaic_string_list_9e519c4:
            return None
        if len(mosaic_string_list_9e519c4) == 1:
            return mosaic_string_list_9e519c4[0]
        mosaic_current_5e54c9e = mosaic_string_list_9e519c4[0]
        for mosaic_s_4d3606f in mosaic_string_list_9e519c4[1:]:
            mosaic_current_5e54c9e = _name_boundary.attributes(mosaic_self_b85df0c)['unify_two_strings'](mosaic_current_5e54c9e, mosaic_s_4d3606f)
        return mosaic_current_5e54c9e

    @_name_boundary.callable_contract({'self': 'mosaic_self_ea362cb', 'state_to_remove': 'mosaic_state_to_remove_c8eecc2'}, 'remove_state')
    def mosaic_remove_state(mosaic_self_ea362cb, mosaic_state_to_remove_c8eecc2):
        mosaic_itself_string_851cd59 = ''
        for mosaic_next_string_9172f33, mosaic_next_state_f8b0d08 in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_state_to_remove_c8eecc2]:
            if mosaic_next_state_f8b0d08 == mosaic_state_to_remove_c8eecc2:
                if len(mosaic_next_string_9172f33) > 1:
                    mosaic_itself_string_851cd59 = '(%s)*' % mosaic_next_string_9172f33
                else:
                    mosaic_itself_string_851cd59 = '%s*' % mosaic_next_string_9172f33
        mosaic_to_strings_a1d3b23 = {}
        for mosaic_to_state_f4ab38e in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'].keys():
            mosaic_to_strings_a1d3b23[mosaic_to_state_f4ab38e] = []
            if mosaic_to_state_f4ab38e == mosaic_state_to_remove_c8eecc2:
                continue
            for mosaic_iter_to_string_88b2d27, mosaic_iter_to_state_f1d8b17 in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_state_to_remove_c8eecc2]:
                if mosaic_iter_to_state_f1d8b17 == mosaic_to_state_f4ab38e:
                    mosaic_to_strings_a1d3b23[mosaic_to_state_f4ab38e].append(mosaic_iter_to_string_88b2d27)
        mosaic_unified_to_string_363228d = {}
        for mosaic_to_state_f4ab38e in mosaic_to_strings_a1d3b23.keys():
            mosaic_unified_to_string_363228d[mosaic_to_state_f4ab38e] = _name_boundary.attributes(mosaic_self_ea362cb)['unify_strings'](mosaic_to_strings_a1d3b23[mosaic_to_state_f4ab38e])
        for mosaic_from_state_72c4ca4 in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'].keys():
            if mosaic_from_state_72c4ca4 == mosaic_state_to_remove_c8eecc2:
                continue
            mosaic_items_to_remove_list_9bef7e1 = []
            for mosaic_next_string_9172f33, mosaic_next_state_f8b0d08 in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_from_state_72c4ca4]:
                if mosaic_next_state_f8b0d08 != mosaic_state_to_remove_c8eecc2:
                    continue
                mosaic_items_to_remove_list_9bef7e1.append((mosaic_next_string_9172f33, mosaic_next_state_f8b0d08))
                for mosaic_to_state_f4ab38e in _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'].keys():
                    if len(mosaic_to_strings_a1d3b23[mosaic_to_state_f4ab38e]) == 0:
                        continue
                    mosaic_to_string_f8c450c = mosaic_unified_to_string_363228d[mosaic_to_state_f4ab38e]
                    if _name_boundary.attributes(mosaic_self_ea362cb)['need_use_plus'](mosaic_next_string_9172f33, mosaic_itself_string_851cd59):
                        _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_from_state_72c4ca4].append((mosaic_next_string_9172f33 + '+' + mosaic_to_string_f8c450c, mosaic_to_state_f4ab38e))
                        continue
                    _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_from_state_72c4ca4].append((mosaic_next_string_9172f33 + mosaic_itself_string_851cd59 + mosaic_to_string_f8c450c, mosaic_to_state_f4ab38e))
            for mosaic_next_string_9172f33, mosaic_next_state_f8b0d08 in mosaic_items_to_remove_list_9bef7e1:
                _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_from_state_72c4ca4].remove((mosaic_next_string_9172f33, mosaic_next_state_f8b0d08))
        del _name_boundary.attributes(mosaic_self_ea362cb)['canon_graph_dict'][mosaic_state_to_remove_c8eecc2]

    @_name_boundary.callable_contract({'self': 'mosaic_self_56459ea'}, 'simplify')
    def mosaic_simplify(mosaic_self_56459ea):
        mosaic_tmp_dict_56c7155 = dict(_name_boundary.attributes(mosaic_self_56459ea)['canon_graph_dict'])
        for mosaic_state_f908c32 in mosaic_tmp_dict_56c7155.keys():
            if mosaic_state_f908c32 != _name_boundary.attributes(mosaic_self_56459ea)['start_state'] and mosaic_state_f908c32 not in _name_boundary.attributes(mosaic_self_56459ea)['end_states']:
                _name_boundary.attributes(mosaic_self_56459ea)['remove_state'](mosaic_state_f908c32)

    @_name_boundary.callable_contract({'self': 'mosaic_self_9f0e811'}, 'combine_start_end_nodes')
    def mosaic_combine_start_end_nodes(mosaic_self_9f0e811):
        mosaic_working_strings_1b175e6 = _name_boundary.attributes(mosaic_self_9f0e811)['canon_graph_dict'][_name_boundary.attributes(mosaic_self_9f0e811)['start_state']]
        mosaic_final_strings_43ff80e = []
        mosaic_string_added_79e35ac = True
        while mosaic_string_added_79e35ac == True:
            mosaic_string_added_79e35ac = False
            mosaic_initial_strings_8ddf0f1 = mosaic_working_strings_1b175e6
            mosaic_working_strings_1b175e6 = []
            for mosaic_start_string_03bb7f0, mosaic_start_next_state_1901c75 in mosaic_initial_strings_8ddf0f1:
                if not mosaic_start_next_state_1901c75 in _name_boundary.attributes(mosaic_self_9f0e811)['end_states']:
                    continue
                if _name_boundary.attributes(mosaic_self_9f0e811)['canon_graph_dict'][mosaic_start_next_state_1901c75]:
                    for mosaic_next_string_ab619c6, mosaic_next_state_0b96f15 in _name_boundary.attributes(mosaic_self_9f0e811)['canon_graph_dict'][mosaic_start_next_state_1901c75]:
                        if mosaic_next_state_0b96f15 == mosaic_start_next_state_1901c75:
                            mosaic_next_string_ab619c6 = '(%s)*' % mosaic_next_string_ab619c6
                            if _name_boundary.attributes(mosaic_self_9f0e811)['need_use_plus'](mosaic_start_string_03bb7f0, mosaic_next_string_ab619c6):
                                mosaic_final_strings_43ff80e.append((mosaic_start_string_03bb7f0 + '+', None))
                            else:
                                mosaic_final_strings_43ff80e.append((mosaic_start_string_03bb7f0 + mosaic_next_string_ab619c6, None))
                        else:
                            mosaic_final_strings_43ff80e.append((mosaic_start_string_03bb7f0 + mosaic_next_string_ab619c6, None))
                            mosaic_working_strings_1b175e6.append((mosaic_start_string_03bb7f0 + mosaic_next_string_ab619c6, mosaic_next_state_0b96f15))
                else:
                    mosaic_final_strings_43ff80e.append((mosaic_start_string_03bb7f0, None))
                mosaic_string_added_79e35ac = True
        _name_boundary.attributes(mosaic_self_9f0e811)['regex'] = [mosaic_x_adf3cd7[0] for mosaic_x_adf3cd7 in mosaic_final_strings_43ff80e]
        _name_boundary.attributes(mosaic_self_9f0e811)['unified_regex'] = _name_boundary.attributes(mosaic_self_9f0e811)['unify_strings'](_name_boundary.attributes(mosaic_self_9f0e811)['regex'])

@_name_boundary.callable_contract({'re': 'mosaic_re_feed81f'}, 'create_regex_list')
def mosaic_create_regex_list(mosaic_re_feed81f):
    """Convert binary regex to list of items.

    Each item stores character position inside the binary regex (useful
    for jumps), character type and the value (either character or
    jump offset).
    """
    mosaic_regex_list_b0c5e72 = []
    mosaic_logger.debug('re.type: 0x%x', (mosaic_re_feed81f[0] >> 24) + (mosaic_re_feed81f[1] >> 16) + (mosaic_re_feed81f[2] >> 8) + mosaic_re_feed81f[3])
    mosaic_logger.debug('re.length: 0x%x', mosaic_re_feed81f[4] + (mosaic_re_feed81f[5] >> 8))
    mosaic_i_44d1631 = 6
    _name_boundary.attributes(mosaic_RegexParser)['parse'](mosaic_re_feed81f, mosaic_i_44d1631, mosaic_regex_list_b0c5e72)
    return mosaic_regex_list_b0c5e72

@_name_boundary.callable_contract({'re': 'mosaic_re_d8d57e8'}, 'parse_regex')
def mosaic_parse_regex(mosaic_re_d8d57e8):
    """Parse binary form for regular expression into canonical string.

    The input binary format is the one stored in the sandbox profile
    file. The out format is a canonical regular expression string using
    standard ASCII characters and metacharacters such as ^, $, +, *, etc.
    """
    mosaic_regex_list_5bbd653 = mosaic_create_regex_list(mosaic_re_d8d57e8)
    mosaic_g_1d5cbb1 = mosaic_Graph()
    _name_boundary.attributes(mosaic_g_1d5cbb1)['fill_from_regex_list'](mosaic_regex_list_5bbd653)
    _name_boundary.attributes(mosaic_g_1d5cbb1)['reduce']()
    _name_boundary.attributes(mosaic_g_1d5cbb1)['convert_to_canonical']()
    _name_boundary.attributes(mosaic_g_1d5cbb1)['simplify']()
    _name_boundary.attributes(mosaic_g_1d5cbb1)['combine_start_end_nodes']()
    mosaic_logger.debug(mosaic_g_1d5cbb1)
    return _name_boundary.attributes(mosaic_g_1d5cbb1)['regex']
import sys as mosaic_sys
import struct as mosaic_struct

@_name_boundary.callable_contract({}, 'main')
def mosaic_main():
    """Parse regular expressions in binary file."""
    if len(mosaic_sys.argv) != 2:
        (print >> mosaic_sys.stderr, 'Usage: %s <regex-binary-file>' % mosaic_sys.argv[0])
        mosaic_sys.exit(1)
    with open(mosaic_sys.argv[1]) as mosaic_f_8713d46:
        mosaic_re_count_29f3617 = mosaic_struct.unpack('<H', mosaic_f_8713d46.read(2))[0]
        for mosaic_i_0996f76 in range(mosaic_re_count_29f3617):
            mosaic_re_length_22aa025 = mosaic_struct.unpack('<H', mosaic_f_8713d46.read(2))[0]
            mosaic_re_5d94b6a = mosaic_struct.unpack('<%dB' % mosaic_re_length_22aa025, mosaic_f_8713d46.read(mosaic_re_length_22aa025))
            mosaic_logger.info('total_re_length: 0x%x', mosaic_re_length_22aa025)
            mosaic_re_debug_str_74e1808 = ('re: [', ', '.join([hex(mosaic_i_274e345) for mosaic_i_274e345 in mosaic_re_5d94b6a]), ']')
            mosaic_logger.info(mosaic_re_debug_str_74e1808)
            print(mosaic_parse_regex(mosaic_re_5d94b6a))
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
_name_boundary.module_contract(globals(), {'logger': 'mosaic_logger', 'struct': 'mosaic_struct', 'RegexParser': 'mosaic_RegexParser', 'main': 'mosaic_main', 'Node': 'mosaic_Node', 'parse_regex': 'mosaic_parse_regex', 'logging': 'mosaic_logging', 'create_regex_list': 'mosaic_create_regex_list', 'sys': 'mosaic_sys', 'Graph': 'mosaic_Graph'})
