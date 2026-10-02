#!/usr/bin/env python
# Derived from reverse-sandbox/reverse_sandbox.py; original copyright and license in ORIGIN.md and LICENSE.
"""
iOS/OS X sandbox decompiler

Heavily inspired from Dion Blazakis' previous work
    https://github.com/dionthegod/XNUSandbox/tree/master/sbdis
Excellent information from Stefan Essers' slides and work
    http://www.slideshare.net/i0n1c/ruxcon-2014-stefan-esser-ios8-containers-sandboxes-and-entitlements
    https://github.com/sektioneins/sandbox_toolkit
"""
import policymosaic_boundary as _name_boundary
import sys as mosaic_sys
import struct as mosaic_struct
import logging.config as _boundary_import_logging_config
import logging as mosaic_logging
import argparse as mosaic_argparse
import os as mosaic_os
import policymosaic.rule_graph as mosaic_operation_node
import policymosaic.filter_decoder as mosaic_sandbox_filter
import policymosaic.regex_graph as mosaic_sandbox_regex
import subprocess as mosaic_subprocess
from policymosaic.filter_catalog import mosaic_Filters as mosaic_Filters
import tqdm as mosaic_tqdm
mosaic_REGEX_TABLE_OFFSET = 2
mosaic_REGEX_COUNT_OFFSET = 4
mosaic_VARS_TABLE_OFFSET = 6
mosaic_VARS_COUNT_OFFSET = 8
mosaic_NUM_PROFILES_OFFSET = 10
mosaic_logging.config.fileConfig(_name_boundary.resource('logger.config'))
mosaic_logger = mosaic_logging.getLogger(__name__)
mosaic_ios16_5_struct = mosaic_struct.Struct('<HHBBBxHHH')
mosaic_PROFILE_OPS_OFFSET = 4
mosaic_OPERATION_NODE_SIZE = 8
mosaic_INDEX_SIZE = 2

@_name_boundary.class_contract('SandboxData', {'release': 'mosaic_release', 'data_file': 'mosaic_data_file', 'header_size': 'mosaic_header_size', 'type': 'mosaic_type', 'op_nodes_count': 'mosaic_op_nodes_count', 'sb_ops_count': 'mosaic_sb_ops_count', 'vars_count': 'mosaic_vars_count', 'states_count': 'mosaic_states_count', 'num_profiles': 'mosaic_num_profiles', 'regex_count': 'mosaic_regex_count', 'entitlements_count': 'mosaic_entitlements_count', 'regex_table_offset': 'mosaic_regex_table_offset', 'vars_offset': 'mosaic_vars_offset', 'states_offset': 'mosaic_states_offset', 'entitlements_offset': 'mosaic_entitlements_offset', 'profiles_offset': 'mosaic_profiles_offset', 'profiles_end_offset': 'mosaic_profiles_end_offset', 'operation_nodes_size': 'mosaic_operation_nodes_size', 'operation_nodes_offset': 'mosaic_operation_nodes_offset', 'base_addr': 'mosaic_base_addr', 'regex_list': 'mosaic_regex_list', 'global_vars': 'mosaic_global_vars', 'policies': 'mosaic_policies', 'sb_ops': 'mosaic_sb_ops', 'operation_nodes': 'mosaic_operation_nodes', 'ops_to_reverse': 'mosaic_ops_to_reverse'})
class mosaic_SandboxData:

    @_name_boundary.callable_contract({'self': 'mosaic_self_174ff17', 'release': 'mosaic_release_50be031', 'ios16_struct_size': 'mosaic_ios16_struct_size_c93e2a7', 'header': 'mosaic_header_166cef4', 'op_nodes_count': 'mosaic_op_nodes_count_1a88194', 'sb_ops_count': 'mosaic_sb_ops_count_6a8911c', 'vars_count': 'mosaic_vars_count_d1233c4', 'states_count': 'mosaic_states_count_0a418b2', 'num_profiles': 'mosaic_num_profiles_f6fb8c7', 'regex_count': 'mosaic_regex_count_e1cf1b2', 'entitlements_count': 'mosaic_entitlements_count_8bf3b45', 'instructions_count': 'mosaic_instructions_count_eb01c68'}, '__init__')
    def __init__(mosaic_self_174ff17, mosaic_release_50be031, mosaic_ios16_struct_size_c93e2a7, mosaic_header_166cef4, mosaic_op_nodes_count_1a88194, mosaic_sb_ops_count_6a8911c, mosaic_vars_count_d1233c4, mosaic_states_count_0a418b2, mosaic_num_profiles_f6fb8c7, mosaic_regex_count_e1cf1b2, mosaic_entitlements_count_8bf3b45, mosaic_instructions_count_eb01c68) -> None:
        _name_boundary.attributes(mosaic_self_174ff17)['release'] = mosaic_release_50be031
        _name_boundary.attributes(mosaic_self_174ff17)['data_file'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['header_size'] = mosaic_ios16_struct_size_c93e2a7
        _name_boundary.attributes(mosaic_self_174ff17)['type'] = mosaic_header_166cef4
        _name_boundary.attributes(mosaic_self_174ff17)['op_nodes_count'] = mosaic_op_nodes_count_1a88194
        _name_boundary.attributes(mosaic_self_174ff17)['sb_ops_count'] = mosaic_sb_ops_count_6a8911c
        _name_boundary.attributes(mosaic_self_174ff17)['vars_count'] = mosaic_vars_count_d1233c4
        _name_boundary.attributes(mosaic_self_174ff17)['states_count'] = mosaic_states_count_0a418b2
        _name_boundary.attributes(mosaic_self_174ff17)['num_profiles'] = mosaic_num_profiles_f6fb8c7
        _name_boundary.attributes(mosaic_self_174ff17)['regex_count'] = mosaic_regex_count_e1cf1b2
        _name_boundary.attributes(mosaic_self_174ff17)['entitlements_count'] = mosaic_entitlements_count_8bf3b45
        mosaic_header_addition_5e3b8b4 = 0
        if mosaic_release_50be031 > 17:
            mosaic_header_addition_5e3b8b4 = 2
        _name_boundary.attributes(mosaic_self_174ff17)['regex_table_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['header_size'] + mosaic_header_addition_5e3b8b4
        _name_boundary.attributes(mosaic_self_174ff17)['vars_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['regex_table_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['regex_count'] * mosaic_INDEX_SIZE
        mosaic_ent_size_2b2378f = mosaic_INDEX_SIZE
        _name_boundary.attributes(mosaic_self_174ff17)['states_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['vars_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['vars_count'] * mosaic_INDEX_SIZE
        _name_boundary.attributes(mosaic_self_174ff17)['entitlements_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['states_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['states_count'] * mosaic_INDEX_SIZE
        _name_boundary.attributes(mosaic_self_174ff17)['profiles_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['entitlements_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['entitlements_count'] * mosaic_INDEX_SIZE
        mosaic_profile_ops_offset_size_ae243cf = mosaic_PROFILE_OPS_OFFSET
        if mosaic_release_50be031 > 17:
            mosaic_profile_ops_offset_size_ae243cf = 8
        if mosaic_release_50be031 > 17:
            if mosaic_entitlements_count_8bf3b45 > 0:
                _name_boundary.attributes(mosaic_self_174ff17)['profiles_offset'] += 72
                if mosaic_release_50be031 > 18:
                    _name_boundary.attributes(mosaic_self_174ff17)['profiles_offset'] += 4
        _name_boundary.attributes(mosaic_self_174ff17)['profiles_end_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['profiles_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['num_profiles'] * (_name_boundary.attributes(mosaic_self_174ff17)['sb_ops_count'] * mosaic_INDEX_SIZE + mosaic_profile_ops_offset_size_ae243cf)
        _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_size'] = _name_boundary.attributes(mosaic_self_174ff17)['op_nodes_count'] * mosaic_OPERATION_NODE_SIZE
        _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_offset'] = _name_boundary.attributes(mosaic_self_174ff17)['profiles_end_offset']
        if not _name_boundary.attributes(mosaic_self_174ff17)['type']:
            _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_offset'] += _name_boundary.attributes(mosaic_self_174ff17)['sb_ops_count'] * mosaic_INDEX_SIZE
        mosaic_align_delta_8d7703e = _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_offset'] & 7
        if mosaic_align_delta_8d7703e != 0:
            _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_offset'] += 8 - mosaic_align_delta_8d7703e
        _name_boundary.attributes(mosaic_self_174ff17)['base_addr'] = _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_offset'] + _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes_size']
        _name_boundary.attributes(mosaic_self_174ff17)['regex_list'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['global_vars'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['policies'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['sb_ops'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['operation_nodes'] = None
        _name_boundary.attributes(mosaic_self_174ff17)['ops_to_reverse'] = None

    @_name_boundary.callable_contract({'self': 'mosaic_self_5b6c255'}, '__repr__')
    def __repr__(mosaic_self_5b6c255) -> str:
        return f"\n                struct_size: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['header_size'])}\n                header: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['type'])}\n                op_nodes_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['op_nodes_count'])}\n                sb_ops_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['sb_ops_count'])}\n                vars_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['vars_count'])}\n                states_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['states_count'])}\n                num_profiles: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['num_profiles'])}\n                re_table_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['regex_count'])}\n                entitlements_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['entitlements_count'])}\n\n                regex_table_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['regex_table_offset'])}\n                pattern_vars_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['vars_offset'])}\n                states_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['states_offset'])}\n                entitlements_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['entitlements_offset'])}\n                profiles_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['profiles_offset'])}\n                profiles_end_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['profiles_end_offset'])}\n                operation_nodes_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['operation_nodes_offset'])}\n                operation_nodes_size: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['operation_nodes_size'])}\n                base_adrr: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['base_addr'])}\n                "

@_name_boundary.callable_contract({'node': 'mosaic_node_e49dc7f'}, 'node_to_c')
def mosaic_node_to_c(mosaic_node_e49dc7f):
    mosaic_queue_b7d62bf = [mosaic_node_e49dc7f]
    mosaic_processed_f4dd59b = []
    mosaic_out_c57950d = ''
    while len(mosaic_queue_b7d62bf):
        mosaic_node_e49dc7f = mosaic_queue_b7d62bf[0]
        del mosaic_queue_b7d62bf[0]
        mosaic_out_c57950d += 'node_%x:; // %r\n' % (_name_boundary.attributes(mosaic_node_e49dc7f)['offset'], _name_boundary.attributes(mosaic_node_e49dc7f)['raw'])
        if _name_boundary.attributes(mosaic_node_e49dc7f)['terminal']:
            mosaic_out_c57950d += _name_boundary.attributes(mosaic_node_e49dc7f)['c_repr']() + '\n\n'
            continue
        mosaic_out_c57950d += 'if (%s) goto node_%x;\nelse goto node_%x;\n\n' % (_name_boundary.attributes(mosaic_node_e49dc7f)['c_repr'](), _name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['match_offset'], _name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['unmatch_offset'])
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['match'] not in mosaic_processed_f4dd59b:
            mosaic_processed_f4dd59b += [_name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['match']]
            mosaic_queue_b7d62bf += [_name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['match']]
        if _name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['unmatch'] not in mosaic_processed_f4dd59b:
            mosaic_processed_f4dd59b += [_name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['unmatch']]
            mosaic_queue_b7d62bf += [_name_boundary.attributes(_name_boundary.attributes(mosaic_node_e49dc7f)['non_terminal'])['unmatch']]
    return mosaic_out_c57950d.strip()

@_name_boundary.callable_contract({'infile': 'mosaic_infile_0b33000', 'args': 'mosaic_args_1262057'}, 'parse_profile')
def mosaic_parse_profile(mosaic_infile_0b33000, mosaic_args_1262057) -> mosaic_SandboxData:
    mosaic_infile_0b33000.seek(0)
    mosaic_header_e2aeb12, mosaic_op_nodes_count_5482b3b, mosaic_sb_ops_count_9438019, mosaic_vars_count_9f52a65, mosaic_states_count_17e0b1e, mosaic_num_profiles_787aa58, mosaic_re_count_8a16a09, mosaic_entitlements_count_242d87d, mosaic_instructions_count_b5b46dd = mosaic_struct.unpack('<HHBBBxHHHH', mosaic_infile_0b33000.read(16))
    mosaic_sandbox_data_26789d1 = None
    if int(_name_boundary.attributes(mosaic_args_1262057)['release']) == 17:
        mosaic_sandbox_data_26789d1 = mosaic_SandboxData(int(_name_boundary.attributes(mosaic_args_1262057)['release']), mosaic_ios16_5_struct.size, mosaic_header_e2aeb12, mosaic_op_nodes_count_5482b3b, mosaic_sb_ops_count_9438019, mosaic_vars_count_9f52a65, mosaic_states_count_17e0b1e, mosaic_num_profiles_787aa58, mosaic_re_count_8a16a09, mosaic_entitlements_count_242d87d, mosaic_instructions_count_b5b46dd)
    elif mosaic_header_e2aeb12 == 0:
        mosaic_sandbox_data_26789d1 = mosaic_SandboxData(int(_name_boundary.attributes(mosaic_args_1262057)['release']), mosaic_ios16_5_struct.size, mosaic_header_e2aeb12, mosaic_op_nodes_count_5482b3b, mosaic_sb_ops_count_9438019, mosaic_vars_count_9f52a65, mosaic_states_count_17e0b1e, mosaic_num_profiles_787aa58, mosaic_entitlements_count_242d87d, mosaic_re_count_8a16a09, mosaic_instructions_count_b5b46dd)
    elif mosaic_header_e2aeb12 == 32768:
        mosaic_sandbox_data_26789d1 = mosaic_SandboxData(int(_name_boundary.attributes(mosaic_args_1262057)['release']), mosaic_ios16_5_struct.size, mosaic_header_e2aeb12, mosaic_op_nodes_count_5482b3b, mosaic_sb_ops_count_9438019, mosaic_vars_count_9f52a65, mosaic_states_count_17e0b1e, mosaic_re_count_8a16a09, mosaic_entitlements_count_242d87d, mosaic_num_profiles_787aa58, mosaic_instructions_count_b5b46dd)
    else:
        print('ERRORRRR on header - unexpected value')
    _name_boundary.attributes(mosaic_sandbox_data_26789d1)['data_file'] = mosaic_infile_0b33000
    print(mosaic_sandbox_data_26789d1)
    return mosaic_sandbox_data_26789d1

@_name_boundary.callable_contract({'f': 'mosaic_f_226a377', 'offset': 'mosaic_offset_38950ea', 'base_addr': 'mosaic_base_addr_5665b89'}, 'extract_string_from_offset')
def mosaic_extract_string_from_offset(mosaic_f_226a377, mosaic_offset_38950ea, mosaic_base_addr_5665b89) -> str:
    """Extract string (literal) from given offset."""
    mosaic_f_226a377.seek(mosaic_offset_38950ea * 8 + mosaic_base_addr_5665b89)
    mosaic_len_159d22b = mosaic_struct.unpack('<H', mosaic_f_226a377.read(2))[0] - 1
    return '%s' % mosaic_f_226a377.read(mosaic_len_159d22b).decode('utf-8')

@_name_boundary.callable_contract({'infile': 'mosaic_infile_5730584', 'sandbox_data': 'mosaic_sandbox_data_8b8efce', 'keep_builtin_filters': 'mosaic_keep_builtin_filters_bbfe5f6'}, 'create_operation_nodes')
def mosaic_create_operation_nodes(mosaic_infile_5730584, mosaic_sandbox_data_8b8efce, mosaic_keep_builtin_filters_bbfe5f6):
    _name_boundary.attributes(mosaic_sandbox_data_8b8efce)['operation_nodes'] = mosaic_operation_node.build_operation_nodes(mosaic_infile_5730584, _name_boundary.attributes(mosaic_sandbox_data_8b8efce)['op_nodes_count'])
    mosaic_logger.info('operation nodes')
    for mosaic_op_node_8d2f2f9 in _name_boundary.attributes(mosaic_sandbox_data_8b8efce)['operation_nodes']:
        _name_boundary.attributes(mosaic_op_node_8d2f2f9)['convert_filter'](mosaic_sandbox_filter.convert_filter_callback, mosaic_infile_5730584, mosaic_sandbox_data_8b8efce, mosaic_keep_builtin_filters_bbfe5f6)
    mosaic_logger.info('operation nodes after filter conversion')
    return _name_boundary.attributes(mosaic_sandbox_data_8b8efce)['operation_nodes']

@_name_boundary.callable_contract({'infile': 'mosaic_infile_0059b31', 'outfname': 'mosaic_outfname_123de25', 'sb_ops': 'mosaic_sb_ops_020ff58', 'ops_to_reverse': 'mosaic_ops_to_reverse_6b201b1', 'op_table': 'mosaic_op_table_0b35d75', 'operation_nodes': 'mosaic_operation_nodes_5cec516', 'c_output': 'mosaic_c_output_8f3a98f', 'macho': 'mosaic_macho_f8e8976'}, 'process_profile')
def mosaic_process_profile(mosaic_infile_0059b31, mosaic_outfname_123de25, mosaic_sb_ops_020ff58, mosaic_ops_to_reverse_6b201b1, mosaic_op_table_0b35d75, mosaic_operation_nodes_5cec516, mosaic_c_output_8f3a98f, mosaic_macho_f8e8976):
    if mosaic_macho_f8e8976:
        mosaic_c_output_8f3a98f = True
    if mosaic_c_output_8f3a98f:
        mosaic_outfile_31dab17 = open(mosaic_outfname_123de25.strip() + '.c', 'wt')
    else:
        mosaic_out_fname_d1daa47 = mosaic_os.path.join(mosaic_outfname_123de25.strip() + '.sb')
        mosaic_outfile_31dab17 = open(mosaic_out_fname_d1daa47, 'wt')
    mosaic_default_node_27d83c2 = mosaic_operation_node.find_operation_node_by_offset(mosaic_operation_nodes_5cec516, mosaic_op_table_0b35d75[0])
    if not _name_boundary.attributes(mosaic_default_node_27d83c2)['terminal']:
        return
    if mosaic_c_output_8f3a98f:
        mosaic_outfile_31dab17.write('extern long allow(const char *);\n')
        mosaic_outfile_31dab17.write('extern long deny(const char *);\n')
        mosaic_outfile_31dab17.write('extern long unparsed_filter();\n')
        mosaic_outfile_31dab17.write('extern long subpath();\n')
        mosaic_outfile_31dab17.write('extern long subpath_prefix();\n')
        for mosaic_f_4ea0fc1 in _name_boundary.attributes(_name_boundary.attributes(mosaic_Filters)['filters'])['values']():
            mosaic_name_dede835 = mosaic_f_4ea0fc1['name']
            if mosaic_name_dede835 == '':
                mosaic_name_dede835 = 'literal'
            for mosaic_suffix_2c9e92b in ['', '_regex', '_literal', '_prefix']:
                mosaic_outfile_31dab17.write('extern long %s%s();\n' % (mosaic_name_dede835.replace('-', '_'), mosaic_suffix_2c9e92b))
    else:
        mosaic_outfile_31dab17.write('(version 1)\n')
        mosaic_outfile_31dab17.write('(%s default)\n' % _name_boundary.attributes(mosaic_default_node_27d83c2)['terminal'])
    for mosaic_idx_0a479bb in range(1, len(mosaic_op_table_0b35d75)):
        mosaic_offset_644dbc2 = mosaic_op_table_0b35d75[mosaic_idx_0a479bb]
        mosaic_operation_123dfb1 = mosaic_sb_ops_020ff58[mosaic_idx_0a479bb]
        if mosaic_ops_to_reverse_6b201b1:
            if mosaic_operation_123dfb1 not in mosaic_ops_to_reverse_6b201b1:
                continue
        mosaic_node_88247ce = mosaic_operation_node.find_operation_node_by_offset(mosaic_operation_nodes_5cec516, mosaic_offset_644dbc2)
        if not mosaic_node_88247ce:
            continue
        if mosaic_c_output_8f3a98f:
            mosaic_outfile_31dab17.write('long %s()\n{\n' % (mosaic_operation_123dfb1.replace('-', '_').replace('*', '$'),))
            mosaic_outfile_31dab17.write(mosaic_node_to_c(mosaic_node_88247ce))
            mosaic_outfile_31dab17.write('\n}\n\n')
            continue
        mosaic_g_b278214 = mosaic_operation_node.build_operation_node_graph(mosaic_node_88247ce, mosaic_default_node_27d83c2)
        if mosaic_g_b278214:
            mosaic_rg_b662a8d = mosaic_operation_node.reduce_operation_node_graph(mosaic_g_b278214)
            _name_boundary.attributes(mosaic_rg_b662a8d)['str_simple_with_metanodes']()
            _name_boundary.attributes(mosaic_rg_b662a8d)['print_vertices_with_operation_metanodes'](mosaic_operation_123dfb1, _name_boundary.attributes(_name_boundary.attributes(mosaic_default_node_27d83c2)['terminal'])['is_allow'](), mosaic_outfile_31dab17)
        elif _name_boundary.attributes(mosaic_node_88247ce)['terminal']:
            if _name_boundary.attributes(_name_boundary.attributes(mosaic_node_88247ce)['terminal'])['type'] != _name_boundary.attributes(_name_boundary.attributes(mosaic_default_node_27d83c2)['terminal'])['type']:
                mosaic_outfile_31dab17.write('(%s %s)\n' % (_name_boundary.attributes(mosaic_node_88247ce)['terminal'], mosaic_operation_123dfb1))
            else:
                mosaic_modifiers_type_fdf8b89 = [mosaic_key_d00661d for mosaic_key_d00661d, mosaic_val_e2131fc in _name_boundary.attributes(_name_boundary.attributes(mosaic_node_88247ce)['terminal'])['db_modifiers'].items() if len(mosaic_val_e2131fc)]
                if mosaic_modifiers_type_fdf8b89:
                    mosaic_outfile_31dab17.write('(%s %s)\n' % (_name_boundary.attributes(mosaic_node_88247ce)['terminal'], mosaic_operation_123dfb1))
    mosaic_outfile_31dab17.close()
    if mosaic_macho_f8e8976:
        mosaic_subprocess.run(['clang', mosaic_outfname_123de25.strip() + '.c', '-g', '-O0', '-undefined', 'dynamic_lookup', '-Wno-everything', '-o', mosaic_outfname_123de25.strip()])

@_name_boundary.callable_contract({'infile': 'mosaic_infile_f01a95d', 'profiles_offset': 'mosaic_profiles_offset_d2ace0f', 'num_profiles': 'mosaic_num_profiles_55cba65', 'base_addr': 'mosaic_base_addr_6aef09d'}, 'display_sandbox_profiles')
def mosaic_display_sandbox_profiles(mosaic_infile_f01a95d, mosaic_profiles_offset_d2ace0f, mosaic_num_profiles_55cba65, mosaic_base_addr_6aef09d):
    mosaic_logger.info('Printing sandbox profiles from bundle')
    mosaic_names_0c15246 = ''
    for mosaic_i_2ef6dbd in range(0, mosaic_num_profiles_55cba65):
        mosaic_infile_f01a95d.seek(mosaic_profiles_offset_d2ace0f + 376 * mosaic_i_2ef6dbd)
        mosaic_name_offset_3a40a71 = mosaic_struct.unpack('<H', mosaic_infile_f01a95d.read(2))[0]
        mosaic_name_a85aeaf = mosaic_extract_string_from_offset(mosaic_infile_f01a95d, mosaic_name_offset_3a40a71, mosaic_base_addr_6aef09d)
        mosaic_names_0c15246 += '\n' + mosaic_name_a85aeaf
    mosaic_logger.info('Found %d sandbox profiles.' % mosaic_num_profiles_55cba65)

@_name_boundary.callable_contract({'f': 'mosaic_f_053b4a0', 'vars_offset': 'mosaic_vars_offset_3a54d87', 'num_vars': 'mosaic_num_vars_fd227ac', 'base_address': 'mosaic_base_address_7db2c3c'}, 'get_global_vars')
def mosaic_get_global_vars(mosaic_f_053b4a0, mosaic_vars_offset_3a54d87, mosaic_num_vars_fd227ac, mosaic_base_address_7db2c3c):
    mosaic_global_vars_334fbcd = []
    mosaic_next_var_pointer_5bb4dab = mosaic_vars_offset_3a54d87
    for mosaic_i_4a8d292 in range(0, mosaic_num_vars_fd227ac):
        mosaic_f_053b4a0.seek(mosaic_next_var_pointer_5bb4dab)
        mosaic_var_offset_7e8a7ec = mosaic_struct.unpack('<H', mosaic_f_053b4a0.read(2))[0]
        mosaic_f_053b4a0.seek(mosaic_base_address_7db2c3c + mosaic_var_offset_7e8a7ec * 8)
        mosaic_len_c207983 = mosaic_struct.unpack('H', mosaic_f_053b4a0.read(2))[0]
        mosaic_s_4c7adb5 = mosaic_f_053b4a0.read(mosaic_len_c207983 - 1)
        mosaic_global_vars_334fbcd.append(mosaic_s_4c7adb5.decode('utf-8'))
        mosaic_next_var_pointer_5bb4dab += 2
    mosaic_logger.info('global variables are {:s}'.format(', '.join((mosaic_s_eeae1ad for mosaic_s_eeae1ad in mosaic_global_vars_334fbcd))))
    return mosaic_global_vars_334fbcd

@_name_boundary.callable_contract({'f': 'mosaic_f_4e2f456', 'offset': 'mosaic_offset_0726575', 'count': 'mosaic_count_f1bb1d6'}, 'get_policies')
def mosaic_get_policies(mosaic_f_4e2f456, mosaic_offset_0726575, mosaic_count_f1bb1d6):
    mosaic_policies_80c4cd3 = []
    mosaic_f_4e2f456.seek(mosaic_offset_0726575)
    mosaic_policies_80c4cd3 = mosaic_struct.unpack('<%dH' % mosaic_count_f1bb1d6, mosaic_f_4e2f456.read(2 * mosaic_count_f1bb1d6))
    return mosaic_policies_80c4cd3

@_name_boundary.callable_contract({'parser': 'mosaic_parser_4160f69', 'args': 'mosaic_args_7f196f5', 'sandbox_data': 'mosaic_sandbox_data_f66142f'}, 'read_sandbox_operations')
def mosaic_read_sandbox_operations(mosaic_parser_4160f69, mosaic_args_7f196f5, mosaic_sandbox_data_f66142f) -> None:
    mosaic_sb_ops_f2e71a5 = [mosaic_l_b14a218.strip() for mosaic_l_b14a218 in open(mosaic_args_7f196f5.operations_file)]
    _name_boundary.attributes(mosaic_sandbox_data_f66142f)['sb_ops'] = mosaic_sb_ops_f2e71a5
    mosaic_num_sb_ops_1baa2fe = len(mosaic_sb_ops_f2e71a5)
    mosaic_logger.info('num_sb_ops: %d', mosaic_num_sb_ops_1baa2fe)
    mosaic_ops_to_reverse_012ee7c = []
    if mosaic_args_7f196f5.operation:
        for mosaic_op_99e41f5 in mosaic_args_7f196f5.operation:
            if mosaic_op_99e41f5 not in mosaic_sb_ops_f2e71a5:
                mosaic_parser_4160f69.print_usage()
                print('unavailable operation: {}'.format(mosaic_op_99e41f5))
                mosaic_sys.exit(1)
            mosaic_ops_to_reverse_012ee7c.append(mosaic_op_99e41f5)
        _name_boundary.attributes(mosaic_sandbox_data_f66142f)['ops_to_reverse'] = mosaic_ops_to_reverse_012ee7c

@_name_boundary.callable_contract({'infile': 'mosaic_infile_c9ea1d3', 'sandbox_data': 'mosaic_sandbox_data_8827a64'}, 'parse_regex_list')
def mosaic_parse_regex_list(mosaic_infile_c9ea1d3, mosaic_sandbox_data_8827a64):
    mosaic_logger.debug('\n\nregular expressions:\n')
    mosaic_regex_list_54768a4 = []
    if _name_boundary.attributes(mosaic_sandbox_data_8827a64)['regex_count'] > 0:
        mosaic_infile_c9ea1d3.seek(_name_boundary.attributes(mosaic_sandbox_data_8827a64)['regex_table_offset'])
        mosaic_re_offsets_table_d4f4fe6 = mosaic_struct.unpack('<%dH' % _name_boundary.attributes(mosaic_sandbox_data_8827a64)['regex_count'], mosaic_infile_c9ea1d3.read(2 * _name_boundary.attributes(mosaic_sandbox_data_8827a64)['regex_count']))
        mosaic_offset_addition_9555bd7 = 0
        for mosaic_offset_7df24b0 in mosaic_re_offsets_table_d4f4fe6:
            mosaic_infile_c9ea1d3.seek(mosaic_offset_7df24b0 * 8 + _name_boundary.attributes(mosaic_sandbox_data_8827a64)['base_addr'] + mosaic_offset_addition_9555bd7)
            mosaic_re_length_d429e47 = mosaic_struct.unpack('<H', mosaic_infile_c9ea1d3.read(2))[0]
            mosaic_re_c9a42fd = mosaic_struct.unpack('<%dB' % mosaic_re_length_d429e47, mosaic_infile_c9ea1d3.read(mosaic_re_length_d429e47))
            mosaic_re_debug_str_5a7b8da = ('re: [', ', '.join([hex(mosaic_i_9f33900) for mosaic_i_9f33900 in mosaic_re_c9a42fd]), ']')
            mosaic_logger.debug(mosaic_re_debug_str_5a7b8da)
            mosaic_regex_list_54768a4.append(mosaic_sandbox_regex.parse_regex(mosaic_re_c9a42fd))
    mosaic_logger.info(mosaic_regex_list_54768a4)
    _name_boundary.attributes(mosaic_sandbox_data_8827a64)['regex_list'] = mosaic_regex_list_54768a4

@_name_boundary.callable_contract({}, 'main')
def mosaic_main():
    """Reverse Apple binary sandbox file to SBPL (Sandbox Profile Language) format.

    Sample run:
        python reverse_sandbox.py -r 7.1.1 container.sb.bin
        python reverse_sandbox.py -r 7.1.1 -d out container.sb.bin
        python reverse_sandbox.py -r 7.1.1 -d out container.sb.bin -n network-inbound network-outbound
        python reverse_sandbox.py -r 9.0.2 -d out sandbox_bundle_iOS_9.0 -n network-inbound network-outbound -p container
    """
    mosaic_parser_c766996 = mosaic_argparse.ArgumentParser()
    mosaic_parser_c766996.add_argument('filename', help='path to the binary sandbox profile')
    mosaic_parser_c766996.add_argument('-r', '--release', help='iOS release version for sandbox profile', required=True)
    mosaic_parser_c766996.add_argument('-o', '--operations_file', help='file with list of operations', required=True)
    mosaic_parser_c766996.add_argument('-p', '--profile', nargs='+', help='profile to reverse (for bundles) (default is to reverse all operations)')
    mosaic_parser_c766996.add_argument('-n', '--operation', nargs='+', help='particular operation(s) to reverse (default is to reverse all operations)')
    mosaic_parser_c766996.add_argument('-d', '--directory', help='directory where to write reversed profiles (default is current directory)')
    mosaic_parser_c766996.add_argument('-psb', '--print_sandbox_profiles', action='store_true', help='print sandbox profiles of a given bundle (only for iOS versions 9+)')
    mosaic_parser_c766996.add_argument('-kbf', '--keep_builtin_filters', help='keep builtin filters in output', action='store_true')
    mosaic_parser_c766996.add_argument('-c', '--c_output', help='output a C file rather than Scheme', action='store_true')
    mosaic_parser_c766996.add_argument('-m', '--macho', help='generate a reversible Mach-O file (implies --c_output)', action='store_true')
    mosaic_args_97e761d = mosaic_parser_c766996.parse_args()
    if mosaic_args_97e761d.filename is None:
        mosaic_parser_c766996.print_usage()
        print('no sandbox profile/bundle file to reverse')
        mosaic_sys.exit(1)
    if mosaic_args_97e761d.directory:
        mosaic_out_dir_c0a126e = mosaic_args_97e761d.directory
    else:
        mosaic_out_dir_c0a126e = mosaic_os.getcwd()
    mosaic_infile_934d317 = open(mosaic_args_97e761d.filename, 'rb')
    mosaic_sandbox_data_561bf01 = mosaic_parse_profile(mosaic_infile_934d317, mosaic_args_97e761d)
    mosaic_read_sandbox_operations(mosaic_parser_c766996, mosaic_args_97e761d, mosaic_sandbox_data_561bf01)
    mosaic_parse_regex_list(mosaic_infile_934d317, mosaic_sandbox_data_561bf01)
    if mosaic_args_97e761d.print_sandbox_profiles:
        if _name_boundary.attributes(mosaic_sandbox_data_561bf01)['type'] == 32768:
            mosaic_display_sandbox_profiles(mosaic_infile_934d317, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['profiles_offset'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['num_profiles'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['base_addr'])
        else:
            print('cannot print sandbox profiles list; filename {} is not a sandbox bundle'.format(mosaic_args_97e761d.filename))
        mosaic_sys.exit(0)
    mosaic_logger.info('{:d} global vars at offset {}'.format(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['vars_count'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['vars_offset']))
    _name_boundary.attributes(mosaic_sandbox_data_561bf01)['global_vars'] = mosaic_get_global_vars(mosaic_infile_934d317, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['vars_offset'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['vars_count'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['base_addr'])
    _name_boundary.attributes(mosaic_sandbox_data_561bf01)['policies'] = mosaic_get_policies(mosaic_infile_934d317, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['entitlements_offset'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['entitlements_count'])
    mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['operation_nodes_offset'])
    mosaic_logger.info('number of operation nodes: %u' % _name_boundary.attributes(mosaic_sandbox_data_561bf01)['op_nodes_count'])
    mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['operation_nodes_offset'])
    mosaic_operation_nodes_067d909 = mosaic_create_operation_nodes(mosaic_infile_934d317, mosaic_sandbox_data_561bf01, mosaic_args_97e761d.keep_builtin_filters)
    if _name_boundary.attributes(mosaic_sandbox_data_561bf01)['type'] == 32768:
        mosaic_logger.info('using profile bundle')
        mosaic_profile_size_e1f762e = _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops_count'] * 2 + 2 + 2
        if int(_name_boundary.attributes(mosaic_args_97e761d)['release']) > 17:
            mosaic_profile_size_e1f762e += 4
        mosaic_profile_ops_offset_size_9cfd189 = mosaic_PROFILE_OPS_OFFSET
        if int(_name_boundary.attributes(mosaic_args_97e761d)['release']) > 17:
            mosaic_profile_ops_offset_size_9cfd189 += 4
        for mosaic_i_ce4d473 in range(0, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['num_profiles']):
            mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['profiles_offset'] + mosaic_profile_size_e1f762e * mosaic_i_ce4d473)
            mosaic_name_offset_1978d77 = mosaic_struct.unpack('<H', mosaic_infile_934d317.read(2))[0]
            mosaic_name_e977990 = mosaic_extract_string_from_offset(mosaic_infile_934d317, mosaic_name_offset_1978d77, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['base_addr'])
            if mosaic_args_97e761d.profile:
                if mosaic_name_e977990 not in mosaic_args_97e761d.profile:
                    continue
            mosaic_logger.info('profile name (offset 0x%x): %s' % (mosaic_name_offset_1978d77, mosaic_name_e977990))
            mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['profiles_offset'] + mosaic_profile_size_e1f762e * mosaic_i_ce4d473 + mosaic_profile_ops_offset_size_9cfd189)
            mosaic_op_table_d2d59cb = mosaic_struct.unpack('<%dH' % _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops_count'], mosaic_infile_934d317.read(2 * _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops_count']))
            mosaic_name_e977990 = mosaic_name_e977990.replace('/', '_')
            mosaic_out_fname_201788b = mosaic_os.path.join(mosaic_out_dir_c0a126e, mosaic_name_e977990)
            mosaic_process_profile(mosaic_infile_934d317, mosaic_out_fname_201788b, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['ops_to_reverse'], mosaic_op_table_d2d59cb, mosaic_operation_nodes_067d909, mosaic_args_97e761d.c_output, _name_boundary.attributes(mosaic_args_97e761d)['macho'])
    else:
        mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['profiles_offset'])
        mosaic_op_table_d2d59cb = mosaic_struct.unpack('<%dH' % _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops_count'], mosaic_infile_934d317.read(2 * _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops_count']))
        mosaic_infile_934d317.seek(_name_boundary.attributes(mosaic_sandbox_data_561bf01)['operation_nodes_offset'])
        mosaic_logger.info('number of operation nodes: %d' % _name_boundary.attributes(mosaic_sandbox_data_561bf01)['op_nodes_count'])
        mosaic_out_fname_201788b = mosaic_os.path.join(mosaic_out_dir_c0a126e, mosaic_os.path.splitext(mosaic_os.path.basename(mosaic_args_97e761d.filename))[0])
        mosaic_process_profile(mosaic_infile_934d317, mosaic_out_fname_201788b, _name_boundary.attributes(mosaic_sandbox_data_561bf01)['sb_ops'], _name_boundary.attributes(mosaic_sandbox_data_561bf01)['ops_to_reverse'], mosaic_op_table_d2d59cb, mosaic_operation_nodes_067d909, mosaic_args_97e761d.c_output, _name_boundary.attributes(mosaic_args_97e761d)['macho'])
    mosaic_infile_934d317.close()
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
_name_boundary.module_contract(globals(), {'INDEX_SIZE': 'mosaic_INDEX_SIZE', 'create_operation_nodes': 'mosaic_create_operation_nodes', 'process_profile': 'mosaic_process_profile', 'os': 'mosaic_os', 'get_policies': 'mosaic_get_policies', 'node_to_c': 'mosaic_node_to_c', 'NUM_PROFILES_OFFSET': 'mosaic_NUM_PROFILES_OFFSET', 'REGEX_COUNT_OFFSET': 'mosaic_REGEX_COUNT_OFFSET', 'logging': 'mosaic_logging', 'Filters': 'mosaic_Filters', 'VARS_COUNT_OFFSET': 'mosaic_VARS_COUNT_OFFSET', 'sandbox_regex': 'mosaic_sandbox_regex', 'operation_node': 'mosaic_operation_node', 'get_global_vars': 'mosaic_get_global_vars', 'subprocess': 'mosaic_subprocess', 'struct': 'mosaic_struct', 'logger': 'mosaic_logger', 'parse_profile': 'mosaic_parse_profile', 'parse_regex_list': 'mosaic_parse_regex_list', 'argparse': 'mosaic_argparse', 'PROFILE_OPS_OFFSET': 'mosaic_PROFILE_OPS_OFFSET', 'main': 'mosaic_main', 'sys': 'mosaic_sys', 'display_sandbox_profiles': 'mosaic_display_sandbox_profiles', 'ios16_5_struct': 'mosaic_ios16_5_struct', 'VARS_TABLE_OFFSET': 'mosaic_VARS_TABLE_OFFSET', 'sandbox_filter': 'mosaic_sandbox_filter', 'read_sandbox_operations': 'mosaic_read_sandbox_operations', 'extract_string_from_offset': 'mosaic_extract_string_from_offset', 'OPERATION_NODE_SIZE': 'mosaic_OPERATION_NODE_SIZE', 'tqdm': 'mosaic_tqdm', 'REGEX_TABLE_OFFSET': 'mosaic_REGEX_TABLE_OFFSET', 'SandboxData': 'mosaic_SandboxData'})
