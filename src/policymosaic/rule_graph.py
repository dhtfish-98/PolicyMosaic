#!/usr/bin/env python3
# Derived from sandblaster_26; attributed graph algorithms with explicit work/expansion guards.
import policymosaic_boundary as _name_boundary
import sys as mosaic_sys
import struct as mosaic_struct
import re as mosaic_re
import logging as mosaic_logging
import logging.config as _boundary_import_logging_config
import logging as mosaic_logging
import json as mosaic_json
from policymosaic.filter_decoder import mosaic_get_filter_arg_string_by_offset_no_skip as mosaic_get_filter_arg_string_by_offset_no_skip
import policymosaic.filter_decoder as mosaic_sandbox_filter
mosaic_logger = mosaic_logging.getLogger(__name__)
from policymosaic.safety import PolicyFormatError, read_exact, MAX_NODES, bounded_analysis, analysis_step, checked_add, checked_multiply, analysis_guard, c_content

@_name_boundary.class_contract('InlineModifier', {'id': 'mosaic_id', 'policy_op_idx': 'mosaic_policy_op_idx', 'argument': 'mosaic_argument'})
class mosaic_InlineModifier:

    @_name_boundary.callable_contract({'self': 'mosaic_self_a8b3112', 'id': 'mosaic_id_fc59aa2', 'policy_op_idx': 'mosaic_policy_op_idx_d0ba2af', 'argument': 'mosaic_argument_d1ff6c1'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_a8b3112, mosaic_id_fc59aa2, mosaic_policy_op_idx_d0ba2af, mosaic_argument_d1ff6c1):
        _name_boundary.attributes(mosaic_self_a8b3112)['id'] = mosaic_id_fc59aa2
        _name_boundary.attributes(mosaic_self_a8b3112)['policy_op_idx'] = mosaic_policy_op_idx_d0ba2af
        _name_boundary.attributes(mosaic_self_a8b3112)['argument'] = mosaic_argument_d1ff6c1

@_name_boundary.class_contract('Modifier', {'flags': 'mosaic_flags', 'count': 'mosaic_count', 'unknown': 'mosaic_unknown', 'offset': 'mosaic_offset'})
class mosaic_Modifier:

    @_name_boundary.callable_contract({'self': 'mosaic_self_db74589', 'flags': 'mosaic_flags_822f126', 'count': 'mosaic_count_d000683', 'unknown': 'mosaic_unknown_10dcd81', 'offset': 'mosaic_offset_0d1e746'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_db74589, mosaic_flags_822f126, mosaic_count_d000683, mosaic_unknown_10dcd81, mosaic_offset_0d1e746):
        _name_boundary.attributes(mosaic_self_db74589)['flags'] = mosaic_flags_822f126
        _name_boundary.attributes(mosaic_self_db74589)['count'] = mosaic_count_d000683
        _name_boundary.attributes(mosaic_self_db74589)['unknown'] = mosaic_unknown_10dcd81
        _name_boundary.attributes(mosaic_self_db74589)['offset'] = mosaic_offset_0d1e746

@_name_boundary.class_contract('TerminalNode', {'TERMINAL_NODE_TYPE_ALLOW': 'mosaic_TERMINAL_NODE_TYPE_ALLOW', 'TERMINAL_NODE_TYPE_DENY': 'mosaic_TERMINAL_NODE_TYPE_DENY', 'INLINE_MODIFIERS': 'mosaic_INLINE_MODIFIERS', 'FLAGS_MODIFIERS': 'mosaic_FLAGS_MODIFIERS', 'c_repr': 'mosaic_c_repr', 'load_modifiers_db': 'mosaic_load_modifiers_db', 'get_modifier': 'mosaic_get_modifier', 'get_modifiers_by_flag': 'mosaic_get_modifiers_by_flag', 'terminal_convert_function': 'mosaic_terminal_convert_function', 'convert_filter': 'mosaic_convert_filter', 'is_allow': 'mosaic_is_allow', 'is_deny': 'mosaic_is_deny', 'type': 'mosaic_type', 'flags': 'mosaic_flags', 'action': 'mosaic_action', 'modifier_flags': 'mosaic_modifier_flags', 'action_inline': 'mosaic_action_inline', 'inline_modifier': 'mosaic_inline_modifier', 'modifier': 'mosaic_modifier', 'inline_operation_node': 'mosaic_inline_operation_node', 'modifiers_db': 'mosaic_modifiers_db', 'ss': 'mosaic_ss', 'db_modifiers': 'mosaic_db_modifiers', 'parsed': 'mosaic_parsed', 'operation_name': 'mosaic_operation_name'})
class mosaic_TerminalNode:
    """Allow or Deny end node in binary sandbox format

    A terminal node, when reached, either denies or allows the rule.
    A node has a type (allow or deny) and a set of flags. Flags are
    currently unused.
    """
    mosaic_TERMINAL_NODE_TYPE_ALLOW = 0
    mosaic_TERMINAL_NODE_TYPE_DENY = 1
    mosaic_INLINE_MODIFIERS = 'inline_modifiers'
    mosaic_FLAGS_MODIFIERS = 'flags_modifiers'

    @_name_boundary.callable_contract({'self': 'mosaic_self_dd84d3e'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_dd84d3e):
        _name_boundary.attributes(mosaic_self_dd84d3e)['type'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['flags'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['action'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['modifier_flags'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['action_inline'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['inline_modifier'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['modifier'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['inline_operation_node'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['modifiers_db'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['ss'] = None
        _name_boundary.attributes(mosaic_self_dd84d3e)['db_modifiers'] = {_name_boundary.attributes(mosaic_self_dd84d3e)['INLINE_MODIFIERS']: [], _name_boundary.attributes(mosaic_self_dd84d3e)['FLAGS_MODIFIERS']: []}
        _name_boundary.attributes(mosaic_self_dd84d3e)['parsed'] = False
        _name_boundary.attributes(mosaic_self_dd84d3e)['operation_name'] = None

    @_name_boundary.callable_contract({'self': 'mosaic_self_6a07b28', 'other': 'mosaic_other_d8a8f88'}, '__eq__')
    @analysis_guard
    def __eq__(mosaic_self_6a07b28, mosaic_other_d8a8f88):
        return _name_boundary.attributes(mosaic_self_6a07b28)['type'] == _name_boundary.attributes(mosaic_other_d8a8f88)['type'] and _name_boundary.attributes(mosaic_self_6a07b28)['flags'] == _name_boundary.attributes(mosaic_other_d8a8f88)['flags']

    @_name_boundary.callable_contract({'self': 'mosaic_self_ed64d8d'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_ed64d8d):
        mosaic_ret_e1b55fe = ''
        if _name_boundary.attributes(mosaic_self_ed64d8d)['type'] == _name_boundary.attributes(mosaic_self_ed64d8d)['TERMINAL_NODE_TYPE_ALLOW']:
            mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, 'allow')
        elif _name_boundary.attributes(mosaic_self_ed64d8d)['type'] == _name_boundary.attributes(mosaic_self_ed64d8d)['TERMINAL_NODE_TYPE_DENY']:
            mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, 'deny')
        else:
            mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, 'unknown')
        if _name_boundary.attributes(mosaic_self_ed64d8d)['parsed']:
            if _name_boundary.attributes(mosaic_self_ed64d8d)['action_inline']:
                if not _name_boundary.attributes(_name_boundary.attributes(mosaic_self_ed64d8d)['inline_modifier'])['policy_op_idx']:
                    for mosaic_modifier_3f69367 in _name_boundary.attributes(mosaic_self_ed64d8d)['db_modifiers'][_name_boundary.attributes(mosaic_self_ed64d8d)['INLINE_MODIFIERS']]:
                        analysis_step()
                        mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, f" (with {mosaic_modifier_3f69367['name']} {_name_boundary.attributes(mosaic_self_ed64d8d)['ss']})")
                else:
                    mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, str(_name_boundary.attributes(mosaic_self_ed64d8d)['inline_operation_node']))
        for mosaic_modifier_3f69367 in _name_boundary.attributes(mosaic_self_ed64d8d)['db_modifiers'][_name_boundary.attributes(mosaic_self_ed64d8d)['FLAGS_MODIFIERS']]:
            analysis_step()
            if mosaic_modifier_3f69367 and 'name' in mosaic_modifier_3f69367.keys():
                mosaic_ret_e1b55fe = checked_add(mosaic_ret_e1b55fe, f" (with {mosaic_modifier_3f69367['name']})")
        return mosaic_ret_e1b55fe

    @_name_boundary.callable_contract({'self': 'mosaic_self_004265c'}, 'c_repr')
    @analysis_guard
    def mosaic_c_repr(mosaic_self_004265c):
        mosaic_ret_4bcb81d = ''
        assert _name_boundary.attributes(mosaic_self_004265c)['type'] == _name_boundary.attributes(mosaic_self_004265c.parent)['raw'][1] & 1
        if _name_boundary.attributes(mosaic_self_004265c)['type'] == _name_boundary.attributes(mosaic_self_004265c)['TERMINAL_NODE_TYPE_ALLOW']:
            mosaic_ret_4bcb81d = checked_add(mosaic_ret_4bcb81d, 'return allow("')
        elif _name_boundary.attributes(mosaic_self_004265c)['type'] == _name_boundary.attributes(mosaic_self_004265c)['TERMINAL_NODE_TYPE_DENY']:
            mosaic_ret_4bcb81d = checked_add(mosaic_ret_4bcb81d, 'return deny("')
        else:
            mosaic_ret_4bcb81d = checked_add(mosaic_ret_4bcb81d, 'return unknown("')
        mosaic_modifier_strings_19df7c6 = []
        for mosaic_modifier_4f6c343 in _name_boundary.attributes(mosaic_self_004265c)['db_modifiers'][_name_boundary.attributes(mosaic_self_004265c)['FLAGS_MODIFIERS']]:
            analysis_step()
            if mosaic_modifier_4f6c343 and 'name' in mosaic_modifier_4f6c343.keys():
                mosaic_modifier_strings_19df7c6 = checked_add(mosaic_modifier_strings_19df7c6, [mosaic_modifier_4f6c343['name']])
        if _name_boundary.attributes(mosaic_self_004265c)['parsed']:
            if _name_boundary.attributes(mosaic_self_004265c)['action_inline']:
                if not _name_boundary.attributes(_name_boundary.attributes(mosaic_self_004265c)['inline_modifier'])['policy_op_idx']:
                    for mosaic_modifier_4f6c343 in _name_boundary.attributes(mosaic_self_004265c)['db_modifiers'][_name_boundary.attributes(mosaic_self_004265c)['INLINE_MODIFIERS']]:
                        analysis_step()
                        mosaic_modifier_strings_19df7c6 = checked_add(mosaic_modifier_strings_19df7c6, [f"{mosaic_modifier_4f6c343['name']} '{_name_boundary.attributes(mosaic_self_004265c)['ss']}'"])
        mosaic_ret_4bcb81d = checked_add(mosaic_ret_4bcb81d, c_content('; '.join(mosaic_modifier_strings_19df7c6)))
        mosaic_ret_4bcb81d = checked_add(mosaic_ret_4bcb81d, '");')
        return mosaic_ret_4bcb81d

    @_name_boundary.callable_contract({'self': 'mosaic_self_8b5ec3e'}, 'load_modifiers_db')
    @analysis_guard
    def mosaic_load_modifiers_db(mosaic_self_8b5ec3e):
        if not _name_boundary.attributes(mosaic_self_8b5ec3e)['modifiers_db']:
            with open(_name_boundary.resource('modifiers.json')) as mosaic_data_702b8aa:
                mosaic_temp_16d6eec = mosaic_json.load(mosaic_data_702b8aa)
            _name_boundary.attributes(mosaic_self_8b5ec3e)['modifiers_db'] = mosaic_temp_16d6eec['modifiers']

    @_name_boundary.callable_contract({'self': 'mosaic_self_3139d16', 'key_value': 'mosaic_key_value_69916f2', 'key_name': 'mosaic_key_name_485d762'}, 'get_modifier')
    @analysis_guard
    def mosaic_get_modifier(mosaic_self_3139d16, mosaic_key_value_69916f2, mosaic_key_name_485d762):
        _name_boundary.attributes(mosaic_self_3139d16)['load_modifiers_db']()
        for mosaic_i_55f64cb in _name_boundary.attributes(mosaic_self_3139d16)['modifiers_db']:
            analysis_step()
            if mosaic_i_55f64cb[mosaic_key_name_485d762] == mosaic_key_value_69916f2:
                return mosaic_i_55f64cb

    @_name_boundary.callable_contract({'self': 'mosaic_self_6df7e83', 'flags': 'mosaic_flags_019d6b9'}, 'get_modifiers_by_flag')
    @analysis_guard
    def mosaic_get_modifiers_by_flag(mosaic_self_6df7e83, mosaic_flags_019d6b9):
        _name_boundary.attributes(mosaic_self_6df7e83)['load_modifiers_db']()
        mosaic_modifiers_43d41dc = []
        for mosaic_modifier_208658e in _name_boundary.attributes(mosaic_self_6df7e83)['modifiers_db']:
            analysis_step()
            if mosaic_modifier_208658e['action_mask'] and mosaic_flags_019d6b9 & mosaic_modifier_208658e['action_mask'] == mosaic_modifier_208658e['action_flag']:
                if mosaic_modifier_208658e['name'] == 'report' and _name_boundary.attributes(mosaic_self_6df7e83)['is_deny']():
                    continue
                if mosaic_modifier_208658e['name'] == 'no-report' and _name_boundary.attributes(mosaic_self_6df7e83)['is_allow']():
                    continue
                mosaic_modifiers_43d41dc.append(mosaic_modifier_208658e)
        return mosaic_modifiers_43d41dc

    @_name_boundary.callable_contract({'self': 'mosaic_self_6f258bf', 'convert_fn': 'mosaic_convert_fn_aecb67a', 'infile': 'mosaic_infile_93da601', 'sandbox_data': 'mosaic_sandbox_data_e645c66', 'keep_builtin_filters': 'mosaic_keep_builtin_filters_8dd491e'}, 'terminal_convert_function')
    @analysis_guard
    def mosaic_terminal_convert_function(mosaic_self_6f258bf, mosaic_convert_fn_aecb67a, mosaic_infile_93da601, mosaic_sandbox_data_e645c66, mosaic_keep_builtin_filters_8dd491e):
        if _name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier']:
            if not _name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['policy_op_idx']:
                _name_boundary.attributes(mosaic_self_6f258bf)['db_modifiers'][_name_boundary.attributes(mosaic_self_6f258bf)['INLINE_MODIFIERS']].append(_name_boundary.attributes(mosaic_self_6f258bf)['get_modifier'](_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['id'], 'id'))
                _name_boundary.attributes(mosaic_self_6f258bf)['ss'] = mosaic_sandbox_filter.convert_modifier_callback(mosaic_infile_93da601, mosaic_sandbox_data_e645c66, _name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['id'], _name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['argument'])
            else:
                _name_boundary.attributes(mosaic_self_6f258bf)['operation_name'] = _name_boundary.attributes(mosaic_sandbox_data_e645c66)['sb_ops'][_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['policy_op_idx']]
                _name_boundary.attributes(mosaic_self_6f258bf)['inline_operation_node'] = _name_boundary.attributes(mosaic_sandbox_data_e645c66)['operation_nodes'][_name_boundary.attributes(mosaic_sandbox_data_e645c66)['policies'][_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['inline_modifier'])['argument']]]
        _name_boundary.attributes(mosaic_self_6f258bf)['db_modifiers'][_name_boundary.attributes(mosaic_self_6f258bf)['FLAGS_MODIFIERS']].extend(_name_boundary.attributes(mosaic_self_6f258bf)['get_modifiers_by_flag'](_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6f258bf)['modifier'])['flags']))
        _name_boundary.attributes(mosaic_self_6f258bf)['parsed'] = True

    @_name_boundary.callable_contract({'self': 'mosaic_self_82e1d21', 'convert_fn': 'mosaic_convert_fn_c428f20', 'f': 'mosaic_f_0f2d846', 'sandbox_data': 'mosaic_sandbox_data_cf0e3b7', 'keep_builtin_filters': 'mosaic_keep_builtin_filters_fea1682'}, 'convert_filter')
    @analysis_guard
    def mosaic_convert_filter(mosaic_self_82e1d21, mosaic_convert_fn_c428f20, mosaic_f_0f2d846, mosaic_sandbox_data_cf0e3b7, mosaic_keep_builtin_filters_fea1682):
        _name_boundary.attributes(mosaic_self_82e1d21)['terminal_convert_function'](mosaic_convert_fn_c428f20, mosaic_f_0f2d846, mosaic_sandbox_data_cf0e3b7, mosaic_keep_builtin_filters_fea1682)

    @_name_boundary.callable_contract({'self': 'mosaic_self_ad92123'}, 'is_allow')
    @analysis_guard
    def mosaic_is_allow(mosaic_self_ad92123):
        return _name_boundary.attributes(mosaic_self_ad92123)['type'] == _name_boundary.attributes(mosaic_self_ad92123)['TERMINAL_NODE_TYPE_ALLOW']

    @_name_boundary.callable_contract({'self': 'mosaic_self_57e2db1'}, 'is_deny')
    @analysis_guard
    def mosaic_is_deny(mosaic_self_57e2db1):
        return _name_boundary.attributes(mosaic_self_57e2db1)['type'] == _name_boundary.attributes(mosaic_self_57e2db1)['TERMINAL_NODE_TYPE_DENY']

@_name_boundary.class_contract('NonTerminalNode', {'simplify_list': 'mosaic_simplify_list', 'str_debug': 'mosaic_str_debug', 'c_repr': 'mosaic_c_repr', 'str_not': 'mosaic_str_not', 'values': 'mosaic_values', 'is_entitlement_start': 'mosaic_is_entitlement_start', 'is_entitlement': 'mosaic_is_entitlement', 'is_last_regular_expression': 'mosaic_is_last_regular_expression', 'convert_filter': 'mosaic_convert_filter', 'is_non_terminal_deny': 'mosaic_is_non_terminal_deny', 'is_non_terminal_allow': 'mosaic_is_non_terminal_allow', 'is_non_terminal_non_terminal': 'mosaic_is_non_terminal_non_terminal', 'is_allow_non_terminal': 'mosaic_is_allow_non_terminal', 'is_deny_non_terminal': 'mosaic_is_deny_non_terminal', 'is_deny_allow': 'mosaic_is_deny_allow', 'is_allow_deny': 'mosaic_is_allow_deny', 'filter_id': 'mosaic_filter_id', 'filter': 'mosaic_filter', 'argument_id': 'mosaic_argument_id', 'argument': 'mosaic_argument', 'match_offset': 'mosaic_match_offset', 'match': 'mosaic_match', 'unmatch_offset': 'mosaic_unmatch_offset', 'unmatch': 'mosaic_unmatch'})
class mosaic_NonTerminalNode:
    """Intermediary node consisting of a filter to match

    The non-terminal node, when matched, points to a new node, and
    when unmatched, to another node.

    A non-terminal node consists of the filter to match, its argument and
    the match and unmatch nodes.
    """

    @_name_boundary.callable_contract({'self': 'mosaic_self_32e884c'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_32e884c):
        _name_boundary.attributes(mosaic_self_32e884c)['filter_id'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['filter'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['argument_id'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['argument'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['match_offset'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['match'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['unmatch_offset'] = None
        _name_boundary.attributes(mosaic_self_32e884c)['unmatch'] = None

    @_name_boundary.callable_contract({'self': 'mosaic_self_e08dae0', 'other': 'mosaic_other_5240648'}, '__eq__')
    @analysis_guard
    def __eq__(mosaic_self_e08dae0, mosaic_other_5240648):
        return _name_boundary.attributes(mosaic_self_e08dae0)['filter_id'] == _name_boundary.attributes(mosaic_other_5240648)['filter_id'] and _name_boundary.attributes(mosaic_self_e08dae0)['argument_id'] == _name_boundary.attributes(mosaic_other_5240648)['argument_id'] and (_name_boundary.attributes(mosaic_self_e08dae0)['match_offset'] == _name_boundary.attributes(mosaic_other_5240648)['match_offset']) and (_name_boundary.attributes(mosaic_self_e08dae0)['unmatch_offset'] == _name_boundary.attributes(mosaic_other_5240648)['unmatch_offset'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_4953f20', 'arg_list': 'mosaic_arg_list_6153cec'}, 'simplify_list')
    @analysis_guard
    def mosaic_simplify_list(mosaic_self_4953f20, mosaic_arg_list_6153cec):
        mosaic_result_list_45b3f7b = []
        for mosaic_a_80b004d in mosaic_arg_list_6153cec:
            analysis_step()
            if len(mosaic_a_80b004d) == 0:
                continue
            mosaic_tmp_list_f806400 = list(mosaic_result_list_45b3f7b)
            mosaic_match_found_29e1d13 = False
            for mosaic_r_da8b518 in mosaic_tmp_list_f806400:
                analysis_step()
                if len(mosaic_r_da8b518) == 0:
                    continue
                if mosaic_a_80b004d == mosaic_r_da8b518 or checked_add(mosaic_a_80b004d, '/') == mosaic_r_da8b518 or mosaic_a_80b004d == checked_add(mosaic_r_da8b518, '/'):
                    mosaic_match_found_29e1d13 = True
                    mosaic_result_list_45b3f7b.remove(mosaic_r_da8b518)
                    if mosaic_a_80b004d[-1] == '/':
                        mosaic_result_list_45b3f7b.append(checked_add(mosaic_a_80b004d, '^^^'))
                    else:
                        mosaic_result_list_45b3f7b.append(checked_add(mosaic_a_80b004d, '/^^^'))
            if mosaic_match_found_29e1d13 == False:
                mosaic_result_list_45b3f7b.append(mosaic_a_80b004d)
        return mosaic_result_list_45b3f7b

    @_name_boundary.callable_contract({'self': 'mosaic_self_a1249eb'}, 'str_debug')
    @analysis_guard
    def mosaic_str_debug(mosaic_self_a1249eb):
        if _name_boundary.attributes(mosaic_self_a1249eb)['filter']:
            if _name_boundary.attributes(mosaic_self_a1249eb)['argument']:
                if type(_name_boundary.attributes(mosaic_self_a1249eb)['argument']) is list:
                    if len(_name_boundary.attributes(mosaic_self_a1249eb)['argument']) == 1:
                        mosaic_ret_str_cbde0a0 = ''
                    else:
                        _name_boundary.attributes(mosaic_self_a1249eb)['argument'] = _name_boundary.attributes(mosaic_self_a1249eb)['simplify_list'](_name_boundary.attributes(mosaic_self_a1249eb)['argument'])
                        if len(_name_boundary.attributes(mosaic_self_a1249eb)['argument']) == 1:
                            mosaic_ret_str_cbde0a0 = ''
                        else:
                            mosaic_ret_str_cbde0a0 = '(require-any '
                    for mosaic_s_f53797b in _name_boundary.attributes(mosaic_self_a1249eb)['argument']:
                        analysis_step()
                        mosaic_curr_filter_dd5569e = _name_boundary.attributes(mosaic_self_a1249eb)['filter']
                        mosaic_regex_added_9481e51 = False
                        mosaic_prefix_added_33eba60 = False
                        if len(mosaic_s_f53797b) == 0:
                            mosaic_s_f53797b = '.+'
                            if not mosaic_regex_added_9481e51:
                                mosaic_regex_added_9481e51 = True
                                if _name_boundary.attributes(mosaic_self_a1249eb)['filter'] == 'literal':
                                    mosaic_curr_filter_dd5569e = 'regex'
                                else:
                                    mosaic_curr_filter_dd5569e = checked_add(mosaic_curr_filter_dd5569e, '-regex')
                        else:
                            if mosaic_s_f53797b[-4:] == '/^^^':
                                mosaic_curr_filter_dd5569e = 'subpath'
                                mosaic_s_f53797b = mosaic_s_f53797b[:-4]
                            if '\\' in mosaic_s_f53797b or '|' in mosaic_s_f53797b or ('[' in mosaic_s_f53797b and ']' in mosaic_s_f53797b) or ('+' in mosaic_s_f53797b):
                                if mosaic_curr_filter_dd5569e == 'subpath':
                                    mosaic_s_f53797b = checked_add(mosaic_s_f53797b, '/?')
                                if _name_boundary.attributes(mosaic_self_a1249eb)['filter'] == 'literal':
                                    mosaic_curr_filter_dd5569e = 'regex'
                                else:
                                    mosaic_curr_filter_dd5569e = checked_add(mosaic_curr_filter_dd5569e, '-regex')
                                mosaic_s_f53797b = mosaic_s_f53797b.replace('\\\\.', '[.]')
                                mosaic_s_f53797b = mosaic_s_f53797b.replace('\\.', '[.]')
                            if '${' in mosaic_s_f53797b and '}' in mosaic_s_f53797b:
                                if not mosaic_prefix_added_33eba60:
                                    mosaic_prefix_added_33eba60 = True
                                    mosaic_curr_filter_dd5569e = checked_add(mosaic_curr_filter_dd5569e, '-prefix')
                        if 'regex' in mosaic_curr_filter_dd5569e:
                            mosaic_ret_str_cbde0a0 = checked_add(mosaic_ret_str_cbde0a0, '(%04x, %04x) (%s #"%s")\n' % (_name_boundary.attributes(mosaic_self_a1249eb)['match_offset'], _name_boundary.attributes(mosaic_self_a1249eb)['unmatch_offset'], mosaic_curr_filter_dd5569e, mosaic_s_f53797b))
                        else:
                            mosaic_ret_str_cbde0a0 = checked_add(mosaic_ret_str_cbde0a0, '(%s "%s")\n' % (mosaic_curr_filter_dd5569e, mosaic_s_f53797b))
                    if len(_name_boundary.attributes(mosaic_self_a1249eb)['argument']) == 1:
                        mosaic_ret_str_cbde0a0 = mosaic_ret_str_cbde0a0[:-1]
                    else:
                        mosaic_ret_str_cbde0a0 = checked_add(mosaic_ret_str_cbde0a0[:-1], ')')
                    return mosaic_ret_str_cbde0a0
                mosaic_s_f53797b = _name_boundary.attributes(mosaic_self_a1249eb)['argument']
                mosaic_curr_filter_dd5569e = _name_boundary.attributes(mosaic_self_a1249eb)['filter']
                if not 'regex' in mosaic_curr_filter_dd5569e:
                    if '\\' in mosaic_s_f53797b or '|' in mosaic_s_f53797b or ('[' in mosaic_s_f53797b and ']' in mosaic_s_f53797b) or ('+' in mosaic_s_f53797b):
                        if _name_boundary.attributes(mosaic_self_a1249eb)['filter'] == 'literal':
                            mosaic_curr_filter_dd5569e = 'regex'
                        else:
                            mosaic_curr_filter_dd5569e = checked_add(mosaic_curr_filter_dd5569e, '-regex')
                        mosaic_s_f53797b = mosaic_s_f53797b.replace('\\\\.', '[.]')
                        mosaic_s_f53797b = mosaic_s_f53797b.replace('\\.', '[.]')
                if '${' in mosaic_s_f53797b and '}' in mosaic_s_f53797b:
                    if not 'prefix' in mosaic_curr_filter_dd5569e:
                        mosaic_curr_filter_dd5569e = checked_add(mosaic_curr_filter_dd5569e, '-prefix')
                return '(%04x, %04x) (%s %s)' % (_name_boundary.attributes(mosaic_self_a1249eb)['match_offset'], _name_boundary.attributes(mosaic_self_a1249eb)['unmatch_offset'], mosaic_curr_filter_dd5569e, mosaic_s_f53797b)
            else:
                return '(%04x, %04x) (%s)' % (_name_boundary.attributes(mosaic_self_a1249eb)['match_offset'], _name_boundary.attributes(mosaic_self_a1249eb)['unmatch_offset'], _name_boundary.attributes(mosaic_self_a1249eb)['filter'])
        return '(%02x %04x %04x %04x)' % (_name_boundary.attributes(mosaic_self_a1249eb)['filter_id'], _name_boundary.attributes(mosaic_self_a1249eb)['argument_id'], _name_boundary.attributes(mosaic_self_a1249eb)['match_offset'], _name_boundary.attributes(mosaic_self_a1249eb)['unmatch_offset'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_6ae2808'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_6ae2808):
        if _name_boundary.attributes(mosaic_self_6ae2808)['filter']:
            if _name_boundary.attributes(mosaic_self_6ae2808)['argument']:
                if type(_name_boundary.attributes(mosaic_self_6ae2808)['argument']) is list:
                    if len(_name_boundary.attributes(mosaic_self_6ae2808)['argument']) == 1:
                        mosaic_ret_str_eb069ce = ''
                    else:
                        _name_boundary.attributes(mosaic_self_6ae2808)['argument'] = _name_boundary.attributes(mosaic_self_6ae2808)['simplify_list'](_name_boundary.attributes(mosaic_self_6ae2808)['argument'])
                        if len(_name_boundary.attributes(mosaic_self_6ae2808)['argument']) == 1:
                            mosaic_ret_str_eb069ce = ''
                        else:
                            mosaic_ret_str_eb069ce = '(require-any '
                    for mosaic_s_1f0bbbc in _name_boundary.attributes(mosaic_self_6ae2808)['argument']:
                        analysis_step()
                        mosaic_curr_filter_19fea61 = _name_boundary.attributes(mosaic_self_6ae2808)['filter']
                        mosaic_regex_added_448d7c3 = False
                        mosaic_prefix_added_3796677 = False
                        if len(mosaic_s_1f0bbbc) == 0:
                            mosaic_s_1f0bbbc = '.+'
                            if not mosaic_regex_added_448d7c3:
                                mosaic_regex_added_448d7c3 = True
                                if _name_boundary.attributes(mosaic_self_6ae2808)['filter'] == 'literal':
                                    mosaic_curr_filter_19fea61 = 'regex'
                                else:
                                    mosaic_curr_filter_19fea61 = checked_add(mosaic_curr_filter_19fea61, '-regex')
                        else:
                            if mosaic_s_1f0bbbc[-4:] == '/^^^':
                                mosaic_curr_filter_19fea61 = 'subpath'
                                mosaic_s_1f0bbbc = mosaic_s_1f0bbbc[:-4]
                            if '\\' in mosaic_s_1f0bbbc or '|' in mosaic_s_1f0bbbc or ('[' in mosaic_s_1f0bbbc and ']' in mosaic_s_1f0bbbc) or ('+' in mosaic_s_1f0bbbc):
                                if mosaic_curr_filter_19fea61 == 'subpath':
                                    mosaic_s_1f0bbbc = checked_add(mosaic_s_1f0bbbc, '/?')
                                if _name_boundary.attributes(mosaic_self_6ae2808)['filter'] == 'literal':
                                    mosaic_curr_filter_19fea61 = 'regex'
                                else:
                                    mosaic_curr_filter_19fea61 = checked_add(mosaic_curr_filter_19fea61, '-regex')
                                mosaic_s_1f0bbbc = mosaic_s_1f0bbbc.replace('\\\\.', '[.]')
                                mosaic_s_1f0bbbc = mosaic_s_1f0bbbc.replace('\\.', '[.]')
                            if '${' in mosaic_s_1f0bbbc and '}' in mosaic_s_1f0bbbc:
                                if not mosaic_prefix_added_3796677:
                                    mosaic_prefix_added_3796677 = True
                                    mosaic_curr_filter_19fea61 = checked_add(mosaic_curr_filter_19fea61, '-prefix')
                        if 'regex' in mosaic_curr_filter_19fea61:
                            mosaic_ret_str_eb069ce = checked_add(mosaic_ret_str_eb069ce, '(%s #"%s")\n' % (mosaic_curr_filter_19fea61, mosaic_s_1f0bbbc))
                        else:
                            mosaic_ret_str_eb069ce = checked_add(mosaic_ret_str_eb069ce, '(%s "%s")\n' % (mosaic_curr_filter_19fea61, mosaic_s_1f0bbbc))
                    if len(_name_boundary.attributes(mosaic_self_6ae2808)['argument']) == 1:
                        mosaic_ret_str_eb069ce = mosaic_ret_str_eb069ce[:-1]
                    else:
                        mosaic_ret_str_eb069ce = checked_add(mosaic_ret_str_eb069ce[:-1], ')')
                    return mosaic_ret_str_eb069ce
                mosaic_s_1f0bbbc = _name_boundary.attributes(mosaic_self_6ae2808)['argument']
                mosaic_curr_filter_19fea61 = _name_boundary.attributes(mosaic_self_6ae2808)['filter']
                if not 'regex' in mosaic_curr_filter_19fea61:
                    if '\\' in mosaic_s_1f0bbbc or '|' in mosaic_s_1f0bbbc or ('[' in mosaic_s_1f0bbbc and ']' in mosaic_s_1f0bbbc) or ('+' in mosaic_s_1f0bbbc):
                        if _name_boundary.attributes(mosaic_self_6ae2808)['filter'] == 'literal':
                            mosaic_curr_filter_19fea61 = 'regex'
                        else:
                            mosaic_curr_filter_19fea61 = checked_add(mosaic_curr_filter_19fea61, '-regex')
                        mosaic_s_1f0bbbc = mosaic_s_1f0bbbc.replace('\\\\.', '[.]')
                        mosaic_s_1f0bbbc = mosaic_s_1f0bbbc.replace('\\.', '[.]')
                if '${' in mosaic_s_1f0bbbc and '}' in mosaic_s_1f0bbbc:
                    if not 'prefix' in mosaic_curr_filter_19fea61:
                        mosaic_curr_filter_19fea61 = checked_add(mosaic_curr_filter_19fea61, '-prefix')
                return '(%s %s)' % (mosaic_curr_filter_19fea61, mosaic_s_1f0bbbc)
            else:
                return '(%s)' % _name_boundary.attributes(mosaic_self_6ae2808)['filter']
        return '(%02x %04x %04x %04x)' % (_name_boundary.attributes(mosaic_self_6ae2808)['filter_id'], _name_boundary.attributes(mosaic_self_6ae2808)['argument_id'], _name_boundary.attributes(mosaic_self_6ae2808)['match_offset'], _name_boundary.attributes(mosaic_self_6ae2808)['unmatch_offset'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_900095a'}, 'c_repr')
    @analysis_guard
    def mosaic_c_repr(mosaic_self_900095a):
        if _name_boundary.attributes(mosaic_self_900095a)['filter']:
            if _name_boundary.attributes(mosaic_self_900095a)['argument']:
                if type(_name_boundary.attributes(mosaic_self_900095a)['argument']) is list:
                    if len(_name_boundary.attributes(mosaic_self_900095a)['argument']) != 1:
                        _name_boundary.attributes(mosaic_self_900095a)['argument'] = _name_boundary.attributes(mosaic_self_900095a)['simplify_list'](_name_boundary.attributes(mosaic_self_900095a)['argument'])
                    mosaic_c_style_arguments_956b6ac = []
                    for mosaic_s_cd8c6bb in _name_boundary.attributes(mosaic_self_900095a)['argument']:
                        analysis_step()
                        mosaic_curr_filter_c3002ec = _name_boundary.attributes(mosaic_self_900095a)['filter']
                        mosaic_regex_added_5590350 = False
                        mosaic_prefix_added_f88f8d7 = False
                        if len(mosaic_s_cd8c6bb) == 0:
                            mosaic_s_cd8c6bb = '.+'
                            if not mosaic_regex_added_5590350:
                                mosaic_regex_added_5590350 = True
                                if _name_boundary.attributes(mosaic_self_900095a)['filter'] == 'literal':
                                    mosaic_curr_filter_c3002ec = 'regex'
                                else:
                                    mosaic_curr_filter_c3002ec = checked_add(mosaic_curr_filter_c3002ec, '_regex')
                        else:
                            if mosaic_s_cd8c6bb[-4:] == '/^^^':
                                mosaic_curr_filter_c3002ec = 'subpath'
                                mosaic_s_cd8c6bb = mosaic_s_cd8c6bb[:-4]
                            if '\\' in mosaic_s_cd8c6bb or '|' in mosaic_s_cd8c6bb or ('[' in mosaic_s_cd8c6bb and ']' in mosaic_s_cd8c6bb) or ('+' in mosaic_s_cd8c6bb):
                                if mosaic_curr_filter_c3002ec == 'subpath':
                                    mosaic_s_cd8c6bb = checked_add(mosaic_s_cd8c6bb, '/?')
                                if _name_boundary.attributes(mosaic_self_900095a)['filter'] == 'literal':
                                    mosaic_curr_filter_c3002ec = 'regex'
                                else:
                                    mosaic_curr_filter_c3002ec = checked_add(mosaic_curr_filter_c3002ec, '_regex')
                                mosaic_s_cd8c6bb = mosaic_s_cd8c6bb.replace('\\\\.', '[.]')
                                mosaic_s_cd8c6bb = mosaic_s_cd8c6bb.replace('\\.', '[.]')
                            if '${' in mosaic_s_cd8c6bb and '}' in mosaic_s_cd8c6bb:
                                if not mosaic_prefix_added_f88f8d7:
                                    mosaic_prefix_added_f88f8d7 = True
                                    mosaic_curr_filter_c3002ec = checked_add(mosaic_curr_filter_c3002ec, '_prefix')
                        mosaic_c_style_arguments_956b6ac = checked_add(mosaic_c_style_arguments_956b6ac, ['%s("%s")' % (mosaic_curr_filter_c3002ec.replace('-', '_'), c_content(mosaic_s_cd8c6bb))])
                    return ' || '.join(mosaic_c_style_arguments_956b6ac)
                mosaic_s_cd8c6bb = _name_boundary.attributes(mosaic_self_900095a)['argument']
                mosaic_curr_filter_c3002ec = _name_boundary.attributes(mosaic_self_900095a)['filter'].replace('-', '_')
                if not 'regex' in mosaic_curr_filter_c3002ec:
                    if '\\' in mosaic_s_cd8c6bb or '|' in mosaic_s_cd8c6bb or ('[' in mosaic_s_cd8c6bb and ']' in mosaic_s_cd8c6bb) or ('+' in mosaic_s_cd8c6bb):
                        if _name_boundary.attributes(mosaic_self_900095a)['filter'] == 'literal':
                            mosaic_curr_filter_c3002ec = 'regex'
                        else:
                            mosaic_curr_filter_c3002ec = checked_add(mosaic_curr_filter_c3002ec, '_regex')
                        mosaic_s_cd8c6bb = mosaic_s_cd8c6bb.replace('\\\\.', '[.]')
                        mosaic_s_cd8c6bb = mosaic_s_cd8c6bb.replace('\\.', '[.]')
                if '${' in mosaic_s_cd8c6bb and '}' in mosaic_s_cd8c6bb:
                    if not 'prefix' in mosaic_curr_filter_c3002ec:
                        mosaic_curr_filter_c3002ec = checked_add(mosaic_curr_filter_c3002ec, '_prefix')
                return '%s("%s")' % (mosaic_curr_filter_c3002ec, c_content(mosaic_s_cd8c6bb))
            else:
                if _name_boundary.attributes(mosaic_self_900095a)['filter'] == 'literal':
                    return '%s("")' % _name_boundary.attributes(mosaic_self_900095a)['filter'].replace('-', '_')
                return '%s()' % _name_boundary.attributes(mosaic_self_900095a)['filter'].replace('-', '_')
        return 'unparsed_filter(0x%02x, 0x%04x)' % (_name_boundary.attributes(mosaic_self_900095a)['filter_id'], _name_boundary.attributes(mosaic_self_900095a)['argument_id'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_d410873'}, 'str_not')
    @analysis_guard
    def mosaic_str_not(mosaic_self_d410873):
        if _name_boundary.attributes(mosaic_self_d410873)['filter']:
            if _name_boundary.attributes(mosaic_self_d410873)['argument']:
                if type(_name_boundary.attributes(mosaic_self_d410873)['argument']) is list:
                    if len(_name_boundary.attributes(mosaic_self_d410873)['argument']) == 1:
                        mosaic_ret_str_0f82e51 = ''
                    else:
                        _name_boundary.attributes(mosaic_self_d410873)['argument'] = _name_boundary.attributes(mosaic_self_d410873)['simplify_list'](_name_boundary.attributes(mosaic_self_d410873)['argument'])
                        if len(_name_boundary.attributes(mosaic_self_d410873)['argument']) == 1:
                            mosaic_ret_str_0f82e51 = ''
                        else:
                            mosaic_ret_str_0f82e51 = '(require-all '
                    for mosaic_s_6aa5b5e in _name_boundary.attributes(mosaic_self_d410873)['argument']:
                        analysis_step()
                        mosaic_curr_filter_64041bd = _name_boundary.attributes(mosaic_self_d410873)['filter']
                        mosaic_regex_added_66ee190 = False
                        mosaic_prefix_added_75356a2 = False
                        if len(mosaic_s_6aa5b5e) == 0:
                            mosaic_s_6aa5b5e = '.+'
                            if not mosaic_regex_added_66ee190:
                                mosaic_regex_added_66ee190 = True
                                if _name_boundary.attributes(mosaic_self_d410873)['filter'] == 'literal':
                                    mosaic_curr_filter_64041bd = 'regex'
                                else:
                                    mosaic_curr_filter_64041bd = checked_add(mosaic_curr_filter_64041bd, '-regex')
                        else:
                            if mosaic_s_6aa5b5e[-4:] == '/^^^':
                                mosaic_curr_filter_64041bd = 'subpath'
                                mosaic_s_6aa5b5e = mosaic_s_6aa5b5e[:-4]
                            if '\\' in mosaic_s_6aa5b5e or '|' in mosaic_s_6aa5b5e or ('[' in mosaic_s_6aa5b5e and ']' in mosaic_s_6aa5b5e) or ('+' in mosaic_s_6aa5b5e):
                                if mosaic_curr_filter_64041bd == 'subpath':
                                    mosaic_s_6aa5b5e = checked_add(mosaic_s_6aa5b5e, '/?')
                                if _name_boundary.attributes(mosaic_self_d410873)['filter'] == 'literal':
                                    mosaic_curr_filter_64041bd = 'regex'
                                else:
                                    mosaic_curr_filter_64041bd = checked_add(mosaic_curr_filter_64041bd, '-regex')
                                mosaic_s_6aa5b5e = mosaic_s_6aa5b5e.replace('\\\\.', '[.]')
                                mosaic_s_6aa5b5e = mosaic_s_6aa5b5e.replace('\\.', '[.]')
                            if '${' in mosaic_s_6aa5b5e and '}' in mosaic_s_6aa5b5e:
                                if not mosaic_prefix_added_75356a2:
                                    mosaic_prefix_added_75356a2 = True
                                    mosaic_curr_filter_64041bd = checked_add(mosaic_curr_filter_64041bd, '-prefix')
                        if 'regex' in mosaic_curr_filter_64041bd:
                            mosaic_ret_str_0f82e51 = checked_add(mosaic_ret_str_0f82e51, '(require-not (%s #"%s"))\n' % (mosaic_curr_filter_64041bd, mosaic_s_6aa5b5e))
                        else:
                            mosaic_ret_str_0f82e51 = checked_add(mosaic_ret_str_0f82e51, '(require-not (%s "%s"))\n' % (mosaic_curr_filter_64041bd, mosaic_s_6aa5b5e))
                    if len(_name_boundary.attributes(mosaic_self_d410873)['argument']) == 1:
                        mosaic_ret_str_0f82e51 = mosaic_ret_str_0f82e51[:-1]
                    else:
                        mosaic_ret_str_0f82e51 = checked_add(mosaic_ret_str_0f82e51[:-1], ')')
                    return mosaic_ret_str_0f82e51
                mosaic_s_6aa5b5e = _name_boundary.attributes(mosaic_self_d410873)['argument']
                mosaic_curr_filter_64041bd = _name_boundary.attributes(mosaic_self_d410873)['filter']
                if not 'regex' in mosaic_curr_filter_64041bd:
                    if '\\' in mosaic_s_6aa5b5e or '|' in mosaic_s_6aa5b5e or ('[' in mosaic_s_6aa5b5e and ']' in mosaic_s_6aa5b5e) or ('+' in mosaic_s_6aa5b5e):
                        if _name_boundary.attributes(mosaic_self_d410873)['filter'] == 'literal':
                            mosaic_curr_filter_64041bd = 'regex'
                        else:
                            mosaic_curr_filter_64041bd = checked_add(mosaic_curr_filter_64041bd, '-regex')
                        mosaic_s_6aa5b5e = mosaic_s_6aa5b5e.replace('\\\\.', '[.]')
                        mosaic_s_6aa5b5e = mosaic_s_6aa5b5e.replace('\\.', '[.]')
                if '${' in mosaic_s_6aa5b5e and '}' in mosaic_s_6aa5b5e:
                    if not 'prefix' in mosaic_curr_filter_64041bd:
                        mosaic_curr_filter_64041bd = checked_add(mosaic_curr_filter_64041bd, '-prefix')
                return '(%s %s)' % (mosaic_curr_filter_64041bd, mosaic_s_6aa5b5e)
            else:
                return '(%s)' % _name_boundary.attributes(mosaic_self_d410873)['filter']
        return '(%02x %04x %04x %04x)' % (_name_boundary.attributes(mosaic_self_d410873)['filter_id'], _name_boundary.attributes(mosaic_self_d410873)['argument_id'], _name_boundary.attributes(mosaic_self_d410873)['match_offset'], _name_boundary.attributes(mosaic_self_d410873)['unmatch_offset'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_8028216'}, 'values')
    @analysis_guard
    def mosaic_values(mosaic_self_8028216):
        if _name_boundary.attributes(mosaic_self_8028216)['filter']:
            return (_name_boundary.attributes(mosaic_self_8028216)['filter'], _name_boundary.attributes(mosaic_self_8028216)['argument'])
        return ('%02x' % _name_boundary.attributes(mosaic_self_8028216)['filter_id'], '%04x' % _name_boundary.attributes(mosaic_self_8028216)['argument_id'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_2a0da02'}, 'is_entitlement_start')
    @analysis_guard
    def mosaic_is_entitlement_start(mosaic_self_2a0da02):
        return _name_boundary.attributes(mosaic_self_2a0da02)['filter_id'] == 30 or _name_boundary.attributes(mosaic_self_2a0da02)['filter_id'] == 160

    @_name_boundary.callable_contract({'self': 'mosaic_self_7ed86b0'}, 'is_entitlement')
    @analysis_guard
    def mosaic_is_entitlement(mosaic_self_7ed86b0):
        return _name_boundary.attributes(mosaic_self_7ed86b0)['filter_id'] == 30 or _name_boundary.attributes(mosaic_self_7ed86b0)['filter_id'] == 31 or _name_boundary.attributes(mosaic_self_7ed86b0)['filter_id'] == 32 or (_name_boundary.attributes(mosaic_self_7ed86b0)['filter_id'] == 160)

    @_name_boundary.callable_contract({'self': 'mosaic_self_7c559c4'}, 'is_last_regular_expression')
    @analysis_guard
    def mosaic_is_last_regular_expression(mosaic_self_7c559c4):
        return _name_boundary.attributes(mosaic_self_7c559c4)['filter_id'] == 129 and _name_boundary.attributes(mosaic_self_7c559c4)['argument_id'] == mosaic_num_regex - 1

    @_name_boundary.callable_contract({'self': 'mosaic_self_10af929', 'convert_fn': 'mosaic_convert_fn_430696e', 'f': 'mosaic_f_e7989d9', 'sandbox_data': 'mosaic_sandbox_data_58a7454', 'keep_builtin_filters': 'mosaic_keep_builtin_filters_e59f864'}, 'convert_filter')
    @analysis_guard
    def mosaic_convert_filter(mosaic_self_10af929, mosaic_convert_fn_430696e, mosaic_f_e7989d9, mosaic_sandbox_data_58a7454, mosaic_keep_builtin_filters_e59f864):
        _name_boundary.attributes(mosaic_self_10af929)['filter'], _name_boundary.attributes(mosaic_self_10af929)['argument'] = mosaic_convert_fn_430696e(mosaic_f_e7989d9, mosaic_sandbox_data_58a7454, mosaic_keep_builtin_filters_e59f864, _name_boundary.attributes(mosaic_self_10af929)['filter_id'], _name_boundary.attributes(mosaic_self_10af929)['argument_id'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_d796e8c'}, 'is_non_terminal_deny')
    @analysis_guard
    def mosaic_is_non_terminal_deny(mosaic_self_d796e8c):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_d796e8c)['match'])['is_non_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_d796e8c)['unmatch'])['is_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_d796e8c)['unmatch'])['terminal'])['is_deny']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_4775a97'}, 'is_non_terminal_allow')
    @analysis_guard
    def mosaic_is_non_terminal_allow(mosaic_self_4775a97):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_4775a97)['match'])['is_non_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_4775a97)['unmatch'])['is_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_4775a97)['unmatch'])['terminal'])['is_allow']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_b1908eb'}, 'is_non_terminal_non_terminal')
    @analysis_guard
    def mosaic_is_non_terminal_non_terminal(mosaic_self_b1908eb):
        return _name_boundary.attributes(_name_boundary.attributes(mosaic_self_b1908eb)['match'])['is_non_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_b1908eb)['unmatch'])['is_non_terminal']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_e589e3c'}, 'is_allow_non_terminal')
    @analysis_guard
    def mosaic_is_allow_non_terminal(mosaic_self_e589e3c):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_e589e3c)['match'])['is_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_e589e3c)['unmatch'])['is_non_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_e589e3c)['match'])['terminal'])['is_allow']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_5b178ca'}, 'is_deny_non_terminal')
    @analysis_guard
    def mosaic_is_deny_non_terminal(mosaic_self_5b178ca):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_5b178ca)['match'])['is_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_5b178ca)['unmatch'])['is_non_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_5b178ca)['match'])['terminal'])['is_deny']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_6b516d6'}, 'is_deny_allow')
    @analysis_guard
    def mosaic_is_deny_allow(mosaic_self_6b516d6):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_6b516d6)['match'])['is_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_6b516d6)['unmatch'])['is_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6b516d6)['match'])['terminal'])['is_deny']() and _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_6b516d6)['unmatch'])['terminal'])['is_allow']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_f1c5cb4'}, 'is_allow_deny')
    @analysis_guard
    def mosaic_is_allow_deny(mosaic_self_f1c5cb4):
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_f1c5cb4)['match'])['is_terminal']() and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_f1c5cb4)['unmatch'])['is_terminal']():
            return _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_f1c5cb4)['match'])['terminal'])['is_allow']() and _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_f1c5cb4)['unmatch'])['terminal'])['is_deny']()

@_name_boundary.class_contract('OperationNode', {'OPERATION_NODE_TYPE_NON_TERMINAL': 'mosaic_OPERATION_NODE_TYPE_NON_TERMINAL', 'OPERATION_NODE_TYPE_TERMINAL': 'mosaic_OPERATION_NODE_TYPE_TERMINAL', 'is_terminal': 'mosaic_is_terminal', 'is_non_terminal': 'mosaic_is_non_terminal', 'parse_terminal': 'mosaic_parse_terminal', 'parse_non_terminal': 'mosaic_parse_non_terminal', 'parse_raw': 'mosaic_parse_raw', 'convert_filter': 'mosaic_convert_filter', 'str_debug': 'mosaic_str_debug', 'c_repr': 'mosaic_c_repr', 'str_not': 'mosaic_str_not', 'values': 'mosaic_values', 'offset': 'mosaic_offset', 'raw': 'mosaic_raw', 'type': 'mosaic_type', 'terminal': 'mosaic_terminal', 'non_terminal': 'mosaic_non_terminal'})
class mosaic_OperationNode:
    """A rule item in the binary sandbox profile

    It may either be a teminal node (end node) or a non-terminal node
    (intermediary node). Each node type uses another class, as defined
    above.
    """
    mosaic_OPERATION_NODE_TYPE_NON_TERMINAL = 0
    mosaic_OPERATION_NODE_TYPE_TERMINAL = 1

    @_name_boundary.callable_contract({'self': 'mosaic_self_28d2cc3', 'offset': 'mosaic_offset_ac12ca2', 'raw': 'mosaic_raw_af3a32f'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_28d2cc3, mosaic_offset_ac12ca2, mosaic_raw_af3a32f):
        _name_boundary.attributes(mosaic_self_28d2cc3)['offset'] = mosaic_offset_ac12ca2
        _name_boundary.attributes(mosaic_self_28d2cc3)['raw'] = mosaic_raw_af3a32f
        _name_boundary.attributes(mosaic_self_28d2cc3)['type'] = None
        _name_boundary.attributes(mosaic_self_28d2cc3)['terminal'] = None
        _name_boundary.attributes(mosaic_self_28d2cc3)['non_terminal'] = None

    @_name_boundary.callable_contract({'self': 'mosaic_self_9ebd78b'}, 'is_terminal')
    @analysis_guard
    def mosaic_is_terminal(mosaic_self_9ebd78b):
        return _name_boundary.attributes(mosaic_self_9ebd78b)['type'] == _name_boundary.attributes(mosaic_self_9ebd78b)['OPERATION_NODE_TYPE_TERMINAL']

    @_name_boundary.callable_contract({'self': 'mosaic_self_817fa89'}, 'is_non_terminal')
    @analysis_guard
    def mosaic_is_non_terminal(mosaic_self_817fa89):
        return _name_boundary.attributes(mosaic_self_817fa89)['type'] == _name_boundary.attributes(mosaic_self_817fa89)['OPERATION_NODE_TYPE_NON_TERMINAL']

    @_name_boundary.callable_contract({'self': 'mosaic_self_3fec68e'}, 'parse_terminal')
    @analysis_guard
    def mosaic_parse_terminal(mosaic_self_3fec68e):
        _name_boundary.attributes(mosaic_self_3fec68e)['terminal'] = mosaic_TerminalNode()
        _name_boundary.attributes(mosaic_self_3fec68e)['terminal'].parent = mosaic_self_3fec68e
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['type'] = _name_boundary.attributes(mosaic_self_3fec68e)['raw'][1] & 1
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['modifier_flags'] = _name_boundary.attributes(mosaic_self_3fec68e)['raw'][1] | _name_boundary.attributes(mosaic_self_3fec68e)['raw'][2] << 8 | _name_boundary.attributes(mosaic_self_3fec68e)['raw'][3] << 16
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['action_inline'] = _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['modifier_flags'] & 8388608 != 0
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['action_inline']:
            _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['inline_modifier'] = mosaic_InlineModifier(_name_boundary.attributes(mosaic_self_3fec68e)['raw'][4], _name_boundary.attributes(mosaic_self_3fec68e)['raw'][5], checked_add(_name_boundary.attributes(mosaic_self_3fec68e)['raw'][6], _name_boundary.attributes(mosaic_self_3fec68e)['raw'][7] << 8))
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['modifier'] = mosaic_Modifier(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_3fec68e)['terminal'])['modifier_flags'], _name_boundary.attributes(mosaic_self_3fec68e)['raw'][4], _name_boundary.attributes(mosaic_self_3fec68e)['raw'][5], checked_add(_name_boundary.attributes(mosaic_self_3fec68e)['raw'][6], _name_boundary.attributes(mosaic_self_3fec68e)['raw'][7] << 8))

    @_name_boundary.callable_contract({'self': 'mosaic_self_83d4124'}, 'parse_non_terminal')
    @analysis_guard
    def mosaic_parse_non_terminal(mosaic_self_83d4124):
        _name_boundary.attributes(mosaic_self_83d4124)['non_terminal'] = mosaic_NonTerminalNode()
        _name_boundary.attributes(mosaic_self_83d4124)['non_terminal'].parent = mosaic_self_83d4124
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_83d4124)['non_terminal'])['filter_id'] = _name_boundary.attributes(mosaic_self_83d4124)['raw'][1]
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_83d4124)['non_terminal'])['argument_id'] = checked_add(_name_boundary.attributes(mosaic_self_83d4124)['raw'][2], _name_boundary.attributes(mosaic_self_83d4124)['raw'][3] << 8)
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_83d4124)['non_terminal'])['match_offset'] = checked_add(_name_boundary.attributes(mosaic_self_83d4124)['raw'][4], _name_boundary.attributes(mosaic_self_83d4124)['raw'][5] << 8)
        _name_boundary.attributes(_name_boundary.attributes(mosaic_self_83d4124)['non_terminal'])['unmatch_offset'] = checked_add(_name_boundary.attributes(mosaic_self_83d4124)['raw'][6], _name_boundary.attributes(mosaic_self_83d4124)['raw'][7] << 8)

    @_name_boundary.callable_contract({'self': 'mosaic_self_4295ae9'}, 'parse_raw')
    @analysis_guard
    def mosaic_parse_raw(mosaic_self_4295ae9):
        _name_boundary.attributes(mosaic_self_4295ae9)['type'] = _name_boundary.attributes(mosaic_self_4295ae9)['raw'][0]
        if _name_boundary.attributes(mosaic_self_4295ae9)['is_terminal']():
            _name_boundary.attributes(mosaic_self_4295ae9)['parse_terminal']()
        elif _name_boundary.attributes(mosaic_self_4295ae9)['is_non_terminal']():
            _name_boundary.attributes(mosaic_self_4295ae9)['parse_non_terminal']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_cd6ee94', 'convert_fn': 'mosaic_convert_fn_6fcfc9d', 'f': 'mosaic_f_998afa5', 'sandbox_data': 'mosaic_sandbox_data_60a37fc', 'keep_builtin_filters': 'mosaic_keep_builtin_filters_c3a0d01'}, 'convert_filter')
    @analysis_guard
    def mosaic_convert_filter(mosaic_self_cd6ee94, mosaic_convert_fn_6fcfc9d, mosaic_f_998afa5, mosaic_sandbox_data_60a37fc, mosaic_keep_builtin_filters_c3a0d01):
        if _name_boundary.attributes(mosaic_self_cd6ee94)['is_non_terminal']():
            _name_boundary.attributes(_name_boundary.attributes(mosaic_self_cd6ee94)['non_terminal'])['convert_filter'](mosaic_convert_fn_6fcfc9d, mosaic_f_998afa5, mosaic_sandbox_data_60a37fc, mosaic_keep_builtin_filters_c3a0d01)
        elif _name_boundary.attributes(mosaic_self_cd6ee94)['terminal']:
            _name_boundary.attributes(_name_boundary.attributes(mosaic_self_cd6ee94)['terminal'])['convert_filter'](_name_boundary.attributes(_name_boundary.attributes(mosaic_self_cd6ee94)['terminal'])['terminal_convert_function'], mosaic_f_998afa5, mosaic_sandbox_data_60a37fc, mosaic_keep_builtin_filters_c3a0d01)

    @_name_boundary.callable_contract({'self': 'mosaic_self_ae24a6c'}, 'str_debug')
    @analysis_guard
    def mosaic_str_debug(mosaic_self_ae24a6c):
        mosaic_ret_b061271 = '(%02x) ' % _name_boundary.attributes(mosaic_self_ae24a6c)['offset']
        if _name_boundary.attributes(mosaic_self_ae24a6c)['is_terminal']():
            mosaic_ret_b061271 = checked_add(mosaic_ret_b061271, 'terminal: ')
            mosaic_ret_b061271 = checked_add(mosaic_ret_b061271, str(_name_boundary.attributes(mosaic_self_ae24a6c)['terminal']))
        if _name_boundary.attributes(mosaic_self_ae24a6c)['is_non_terminal']():
            mosaic_ret_b061271 = checked_add(mosaic_ret_b061271, 'non-terminal: ')
            mosaic_ret_b061271 = checked_add(mosaic_ret_b061271, str(_name_boundary.attributes(mosaic_self_ae24a6c)['non_terminal']))
        return mosaic_ret_b061271

    @_name_boundary.callable_contract({'self': 'mosaic_self_fa23e5d'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_fa23e5d):
        mosaic_ret_8347775 = ''
        if _name_boundary.attributes(mosaic_self_fa23e5d)['is_terminal']():
            mosaic_ret_8347775 = checked_add(mosaic_ret_8347775, str(_name_boundary.attributes(mosaic_self_fa23e5d)['terminal']))
        if _name_boundary.attributes(mosaic_self_fa23e5d)['is_non_terminal']():
            mosaic_ret_8347775 = checked_add(mosaic_ret_8347775, str(_name_boundary.attributes(mosaic_self_fa23e5d)['non_terminal']))
        return mosaic_ret_8347775

    @_name_boundary.callable_contract({'self': 'mosaic_self_498a555'}, 'c_repr')
    @analysis_guard
    def mosaic_c_repr(mosaic_self_498a555):
        mosaic_ret_a40091c = ''
        if _name_boundary.attributes(mosaic_self_498a555)['is_terminal']():
            mosaic_ret_a40091c = checked_add(mosaic_ret_a40091c, _name_boundary.attributes(_name_boundary.attributes(mosaic_self_498a555)['terminal'])['c_repr']())
        if _name_boundary.attributes(mosaic_self_498a555)['is_non_terminal']():
            mosaic_ret_a40091c = checked_add(mosaic_ret_a40091c, _name_boundary.attributes(_name_boundary.attributes(mosaic_self_498a555)['non_terminal'])['c_repr']())
        return mosaic_ret_a40091c

    @_name_boundary.callable_contract({'self': 'mosaic_self_73714ac'}, 'str_not')
    @analysis_guard
    def mosaic_str_not(mosaic_self_73714ac):
        mosaic_ret_fdd4e48 = ''
        if _name_boundary.attributes(mosaic_self_73714ac)['is_terminal']():
            mosaic_ret_fdd4e48 = checked_add(mosaic_ret_fdd4e48, str(_name_boundary.attributes(mosaic_self_73714ac)['terminal']))
        if _name_boundary.attributes(mosaic_self_73714ac)['is_non_terminal']():
            mosaic_ret_fdd4e48 = checked_add(mosaic_ret_fdd4e48, _name_boundary.attributes(_name_boundary.attributes(mosaic_self_73714ac)['non_terminal'])['str_not']())
        return mosaic_ret_fdd4e48

    @_name_boundary.callable_contract({'self': 'mosaic_self_ed1e810'}, 'values')
    @analysis_guard
    def mosaic_values(mosaic_self_ed1e810):
        if _name_boundary.attributes(mosaic_self_ed1e810)['is_terminal']():
            return (None, None)
        else:
            return _name_boundary.attributes(_name_boundary.attributes(mosaic_self_ed1e810)['non_terminal'])['values']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_7737571', 'other': 'mosaic_other_33443cf'}, '__eq__')
    @analysis_guard
    def __eq__(mosaic_self_7737571, mosaic_other_33443cf):
        return _name_boundary.attributes(mosaic_self_7737571)['offset'] == _name_boundary.attributes(mosaic_other_33443cf)['offset']

    @_name_boundary.callable_contract({'self': 'mosaic_self_1811ffe'}, '__hash__')
    @analysis_guard
    def __hash__(mosaic_self_1811ffe):
        return hash(_name_boundary.attributes(mosaic_self_1811ffe)['offset'])
mosaic_processed_nodes = []
mosaic_num_regex = 0

@_name_boundary.callable_contract({'node': 'mosaic_node_f908608'}, 'has_been_processed')
@analysis_guard
def mosaic_has_been_processed(mosaic_node_f908608):
    global mosaic_processed_nodes
    return mosaic_node_f908608 in mosaic_processed_nodes

@_name_boundary.callable_contract({'raw': 'mosaic_raw_5469cb5', 'index': 'mosaic_index_8d21ec5'}, 'build_operation_node')
@analysis_guard
def mosaic_build_operation_node(mosaic_raw_5469cb5, mosaic_index_8d21ec5):
    mosaic_node_766827d = mosaic_OperationNode(mosaic_index_8d21ec5, mosaic_raw_5469cb5)
    _name_boundary.attributes(mosaic_node_766827d)['parse_raw']()
    return mosaic_node_766827d

@analysis_guard
def mosaic_build_operation_nodes(f, num_operation_nodes):
    if type(num_operation_nodes) is not int or not 0 <= num_operation_nodes <= MAX_NODES:
        raise PolicyFormatError('operation node count exceeds limit')
    raw = read_exact(f, checked_multiply(num_operation_nodes, 8))
    nodes = []
    for index in range(num_operation_nodes):
        analysis_step()
        record = tuple(raw[checked_multiply(index, 8):checked_multiply(checked_add(index, 1), 8)])
        if record[0] not in (0, 1):
            raise PolicyFormatError('unsupported operation node type')
        nodes.append(mosaic_build_operation_node(record, index))
    for node in nodes:
        analysis_step()
        branch = node.non_terminal
        if branch is not None:
            if branch.match_offset >= len(nodes) or branch.unmatch_offset >= len(nodes):
                raise PolicyFormatError('operation graph reference outside node table')
            branch.match = nodes[branch.match_offset]
            branch.unmatch = nodes[branch.unmatch_offset]
    return nodes

@analysis_guard
def mosaic_find_operation_node_by_offset(operation_nodes, offset):
    if type(offset) is not int or offset < 0:
        raise PolicyFormatError('invalid operation node reference')
    if offset < len(operation_nodes) and operation_nodes[offset].offset == offset:
        return operation_nodes[offset]
    for node in operation_nodes:
        analysis_step()
        if node.offset == offset:
            return node
    raise PolicyFormatError('operation node reference is unavailable')

@_name_boundary.callable_contract({'g': 'mosaic_g_6d96662', 'node': 'mosaic_node_91a22d4', 'parent_node': 'mosaic_parent_node_b102873', 'nodes_to_process': 'mosaic_nodes_to_process_a28e996'}, 'ong_mark_not')
@analysis_guard
def mosaic_ong_mark_not(mosaic_g_6d96662, mosaic_node_91a22d4, mosaic_parent_node_b102873, mosaic_nodes_to_process_a28e996):
    mosaic_g_6d96662[mosaic_node_91a22d4]['not'] = True
    mosaic_tmp_ac3c43a = _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['match']
    _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['match'] = _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['unmatch']
    _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['unmatch'] = mosaic_tmp_ac3c43a
    mosaic_tmp_offset_9475d83 = _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['match_offset']
    _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['match_offset'] = _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['unmatch_offset']
    _name_boundary.attributes(_name_boundary.attributes(mosaic_node_91a22d4)['non_terminal'])['unmatch_offset'] = mosaic_tmp_offset_9475d83

@_name_boundary.callable_contract({'g': 'mosaic_g_66189bd', 'node': 'mosaic_node_5031d6d', 'parent_node': 'mosaic_parent_node_60d704c', 'nodes_to_process': 'mosaic_nodes_to_process_ec20e4e'}, 'ong_end_path')
@analysis_guard
def mosaic_ong_end_path(mosaic_g_66189bd, mosaic_node_5031d6d, mosaic_parent_node_60d704c, mosaic_nodes_to_process_ec20e4e):
    mosaic_g_66189bd[mosaic_node_5031d6d]['decision'] = str(_name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_node_5031d6d)['non_terminal'])['match'])['terminal'])
    mosaic_g_66189bd[mosaic_node_5031d6d]['type'].add('final')

@_name_boundary.callable_contract({'g': 'mosaic_g_a23761e', 'node': 'mosaic_node_7201def', 'parent_node': 'mosaic_parent_node_f9eacff', 'nodes_to_process': 'mosaic_nodes_to_process_a43956e'}, 'ong_add_to_path')
@analysis_guard
def mosaic_ong_add_to_path(mosaic_g_a23761e, mosaic_node_7201def, mosaic_parent_node_f9eacff, mosaic_nodes_to_process_a43956e):
    if not mosaic_has_been_processed(_name_boundary.attributes(_name_boundary.attributes(mosaic_node_7201def)['non_terminal'])['match']):
        mosaic_g_a23761e[mosaic_node_7201def]['list'].add(_name_boundary.attributes(_name_boundary.attributes(mosaic_node_7201def)['non_terminal'])['match'])
        mosaic_nodes_to_process_a43956e.add((mosaic_node_7201def, _name_boundary.attributes(_name_boundary.attributes(mosaic_node_7201def)['non_terminal'])['match']))

@_name_boundary.callable_contract({'g': 'mosaic_g_e10b5c4', 'node': 'mosaic_node_8635f1a', 'parent_node': 'mosaic_parent_node_3438a17', 'nodes_to_process': 'mosaic_nodes_to_process_eafee85'}, 'ong_add_to_parent_path')
@analysis_guard
def mosaic_ong_add_to_parent_path(mosaic_g_e10b5c4, mosaic_node_8635f1a, mosaic_parent_node_3438a17, mosaic_nodes_to_process_eafee85):
    if not mosaic_has_been_processed(_name_boundary.attributes(_name_boundary.attributes(mosaic_node_8635f1a)['non_terminal'])['unmatch']):
        if mosaic_parent_node_3438a17:
            mosaic_g_e10b5c4[mosaic_parent_node_3438a17]['list'].add(_name_boundary.attributes(_name_boundary.attributes(mosaic_node_8635f1a)['non_terminal'])['unmatch'])
        mosaic_nodes_to_process_eafee85.add((mosaic_parent_node_3438a17, _name_boundary.attributes(_name_boundary.attributes(mosaic_node_8635f1a)['non_terminal'])['unmatch']))

@_name_boundary.callable_contract({'node': 'mosaic_node_ea867bb', 'default_node': 'mosaic_default_node_7f4d93d'}, 'build_operation_node_graph')
@analysis_guard
def mosaic_build_operation_node_graph(mosaic_node_ea867bb, mosaic_default_node_7f4d93d):
    if _name_boundary.attributes(mosaic_node_ea867bb)['is_terminal']():
        return None
    if mosaic_has_been_processed(mosaic_node_ea867bb):
        return None
    mosaic_g_6883141 = {}
    mosaic_nodes_to_process_7f0fef6 = set()
    mosaic_nodes_to_process_7f0fef6.add((None, mosaic_node_ea867bb))
    while mosaic_nodes_to_process_7f0fef6:
        analysis_step()
        mosaic_parent_node_1411aad, mosaic_current_node_c0d1d9c = mosaic_nodes_to_process_7f0fef6.pop()
        if mosaic_current_node_c0d1d9c not in mosaic_g_6883141:
            mosaic_g_6883141[mosaic_current_node_c0d1d9c] = {'list': set(), 'decision': None, 'type': {'normal'}, 'reduce': None, 'not': False}
        if not mosaic_parent_node_1411aad:
            mosaic_g_6883141[mosaic_current_node_c0d1d9c]['type'].add('start')
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_default_node_7f4d93d)['terminal'])['is_deny']():
            if _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_deny']():
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_allow']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_non_terminal']():
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_allow_non_terminal']():
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_deny_non_terminal']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_deny_allow']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_allow_deny']():
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
        elif _name_boundary.attributes(_name_boundary.attributes(mosaic_default_node_7f4d93d)['terminal'])['is_allow']():
            if _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_deny']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_allow']():
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_non_terminal_non_terminal']():
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_allow_non_terminal']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_deny_non_terminal']():
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_add_to_parent_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_deny_allow']():
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
            elif _name_boundary.attributes(_name_boundary.attributes(mosaic_current_node_c0d1d9c)['non_terminal'])['is_allow_deny']():
                mosaic_ong_mark_not(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
                mosaic_ong_end_path(mosaic_g_6883141, mosaic_current_node_c0d1d9c, mosaic_parent_node_1411aad, mosaic_nodes_to_process_7f0fef6)
        else:
            raise RuntimeError('terminal is neither deny or allow')
    mosaic_processed_nodes.append(mosaic_node_ea867bb)
    mosaic_print_operation_node_graph(mosaic_g_6883141)
    mosaic_g_6883141 = mosaic_clean_edges_in_operation_node_graph(mosaic_g_6883141)
    '\n    while True:\n        (g, more) = clean_nodes_in_operation_node_graph(g)\n        if more == False:\n            break\n    '
    assert mosaic_g_6883141
    mosaic_logger.debug('*** after cleaning nodes:')
    mosaic_print_operation_node_graph(mosaic_g_6883141)
    return mosaic_g_6883141

@_name_boundary.callable_contract({'g': 'mosaic_g_4d13cc3'}, 'print_operation_node_graph')
@analysis_guard
def mosaic_print_operation_node_graph(mosaic_g_4d13cc3):
    if not mosaic_g_4d13cc3:
        return
    mosaic_message_e3e15cf = ''
    for mosaic_node_iter_0664086 in mosaic_g_4d13cc3.keys():
        analysis_step()
        mosaic_message_e3e15cf = checked_add(mosaic_message_e3e15cf, '0x%x (%s) (%s) (decision: %s): [ ' % (_name_boundary.attributes(mosaic_node_iter_0664086)['offset'], str(mosaic_node_iter_0664086), mosaic_g_4d13cc3[mosaic_node_iter_0664086]['type'], mosaic_g_4d13cc3[mosaic_node_iter_0664086]['decision']))
        for mosaic_edge_69f75ce in mosaic_g_4d13cc3[mosaic_node_iter_0664086]['list']:
            analysis_step()
            mosaic_message_e3e15cf = checked_add(mosaic_message_e3e15cf, '0x%x (%s) ' % (_name_boundary.attributes(mosaic_edge_69f75ce)['offset'], str(mosaic_edge_69f75ce)))
        mosaic_message_e3e15cf = checked_add(mosaic_message_e3e15cf, ']\n')
    mosaic_logger.debug(mosaic_message_e3e15cf)

@_name_boundary.callable_contract({'g': 'mosaic_g_b24ee85', 'node_start': 'mosaic_node_start_af5032f', 'node_end': 'mosaic_node_end_1b4ef4f'}, 'remove_edge_in_operation_node_graph')
@analysis_guard
def mosaic_remove_edge_in_operation_node_graph(mosaic_g_b24ee85, mosaic_node_start_af5032f, mosaic_node_end_1b4ef4f):
    if mosaic_node_end_1b4ef4f in mosaic_g_b24ee85[mosaic_node_start_af5032f]['list']:
        mosaic_g_b24ee85[mosaic_node_start_af5032f]['list'].remove(mosaic_node_end_1b4ef4f)
    return mosaic_g_b24ee85

@_name_boundary.callable_contract({'g': 'mosaic_g_01e83bb', 'node_to_remove': 'mosaic_node_to_remove_1f7c29d'}, 'remove_node_in_operation_node_graph')
@analysis_guard
def mosaic_remove_node_in_operation_node_graph(mosaic_g_01e83bb, mosaic_node_to_remove_1f7c29d):
    for mosaic_n_910d1e2 in mosaic_g_01e83bb[mosaic_node_to_remove_1f7c29d]['list']:
        analysis_step()
        mosaic_g_01e83bb = mosaic_remove_edge_in_operation_node_graph(mosaic_g_01e83bb, mosaic_node_to_remove_1f7c29d, mosaic_n_910d1e2)
    mosaic_node_list_f2fccf2 = list(mosaic_g_01e83bb.keys())
    for mosaic_n_910d1e2 in mosaic_node_list_f2fccf2:
        analysis_step()
        if mosaic_node_to_remove_1f7c29d in mosaic_g_01e83bb[mosaic_n_910d1e2]['list']:
            mosaic_g_01e83bb = mosaic_remove_edge_in_operation_node_graph(mosaic_g_01e83bb, mosaic_n_910d1e2, mosaic_node_to_remove_1f7c29d)
    del mosaic_g_01e83bb[mosaic_node_to_remove_1f7c29d]
    return mosaic_g_01e83bb
mosaic_paths = []
mosaic_current_path = []

@_name_boundary.callable_contract({'g': 'mosaic_g_78b0e16', 'node': 'mosaic_node_ebb2b0b'}, '_get_operation_node_graph_paths')
@analysis_guard
def mosaic__get_operation_node_graph_paths(mosaic_g_78b0e16, mosaic_node_ebb2b0b):
    from policymosaic.reduction import operation_paths
    return operation_paths(mosaic_g_78b0e16, mosaic_node_ebb2b0b)

@_name_boundary.callable_contract({'g': 'mosaic_g_dafc29f', 'start_node': 'mosaic_start_node_a872404'}, 'get_operation_node_graph_paths')
@analysis_guard
def mosaic_get_operation_node_graph_paths(mosaic_g_dafc29f, mosaic_start_node_a872404):
    from policymosaic.reduction import operation_paths
    return operation_paths(mosaic_g_dafc29f, mosaic_start_node_a872404)
mosaic_nodes_traversed_for_removal = []

@_name_boundary.callable_contract({'g': 'mosaic_g_790f4a1', 'node': 'mosaic_node_fb0ae84', 'start_list': 'mosaic_start_list_58a4894'}, '_remove_duplicate_node_edges')
@analysis_guard
def mosaic__remove_duplicate_node_edges(mosaic_g_790f4a1, mosaic_node_fb0ae84, mosaic_start_list_58a4894):
    global mosaic_nodes_traversed_for_removal
    mosaic_nodes_traversed_for_removal.append(mosaic_node_fb0ae84)
    mosaic_nexts_f495b5a = list(mosaic_g_790f4a1[mosaic_node_fb0ae84]['list'])
    for mosaic_n_731bc8f in mosaic_nexts_f495b5a:
        analysis_step()
        if mosaic_n_731bc8f in mosaic_start_list_58a4894:
            mosaic_g_790f4a1 = mosaic_remove_edge_in_operation_node_graph(mosaic_g_790f4a1, mosaic_node_fb0ae84, mosaic_n_731bc8f)
        elif not mosaic_n_731bc8f in mosaic_nodes_traversed_for_removal:
            mosaic__remove_duplicate_node_edges(mosaic_g_790f4a1, mosaic_n_731bc8f, mosaic_start_list_58a4894)

@_name_boundary.callable_contract({'g': 'mosaic_g_2b2a1b5', 'start_list': 'mosaic_start_list_0e96498'}, 'remove_duplicate_node_edges')
@analysis_guard
def mosaic_remove_duplicate_node_edges(mosaic_g_2b2a1b5, mosaic_start_list_0e96498):
    for mosaic_n_ff4667c in mosaic_start_list_0e96498:
        analysis_step()
        mosaic_logger.debug(checked_add('removing from node: ', _name_boundary.attributes(mosaic_n_ff4667c)['str_debug']()))
        mosaic__remove_duplicate_node_edges(mosaic_g_2b2a1b5, mosaic_n_ff4667c, mosaic_start_list_0e96498)

@_name_boundary.callable_contract({'g': 'mosaic_g_56c1591'}, 'clean_edges_in_operation_node_graph')
@analysis_guard
def mosaic_clean_edges_in_operation_node_graph(mosaic_g_56c1591):
    """From the initial graph remove edges that are redundant.
    """
    global mosaic_nodes_traversed_for_removal
    mosaic_start_nodes_cf04b2b = []
    mosaic_final_nodes_4d0fd7c = []
    for mosaic_node_iter_cc4aa45 in mosaic_g_56c1591.keys():
        analysis_step()
        if 'start' in mosaic_g_56c1591[mosaic_node_iter_cc4aa45]['type']:
            mosaic_start_nodes_cf04b2b.append(mosaic_node_iter_cc4aa45)
        if 'final' in mosaic_g_56c1591[mosaic_node_iter_cc4aa45]['type']:
            mosaic_final_nodes_4d0fd7c.append(mosaic_node_iter_cc4aa45)
    for mosaic_snode_64958d8 in mosaic_start_nodes_cf04b2b:
        analysis_step()
        for mosaic_node_iter_cc4aa45 in mosaic_g_56c1591.keys():
            analysis_step()
            mosaic_g_56c1591 = mosaic_remove_edge_in_operation_node_graph(mosaic_g_56c1591, mosaic_node_iter_cc4aa45, mosaic_snode_64958d8)
    for mosaic_snode_64958d8 in mosaic_start_nodes_cf04b2b:
        analysis_step()
        mosaic_nodes_bag_fbb3502 = [mosaic_snode_64958d8]
        while True:
            analysis_step()
            mosaic_node_ce5fe64 = mosaic_nodes_bag_fbb3502.pop()
            mosaic_nodes_traversed_for_removal = []
            mosaic_logger.debug(checked_add('%%% going through ', _name_boundary.attributes(mosaic_node_ce5fe64)['str_debug']()))
            mosaic_remove_duplicate_node_edges(mosaic_g_56c1591, mosaic_g_56c1591[mosaic_node_ce5fe64]['list'])
            mosaic_nodes_bag_fbb3502.extend(mosaic_g_56c1591[mosaic_node_ce5fe64]['list'])
            if not mosaic_nodes_bag_fbb3502:
                break
    for mosaic_snode_64958d8 in mosaic_start_nodes_cf04b2b:
        analysis_step()
        mosaic_logger.debug(checked_add('traversing node ', str(mosaic_snode_64958d8)))
        mosaic_paths_bdf7fff = mosaic_get_operation_node_graph_paths(mosaic_g_56c1591, mosaic_snode_64958d8)
        mosaic_debug_message_2281b40 = checked_add(checked_add('for start node ', str(mosaic_snode_64958d8)), str(' paths are'))
        for mosaic_p_64237a2 in mosaic_paths_bdf7fff:
            analysis_step()
            mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, '[ ')
            for mosaic_n_ecdfb10 in mosaic_p_64237a2:
                analysis_step()
                mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, checked_add(_name_boundary.attributes(mosaic_n_ecdfb10)['str_debug'](), ' '))
            mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, ']\n')
        mosaic_logger.debug(mosaic_debug_message_2281b40)
        for mosaic_i_a4560c9 in range(0, len(mosaic_paths_bdf7fff)):
            analysis_step()
            for mosaic_j_21fb132 in range(checked_add(mosaic_i_a4560c9, 1), len(mosaic_paths_bdf7fff)):
                analysis_step()
                if len(mosaic_paths_bdf7fff[mosaic_i_a4560c9]) == len(mosaic_paths_bdf7fff[mosaic_j_21fb132]):
                    continue
                elif len(mosaic_paths_bdf7fff[mosaic_i_a4560c9]) < len(mosaic_paths_bdf7fff[mosaic_j_21fb132]):
                    mosaic_p_64237a2 = mosaic_paths_bdf7fff[mosaic_i_a4560c9]
                    mosaic_q_878cf9d = mosaic_paths_bdf7fff[mosaic_j_21fb132]
                else:
                    mosaic_p_64237a2 = mosaic_paths_bdf7fff[mosaic_j_21fb132]
                    mosaic_q_878cf9d = mosaic_paths_bdf7fff[mosaic_i_a4560c9]
                mosaic_debug_message_2281b40 = ''
                mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, 'short path: [')
                for mosaic_n_ecdfb10 in mosaic_p_64237a2:
                    analysis_step()
                    mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, str(mosaic_n_ecdfb10))
                mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, ']\n')
                mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, 'long path: [')
                for mosaic_n_ecdfb10 in mosaic_q_878cf9d:
                    analysis_step()
                    mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, str(mosaic_n_ecdfb10))
                mosaic_debug_message_2281b40 = checked_add(mosaic_debug_message_2281b40, ']')
                if mosaic_p_64237a2[len(mosaic_p_64237a2) - 1] == mosaic_q_878cf9d[len(mosaic_q_878cf9d) - 1]:
                    for mosaic_k_61baa57 in range(0, len(mosaic_p_64237a2)):
                        analysis_step()
                        if mosaic_p_64237a2[len(mosaic_p_64237a2) - 1 - mosaic_k_61baa57] == mosaic_q_878cf9d[len(mosaic_q_878cf9d) - 1 - mosaic_k_61baa57]:
                            continue
                        else:
                            mosaic_g_56c1591 = mosaic_remove_edge_in_operation_node_graph(mosaic_g_56c1591, mosaic_q_878cf9d[len(mosaic_q_878cf9d) - 1 - mosaic_k_61baa57], mosaic_q_878cf9d[len(mosaic_q_878cf9d) - mosaic_k_61baa57])
                            break
    return mosaic_g_56c1591

@_name_boundary.callable_contract({'g': 'mosaic_g_b1ffa41'}, 'clean_nodes_in_operation_node_graph')
@analysis_guard
def mosaic_clean_nodes_in_operation_node_graph(mosaic_g_b1ffa41):
    mosaic_made_change_5234b32 = False
    mosaic_node_list_42ba3e8 = list(mosaic_g_b1ffa41.keys())
    for mosaic_node_iter_bd0720d in mosaic_node_list_42ba3e8:
        analysis_step()
        if 'final' in mosaic_g_b1ffa41[mosaic_node_iter_bd0720d]['type']:
            continue
        if mosaic_g_b1ffa41[mosaic_node_iter_bd0720d]['list']:
            continue
        mosaic_logger.warn(checked_add('going to remove', str(mosaic_node_iter_bd0720d)))
        mosaic_made_change_5234b32 = True
        mosaic_g_b1ffa41 = mosaic_remove_node_in_operation_node_graph(mosaic_g_b1ffa41, mosaic_node_iter_bd0720d)
    return (mosaic_g_b1ffa41, mosaic_made_change_5234b32)
mosaic_replace_occurred = False

@_name_boundary.class_contract('ReducedVertice', {'TYPE_SINGLE': 'mosaic_TYPE_SINGLE', 'TYPE_START': 'mosaic_TYPE_START', 'TYPE_REQUIRE_ANY': 'mosaic_TYPE_REQUIRE_ANY', 'TYPE_REQUIRE_ALL': 'mosaic_TYPE_REQUIRE_ALL', 'TYPE_REQUIRE_ENTITLEMENT': 'mosaic_TYPE_REQUIRE_ENTITLEMENT', 'set_value': 'mosaic_set_value', 'set_type': 'mosaic_set_type', '_replace_in_list': 'mosaic__replace_in_list', 'replace_in_list': 'mosaic_replace_in_list', '_replace_sublist_in_list': 'mosaic__replace_sublist_in_list', 'replace_sublist_in_list': 'mosaic_replace_sublist_in_list', 'set_decision': 'mosaic_set_decision', 'set_type_single': 'mosaic_set_type_single', 'set_type_start': 'mosaic_set_type_start', 'set_type_require_entitlement': 'mosaic_set_type_require_entitlement', 'set_type_require_any': 'mosaic_set_type_require_any', 'set_type_require_all': 'mosaic_set_type_require_all', 'set_integrated_vertice': 'mosaic_set_integrated_vertice', 'is_type_single': 'mosaic_is_type_single', 'is_type_start': 'mosaic_is_type_start', 'is_type_require_entitlement': 'mosaic_is_type_require_entitlement', 'is_type_require_all': 'mosaic_is_type_require_all', 'is_type_require_any': 'mosaic_is_type_require_any', 'recursive_str': 'mosaic_recursive_str', 'recursive_str_debug': 'mosaic_recursive_str_debug', 'recursive_xml_str': 'mosaic_recursive_xml_str', 'str_debug': 'mosaic_str_debug', 'str_simple': 'mosaic_str_simple', 'str_print_debug': 'mosaic_str_print_debug', 'str_print': 'mosaic_str_print', 'str_print_not': 'mosaic_str_print_not', 'xml_str': 'mosaic_xml_str', 'type': 'mosaic_type', 'value': 'mosaic_value', 'decision': 'mosaic_decision', 'is_not': 'mosaic_is_not'})
class mosaic_ReducedVertice:
    mosaic_TYPE_SINGLE = 'single'
    mosaic_TYPE_START = 'start'
    mosaic_TYPE_REQUIRE_ANY = 'require-any'
    mosaic_TYPE_REQUIRE_ALL = 'require-all'
    mosaic_TYPE_REQUIRE_ENTITLEMENT = 'require-entitlement'

    @_name_boundary.callable_contract({'self': 'mosaic_self_9e929c1', 'type': 'mosaic_type_6e38ca6', 'value': 'mosaic_value_e75aea8', 'decision': 'mosaic_decision_21da1a4', 'is_not': 'mosaic_is_not_4c33d24'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_9e929c1, mosaic_type_6e38ca6=mosaic_TYPE_SINGLE, mosaic_value_e75aea8=None, mosaic_decision_21da1a4=None, mosaic_is_not_4c33d24=False):
        _name_boundary.attributes(mosaic_self_9e929c1)['type'] = mosaic_type_6e38ca6
        _name_boundary.attributes(mosaic_self_9e929c1)['value'] = mosaic_value_e75aea8
        _name_boundary.attributes(mosaic_self_9e929c1)['decision'] = mosaic_decision_21da1a4
        _name_boundary.attributes(mosaic_self_9e929c1)['is_not'] = mosaic_is_not_4c33d24

    @_name_boundary.callable_contract({'self': 'mosaic_self_706f19f', 'value': 'mosaic_value_6451fdc'}, 'set_value')
    @analysis_guard
    def mosaic_set_value(mosaic_self_706f19f, mosaic_value_6451fdc):
        _name_boundary.attributes(mosaic_self_706f19f)['value'] = mosaic_value_6451fdc

    @_name_boundary.callable_contract({'self': 'mosaic_self_1438621', 'type': 'mosaic_type_c7efbf0'}, 'set_type')
    @analysis_guard
    def mosaic_set_type(mosaic_self_1438621, mosaic_type_c7efbf0):
        _name_boundary.attributes(mosaic_self_1438621)['type'] = mosaic_type_c7efbf0

    @_name_boundary.callable_contract({'self': 'mosaic_self_85262ab', 'lst': 'mosaic_lst_cf0ebba', 'old': 'mosaic_old_9fea31e', 'new': 'mosaic_new_805febf'}, '_replace_in_list')
    @analysis_guard
    def mosaic__replace_in_list(mosaic_self_85262ab, mosaic_lst_cf0ebba, mosaic_old_9fea31e, mosaic_new_805febf):
        global mosaic_replace_occurred
        mosaic_tmp_list_ea4d792 = list(mosaic_lst_cf0ebba)
        for mosaic_i_7f97d18, mosaic_v_7879096 in enumerate(mosaic_tmp_list_ea4d792):
            analysis_step()
            if isinstance(_name_boundary.attributes(mosaic_v_7879096)['value'], list):
                _name_boundary.attributes(mosaic_self_85262ab)['_replace_in_list'](_name_boundary.attributes(mosaic_v_7879096)['value'], mosaic_old_9fea31e, mosaic_new_805febf)
            elif mosaic_v_7879096 == mosaic_old_9fea31e:
                mosaic_lst_cf0ebba[mosaic_i_7f97d18] = mosaic_new_805febf
                mosaic_replace_occurred = True
                return

    @_name_boundary.callable_contract({'self': 'mosaic_self_5d8264a', 'old': 'mosaic_old_a49b27d', 'new': 'mosaic_new_11af2a3'}, 'replace_in_list')
    @analysis_guard
    def mosaic_replace_in_list(mosaic_self_5d8264a, mosaic_old_a49b27d, mosaic_new_11af2a3):
        if isinstance(_name_boundary.attributes(mosaic_self_5d8264a)['value'], list):
            _name_boundary.attributes(mosaic_self_5d8264a)['_replace_in_list'](_name_boundary.attributes(mosaic_self_5d8264a)['value'], mosaic_old_a49b27d, mosaic_new_11af2a3)

    @_name_boundary.callable_contract({'self': 'mosaic_self_56878dd', 'lst': 'mosaic_lst_6c907a4', 'old': 'mosaic_old_d438910', 'new': 'mosaic_new_d86561d'}, '_replace_sublist_in_list')
    @analysis_guard
    def mosaic__replace_sublist_in_list(mosaic_self_56878dd, mosaic_lst_6c907a4, mosaic_old_d438910, mosaic_new_d86561d):
        global mosaic_replace_occurred
        mosaic_all_found_f2569f0 = True
        for mosaic_v_7dd05ac in mosaic_old_d438910:
            analysis_step()
            if mosaic_v_7dd05ac not in mosaic_lst_6c907a4:
                mosaic_all_found_f2569f0 = False
                break
        if mosaic_all_found_f2569f0:
            for mosaic_v_7dd05ac in mosaic_old_d438910:
                analysis_step()
                mosaic_lst_6c907a4.remove(mosaic_v_7dd05ac)
            mosaic_lst_6c907a4.append(mosaic_new_d86561d)
            mosaic_replace_occurred = True
            return
        for mosaic_i_f2181ed, mosaic_v_7dd05ac in enumerate(mosaic_lst_6c907a4):
            analysis_step()
            if isinstance(_name_boundary.attributes(mosaic_v_7dd05ac)['value'], list):
                _name_boundary.attributes(mosaic_self_56878dd)['_replace_sublist_in_list'](_name_boundary.attributes(mosaic_v_7dd05ac)['value'], mosaic_old_d438910, mosaic_new_d86561d)
            else:
                return

    @_name_boundary.callable_contract({'self': 'mosaic_self_a5c1a32', 'old': 'mosaic_old_ff78831', 'new': 'mosaic_new_26f5837'}, 'replace_sublist_in_list')
    @analysis_guard
    def mosaic_replace_sublist_in_list(mosaic_self_a5c1a32, mosaic_old_ff78831, mosaic_new_26f5837):
        if isinstance(_name_boundary.attributes(mosaic_self_a5c1a32)['value'], list):
            _name_boundary.attributes(mosaic_self_a5c1a32)['_replace_sublist_in_list'](_name_boundary.attributes(mosaic_self_a5c1a32)['value'], mosaic_old_ff78831, mosaic_new_26f5837)

    @_name_boundary.callable_contract({'self': 'mosaic_self_3a655d7', 'decision': 'mosaic_decision_8031877'}, 'set_decision')
    @analysis_guard
    def mosaic_set_decision(mosaic_self_3a655d7, mosaic_decision_8031877):
        _name_boundary.attributes(mosaic_self_3a655d7)['decision'] = mosaic_decision_8031877

    @_name_boundary.callable_contract({'self': 'mosaic_self_de32290'}, 'set_type_single')
    @analysis_guard
    def mosaic_set_type_single(mosaic_self_de32290):
        _name_boundary.attributes(mosaic_self_de32290)['type'] = _name_boundary.attributes(mosaic_self_de32290)['TYPE_SINGLE']

    @_name_boundary.callable_contract({'self': 'mosaic_self_5338bf1'}, 'set_type_start')
    @analysis_guard
    def mosaic_set_type_start(mosaic_self_5338bf1):
        _name_boundary.attributes(mosaic_self_5338bf1)['type'] = _name_boundary.attributes(mosaic_self_5338bf1)['TYPE_START']

    @_name_boundary.callable_contract({'self': 'mosaic_self_c0f4fea'}, 'set_type_require_entitlement')
    @analysis_guard
    def mosaic_set_type_require_entitlement(mosaic_self_c0f4fea):
        _name_boundary.attributes(mosaic_self_c0f4fea)['type'] = _name_boundary.attributes(mosaic_self_c0f4fea)['TYPE_REQUIRE_ENTITLEMENT']

    @_name_boundary.callable_contract({'self': 'mosaic_self_065feeb'}, 'set_type_require_any')
    @analysis_guard
    def mosaic_set_type_require_any(mosaic_self_065feeb):
        _name_boundary.attributes(mosaic_self_065feeb)['type'] = _name_boundary.attributes(mosaic_self_065feeb)['TYPE_REQUIRE_ANY']

    @_name_boundary.callable_contract({'self': 'mosaic_self_db86d77'}, 'set_type_require_all')
    @analysis_guard
    def mosaic_set_type_require_all(mosaic_self_db86d77):
        _name_boundary.attributes(mosaic_self_db86d77)['type'] = _name_boundary.attributes(mosaic_self_db86d77)['TYPE_REQUIRE_ALL']

    @_name_boundary.callable_contract({'self': 'mosaic_self_25493ed', 'integrated_vertice': 'mosaic_integrated_vertice_b664b85'}, 'set_integrated_vertice')
    @analysis_guard
    def mosaic_set_integrated_vertice(mosaic_self_25493ed, mosaic_integrated_vertice_b664b85):
        mosaic_n_5b1c263, mosaic_i_114ad40 = _name_boundary.attributes(mosaic_self_25493ed)['value']
        _name_boundary.attributes(mosaic_self_25493ed)['value'] = (mosaic_n_5b1c263, mosaic_integrated_vertice_b664b85)

    @_name_boundary.callable_contract({'self': 'mosaic_self_0650350'}, 'is_type_single')
    @analysis_guard
    def mosaic_is_type_single(mosaic_self_0650350):
        return _name_boundary.attributes(mosaic_self_0650350)['type'] == _name_boundary.attributes(mosaic_self_0650350)['TYPE_SINGLE']

    @_name_boundary.callable_contract({'self': 'mosaic_self_331d6e1'}, 'is_type_start')
    @analysis_guard
    def mosaic_is_type_start(mosaic_self_331d6e1):
        return _name_boundary.attributes(mosaic_self_331d6e1)['type'] == _name_boundary.attributes(mosaic_self_331d6e1)['TYPE_START']

    @_name_boundary.callable_contract({'self': 'mosaic_self_84bf412'}, 'is_type_require_entitlement')
    @analysis_guard
    def mosaic_is_type_require_entitlement(mosaic_self_84bf412):
        return _name_boundary.attributes(mosaic_self_84bf412)['type'] == _name_boundary.attributes(mosaic_self_84bf412)['TYPE_REQUIRE_ENTITLEMENT']

    @_name_boundary.callable_contract({'self': 'mosaic_self_15cc7fe'}, 'is_type_require_all')
    @analysis_guard
    def mosaic_is_type_require_all(mosaic_self_15cc7fe):
        return _name_boundary.attributes(mosaic_self_15cc7fe)['type'] == _name_boundary.attributes(mosaic_self_15cc7fe)['TYPE_REQUIRE_ALL']

    @_name_boundary.callable_contract({'self': 'mosaic_self_5067650'}, 'is_type_require_any')
    @analysis_guard
    def mosaic_is_type_require_any(mosaic_self_5067650):
        return _name_boundary.attributes(mosaic_self_5067650)['type'] == _name_boundary.attributes(mosaic_self_5067650)['TYPE_REQUIRE_ANY']

    @_name_boundary.callable_contract({'self': 'mosaic_self_10e268f', 'level': 'mosaic_level_03a8290', 'recursive_is_not': 'mosaic_recursive_is_not_9d5a683'}, 'recursive_str')
    @analysis_guard
    def mosaic_recursive_str(mosaic_self_10e268f, mosaic_level_03a8290, mosaic_recursive_is_not_9d5a683):
        mosaic_result_str_d5f5254 = ''
        if _name_boundary.attributes(mosaic_self_10e268f)['is_type_single']():
            if _name_boundary.attributes(mosaic_self_10e268f)['is_not'] and (not mosaic_recursive_is_not_9d5a683):
                mosaic_value_b7063b1 = str(_name_boundary.attributes(mosaic_self_10e268f)['value'])
                if '(require-any' in mosaic_value_b7063b1:
                    mosaic_result_str_d5f5254 = _name_boundary.attributes(_name_boundary.attributes(mosaic_self_10e268f)['value'])['str_not']()
                else:
                    mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add(checked_add('(require-not ', str(_name_boundary.attributes(mosaic_self_10e268f)['value'])), ')'))
            else:
                mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, str(_name_boundary.attributes(mosaic_self_10e268f)['value']))
        elif _name_boundary.attributes(mosaic_self_10e268f)['is_type_require_entitlement']():
            mosaic_ent_str_6bb4a35 = ''
            mosaic_n_c87fb92, mosaic_i_032c501 = _name_boundary.attributes(mosaic_self_10e268f)['value']
            if mosaic_i_032c501 == None:
                mosaic_ent_str_6bb4a35 = checked_add(mosaic_ent_str_6bb4a35, str(_name_boundary.attributes(mosaic_n_c87fb92)['value']))
            else:
                mosaic_ent_str_6bb4a35 = checked_add(mosaic_ent_str_6bb4a35, checked_add(str(_name_boundary.attributes(mosaic_n_c87fb92)['value'])[:-1], ' '))
                mosaic_ent_str_6bb4a35 = checked_add(mosaic_ent_str_6bb4a35, _name_boundary.attributes(mosaic_i_032c501)['recursive_str'](mosaic_level_03a8290, _name_boundary.attributes(mosaic_self_10e268f)['is_not']))
                mosaic_ent_str_6bb4a35 = checked_add(mosaic_ent_str_6bb4a35, ')')
            if _name_boundary.attributes(mosaic_self_10e268f)['is_not']:
                mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add(checked_add('(require-not ', mosaic_ent_str_6bb4a35), ')'))
            else:
                mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, mosaic_ent_str_6bb4a35)
        else:
            if mosaic_level_03a8290 == 1:
                mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add('\n', checked_multiply(13, ' ')))
            mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add('(', _name_boundary.attributes(mosaic_self_10e268f)['type']))
            mosaic_level_03a8290 = checked_add(mosaic_level_03a8290, 1)
            for mosaic_i_032c501, mosaic_v_69ab1a6 in enumerate(_name_boundary.attributes(mosaic_self_10e268f)['value']):
                analysis_step()
                if mosaic_i_032c501 == 0:
                    mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add(' ', _name_boundary.attributes(mosaic_v_69ab1a6)['recursive_str'](mosaic_level_03a8290, mosaic_recursive_is_not_9d5a683)))
                else:
                    mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, checked_add(checked_add('\n', checked_multiply(checked_multiply(13, mosaic_level_03a8290), ' ')), _name_boundary.attributes(mosaic_v_69ab1a6)['recursive_str'](mosaic_level_03a8290, mosaic_recursive_is_not_9d5a683)))
            mosaic_result_str_d5f5254 = checked_add(mosaic_result_str_d5f5254, ')')
        return mosaic_result_str_d5f5254

    @_name_boundary.callable_contract({'self': 'mosaic_self_c892829', 'level': 'mosaic_level_746c0a6', 'recursive_is_not': 'mosaic_recursive_is_not_c389eb5'}, 'recursive_str_debug')
    @analysis_guard
    def mosaic_recursive_str_debug(mosaic_self_c892829, mosaic_level_746c0a6, mosaic_recursive_is_not_c389eb5):
        mosaic_result_str_14240c5 = ''
        if _name_boundary.attributes(mosaic_self_c892829)['is_type_single']():
            if _name_boundary.attributes(mosaic_self_c892829)['is_not'] and (not mosaic_recursive_is_not_c389eb5):
                mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add(checked_add('(require-not ', _name_boundary.attributes(_name_boundary.attributes(mosaic_self_c892829)['value'])['str_debug']()), ')'))
            else:
                mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, _name_boundary.attributes(_name_boundary.attributes(mosaic_self_c892829)['value'])['str_debug']())
        elif _name_boundary.attributes(mosaic_self_c892829)['is_type_require_entitlement']():
            mosaic_ent_str_30fe4f4 = ''
            mosaic_n_c62100a, mosaic_i_b9573f3 = _name_boundary.attributes(mosaic_self_c892829)['value']
            if mosaic_i_b9573f3 == None:
                mosaic_ent_str_30fe4f4 = checked_add(mosaic_ent_str_30fe4f4, _name_boundary.attributes(_name_boundary.attributes(mosaic_n_c62100a)['value'])['str_debug']())
            else:
                mosaic_ent_str_30fe4f4 = checked_add(mosaic_ent_str_30fe4f4, checked_add(_name_boundary.attributes(_name_boundary.attributes(mosaic_n_c62100a)['value'])['str_debug']()[:-1], ' '))
                mosaic_ent_str_30fe4f4 = checked_add(mosaic_ent_str_30fe4f4, _name_boundary.attributes(mosaic_i_b9573f3)['recursive_str_debug'](mosaic_level_746c0a6, _name_boundary.attributes(mosaic_self_c892829)['is_not']))
                mosaic_ent_str_30fe4f4 = checked_add(mosaic_ent_str_30fe4f4, ')')
            if _name_boundary.attributes(mosaic_self_c892829)['is_not']:
                mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add(checked_add('(require-not ', mosaic_ent_str_30fe4f4), ')'))
            else:
                mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, mosaic_ent_str_30fe4f4)
        else:
            if mosaic_level_746c0a6 == 1:
                mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add('\n', checked_multiply(13, ' ')))
            mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add('(', _name_boundary.attributes(mosaic_self_c892829)['type']))
            mosaic_level_746c0a6 = checked_add(mosaic_level_746c0a6, 1)
            for mosaic_i_b9573f3, mosaic_v_8cec1cb in enumerate(_name_boundary.attributes(mosaic_self_c892829)['value']):
                analysis_step()
                if mosaic_i_b9573f3 == 0:
                    mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add(' ', _name_boundary.attributes(mosaic_v_8cec1cb)['recursive_str_debug'](mosaic_level_746c0a6, mosaic_recursive_is_not_c389eb5)))
                else:
                    mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, checked_add(checked_add('\n', checked_multiply(checked_multiply(13, mosaic_level_746c0a6), ' ')), _name_boundary.attributes(mosaic_v_8cec1cb)['recursive_str_debug'](mosaic_level_746c0a6, mosaic_recursive_is_not_c389eb5)))
            mosaic_result_str_14240c5 = checked_add(mosaic_result_str_14240c5, ')')
        return mosaic_result_str_14240c5

    @_name_boundary.callable_contract({'self': 'mosaic_self_255711e', 'level': 'mosaic_level_e4a17ab', 'recursive_is_not': 'mosaic_recursive_is_not_5b68de0'}, 'recursive_xml_str')
    @analysis_guard
    def mosaic_recursive_xml_str(mosaic_self_255711e, mosaic_level_e4a17ab, mosaic_recursive_is_not_5b68de0):
        mosaic_result_str_cfdaa4e = ''
        if _name_boundary.attributes(mosaic_self_255711e)['is_type_single']():
            if _name_boundary.attributes(mosaic_self_255711e)['is_not'] and (not mosaic_recursive_is_not_5b68de0):
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<require type="require-not">\n'))
                mosaic_name_b8ef87a, mosaic_argument_2083638 = _name_boundary.attributes(_name_boundary.attributes(mosaic_self_255711e)['value'])['values']()
                if mosaic_argument_2083638 == None:
                    mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(checked_add(checked_multiply(checked_add(mosaic_level_e4a17ab, 1), '\t'), '<filter name="'), str(mosaic_name_b8ef87a)), '" />\n'))
                else:
                    mosaic_arg_0601351 = str(mosaic_argument_2083638).replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                    mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(checked_add(checked_add(checked_add(checked_multiply(checked_add(mosaic_level_e4a17ab, 1), '\t'), '<filter name="'), str(mosaic_name_b8ef87a)), '" argument="'), mosaic_arg_0601351), '" />\n'))
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '</require>\n'))
            else:
                mosaic_name_b8ef87a, mosaic_argument_2083638 = _name_boundary.attributes(_name_boundary.attributes(mosaic_self_255711e)['value'])['values']()
                if mosaic_argument_2083638 == None:
                    mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<filter name="'), str(mosaic_name_b8ef87a)), '" />\n'))
                else:
                    mosaic_arg_0601351 = str(mosaic_argument_2083638).replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                    mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(checked_add(checked_add(checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<filter name="'), str(mosaic_name_b8ef87a)), '" argument="'), mosaic_arg_0601351), '" />\n'))
        elif _name_boundary.attributes(mosaic_self_255711e)['is_type_require_entitlement']():
            if _name_boundary.attributes(mosaic_self_255711e)['is_not']:
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<require type="require-not">\n'))
                mosaic_level_e4a17ab = checked_add(mosaic_level_e4a17ab, 1)
            mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<require type="require-entitlement"'))
            mosaic_n_d724496, mosaic_i_138c064 = _name_boundary.attributes(mosaic_self_255711e)['value']
            if mosaic_i_138c064 == None:
                mosaic__tmp_fe0861d = str(_name_boundary.attributes(mosaic_n_d724496)['value'])[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(' value="', mosaic__tmp_fe0861d), '" />\n'))
            else:
                mosaic__tmp_fe0861d = str(_name_boundary.attributes(mosaic_n_d724496)['value'])[21:-1].replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(' value="', mosaic__tmp_fe0861d), '">\n'))
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, _name_boundary.attributes(mosaic_i_138c064)['recursive_xml_str'](checked_add(mosaic_level_e4a17ab, 1), _name_boundary.attributes(mosaic_self_255711e)['is_not']))
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '</require>\n'))
            if _name_boundary.attributes(mosaic_self_255711e)['is_not']:
                mosaic_level_e4a17ab -= 1
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '</require>\n'))
        else:
            mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_add(checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '<require type="'), _name_boundary.attributes(mosaic_self_255711e)['type']), '">\n'))
            for mosaic_i_138c064, mosaic_v_b04ecc7 in enumerate(_name_boundary.attributes(mosaic_self_255711e)['value']):
                analysis_step()
                mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, _name_boundary.attributes(mosaic_v_b04ecc7)['recursive_xml_str'](checked_add(mosaic_level_e4a17ab, 1), mosaic_recursive_is_not_5b68de0))
            mosaic_result_str_cfdaa4e = checked_add(mosaic_result_str_cfdaa4e, checked_add(checked_multiply(mosaic_level_e4a17ab, '\t'), '</require>\n'))
        return mosaic_result_str_cfdaa4e

    @_name_boundary.callable_contract({'self': 'mosaic_self_462033b'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_462033b):
        return _name_boundary.attributes(mosaic_self_462033b)['recursive_str'](1, False)

    @_name_boundary.callable_contract({'self': 'mosaic_self_c9a7c60'}, 'str_debug')
    @analysis_guard
    def mosaic_str_debug(mosaic_self_c9a7c60):
        return _name_boundary.attributes(mosaic_self_c9a7c60)['recursive_str_debug'](1, False)

    @_name_boundary.callable_contract({'self': 'mosaic_self_3ecfdbb'}, 'str_simple')
    @analysis_guard
    def mosaic_str_simple(mosaic_self_3ecfdbb):
        if _name_boundary.attributes(mosaic_self_3ecfdbb)['is_type_single']():
            return _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3ecfdbb)['value'])['str_debug']()
        elif _name_boundary.attributes(mosaic_self_3ecfdbb)['is_type_require_any']():
            return 'require-any'
        elif _name_boundary.attributes(mosaic_self_3ecfdbb)['is_type_require_all']():
            return 'require-all'
        elif _name_boundary.attributes(mosaic_self_3ecfdbb)['is_type_require_entitlement']():
            return _name_boundary.attributes(_name_boundary.attributes(mosaic_self_3ecfdbb)['value'])['str_debug']()[1:-1]
        elif _name_boundary.attributes(mosaic_self_3ecfdbb)['is_type_start']():
            return 'start'
        else:
            return 'unknown-type'

    @_name_boundary.callable_contract({'self': 'mosaic_self_0b7c589'}, 'str_print_debug')
    @analysis_guard
    def mosaic_str_print_debug(mosaic_self_0b7c589):
        if _name_boundary.attributes(mosaic_self_0b7c589)['is_type_single']():
            return (_name_boundary.attributes(_name_boundary.attributes(mosaic_self_0b7c589)['value'])['str_debug'](), None)
        elif _name_boundary.attributes(mosaic_self_0b7c589)['is_type_require_any']():
            return ('(require-any', ')')
        elif _name_boundary.attributes(mosaic_self_0b7c589)['is_type_require_all']():
            return ('(require-all', ')')
        elif _name_boundary.attributes(mosaic_self_0b7c589)['is_type_require_entitlement']():
            return (_name_boundary.attributes(_name_boundary.attributes(mosaic_self_0b7c589)['value'])['str_debug']()[:-1], ')')
        elif _name_boundary.attributes(mosaic_self_0b7c589)['is_type_start']():
            return (None, None)
        else:
            return ('unknown-type', None)

    @_name_boundary.callable_contract({'self': 'mosaic_self_e16faf5'}, 'str_print')
    @analysis_guard
    def mosaic_str_print(mosaic_self_e16faf5):
        if _name_boundary.attributes(mosaic_self_e16faf5)['is_type_single']():
            return (str(_name_boundary.attributes(mosaic_self_e16faf5)['value']), None)
        elif _name_boundary.attributes(mosaic_self_e16faf5)['is_type_require_any']():
            return ('(require-any', ')')
        elif _name_boundary.attributes(mosaic_self_e16faf5)['is_type_require_all']():
            return ('(require-all', ')')
        elif _name_boundary.attributes(mosaic_self_e16faf5)['is_type_require_entitlement']():
            return (str(_name_boundary.attributes(mosaic_self_e16faf5)['value'])[:-1], ')')
        elif _name_boundary.attributes(mosaic_self_e16faf5)['is_type_start']():
            return (None, None)
        else:
            return ('unknown-type', None)

    @_name_boundary.callable_contract({'self': 'mosaic_self_d848501'}, 'str_print_not')
    @analysis_guard
    def mosaic_str_print_not(mosaic_self_d848501):
        mosaic_result_str_43873a2 = ''
        if _name_boundary.attributes(mosaic_self_d848501)['is_type_single']():
            if _name_boundary.attributes(mosaic_self_d848501)['is_not']:
                mosaic_value_9611ea0 = str(_name_boundary.attributes(mosaic_self_d848501)['value'])
                if '(require-any' in mosaic_value_9611ea0:
                    mosaic_result_str_43873a2 = _name_boundary.attributes(_name_boundary.attributes(mosaic_self_d848501)['value'])['str_not']()
                else:
                    mosaic_result_str_43873a2 = checked_add(mosaic_result_str_43873a2, checked_add(checked_add('(require-not ', str(_name_boundary.attributes(mosaic_self_d848501)['value'])), ')'))
        return mosaic_result_str_43873a2

    @_name_boundary.callable_contract({'self': 'mosaic_self_ea884f9'}, 'xml_str')
    @analysis_guard
    def mosaic_xml_str(mosaic_self_ea884f9):
        return _name_boundary.attributes(mosaic_self_ea884f9)['recursive_xml_str'](3, False)

@_name_boundary.class_contract('ReducedEdge', {'str_debug': 'mosaic_str_debug', 'str_simple': 'mosaic_str_simple', 'start': 'mosaic_start', 'end': 'mosaic_end'})
class mosaic_ReducedEdge:

    @_name_boundary.callable_contract({'self': 'mosaic_self_f0d8570', 'start': 'mosaic_start_e2a9523', 'end': 'mosaic_end_af099d9'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_f0d8570, mosaic_start_e2a9523=None, mosaic_end_af099d9=None):
        _name_boundary.attributes(mosaic_self_f0d8570)['start'] = mosaic_start_e2a9523
        _name_boundary.attributes(mosaic_self_f0d8570)['end'] = mosaic_end_af099d9

    @_name_boundary.callable_contract({'self': 'mosaic_self_abf16c8'}, 'str_debug')
    @analysis_guard
    def mosaic_str_debug(mosaic_self_abf16c8):
        return checked_add(checked_add(_name_boundary.attributes(_name_boundary.attributes(mosaic_self_abf16c8)['start'])['str_debug'](), ' -> '), _name_boundary.attributes(_name_boundary.attributes(mosaic_self_abf16c8)['end'])['str_debug']())

    @_name_boundary.callable_contract({'self': 'mosaic_self_58e4a3b'}, 'str_simple')
    @analysis_guard
    def mosaic_str_simple(mosaic_self_58e4a3b):
        return '%s -----> %s' % (_name_boundary.attributes(_name_boundary.attributes(mosaic_self_58e4a3b)['start'])['str_simple'](), _name_boundary.attributes(_name_boundary.attributes(mosaic_self_58e4a3b)['end'])['str_simple']())

    @_name_boundary.callable_contract({'self': 'mosaic_self_b17d358'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_b17d358):
        return checked_add(checked_add(str(_name_boundary.attributes(mosaic_self_b17d358)['start']), ' -> '), str(_name_boundary.attributes(mosaic_self_b17d358)['end']))

@_name_boundary.class_contract('ReducedGraph', {'add_vertice': 'mosaic_add_vertice', 'add_edge': 'mosaic_add_edge', 'add_edge_by_vertices': 'mosaic_add_edge_by_vertices', 'set_final_vertices': 'mosaic_set_final_vertices', 'contains_vertice': 'mosaic_contains_vertice', 'contains_edge': 'mosaic_contains_edge', 'contains_edge_by_vertices': 'mosaic_contains_edge_by_vertices', 'get_vertice_by_value': 'mosaic_get_vertice_by_value', 'get_edge_by_vertices': 'mosaic_get_edge_by_vertices', 'remove_vertice': 'mosaic_remove_vertice', 'remove_vertice_update_decision': 'mosaic_remove_vertice_update_decision', 'remove_edge': 'mosaic_remove_edge', 'remove_edge_by_vertices': 'mosaic_remove_edge_by_vertices', 'replace_vertice_in_edge_start': 'mosaic_replace_vertice_in_edge_start', 'replace_vertice_in_edge_end': 'mosaic_replace_vertice_in_edge_end', 'replace_vertice_in_single_vertices': 'mosaic_replace_vertice_in_single_vertices', 'replace_vertice_list': 'mosaic_replace_vertice_list', 'get_next_vertices': 'mosaic_get_next_vertices', 'get_prev_vertices': 'mosaic_get_prev_vertices', 'get_start_vertices': 'mosaic_get_start_vertices', 'get_end_vertices': 'mosaic_get_end_vertices', 'reduce_next_vertices': 'mosaic_reduce_next_vertices', 'reduce_prev_vertices': 'mosaic_reduce_prev_vertices', 'reduce_vertice_single_prev': 'mosaic_reduce_vertice_single_prev', 'reduce_vertice_single_next': 'mosaic_reduce_vertice_single_next', 'reduce_graph': 'mosaic_reduce_graph', 'reduce_graph_with_metanodes': 'mosaic_reduce_graph_with_metanodes', 'str_simple_with_metanodes': 'mosaic_str_simple_with_metanodes', 'str_simple': 'mosaic_str_simple', 'remove_builtin_filters': 'mosaic_remove_builtin_filters', 'reduce_integrated_vertices': 'mosaic_reduce_integrated_vertices', 'aggregate_require_entitlement': 'mosaic_aggregate_require_entitlement', 'aggregate_require_entitlement_nodes': 'mosaic_aggregate_require_entitlement_nodes', 'cleanup_filters': 'mosaic_cleanup_filters', 'remove_builtin_filters_with_metanodes': 'mosaic_remove_builtin_filters_with_metanodes', 'replace_require_entitlement_with_metanodes': 'mosaic_replace_require_entitlement_with_metanodes', 'aggregate_require_entitlement_with_metanodes': 'mosaic_aggregate_require_entitlement_with_metanodes', 'cleanup_filters_with_metanodes': 'mosaic_cleanup_filters_with_metanodes', 'print_vertices_with_operation': 'mosaic_print_vertices_with_operation', 'print_vertices_with_operation_metanodes': 'mosaic_print_vertices_with_operation_metanodes', 'dump_xml': 'mosaic_dump_xml', 'vertices': 'mosaic_vertices', 'edges': 'mosaic_edges', 'final_vertices': 'mosaic_final_vertices', 'reduce_changes_occurred': 'mosaic_reduce_changes_occurred'})
class mosaic_ReducedGraph:

    @_name_boundary.callable_contract({'self': 'mosaic_self_9c5d5e5'}, '__init__')
    @analysis_guard
    def __init__(mosaic_self_9c5d5e5):
        _name_boundary.attributes(mosaic_self_9c5d5e5)['vertices'] = []
        _name_boundary.attributes(mosaic_self_9c5d5e5)['edges'] = []
        _name_boundary.attributes(mosaic_self_9c5d5e5)['final_vertices'] = []
        _name_boundary.attributes(mosaic_self_9c5d5e5)['reduce_changes_occurred'] = False

    @_name_boundary.callable_contract({'self': 'mosaic_self_7fb2982', 'v': 'mosaic_v_cbfebff'}, 'add_vertice')
    @analysis_guard
    def mosaic_add_vertice(mosaic_self_7fb2982, mosaic_v_cbfebff):
        _name_boundary.attributes(mosaic_self_7fb2982)['vertices'].append(mosaic_v_cbfebff)

    @_name_boundary.callable_contract({'self': 'mosaic_self_4003a03', 'e': 'mosaic_e_0745c64'}, 'add_edge')
    @analysis_guard
    def mosaic_add_edge(mosaic_self_4003a03, mosaic_e_0745c64):
        _name_boundary.attributes(mosaic_self_4003a03)['edges'].append(mosaic_e_0745c64)

    @_name_boundary.callable_contract({'self': 'mosaic_self_fb2aad2', 'v_start': 'mosaic_v_start_ed24d52', 'v_end': 'mosaic_v_end_c8fcf58'}, 'add_edge_by_vertices')
    @analysis_guard
    def mosaic_add_edge_by_vertices(mosaic_self_fb2aad2, mosaic_v_start_ed24d52, mosaic_v_end_c8fcf58):
        mosaic_e_775127a = mosaic_ReducedEdge(mosaic_v_start_ed24d52, mosaic_v_end_c8fcf58)
        _name_boundary.attributes(mosaic_self_fb2aad2)['edges'].append(mosaic_e_775127a)

    @_name_boundary.callable_contract({'self': 'mosaic_self_2e6d827'}, 'set_final_vertices')
    @analysis_guard
    def mosaic_set_final_vertices(mosaic_self_2e6d827):
        _name_boundary.attributes(mosaic_self_2e6d827)['final_vertices'] = []
        for mosaic_v_db213d4 in _name_boundary.attributes(mosaic_self_2e6d827)['vertices']:
            analysis_step()
            mosaic_is_final_eb83909 = True
            for mosaic_e_e8f1fab in _name_boundary.attributes(mosaic_self_2e6d827)['edges']:
                analysis_step()
                if mosaic_v_db213d4 == _name_boundary.attributes(mosaic_e_e8f1fab)['start']:
                    mosaic_is_final_eb83909 = False
                    break
            if mosaic_is_final_eb83909:
                _name_boundary.attributes(mosaic_self_2e6d827)['final_vertices'].append(mosaic_v_db213d4)

    @_name_boundary.callable_contract({'self': 'mosaic_self_a4d489f', 'v': 'mosaic_v_79813af'}, 'contains_vertice')
    @analysis_guard
    def mosaic_contains_vertice(mosaic_self_a4d489f, mosaic_v_79813af):
        return mosaic_v_79813af in _name_boundary.attributes(mosaic_self_a4d489f)['vertices']

    @_name_boundary.callable_contract({'self': 'mosaic_self_a6daa23', 'e': 'mosaic_e_469f475'}, 'contains_edge')
    @analysis_guard
    def mosaic_contains_edge(mosaic_self_a6daa23, mosaic_e_469f475):
        return mosaic_e_469f475 in _name_boundary.attributes(mosaic_self_a6daa23)['edges']

    @_name_boundary.callable_contract({'self': 'mosaic_self_ee45aa0', 'v_start': 'mosaic_v_start_5cf43ff', 'v_end': 'mosaic_v_end_3ec1b35'}, 'contains_edge_by_vertices')
    @analysis_guard
    def mosaic_contains_edge_by_vertices(mosaic_self_ee45aa0, mosaic_v_start_5cf43ff, mosaic_v_end_3ec1b35):
        for mosaic_e_f4c7c19 in _name_boundary.attributes(mosaic_self_ee45aa0)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_f4c7c19)['start'] == mosaic_v_start_5cf43ff and _name_boundary.attributes(mosaic_e_f4c7c19)['end'] == mosaic_v_end_3ec1b35:
                return True
        return False

    @_name_boundary.callable_contract({'self': 'mosaic_self_9d433dd', 'value': 'mosaic_value_8e23998'}, 'get_vertice_by_value')
    @analysis_guard
    def mosaic_get_vertice_by_value(mosaic_self_9d433dd, mosaic_value_8e23998):
        for mosaic_v_8f232f2 in _name_boundary.attributes(mosaic_self_9d433dd)['vertices']:
            analysis_step()
            if _name_boundary.attributes(mosaic_v_8f232f2)['is_type_single']():
                if _name_boundary.attributes(mosaic_v_8f232f2)['value'] == mosaic_value_8e23998:
                    return mosaic_v_8f232f2

    @_name_boundary.callable_contract({'self': 'mosaic_self_7a7835d', 'v_start': 'mosaic_v_start_1734954', 'v_end': 'mosaic_v_end_d079f39'}, 'get_edge_by_vertices')
    @analysis_guard
    def mosaic_get_edge_by_vertices(mosaic_self_7a7835d, mosaic_v_start_1734954, mosaic_v_end_d079f39):
        for mosaic_e_6747963 in _name_boundary.attributes(mosaic_self_7a7835d)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_6747963)['start'] == mosaic_v_start_1734954 and _name_boundary.attributes(mosaic_e_6747963)['end'] == mosaic_v_end_d079f39:
                return mosaic_e_6747963
        return None

    @_name_boundary.callable_contract({'self': 'mosaic_self_a9ecc7e', 'v': 'mosaic_v_ef9a75a'}, 'remove_vertice')
    @analysis_guard
    def mosaic_remove_vertice(mosaic_self_a9ecc7e, mosaic_v_ef9a75a):
        mosaic_edges_copy_26a69d9 = list(_name_boundary.attributes(mosaic_self_a9ecc7e)['edges'])
        for mosaic_e_8b791ae in mosaic_edges_copy_26a69d9:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_8b791ae)['start'] == mosaic_v_ef9a75a or _name_boundary.attributes(mosaic_e_8b791ae)['end'] == mosaic_v_ef9a75a:
                _name_boundary.attributes(mosaic_self_a9ecc7e)['edges'].remove(mosaic_e_8b791ae)
        if mosaic_v_ef9a75a in _name_boundary.attributes(mosaic_self_a9ecc7e)['vertices']:
            _name_boundary.attributes(mosaic_self_a9ecc7e)['vertices'].remove(mosaic_v_ef9a75a)

    @_name_boundary.callable_contract({'self': 'mosaic_self_b615d08', 'v': 'mosaic_v_2bec625'}, 'remove_vertice_update_decision')
    @analysis_guard
    def mosaic_remove_vertice_update_decision(mosaic_self_b615d08, mosaic_v_2bec625):
        mosaic_edges_copy_4324022 = list(_name_boundary.attributes(mosaic_self_b615d08)['edges'])
        for mosaic_e_a5e3bcf in mosaic_edges_copy_4324022:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_a5e3bcf)['start'] == mosaic_v_2bec625:
                _name_boundary.attributes(mosaic_self_b615d08)['edges'].remove(mosaic_e_a5e3bcf)
            if _name_boundary.attributes(mosaic_e_a5e3bcf)['end'] == mosaic_v_2bec625:
                _name_boundary.attributes(_name_boundary.attributes(mosaic_e_a5e3bcf)['start'])['decision'] = _name_boundary.attributes(mosaic_v_2bec625)['decision']
                _name_boundary.attributes(mosaic_self_b615d08)['edges'].remove(mosaic_e_a5e3bcf)
        if mosaic_v_2bec625 in _name_boundary.attributes(mosaic_self_b615d08)['vertices']:
            _name_boundary.attributes(mosaic_self_b615d08)['vertices'].remove(mosaic_v_2bec625)

    @_name_boundary.callable_contract({'self': 'mosaic_self_d939ea5', 'e': 'mosaic_e_637fdb0'}, 'remove_edge')
    @analysis_guard
    def mosaic_remove_edge(mosaic_self_d939ea5, mosaic_e_637fdb0):
        if mosaic_e_637fdb0 in _name_boundary.attributes(mosaic_self_d939ea5)['edges']:
            _name_boundary.attributes(mosaic_self_d939ea5)['edges'].remove(mosaic_e_637fdb0)

    @_name_boundary.callable_contract({'self': 'mosaic_self_2dfae7e', 'v_start': 'mosaic_v_start_feb9f56', 'v_end': 'mosaic_v_end_9c59718'}, 'remove_edge_by_vertices')
    @analysis_guard
    def mosaic_remove_edge_by_vertices(mosaic_self_2dfae7e, mosaic_v_start_feb9f56, mosaic_v_end_9c59718):
        mosaic_e_b7bdebf = _name_boundary.attributes(mosaic_self_2dfae7e)['get_edge_by_vertices'](mosaic_v_start_feb9f56, mosaic_v_end_9c59718)
        if mosaic_e_b7bdebf:
            _name_boundary.attributes(mosaic_self_2dfae7e)['edges'].remove(mosaic_e_b7bdebf)

    @_name_boundary.callable_contract({'self': 'mosaic_self_257a232', 'old': 'mosaic_old_e4cad30', 'new': 'mosaic_new_eb75098'}, 'replace_vertice_in_edge_start')
    @analysis_guard
    def mosaic_replace_vertice_in_edge_start(mosaic_self_257a232, mosaic_old_e4cad30, mosaic_new_eb75098):
        global mosaic_replace_occurred
        for mosaic_e_281ba6c in _name_boundary.attributes(mosaic_self_257a232)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_281ba6c)['start'] == mosaic_old_e4cad30:
                _name_boundary.attributes(mosaic_e_281ba6c)['start'] = mosaic_new_eb75098
                mosaic_replace_occurred = True
            elif isinstance(_name_boundary.attributes(_name_boundary.attributes(mosaic_e_281ba6c)['start'])['value'], list):
                _name_boundary.attributes(_name_boundary.attributes(mosaic_e_281ba6c)['start'])['replace_in_list'](mosaic_old_e4cad30, mosaic_new_eb75098)
                if mosaic_replace_occurred:
                    _name_boundary.attributes(_name_boundary.attributes(mosaic_e_281ba6c)['start'])['decision'] = _name_boundary.attributes(mosaic_new_eb75098)['decision']

    @_name_boundary.callable_contract({'self': 'mosaic_self_bc30b07', 'old': 'mosaic_old_d8aab4c', 'new': 'mosaic_new_fde63ad'}, 'replace_vertice_in_edge_end')
    @analysis_guard
    def mosaic_replace_vertice_in_edge_end(mosaic_self_bc30b07, mosaic_old_d8aab4c, mosaic_new_fde63ad):
        global mosaic_replace_occurred
        for mosaic_e_7c910f3 in _name_boundary.attributes(mosaic_self_bc30b07)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_7c910f3)['end'] == mosaic_old_d8aab4c:
                _name_boundary.attributes(mosaic_e_7c910f3)['end'] = mosaic_new_fde63ad
                mosaic_replace_occurred = True
            elif isinstance(_name_boundary.attributes(_name_boundary.attributes(mosaic_e_7c910f3)['end'])['value'], list):
                _name_boundary.attributes(_name_boundary.attributes(mosaic_e_7c910f3)['end'])['replace_in_list'](mosaic_old_d8aab4c, mosaic_new_fde63ad)
                if mosaic_replace_occurred:
                    _name_boundary.attributes(_name_boundary.attributes(mosaic_e_7c910f3)['end'])['decision'] = _name_boundary.attributes(mosaic_new_fde63ad)['decision']

    @_name_boundary.callable_contract({'self': 'mosaic_self_bd3ee2d', 'old': 'mosaic_old_e7144ea', 'new': 'mosaic_new_3a4ef0b'}, 'replace_vertice_in_single_vertices')
    @analysis_guard
    def mosaic_replace_vertice_in_single_vertices(mosaic_self_bd3ee2d, mosaic_old_e7144ea, mosaic_new_3a4ef0b):
        for mosaic_v_1738a71 in _name_boundary.attributes(mosaic_self_bd3ee2d)['vertices']:
            analysis_step()
            if len(_name_boundary.attributes(mosaic_self_bd3ee2d)['get_next_vertices'](mosaic_v_1738a71)) == 0 and len(_name_boundary.attributes(mosaic_self_bd3ee2d)['get_prev_vertices'](mosaic_v_1738a71)) == 0:
                if isinstance(_name_boundary.attributes(mosaic_v_1738a71)['value'], list):
                    _name_boundary.attributes(mosaic_v_1738a71)['replace_in_list'](mosaic_old_e7144ea, mosaic_new_3a4ef0b)

    @_name_boundary.callable_contract({'self': 'mosaic_self_512749f', 'old': 'mosaic_old_b445f28', 'new': 'mosaic_new_794416f'}, 'replace_vertice_list')
    @analysis_guard
    def mosaic_replace_vertice_list(mosaic_self_512749f, mosaic_old_b445f28, mosaic_new_794416f):
        for mosaic_v_daeebcf in _name_boundary.attributes(mosaic_self_512749f)['vertices']:
            analysis_step()
            if isinstance(_name_boundary.attributes(mosaic_v_daeebcf)['value'], list):
                _name_boundary.attributes(mosaic_v_daeebcf)['replace_sublist_in_list'](mosaic_old_b445f28, mosaic_new_794416f)
            if set(_name_boundary.attributes(mosaic_self_512749f)['get_next_vertices'](mosaic_v_daeebcf)) == set(mosaic_old_b445f28):
                for mosaic_n_57f85a3 in mosaic_old_b445f28:
                    analysis_step()
                    _name_boundary.attributes(mosaic_self_512749f)['remove_edge_by_vertices'](mosaic_v_daeebcf, mosaic_n_57f85a3)
                _name_boundary.attributes(mosaic_self_512749f)['add_edge_by_vertices'](mosaic_v_daeebcf, mosaic_new_794416f)
            if set(_name_boundary.attributes(mosaic_self_512749f)['get_prev_vertices'](mosaic_v_daeebcf)) == set(mosaic_old_b445f28):
                for mosaic_n_57f85a3 in mosaic_old_b445f28:
                    analysis_step()
                    _name_boundary.attributes(mosaic_self_512749f)['remove_edge_by_vertices'](mosaic_n_57f85a3, mosaic_v_daeebcf)
                _name_boundary.attributes(mosaic_self_512749f)['add_edge_by_vertices'](mosaic_new_794416f, mosaic_v_daeebcf)

    @_name_boundary.callable_contract({'self': 'mosaic_self_a5f3f29', 'v': 'mosaic_v_803b44d'}, 'get_next_vertices')
    @analysis_guard
    def mosaic_get_next_vertices(mosaic_self_a5f3f29, mosaic_v_803b44d):
        mosaic_next_vertices_48d70b1 = []
        for mosaic_e_e322bda in _name_boundary.attributes(mosaic_self_a5f3f29)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_e322bda)['start'] == mosaic_v_803b44d:
                mosaic_next_vertices_48d70b1.append(_name_boundary.attributes(mosaic_e_e322bda)['end'])
        return mosaic_next_vertices_48d70b1

    @_name_boundary.callable_contract({'self': 'mosaic_self_a0e91af', 'v': 'mosaic_v_1e29035'}, 'get_prev_vertices')
    @analysis_guard
    def mosaic_get_prev_vertices(mosaic_self_a0e91af, mosaic_v_1e29035):
        mosaic_prev_vertices_1d3809b = []
        for mosaic_e_2bc625e in _name_boundary.attributes(mosaic_self_a0e91af)['edges']:
            analysis_step()
            if _name_boundary.attributes(mosaic_e_2bc625e)['end'] == mosaic_v_1e29035:
                mosaic_prev_vertices_1d3809b.append(_name_boundary.attributes(mosaic_e_2bc625e)['start'])
        return mosaic_prev_vertices_1d3809b

    @_name_boundary.callable_contract({'self': 'mosaic_self_92f3bef'}, 'get_start_vertices')
    @analysis_guard
    def mosaic_get_start_vertices(mosaic_self_92f3bef):
        mosaic_start_vertices_a177aa8 = []
        for mosaic_v_92c0991 in _name_boundary.attributes(mosaic_self_92f3bef)['vertices']:
            analysis_step()
            if not _name_boundary.attributes(mosaic_self_92f3bef)['get_prev_vertices'](mosaic_v_92c0991):
                mosaic_start_vertices_a177aa8.append(mosaic_v_92c0991)
        return mosaic_start_vertices_a177aa8

    @_name_boundary.callable_contract({'self': 'mosaic_self_2ed6927'}, 'get_end_vertices')
    @analysis_guard
    def mosaic_get_end_vertices(mosaic_self_2ed6927):
        mosaic_end_vertices_21e3add = []
        for mosaic_v_8e96200 in _name_boundary.attributes(mosaic_self_2ed6927)['vertices']:
            analysis_step()
            if not _name_boundary.attributes(mosaic_self_2ed6927)['get_next_vertices'](mosaic_v_8e96200):
                mosaic_end_vertices_21e3add.append(mosaic_v_8e96200)
        return mosaic_end_vertices_21e3add

    @_name_boundary.callable_contract({'self': 'mosaic_self_6c1bdf5', 'v': 'mosaic_v_8129509'}, 'reduce_next_vertices')
    @analysis_guard
    def mosaic_reduce_next_vertices(mosaic_self_6c1bdf5, mosaic_v_8129509):
        mosaic_next_vertices_238763f = _name_boundary.attributes(mosaic_self_6c1bdf5)['get_next_vertices'](mosaic_v_8129509)
        if len(mosaic_next_vertices_238763f) <= 1:
            return
        _name_boundary.attributes(mosaic_self_6c1bdf5)['reduce_changes_occurred'] = True
        mosaic_new_vertice_aeed5f0 = mosaic_ReducedVertice('require-any', mosaic_next_vertices_238763f, _name_boundary.attributes(mosaic_next_vertices_238763f[0])['decision'])
        mosaic_add_to_final_37b9fcf = False
        for mosaic_n_6ede8b6 in mosaic_next_vertices_238763f:
            analysis_step()
            _name_boundary.attributes(mosaic_self_6c1bdf5)['remove_edge_by_vertices'](mosaic_v_8129509, mosaic_n_6ede8b6)
        _name_boundary.attributes(mosaic_self_6c1bdf5)['replace_vertice_list'](mosaic_next_vertices_238763f, mosaic_new_vertice_aeed5f0)
        for mosaic_n_6ede8b6 in mosaic_next_vertices_238763f:
            analysis_step()
            if mosaic_n_6ede8b6 in _name_boundary.attributes(mosaic_self_6c1bdf5)['final_vertices']:
                _name_boundary.attributes(mosaic_self_6c1bdf5)['final_vertices'].remove(mosaic_n_6ede8b6)
                mosaic_add_to_final_37b9fcf = True
            if not _name_boundary.attributes(mosaic_self_6c1bdf5)['get_next_vertices'](mosaic_n_6ede8b6):
                if mosaic_n_6ede8b6 in _name_boundary.attributes(mosaic_self_6c1bdf5)['vertices']:
                    _name_boundary.attributes(mosaic_self_6c1bdf5)['vertices'].remove(mosaic_n_6ede8b6)
        _name_boundary.attributes(mosaic_self_6c1bdf5)['add_edge_by_vertices'](mosaic_v_8129509, mosaic_new_vertice_aeed5f0)
        _name_boundary.attributes(mosaic_self_6c1bdf5)['add_vertice'](mosaic_new_vertice_aeed5f0)
        if mosaic_add_to_final_37b9fcf:
            _name_boundary.attributes(mosaic_self_6c1bdf5)['final_vertices'].append(mosaic_new_vertice_aeed5f0)

    @_name_boundary.callable_contract({'self': 'mosaic_self_8e57c3e', 'v': 'mosaic_v_9a78d9c'}, 'reduce_prev_vertices')
    @analysis_guard
    def mosaic_reduce_prev_vertices(mosaic_self_8e57c3e, mosaic_v_9a78d9c):
        mosaic_prev_vertices_63cbf87 = _name_boundary.attributes(mosaic_self_8e57c3e)['get_prev_vertices'](mosaic_v_9a78d9c)
        if len(mosaic_prev_vertices_63cbf87) <= 1:
            return
        _name_boundary.attributes(mosaic_self_8e57c3e)['reduce_changes_occurred'] = True
        mosaic_new_vertice_bdb3801 = mosaic_ReducedVertice('require-any', mosaic_prev_vertices_63cbf87, _name_boundary.attributes(mosaic_v_9a78d9c)['decision'])
        for mosaic_p_4ee511d in mosaic_prev_vertices_63cbf87:
            analysis_step()
            _name_boundary.attributes(mosaic_self_8e57c3e)['remove_edge_by_vertices'](mosaic_p_4ee511d, mosaic_v_9a78d9c)
        _name_boundary.attributes(mosaic_self_8e57c3e)['replace_vertice_list'](mosaic_prev_vertices_63cbf87, mosaic_new_vertice_bdb3801)
        for mosaic_p_4ee511d in mosaic_prev_vertices_63cbf87:
            analysis_step()
            if not _name_boundary.attributes(mosaic_self_8e57c3e)['get_prev_vertices'](mosaic_p_4ee511d):
                if mosaic_p_4ee511d in _name_boundary.attributes(mosaic_self_8e57c3e)['vertices']:
                    _name_boundary.attributes(mosaic_self_8e57c3e)['vertices'].remove(mosaic_p_4ee511d)
        _name_boundary.attributes(mosaic_self_8e57c3e)['add_vertice'](mosaic_new_vertice_bdb3801)
        _name_boundary.attributes(mosaic_self_8e57c3e)['add_edge_by_vertices'](mosaic_new_vertice_bdb3801, mosaic_v_9a78d9c)

    @_name_boundary.callable_contract({'self': 'mosaic_self_c3c230f', 'v': 'mosaic_v_0ddf311'}, 'reduce_vertice_single_prev')
    @analysis_guard
    def mosaic_reduce_vertice_single_prev(mosaic_self_c3c230f, mosaic_v_0ddf311):
        graph, vertex = mosaic_self_c3c230f, mosaic_v_0ddf311
        previous = graph.get_prev_vertices(vertex)
        if len(previous) != 1: return False
        from policymosaic.reduction import contract_serial
        return contract_serial(graph, previous[0], vertex, mosaic_ReducedVertice, mosaic_ReducedEdge)

    @_name_boundary.callable_contract({'self': 'mosaic_self_ed0dc5b', 'v': 'mosaic_v_bb9d1ed'}, 'reduce_vertice_single_next')
    @analysis_guard
    def mosaic_reduce_vertice_single_next(mosaic_self_ed0dc5b, mosaic_v_bb9d1ed):
        graph, vertex = mosaic_self_ed0dc5b, mosaic_v_bb9d1ed
        following = graph.get_next_vertices(vertex)
        if len(following) != 1: return False
        from policymosaic.reduction import contract_serial
        return contract_serial(graph, vertex, following[0], mosaic_ReducedVertice, mosaic_ReducedEdge)

    @_name_boundary.callable_contract({'self': 'mosaic_self_826f91d'}, 'reduce_graph')
    @analysis_guard
    def mosaic_reduce_graph(mosaic_self_826f91d):
        from policymosaic.reduction import reduce_boolean_graph
        return reduce_boolean_graph(mosaic_self_826f91d, mosaic_ReducedVertice)

    @_name_boundary.callable_contract({'self': 'mosaic_self_f078202'}, 'reduce_graph_with_metanodes')
    @analysis_guard
    def mosaic_reduce_graph_with_metanodes(mosaic_self_f078202):
        mosaic_copy_vertices_477af60 = list(_name_boundary.attributes(mosaic_self_f078202)['vertices'])
        for mosaic_v_e20feae in mosaic_copy_vertices_477af60:
            analysis_step()
            mosaic_nlist_7226b40 = _name_boundary.attributes(mosaic_self_f078202)['get_next_vertices'](mosaic_v_e20feae)
            if len(mosaic_nlist_7226b40) >= 2:
                mosaic_new_node_fa4ac28 = mosaic_ReducedVertice('require-any', None, None)
                _name_boundary.attributes(mosaic_self_f078202)['add_vertice'](mosaic_new_node_fa4ac28)
                _name_boundary.attributes(mosaic_self_f078202)['add_edge_by_vertices'](mosaic_v_e20feae, mosaic_new_node_fa4ac28)
                for mosaic_n_dfed745 in mosaic_nlist_7226b40:
                    analysis_step()
                    _name_boundary.attributes(mosaic_self_f078202)['remove_edge_by_vertices'](mosaic_v_e20feae, mosaic_n_dfed745)
                    _name_boundary.attributes(mosaic_self_f078202)['add_edge_by_vertices'](mosaic_new_node_fa4ac28, mosaic_n_dfed745)
        mosaic_start_list_a464c32 = _name_boundary.attributes(mosaic_self_f078202)['get_start_vertices']()
        mosaic_new_node_fa4ac28 = mosaic_ReducedVertice('start', None, None)
        _name_boundary.attributes(mosaic_self_f078202)['add_vertice'](mosaic_new_node_fa4ac28)
        for mosaic_s_4fa7b7a in mosaic_start_list_a464c32:
            analysis_step()
            _name_boundary.attributes(mosaic_self_f078202)['add_edge_by_vertices'](mosaic_new_node_fa4ac28, mosaic_s_4fa7b7a)
        mosaic_copy_vertices_477af60 = list(_name_boundary.attributes(mosaic_self_f078202)['vertices'])
        for mosaic_v_e20feae in mosaic_copy_vertices_477af60:
            analysis_step()
            mosaic_prev_vertices_b3a8243 = list(_name_boundary.attributes(mosaic_self_f078202)['get_prev_vertices'](mosaic_v_e20feae))
            mosaic_next_vertices_93c17c9 = list(_name_boundary.attributes(mosaic_self_f078202)['get_next_vertices'](mosaic_v_e20feae))
            for mosaic_p_dcaf67f in mosaic_prev_vertices_b3a8243:
                analysis_step()
                if (_name_boundary.attributes(mosaic_p_dcaf67f)['is_type_require_any']() or _name_boundary.attributes(mosaic_p_dcaf67f)['is_type_start']()) and mosaic_next_vertices_93c17c9:
                    if _name_boundary.attributes(mosaic_v_e20feae)['is_type_require_entitlement']():
                        mosaic_has_next_nexts_b74ba25 = False
                        for mosaic_n_dfed745 in mosaic_next_vertices_93c17c9:
                            analysis_step()
                            if _name_boundary.attributes(mosaic_n_dfed745)['is_type_require_any']():
                                for mosaic_n2_e7b2bde in _name_boundary.attributes(mosaic_self_f078202)['get_next_vertices'](mosaic_n_dfed745):
                                    analysis_step()
                                    if _name_boundary.attributes(mosaic_self_f078202)['get_next_vertices'](mosaic_n2_e7b2bde):
                                        mosaic_has_next_nexts_b74ba25 = True
                                        break
                            elif _name_boundary.attributes(mosaic_self_f078202)['get_next_vertices'](mosaic_n_dfed745):
                                mosaic_has_next_nexts_b74ba25 = True
                                break
                        if not mosaic_has_next_nexts_b74ba25:
                            continue
                    mosaic_new_node_fa4ac28 = mosaic_ReducedVertice('require-all', None, None)
                    _name_boundary.attributes(mosaic_self_f078202)['add_vertice'](mosaic_new_node_fa4ac28)
                    _name_boundary.attributes(mosaic_self_f078202)['remove_edge_by_vertices'](mosaic_p_dcaf67f, mosaic_v_e20feae)
                    _name_boundary.attributes(mosaic_self_f078202)['add_edge_by_vertices'](mosaic_p_dcaf67f, mosaic_new_node_fa4ac28)
                    _name_boundary.attributes(mosaic_self_f078202)['add_edge_by_vertices'](mosaic_new_node_fa4ac28, mosaic_v_e20feae)

    @_name_boundary.callable_contract({'self': 'mosaic_self_1080122'}, 'str_simple_with_metanodes')
    @analysis_guard
    def mosaic_str_simple_with_metanodes(mosaic_self_1080122):
        mosaic_logger.debug('==== vertices:\n')
        for mosaic_v_dd14a35 in _name_boundary.attributes(mosaic_self_1080122)['vertices']:
            analysis_step()
            mosaic_logger.debug(_name_boundary.attributes(mosaic_v_dd14a35)['str_simple']())
        mosaic_logger.debug('==== edges:\n')
        for mosaic_e_f9bd870 in _name_boundary.attributes(mosaic_self_1080122)['edges']:
            analysis_step()
            mosaic_logger.debug(_name_boundary.attributes(mosaic_e_f9bd870)['str_simple']())

    @_name_boundary.callable_contract({'self': 'mosaic_self_acb5242'}, 'str_simple')
    @analysis_guard
    def mosaic_str_simple(mosaic_self_acb5242):
        mosaic_message_52361bd = '==== vertices:\n'
        for mosaic_v_fc8fef3 in _name_boundary.attributes(mosaic_self_acb5242)['vertices']:
            analysis_step()
            mosaic_message_52361bd = checked_add(mosaic_message_52361bd, checked_add(checked_add(checked_add(checked_add('decision: ', str(_name_boundary.attributes(mosaic_v_fc8fef3)['decision'])), '\t'), _name_boundary.attributes(mosaic_v_fc8fef3)['str_debug']()), '\n'))
        mosaic_message_52361bd = checked_add(mosaic_message_52361bd, '==== final vertices:\n')
        for mosaic_v_fc8fef3 in _name_boundary.attributes(mosaic_self_acb5242)['final_vertices']:
            analysis_step()
            mosaic_message_52361bd = checked_add(mosaic_message_52361bd, checked_add(checked_add(checked_add(checked_add('decision: ', str(_name_boundary.attributes(mosaic_v_fc8fef3)['decision'])), '\t'), _name_boundary.attributes(mosaic_v_fc8fef3)['str_debug']()), '\n'))
        mosaic_message_52361bd = checked_add(mosaic_message_52361bd, '==== edges:\n')
        for mosaic_e_d8d5113 in _name_boundary.attributes(mosaic_self_acb5242)['edges']:
            analysis_step()
            mosaic_message_52361bd = checked_add(mosaic_message_52361bd, checked_add(checked_add('\t', _name_boundary.attributes(mosaic_e_d8d5113)['str_debug']()), '\n'))
        return mosaic_message_52361bd

    @_name_boundary.callable_contract({'self': 'mosaic_self_2b1a830'}, '__str__')
    @analysis_guard
    def __str__(mosaic_self_2b1a830):
        mosaic_result_str_072252f = ''
        for mosaic_v_6b948a5 in _name_boundary.attributes(mosaic_self_2b1a830)['vertices']:
            analysis_step()
            mosaic_result_str_072252f = checked_add(mosaic_result_str_072252f, checked_add(checked_add('(', str(_name_boundary.attributes(mosaic_v_6b948a5)['decision'])), ' '))
            if len(_name_boundary.attributes(mosaic_self_2b1a830)['get_next_vertices'](mosaic_v_6b948a5)) == 0 and len(_name_boundary.attributes(mosaic_self_2b1a830)['get_next_vertices'](mosaic_v_6b948a5)) == 0:
                if mosaic_v_6b948a5 in _name_boundary.attributes(mosaic_self_2b1a830)['final_vertices']:
                    mosaic_result_str_072252f = checked_add(mosaic_result_str_072252f, checked_add(str(mosaic_v_6b948a5), '\n'))
            mosaic_result_str_072252f = checked_add(mosaic_result_str_072252f, ')\n')
        for mosaic_e_f22f1f7 in _name_boundary.attributes(mosaic_self_2b1a830)['edges']:
            analysis_step()
            mosaic_result_str_072252f = checked_add(mosaic_result_str_072252f, checked_add(str(mosaic_e_f22f1f7), '\n'))
        mosaic_result_str_072252f = checked_add(mosaic_result_str_072252f, '\n')
        return mosaic_result_str_072252f

    @_name_boundary.callable_contract({'self': 'mosaic_self_6f542cb'}, 'remove_builtin_filters')
    @analysis_guard
    def mosaic_remove_builtin_filters(mosaic_self_6f542cb):
        mosaic_copy_vertices_645ef22 = list(_name_boundary.attributes(mosaic_self_6f542cb)['vertices'])
        for mosaic_v_3d02086 in mosaic_copy_vertices_645ef22:
            analysis_step()
            if mosaic_re.search('###\\$\\$\\$\\*\\*\\*', str(mosaic_v_3d02086)):
                _name_boundary.attributes(mosaic_self_6f542cb)['remove_vertice_update_decision'](mosaic_v_3d02086)

    @_name_boundary.callable_contract({'self': 'mosaic_self_1b5bbb8', 'integrated_vertices': 'mosaic_integrated_vertices_b9ffc80'}, 'reduce_integrated_vertices')
    @analysis_guard
    def mosaic_reduce_integrated_vertices(mosaic_self_1b5bbb8, mosaic_integrated_vertices_b9ffc80):
        if len(mosaic_integrated_vertices_b9ffc80) == 0:
            return (None, None)
        if len(mosaic_integrated_vertices_b9ffc80) > 1:
            return (mosaic_ReducedVertice('require-any', mosaic_integrated_vertices_b9ffc80, _name_boundary.attributes(mosaic_integrated_vertices_b9ffc80[0])['decision']), _name_boundary.attributes(mosaic_integrated_vertices_b9ffc80[0])['decision'])
        mosaic_require_all_vertices_2833c93 = []
        mosaic_v_cf80d70 = mosaic_integrated_vertices_b9ffc80[0]
        mosaic_decision_4a69084 = None
        while True:
            analysis_step()
            if not mosaic_re.search('entitlement-value #t', str(mosaic_v_cf80d70)):
                mosaic_require_all_vertices_2833c93.append(mosaic_v_cf80d70)
            mosaic_next_vertices_c674302 = _name_boundary.attributes(mosaic_self_1b5bbb8)['get_next_vertices'](mosaic_v_cf80d70)
            if mosaic_decision_4a69084 == None and _name_boundary.attributes(mosaic_v_cf80d70)['decision'] != None:
                mosaic_decision_4a69084 = _name_boundary.attributes(mosaic_v_cf80d70)['decision']
            _name_boundary.attributes(mosaic_self_1b5bbb8)['remove_vertice'](mosaic_v_cf80d70)
            if mosaic_v_cf80d70 in _name_boundary.attributes(mosaic_self_1b5bbb8)['final_vertices']:
                _name_boundary.attributes(mosaic_self_1b5bbb8)['final_vertices'].remove(mosaic_v_cf80d70)
            if mosaic_next_vertices_c674302:
                mosaic_v_cf80d70 = mosaic_next_vertices_c674302[0]
            else:
                break
        if len(mosaic_require_all_vertices_2833c93) == 0:
            return (None, _name_boundary.attributes(mosaic_v_cf80d70)['decision'])
        if len(mosaic_require_all_vertices_2833c93) == 1:
            return (mosaic_ReducedVertice(value=_name_boundary.attributes(mosaic_require_all_vertices_2833c93[0])['value'], decision=_name_boundary.attributes(mosaic_require_all_vertices_2833c93[0])['decision'], is_not=_name_boundary.attributes(mosaic_require_all_vertices_2833c93[0])['is_not']), _name_boundary.attributes(mosaic_v_cf80d70)['decision'])
        return (mosaic_ReducedVertice('require-all', mosaic_require_all_vertices_2833c93, _name_boundary.attributes(mosaic_require_all_vertices_2833c93[len(mosaic_require_all_vertices_2833c93) - 1])['decision']), _name_boundary.attributes(mosaic_v_cf80d70)['decision'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_7afc40d', 'v': 'mosaic_v_cd8f70c'}, 'aggregate_require_entitlement')
    @analysis_guard
    def mosaic_aggregate_require_entitlement(mosaic_self_7afc40d, mosaic_v_cd8f70c):
        mosaic_next_vertices_9a6b51a = []
        mosaic_prev_vertices_8efbc75 = _name_boundary.attributes(mosaic_self_7afc40d)['get_prev_vertices'](mosaic_v_cd8f70c)
        mosaic_integrated_vertices_ecb8807 = []
        for mosaic_n_884478c in _name_boundary.attributes(mosaic_self_7afc40d)['get_next_vertices'](mosaic_v_cd8f70c):
            analysis_step()
            if not mosaic_re.search('entitlement-value', str(mosaic_n_884478c)):
                mosaic_next_vertices_9a6b51a.append(mosaic_n_884478c)
                break
            mosaic_integrated_vertices_ecb8807.append(mosaic_n_884478c)
            mosaic_current_list_6b34306 = [mosaic_n_884478c]
            while mosaic_current_list_6b34306:
                analysis_step()
                mosaic_current_80c0c2c = mosaic_current_list_6b34306.pop()
                for mosaic_n2_6315df7 in _name_boundary.attributes(mosaic_self_7afc40d)['get_next_vertices'](mosaic_current_80c0c2c):
                    analysis_step()
                    if not mosaic_re.search('entitlement-value', str(mosaic_n2_6315df7)):
                        _name_boundary.attributes(mosaic_self_7afc40d)['remove_edge_by_vertices'](mosaic_current_80c0c2c, mosaic_n2_6315df7)
                        mosaic_next_vertices_9a6b51a.append(mosaic_n2_6315df7)
                    else:
                        mosaic_current_list_6b34306.append(mosaic_n2_6315df7)
        mosaic_new_vertice_30a2034 = mosaic_ReducedVertice(type='require-entitlement', value=(mosaic_v_cd8f70c, None), decision=None, is_not=_name_boundary.attributes(mosaic_v_cd8f70c)['is_not'])
        for mosaic_p_6944b6d in mosaic_prev_vertices_8efbc75:
            analysis_step()
            _name_boundary.attributes(mosaic_self_7afc40d)['remove_edge_by_vertices'](mosaic_p_6944b6d, mosaic_v_cd8f70c)
            _name_boundary.attributes(mosaic_self_7afc40d)['add_edge_by_vertices'](mosaic_p_6944b6d, mosaic_new_vertice_30a2034)
        for mosaic_n_884478c in mosaic_next_vertices_9a6b51a:
            analysis_step()
            _name_boundary.attributes(mosaic_self_7afc40d)['remove_edge_by_vertices'](mosaic_v_cd8f70c, mosaic_n_884478c)
            _name_boundary.attributes(mosaic_self_7afc40d)['add_edge_by_vertices'](mosaic_new_vertice_30a2034, mosaic_n_884478c)
        for mosaic_i_a75ff99 in mosaic_integrated_vertices_ecb8807:
            analysis_step()
            _name_boundary.attributes(mosaic_self_7afc40d)['remove_edge_by_vertices'](mosaic_v_cd8f70c, mosaic_i_a75ff99)
        _name_boundary.attributes(mosaic_self_7afc40d)['remove_vertice'](mosaic_v_cd8f70c)
        _name_boundary.attributes(mosaic_self_7afc40d)['add_vertice'](mosaic_new_vertice_30a2034)
        if mosaic_v_cd8f70c in _name_boundary.attributes(mosaic_self_7afc40d)['final_vertices']:
            _name_boundary.attributes(mosaic_self_7afc40d)['final_vertices'].remove(mosaic_v_cd8f70c)
            _name_boundary.attributes(mosaic_self_7afc40d)['final_vertices'].append(mosaic_new_vertice_30a2034)
        mosaic_new_integrate_40f282f, mosaic_decision_c5d820a = _name_boundary.attributes(mosaic_self_7afc40d)['reduce_integrated_vertices'](mosaic_integrated_vertices_ecb8807)
        for mosaic_i_a75ff99 in mosaic_integrated_vertices_ecb8807:
            analysis_step()
            _name_boundary.attributes(mosaic_self_7afc40d)['remove_vertice'](mosaic_i_a75ff99)
            if mosaic_i_a75ff99 in _name_boundary.attributes(mosaic_self_7afc40d)['final_vertices']:
                _name_boundary.attributes(mosaic_self_7afc40d)['final_vertices'].remove(mosaic_i_a75ff99)
        _name_boundary.attributes(mosaic_new_vertice_30a2034)['set_integrated_vertice'](mosaic_new_integrate_40f282f)
        _name_boundary.attributes(mosaic_new_vertice_30a2034)['set_decision'](mosaic_decision_c5d820a)

    @_name_boundary.callable_contract({'self': 'mosaic_self_e9754b1'}, 'aggregate_require_entitlement_nodes')
    @analysis_guard
    def mosaic_aggregate_require_entitlement_nodes(mosaic_self_e9754b1):
        mosaic_copy_vertices_f0b70fd = list(_name_boundary.attributes(mosaic_self_e9754b1)['vertices'])
        mosaic_idx_1e7aac1 = 0
        while mosaic_idx_1e7aac1 < len(mosaic_copy_vertices_f0b70fd):
            analysis_step()
            mosaic_v_0196152 = mosaic_copy_vertices_f0b70fd[mosaic_idx_1e7aac1]
            if mosaic_re.search('require-entitlement', str(mosaic_v_0196152)):
                _name_boundary.attributes(mosaic_self_e9754b1)['aggregate_require_entitlement'](mosaic_v_0196152)
            mosaic_idx_1e7aac1 = checked_add(mosaic_idx_1e7aac1, 1)

    @_name_boundary.callable_contract({'self': 'mosaic_self_63d1725'}, 'cleanup_filters')
    @analysis_guard
    def mosaic_cleanup_filters(mosaic_self_63d1725):
        _name_boundary.attributes(mosaic_self_63d1725)['remove_builtin_filters']()
        _name_boundary.attributes(mosaic_self_63d1725)['aggregate_require_entitlement_nodes']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_93750e0'}, 'remove_builtin_filters_with_metanodes')
    @analysis_guard
    def mosaic_remove_builtin_filters_with_metanodes(mosaic_self_93750e0):
        mosaic_copy_vertices_566e7d8 = list(_name_boundary.attributes(mosaic_self_93750e0)['vertices'])
        for mosaic_v_feb8dbd in mosaic_copy_vertices_566e7d8:
            analysis_step()
            if mosaic_re.search('###\\$\\$\\$\\*\\*\\*', _name_boundary.attributes(mosaic_v_feb8dbd)['str_simple']()):
                _name_boundary.attributes(mosaic_self_93750e0)['remove_vertice'](mosaic_v_feb8dbd)
            elif mosaic_re.search('entitlement-value #t', _name_boundary.attributes(mosaic_v_feb8dbd)['str_simple']()):
                _name_boundary.attributes(mosaic_self_93750e0)['remove_vertice'](mosaic_v_feb8dbd)
            elif mosaic_re.search('entitlement-value-regex #"\\."', _name_boundary.attributes(mosaic_v_feb8dbd)['str_simple']()):
                _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_v_feb8dbd)['value'])['non_terminal'])['argument'] = '#".+"'
            elif mosaic_re.search('global-name-regex #"\\."', _name_boundary.attributes(mosaic_v_feb8dbd)['str_simple']()):
                _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_v_feb8dbd)['value'])['non_terminal'])['argument'] = '#".+"'
            elif mosaic_re.search('local-name-regex #"\\."', _name_boundary.attributes(mosaic_v_feb8dbd)['str_simple']()):
                _name_boundary.attributes(_name_boundary.attributes(_name_boundary.attributes(mosaic_v_feb8dbd)['value'])['non_terminal'])['argument'] = '#".+"'

    @_name_boundary.callable_contract({'self': 'mosaic_self_eeda12a', 'v': 'mosaic_v_ba0f759'}, 'replace_require_entitlement_with_metanodes')
    @analysis_guard
    def mosaic_replace_require_entitlement_with_metanodes(mosaic_self_eeda12a, mosaic_v_ba0f759):
        mosaic_prev_list_e9eb9c1 = _name_boundary.attributes(mosaic_self_eeda12a)['get_prev_vertices'](mosaic_v_ba0f759)
        mosaic_next_list_5a3297a = _name_boundary.attributes(mosaic_self_eeda12a)['get_next_vertices'](mosaic_v_ba0f759)
        mosaic_new_node_358351d = mosaic_ReducedVertice(type='require-entitlement', value=_name_boundary.attributes(mosaic_v_ba0f759)['value'], decision=None, is_not=_name_boundary.attributes(mosaic_v_ba0f759)['is_not'])
        _name_boundary.attributes(mosaic_self_eeda12a)['add_vertice'](mosaic_new_node_358351d)
        _name_boundary.attributes(mosaic_self_eeda12a)['remove_vertice'](mosaic_v_ba0f759)
        for mosaic_p_dbe2bb7 in mosaic_prev_list_e9eb9c1:
            analysis_step()
            _name_boundary.attributes(mosaic_self_eeda12a)['add_edge_by_vertices'](mosaic_p_dbe2bb7, mosaic_new_node_358351d)
        for mosaic_n_b5cfb69 in mosaic_next_list_5a3297a:
            analysis_step()
            _name_boundary.attributes(mosaic_self_eeda12a)['add_edge_by_vertices'](mosaic_new_node_358351d, mosaic_n_b5cfb69)

    @_name_boundary.callable_contract({'self': 'mosaic_self_380575c'}, 'aggregate_require_entitlement_with_metanodes')
    @analysis_guard
    def mosaic_aggregate_require_entitlement_with_metanodes(mosaic_self_380575c):
        mosaic_copy_vertices_3405f45 = list(_name_boundary.attributes(mosaic_self_380575c)['vertices'])
        for mosaic_v_852e6a0 in mosaic_copy_vertices_3405f45:
            analysis_step()
            if mosaic_re.search('require-entitlement', str(mosaic_v_852e6a0)):
                _name_boundary.attributes(mosaic_self_380575c)['replace_require_entitlement_with_metanodes'](mosaic_v_852e6a0)

    @_name_boundary.callable_contract({'self': 'mosaic_self_f6cbbab'}, 'cleanup_filters_with_metanodes')
    @analysis_guard
    def mosaic_cleanup_filters_with_metanodes(mosaic_self_f6cbbab):
        _name_boundary.attributes(mosaic_self_f6cbbab)['remove_builtin_filters_with_metanodes']()
        _name_boundary.attributes(mosaic_self_f6cbbab)['aggregate_require_entitlement_with_metanodes']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_624e0a7', 'operation': 'mosaic_operation_2ab9bce', 'out_f': 'mosaic_out_f_65b0809'}, 'print_vertices_with_operation')
    @analysis_guard
    def mosaic_print_vertices_with_operation(mosaic_self_624e0a7, mosaic_operation_2ab9bce, mosaic_out_f_65b0809):
        mosaic_allow_vertices_a7f692c = [mosaic_v_9d19ad0 for mosaic_v_9d19ad0 in _name_boundary.attributes(mosaic_self_624e0a7)['vertices'] if 'allow' in _name_boundary.attributes(mosaic_v_9d19ad0)['decision']]
        mosaic_deny_vertices_63cac0a = [mosaic_v_ba019f2 for mosaic_v_ba019f2 in _name_boundary.attributes(mosaic_self_624e0a7)['vertices'] if 'deny' in _name_boundary.attributes(mosaic_v_ba019f2)['decision']]
        if mosaic_allow_vertices_a7f692c:
            mosaic_out_f_65b0809.write('(allow %s ' % mosaic_operation_2ab9bce)
            if len(mosaic_allow_vertices_a7f692c) > 1:
                for mosaic_v_02aca1e in mosaic_allow_vertices_a7f692c:
                    analysis_step()
                    mosaic_out_f_65b0809.write(checked_add(checked_add('\n', checked_multiply(8, ' ')), str(mosaic_v_02aca1e)))
            else:
                mosaic_out_f_65b0809.write(str(mosaic_allow_vertices_a7f692c[0]))
            mosaic_out_f_65b0809.write(')\n')
        if mosaic_deny_vertices_63cac0a:
            mosaic_out_f_65b0809.write('(deny %s ' % mosaic_operation_2ab9bce)
            if len(mosaic_deny_vertices_63cac0a) > 1:
                for mosaic_v_02aca1e in mosaic_deny_vertices_63cac0a:
                    analysis_step()
                    mosaic_out_f_65b0809.write(checked_add(checked_add('\n', checked_multiply(8, ' ')), str(mosaic_v_02aca1e)))
            else:
                mosaic_out_f_65b0809.write(str(mosaic_deny_vertices_63cac0a[0]))
            mosaic_out_f_65b0809.write(')\n')

    @_name_boundary.callable_contract({'self': 'mosaic_self_7aefc99', 'operation': 'mosaic_operation_6bdd001', 'default_is_allow': 'mosaic_default_is_allow_b0ffe56', 'out_f': 'mosaic_out_f_8d18681'}, 'print_vertices_with_operation_metanodes')
    @analysis_guard
    def mosaic_print_vertices_with_operation_metanodes(mosaic_self_7aefc99, mosaic_operation_6bdd001, mosaic_default_is_allow_b0ffe56, mosaic_out_f_8d18681):
        if len(_name_boundary.attributes(mosaic_self_7aefc99)['vertices']) == 1 and _name_boundary.attributes(_name_boundary.attributes(mosaic_self_7aefc99)['vertices'][0])['is_type_start']():
            return
        if mosaic_default_is_allow_b0ffe56:
            mosaic_out_f_8d18681.write('(deny %s' % mosaic_operation_6bdd001)
        else:
            mosaic_out_f_8d18681.write('(allow %s' % mosaic_operation_6bdd001)
        mosaic_vlist_8ec319d = []
        mosaic_start_list_151dcc8 = _name_boundary.attributes(mosaic_self_7aefc99)['get_start_vertices']()
        mosaic_start_list_151dcc8.reverse()
        mosaic_vlist_8ec319d.insert(0, (None, 0))
        for mosaic_s_a743105 in mosaic_start_list_151dcc8:
            analysis_step()
            mosaic_vlist_8ec319d.insert(0, (mosaic_s_a743105, 1))
        while True:
            analysis_step()
            if not mosaic_vlist_8ec319d:
                break
            mosaic_cnode_f418c56, mosaic_indent_82ee94b = mosaic_vlist_8ec319d.pop(0)
            if not mosaic_cnode_f418c56:
                mosaic_out_f_8d18681.write(')')
                continue
            mosaic_first_5953809, mosaic_last_8c9db05 = _name_boundary.attributes(mosaic_cnode_f418c56)['str_print']()
            if mosaic_first_5953809:
                if _name_boundary.attributes(mosaic_cnode_f418c56)['is_not']:
                    if _name_boundary.attributes(mosaic_cnode_f418c56)['str_print_not']() != '':
                        mosaic_out_f_8d18681.write(checked_add(checked_add('\n', checked_multiply(mosaic_indent_82ee94b, '\t')), _name_boundary.attributes(mosaic_cnode_f418c56)['str_print_not']()))
                    else:
                        mosaic_out_f_8d18681.write(checked_add(checked_add(checked_add('\n', checked_multiply(mosaic_indent_82ee94b, '\t')), '(require-not '), mosaic_first_5953809))
                        if _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_any']() or _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_all']() or _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_entitlement']():
                            mosaic_vlist_8ec319d.insert(0, (None, mosaic_indent_82ee94b))
                        else:
                            mosaic_out_f_8d18681.write(')')
                else:
                    mosaic_out_f_8d18681.write(checked_add(checked_add('\n', checked_multiply(mosaic_indent_82ee94b, '\t')), mosaic_first_5953809))
            if mosaic_last_8c9db05:
                mosaic_vlist_8ec319d.insert(0, (None, mosaic_indent_82ee94b))
            mosaic_next_vertices_list_5199918 = _name_boundary.attributes(mosaic_self_7aefc99)['get_next_vertices'](mosaic_cnode_f418c56)
            if mosaic_next_vertices_list_5199918:
                if _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_any']() or _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_all']() or _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_entitlement']():
                    mosaic_indent_82ee94b = checked_add(mosaic_indent_82ee94b, 1)
                mosaic_next_vertices_list_5199918.reverse()
                if _name_boundary.attributes(mosaic_cnode_f418c56)['is_type_require_entitlement']():
                    mosaic_pos_cf86178 = 0
                    for mosaic_n_24b0503 in mosaic_next_vertices_list_5199918:
                        analysis_step()
                        if _name_boundary.attributes(mosaic_n_24b0503)['is_type_single']() and (not mosaic_re.search('entitlement-value', _name_boundary.attributes(mosaic_n_24b0503)['str_simple']())) or _name_boundary.attributes(mosaic_n_24b0503)['is_type_require_entitlement']():
                            mosaic_vlist_8ec319d.insert(checked_add(mosaic_pos_cf86178, 1), (mosaic_n_24b0503, mosaic_indent_82ee94b - 1))
                        else:
                            mosaic_vlist_8ec319d.insert(0, (mosaic_n_24b0503, mosaic_indent_82ee94b))
                            mosaic_pos_cf86178 = checked_add(mosaic_pos_cf86178, 1)
                else:
                    for mosaic_n_24b0503 in mosaic_next_vertices_list_5199918:
                        analysis_step()
                        mosaic_vlist_8ec319d.insert(0, (mosaic_n_24b0503, mosaic_indent_82ee94b))
        mosaic_out_f_8d18681.write('\n')

    @_name_boundary.callable_contract({'self': 'mosaic_self_f616f03', 'operation': 'mosaic_operation_544b9f2', 'out_f': 'mosaic_out_f_6299533'}, 'dump_xml')
    @analysis_guard
    def mosaic_dump_xml(mosaic_self_f616f03, mosaic_operation_544b9f2, mosaic_out_f_6299533):
        mosaic_allow_vertices_fba7e59 = [mosaic_v_d09cedc for mosaic_v_d09cedc in _name_boundary.attributes(mosaic_self_f616f03)['vertices'] if _name_boundary.attributes(mosaic_v_d09cedc)['decision'] == 'allow']
        mosaic_deny_vertices_390ad23 = [mosaic_v_db189e7 for mosaic_v_db189e7 in _name_boundary.attributes(mosaic_self_f616f03)['vertices'] if _name_boundary.attributes(mosaic_v_db189e7)['decision'] == 'deny']
        if mosaic_allow_vertices_fba7e59:
            mosaic_out_f_6299533.write('\t<operation name="%s" action="allow">\n' % mosaic_operation_544b9f2)
            mosaic_out_f_6299533.write('\t\t<filters>\n')
            for mosaic_v_4b6a92a in mosaic_allow_vertices_fba7e59:
                analysis_step()
                mosaic_out_f_6299533.write(_name_boundary.attributes(mosaic_v_4b6a92a)['xml_str']())
            mosaic_out_f_6299533.write('\t\t</filters>\n')
            mosaic_out_f_6299533.write('\t</operation>\n')
        if mosaic_deny_vertices_390ad23:
            mosaic_out_f_6299533.write('\t<operation name="%s" action="deny">\n' % mosaic_operation_544b9f2)
            mosaic_out_f_6299533.write('\t\t<filters>\n')
            for mosaic_v_4b6a92a in mosaic_deny_vertices_390ad23:
                analysis_step()
                mosaic_out_f_6299533.write(_name_boundary.attributes(mosaic_v_4b6a92a)['xml_str']())
            mosaic_out_f_6299533.write('\t\t</filters>\n')
            mosaic_out_f_6299533.write('\t</operation>\n')

@_name_boundary.callable_contract({'g': 'mosaic_g_d317962'}, 'reduce_operation_node_graph')
@analysis_guard
def mosaic_reduce_operation_node_graph(mosaic_g_d317962):
    mosaic_rg_6404a7f = mosaic_ReducedGraph()
    for mosaic_node_iter_6f3a53e in mosaic_g_d317962.keys():
        analysis_step()
        mosaic_rv_ce0f472 = mosaic_ReducedVertice(value=mosaic_node_iter_6f3a53e, decision=mosaic_g_d317962[mosaic_node_iter_6f3a53e]['decision'], is_not=mosaic_g_d317962[mosaic_node_iter_6f3a53e]['not'])
        _name_boundary.attributes(mosaic_rg_6404a7f)['add_vertice'](mosaic_rv_ce0f472)
    for mosaic_node_iter_6f3a53e in mosaic_g_d317962.keys():
        analysis_step()
        mosaic_rv_ce0f472 = _name_boundary.attributes(mosaic_rg_6404a7f)['get_vertice_by_value'](mosaic_node_iter_6f3a53e)
        for mosaic_node_next_209e120 in mosaic_g_d317962[mosaic_node_iter_6f3a53e]['list']:
            analysis_step()
            mosaic_rn_35364de = _name_boundary.attributes(mosaic_rg_6404a7f)['get_vertice_by_value'](mosaic_node_next_209e120)
            _name_boundary.attributes(mosaic_rg_6404a7f)['add_edge_by_vertices'](mosaic_rv_ce0f472, mosaic_rn_35364de)
    mosaic_l_7ba3e38 = len(mosaic_g_d317962.keys())
    for mosaic_idx_c3a99e8, mosaic_node_iter_6f3a53e in enumerate(mosaic_g_d317962.keys()):
        analysis_step()
        mosaic_rv_ce0f472 = _name_boundary.attributes(mosaic_rg_6404a7f)['get_vertice_by_value'](mosaic_node_iter_6f3a53e)
        if not mosaic_re.search('require-entitlement', str(mosaic_rv_ce0f472)):
            continue
        if not _name_boundary.attributes(mosaic_rv_ce0f472)['is_not']:
            continue
        mosaic_c_idx_3280481 = mosaic_idx_c3a99e8
        while True:
            analysis_step()
            mosaic_c_idx_3280481 = checked_add(mosaic_c_idx_3280481, 1)
            if mosaic_c_idx_3280481 >= mosaic_l_7ba3e38:
                break
            mosaic_rn_35364de = _name_boundary.attributes(mosaic_rg_6404a7f)['get_vertice_by_value'](list(mosaic_g_d317962)[mosaic_c_idx_3280481])
            if not mosaic_re.search('entitlement-value', str(mosaic_rn_35364de)):
                break
            mosaic_prevs_rv_bb83844 = _name_boundary.attributes(mosaic_rg_6404a7f)['get_prev_vertices'](mosaic_rv_ce0f472)
            mosaic_prevs_rn_4a70d25 = _name_boundary.attributes(mosaic_rg_6404a7f)['get_prev_vertices'](mosaic_rn_35364de)
            if set(mosaic_prevs_rv_bb83844) != set(mosaic_prevs_rn_4a70d25):
                continue
            for mosaic_pn_82b7ce7 in mosaic_prevs_rn_4a70d25:
                analysis_step()
                _name_boundary.attributes(mosaic_rg_6404a7f)['remove_edge_by_vertices'](mosaic_rn_35364de, mosaic_pn_82b7ce7)
            _name_boundary.attributes(mosaic_rg_6404a7f)['add_edge_by_vertices'](mosaic_rv_ce0f472, mosaic_rn_35364de)
    _name_boundary.attributes(mosaic_rg_6404a7f)['cleanup_filters_with_metanodes']()
    for mosaic_node_iter_6f3a53e in mosaic_g_d317962.keys():
        analysis_step()
        mosaic_rv_ce0f472 = _name_boundary.attributes(mosaic_rg_6404a7f)['get_vertice_by_value'](mosaic_node_iter_6f3a53e)
    _name_boundary.attributes(mosaic_rg_6404a7f)['reduce_graph_with_metanodes']()
    return mosaic_rg_6404a7f

@analysis_guard
def mosaic_main():
    from policymosaic.profile_decoder import mosaic_main as decoder_main
    return decoder_main()
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
_name_boundary.module_contract(globals(), {'build_operation_node_graph': 'mosaic_build_operation_node_graph', 'processed_nodes': 'mosaic_processed_nodes', '_get_operation_node_graph_paths': 'mosaic__get_operation_node_graph_paths', 'clean_nodes_in_operation_node_graph': 'mosaic_clean_nodes_in_operation_node_graph', 'replace_occurred': 'mosaic_replace_occurred', 'nodes_traversed_for_removal': 'mosaic_nodes_traversed_for_removal', 'remove_edge_in_operation_node_graph': 'mosaic_remove_edge_in_operation_node_graph', 'ong_mark_not': 'mosaic_ong_mark_not', 'get_filter_arg_string_by_offset_no_skip': 'mosaic_get_filter_arg_string_by_offset_no_skip', 'current_path': 'mosaic_current_path', 'find_operation_node_by_offset': 'mosaic_find_operation_node_by_offset', 'reduce_operation_node_graph': 'mosaic_reduce_operation_node_graph', 'num_regex': 'mosaic_num_regex', 'OperationNode': 'mosaic_OperationNode', 'Modifier': 'mosaic_Modifier', '_remove_duplicate_node_edges': 'mosaic__remove_duplicate_node_edges', 'ong_add_to_parent_path': 'mosaic_ong_add_to_parent_path', 'logging': 'mosaic_logging', 'clean_edges_in_operation_node_graph': 'mosaic_clean_edges_in_operation_node_graph', 'ong_end_path': 'mosaic_ong_end_path', 'ReducedGraph': 'mosaic_ReducedGraph', 'build_operation_nodes': 'mosaic_build_operation_nodes', 'paths': 'mosaic_paths', 'struct': 'mosaic_struct', 'logger': 'mosaic_logger', 'remove_duplicate_node_edges': 'mosaic_remove_duplicate_node_edges', 'has_been_processed': 'mosaic_has_been_processed', 'main': 'mosaic_main', 'NonTerminalNode': 'mosaic_NonTerminalNode', 'print_operation_node_graph': 'mosaic_print_operation_node_graph', 'ReducedVertice': 'mosaic_ReducedVertice', 'sys': 'mosaic_sys', 'build_operation_node': 'mosaic_build_operation_node', 'get_operation_node_graph_paths': 'mosaic_get_operation_node_graph_paths', 'sandbox_filter': 'mosaic_sandbox_filter', 'TerminalNode': 'mosaic_TerminalNode', 'remove_node_in_operation_node_graph': 'mosaic_remove_node_in_operation_node_graph', 'ReducedEdge': 'mosaic_ReducedEdge', 're': 'mosaic_re', 'json': 'mosaic_json', 'ong_add_to_path': 'mosaic_ong_add_to_path', 'InlineModifier': 'mosaic_InlineModifier'})
