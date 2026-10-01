"""Explicit compatibility boundary for public names and structured data labels."""
import functools as _boundary_functools
import enum as _boundary_enum
import inspect as _boundary_inspect
import types as _boundary_types
from pathlib import Path as _BoundaryPath
import sys as _boundary_sys
from collections import namedtuple as _boundary_namedtuple

_MISSING = object()
ATTRIBUTE_NAMES = {'Emulator': 'mosaic_Emulator', 'hook_unmapped': 'mosaic_hook_unmapped', 'Sandbox': 'mosaic_Sandbox', 'get_sb_kext': 'mosaic_get_sb_kext', '_get_nop': 'mosaic__get_nop', '_get_lines': 'mosaic__get_lines', '_get_load_platform_lines': 'mosaic__get_load_platform_lines', 'get_platform_profile_bytes': 'mosaic_get_platform_profile_bytes', 'get_profile_bytes': 'mosaic_get_profile_bytes', 'get_operations': 'mosaic_get_operations', 'decompile_sb': 'mosaic_decompile_sb', 'decompile_all': 'mosaic_decompile_all', 'addr': 'mosaic_addr', 'code': 'mosaic_code', 'emu': 'mosaic_emu', 'kc': 'mosaic_kc', 'macho': 'mosaic_macho', 'platform_base_addr': 'mosaic_platform_base_addr', 'version': 'mosaic_version', 'dis': 'mosaic_dis', 'ops_file': 'mosaic_ops_file', 'Filters': 'mosaic_Filters', 'filters': 'mosaic_filters', 'exists': 'mosaic_exists', 'get': 'mosaic_get', 'Modifiers': 'mosaic_Modifiers', 'modifiers': 'mosaic_modifiers', 'InlineModifier': 'mosaic_InlineModifier', 'Modifier': 'mosaic_Modifier', 'TerminalNode': 'mosaic_TerminalNode', 'TERMINAL_NODE_TYPE_ALLOW': 'mosaic_TERMINAL_NODE_TYPE_ALLOW', 'TERMINAL_NODE_TYPE_DENY': 'mosaic_TERMINAL_NODE_TYPE_DENY', 'INLINE_MODIFIERS': 'mosaic_INLINE_MODIFIERS', 'FLAGS_MODIFIERS': 'mosaic_FLAGS_MODIFIERS', 'c_repr': 'mosaic_c_repr', 'load_modifiers_db': 'mosaic_load_modifiers_db', 'get_modifier': 'mosaic_get_modifier', 'get_modifiers_by_flag': 'mosaic_get_modifiers_by_flag', 'terminal_convert_function': 'mosaic_terminal_convert_function', 'convert_filter': 'mosaic_convert_filter', 'is_allow': 'mosaic_is_allow', 'is_deny': 'mosaic_is_deny', 'NonTerminalNode': 'mosaic_NonTerminalNode', 'simplify_list': 'mosaic_simplify_list', 'str_debug': 'mosaic_str_debug', 'str_not': 'mosaic_str_not', 'values': 'mosaic_values', 'is_entitlement_start': 'mosaic_is_entitlement_start', 'is_entitlement': 'mosaic_is_entitlement', 'is_last_regular_expression': 'mosaic_is_last_regular_expression', 'is_non_terminal_deny': 'mosaic_is_non_terminal_deny', 'is_non_terminal_allow': 'mosaic_is_non_terminal_allow', 'is_non_terminal_non_terminal': 'mosaic_is_non_terminal_non_terminal', 'is_allow_non_terminal': 'mosaic_is_allow_non_terminal', 'is_deny_non_terminal': 'mosaic_is_deny_non_terminal', 'is_deny_allow': 'mosaic_is_deny_allow', 'is_allow_deny': 'mosaic_is_allow_deny', 'OperationNode': 'mosaic_OperationNode', 'OPERATION_NODE_TYPE_NON_TERMINAL': 'mosaic_OPERATION_NODE_TYPE_NON_TERMINAL', 'OPERATION_NODE_TYPE_TERMINAL': 'mosaic_OPERATION_NODE_TYPE_TERMINAL', 'is_terminal': 'mosaic_is_terminal', 'is_non_terminal': 'mosaic_is_non_terminal', 'parse_terminal': 'mosaic_parse_terminal', 'parse_non_terminal': 'mosaic_parse_non_terminal', 'parse_raw': 'mosaic_parse_raw', 'ReducedVertice': 'mosaic_ReducedVertice', 'TYPE_SINGLE': 'mosaic_TYPE_SINGLE', 'TYPE_START': 'mosaic_TYPE_START', 'TYPE_REQUIRE_ANY': 'mosaic_TYPE_REQUIRE_ANY', 'TYPE_REQUIRE_ALL': 'mosaic_TYPE_REQUIRE_ALL', 'TYPE_REQUIRE_ENTITLEMENT': 'mosaic_TYPE_REQUIRE_ENTITLEMENT', 'set_value': 'mosaic_set_value', 'set_type': 'mosaic_set_type', '_replace_in_list': 'mosaic__replace_in_list', 'replace_in_list': 'mosaic_replace_in_list', '_replace_sublist_in_list': 'mosaic__replace_sublist_in_list', 'replace_sublist_in_list': 'mosaic_replace_sublist_in_list', 'set_decision': 'mosaic_set_decision', 'set_type_single': 'mosaic_set_type_single', 'set_type_start': 'mosaic_set_type_start', 'set_type_require_entitlement': 'mosaic_set_type_require_entitlement', 'set_type_require_any': 'mosaic_set_type_require_any', 'set_type_require_all': 'mosaic_set_type_require_all', 'set_integrated_vertice': 'mosaic_set_integrated_vertice', 'is_type_single': 'mosaic_is_type_single', 'is_type_start': 'mosaic_is_type_start', 'is_type_require_entitlement': 'mosaic_is_type_require_entitlement', 'is_type_require_all': 'mosaic_is_type_require_all', 'is_type_require_any': 'mosaic_is_type_require_any', 'recursive_str': 'mosaic_recursive_str', 'recursive_str_debug': 'mosaic_recursive_str_debug', 'recursive_xml_str': 'mosaic_recursive_xml_str', 'str_simple': 'mosaic_str_simple', 'str_print_debug': 'mosaic_str_print_debug', 'str_print': 'mosaic_str_print', 'str_print_not': 'mosaic_str_print_not', 'xml_str': 'mosaic_xml_str', 'ReducedEdge': 'mosaic_ReducedEdge', 'ReducedGraph': 'mosaic_ReducedGraph', 'add_vertice': 'mosaic_add_vertice', 'add_edge': 'mosaic_add_edge', 'add_edge_by_vertices': 'mosaic_add_edge_by_vertices', 'set_final_vertices': 'mosaic_set_final_vertices', 'contains_vertice': 'mosaic_contains_vertice', 'contains_edge': 'mosaic_contains_edge', 'contains_edge_by_vertices': 'mosaic_contains_edge_by_vertices', 'get_vertice_by_value': 'mosaic_get_vertice_by_value', 'get_edge_by_vertices': 'mosaic_get_edge_by_vertices', 'remove_vertice': 'mosaic_remove_vertice', 'remove_vertice_update_decision': 'mosaic_remove_vertice_update_decision', 'remove_edge': 'mosaic_remove_edge', 'remove_edge_by_vertices': 'mosaic_remove_edge_by_vertices', 'replace_vertice_in_edge_start': 'mosaic_replace_vertice_in_edge_start', 'replace_vertice_in_edge_end': 'mosaic_replace_vertice_in_edge_end', 'replace_vertice_in_single_vertices': 'mosaic_replace_vertice_in_single_vertices', 'replace_vertice_list': 'mosaic_replace_vertice_list', 'get_next_vertices': 'mosaic_get_next_vertices', 'get_prev_vertices': 'mosaic_get_prev_vertices', 'get_start_vertices': 'mosaic_get_start_vertices', 'get_end_vertices': 'mosaic_get_end_vertices', 'reduce_next_vertices': 'mosaic_reduce_next_vertices', 'reduce_prev_vertices': 'mosaic_reduce_prev_vertices', 'reduce_vertice_single_prev': 'mosaic_reduce_vertice_single_prev', 'reduce_vertice_single_next': 'mosaic_reduce_vertice_single_next', 'reduce_graph': 'mosaic_reduce_graph', 'reduce_graph_with_metanodes': 'mosaic_reduce_graph_with_metanodes', 'str_simple_with_metanodes': 'mosaic_str_simple_with_metanodes', 'remove_builtin_filters': 'mosaic_remove_builtin_filters', 'reduce_integrated_vertices': 'mosaic_reduce_integrated_vertices', 'aggregate_require_entitlement': 'mosaic_aggregate_require_entitlement', 'aggregate_require_entitlement_nodes': 'mosaic_aggregate_require_entitlement_nodes', 'cleanup_filters': 'mosaic_cleanup_filters', 'remove_builtin_filters_with_metanodes': 'mosaic_remove_builtin_filters_with_metanodes', 'replace_require_entitlement_with_metanodes': 'mosaic_replace_require_entitlement_with_metanodes', 'aggregate_require_entitlement_with_metanodes': 'mosaic_aggregate_require_entitlement_with_metanodes', 'cleanup_filters_with_metanodes': 'mosaic_cleanup_filters_with_metanodes', 'print_vertices_with_operation': 'mosaic_print_vertices_with_operation', 'print_vertices_with_operation_metanodes': 'mosaic_print_vertices_with_operation_metanodes', 'dump_xml': 'mosaic_dump_xml', 'id': 'mosaic_id', 'policy_op_idx': 'mosaic_policy_op_idx', 'argument': 'mosaic_argument', 'flags': 'mosaic_flags', 'count': 'mosaic_count', 'unknown': 'mosaic_unknown', 'offset': 'mosaic_offset', 'type': 'mosaic_type', 'action': 'mosaic_action', 'modifier_flags': 'mosaic_modifier_flags', 'action_inline': 'mosaic_action_inline', 'inline_modifier': 'mosaic_inline_modifier', 'modifier': 'mosaic_modifier', 'inline_operation_node': 'mosaic_inline_operation_node', 'modifiers_db': 'mosaic_modifiers_db', 'ss': 'mosaic_ss', 'db_modifiers': 'mosaic_db_modifiers', 'parsed': 'mosaic_parsed', 'operation_name': 'mosaic_operation_name', 'filter_id': 'mosaic_filter_id', 'filter': 'mosaic_filter', 'argument_id': 'mosaic_argument_id', 'match_offset': 'mosaic_match_offset', 'match': 'mosaic_match', 'unmatch_offset': 'mosaic_unmatch_offset', 'unmatch': 'mosaic_unmatch', 'raw': 'mosaic_raw', 'terminal': 'mosaic_terminal', 'non_terminal': 'mosaic_non_terminal', 'value': 'mosaic_value', 'decision': 'mosaic_decision', 'is_not': 'mosaic_is_not', 'start': 'mosaic_start', 'end': 'mosaic_end', 'vertices': 'mosaic_vertices', 'edges': 'mosaic_edges', 'final_vertices': 'mosaic_final_vertices', 'reduce_changes_occurred': 'mosaic_reduce_changes_occurred', 'RegexParser': 'mosaic_RegexParser', 'parse': 'mosaic_parse', 'SandboxData': 'mosaic_SandboxData', 'release': 'mosaic_release', 'data_file': 'mosaic_data_file', 'header_size': 'mosaic_header_size', 'op_nodes_count': 'mosaic_op_nodes_count', 'sb_ops_count': 'mosaic_sb_ops_count', 'vars_count': 'mosaic_vars_count', 'states_count': 'mosaic_states_count', 'num_profiles': 'mosaic_num_profiles', 'regex_count': 'mosaic_regex_count', 'entitlements_count': 'mosaic_entitlements_count', 'regex_table_offset': 'mosaic_regex_table_offset', 'vars_offset': 'mosaic_vars_offset', 'states_offset': 'mosaic_states_offset', 'entitlements_offset': 'mosaic_entitlements_offset', 'profiles_offset': 'mosaic_profiles_offset', 'profiles_end_offset': 'mosaic_profiles_end_offset', 'operation_nodes_size': 'mosaic_operation_nodes_size', 'operation_nodes_offset': 'mosaic_operation_nodes_offset', 'base_addr': 'mosaic_base_addr', 'regex_list': 'mosaic_regex_list', 'global_vars': 'mosaic_global_vars', 'policies': 'mosaic_policies', 'sb_ops': 'mosaic_sb_ops', 'operation_nodes': 'mosaic_operation_nodes', 'ops_to_reverse': 'mosaic_ops_to_reverse', 'ReverseStringState': 'mosaic_ReverseStringState', 'binary_string': 'mosaic_binary_string', 'len': 'mosaic_len', 'pos': 'mosaic_pos', 'base': 'mosaic_base', 'base_stack': 'mosaic_base_stack', 'token': 'mosaic_token', 'token_stack': 'mosaic_token_stack', 'output_strings': 'mosaic_output_strings', 'STATE_UNKNOWN': 'mosaic_STATE_UNKNOWN', 'STATE_TOKEN_BYTE_READ': 'mosaic_STATE_TOKEN_BYTE_READ', 'STATE_CONCAT_BYTE_READ': 'mosaic_STATE_CONCAT_BYTE_READ', 'STATE_CONCAT_SAVE_BYTE_READ': 'mosaic_STATE_CONCAT_SAVE_BYTE_READ', 'STATE_END_BYTE_READ': 'mosaic_STATE_END_BYTE_READ', 'STATE_SPLIT_BYTE_READ': 'mosaic_STATE_SPLIT_BYTE_READ', 'STATE_TOKEN_READ': 'mosaic_STATE_TOKEN_READ', 'STATE_RANGE_BYTE_READ': 'mosaic_STATE_RANGE_BYTE_READ', 'STATE_CONSTANT_READ': 'mosaic_STATE_CONSTANT_READ', 'STATE_SINGLE_BYTE_READ': 'mosaic_STATE_SINGLE_BYTE_READ', 'STATE_PLUS_READ': 'mosaic_STATE_PLUS_READ', 'STATE_RESET_STRING': 'mosaic_STATE_RESET_STRING', 'state_stack': 'mosaic_state_stack', 'state': 'mosaic_state', 'state_byte': 'mosaic_state_byte', 'update_state_unknown': 'mosaic_update_state_unknown', 'update_state_token_byte_read': 'mosaic_update_state_token_byte_read', 'update_state_concat_byte_read': 'mosaic_update_state_concat_byte_read', 'update_state_concat_save_byte_read': 'mosaic_update_state_concat_save_byte_read', 'update_state_end_byte_read': 'mosaic_update_state_end_byte_read', 'update_state_split_byte_read': 'mosaic_update_state_split_byte_read', 'update_state_range_byte_read': 'mosaic_update_state_range_byte_read', 'update_state_token_read': 'mosaic_update_state_token_read', 'update_state_reset_string': 'mosaic_update_state_reset_string', 'update_state_constant_read': 'mosaic_update_state_constant_read', 'update_state_single_byte_read': 'mosaic_update_state_single_byte_read', 'update_state_plus_read': 'mosaic_update_state_plus_read', 'update_state': 'mosaic_update_state', 'get_next_byte': 'mosaic_get_next_byte', 'get_length_minus_1': 'mosaic_get_length_minus_1', 'read_token': 'mosaic_read_token', 'update_base': 'mosaic_update_base', 'update_base_stack': 'mosaic_update_base_stack', 'end_current_token': 'mosaic_end_current_token', 'get_last_byte': 'mosaic_get_last_byte', 'get_substring': 'mosaic_get_substring', 'end_with_subtokens': 'mosaic_end_with_subtokens', 'is_end': 'mosaic_is_end', 'reset_base': 'mosaic_reset_base', 'reset_base_full': 'mosaic_reset_base_full', 'SandboxString': 'mosaic_SandboxString', 'rss_stack': 'mosaic_rss_stack', 'parse_byte_string': 'mosaic_parse_byte_string', 'tokens': 'mosaic_tokens', 'Node': 'mosaic_Node', 'TYPE_JUMP_FORWARD': 'mosaic_TYPE_JUMP_FORWARD', 'TYPE_JUMP_BACKWARD': 'mosaic_TYPE_JUMP_BACKWARD', 'TYPE_CHARACTER': 'mosaic_TYPE_CHARACTER', 'TYPE_END': 'mosaic_TYPE_END', 'FLAG_WHITE': 'mosaic_FLAG_WHITE', 'FLAG_GREY': 'mosaic_FLAG_GREY', 'FLAG_BLACK': 'mosaic_FLAG_BLACK', 'name': 'mosaic_name', 'flag': 'mosaic_flag', 'set_name': 'mosaic_set_name', 'set_type_jump_forward': 'mosaic_set_type_jump_forward', 'set_type_jump_backward': 'mosaic_set_type_jump_backward', 'set_type_character': 'mosaic_set_type_character', 'set_type_end': 'mosaic_set_type_end', 'is_type_end': 'mosaic_is_type_end', 'is_type_jump': 'mosaic_is_type_jump', 'is_type_jump_backward': 'mosaic_is_type_jump_backward', 'is_type_jump_forward': 'mosaic_is_type_jump_forward', 'is_type_character': 'mosaic_is_type_character', 'set_flag_white': 'mosaic_set_flag_white', 'set_flag_grey': 'mosaic_set_flag_grey', 'set_flag_black': 'mosaic_set_flag_black', 'Graph': 'mosaic_Graph', 'graph_dict': 'mosaic_graph_dict', 'canon_graph_dict': 'mosaic_canon_graph_dict', 'node_list': 'mosaic_node_list', 'start_node': 'mosaic_start_node', 'end_states': 'mosaic_end_states', 'start_state': 'mosaic_start_state', 'regex': 'mosaic_regex', 'unified_regex': 'mosaic_unified_regex', 'add_node': 'mosaic_add_node', 'has_node': 'mosaic_has_node', 'update_node': 'mosaic_update_node', 'add_new_next_to_node': 'mosaic_add_new_next_to_node', 'get_node_for_idx': 'mosaic_get_node_for_idx', 'get_re_index_for_pos': 'mosaic_get_re_index_for_pos', 'fill_from_regex_list': 'mosaic_fill_from_regex_list', 'get_character_nodes': 'mosaic_get_character_nodes', 'find_node_type_jump': 'mosaic_find_node_type_jump', 'reduce': 'mosaic_reduce', 'get_edges': 'mosaic_get_edges', 'convert_to_canonical': 'mosaic_convert_to_canonical', 'need_use_plus': 'mosaic_need_use_plus', 'unify_two_strings': 'mosaic_unify_two_strings', 'unify_strings': 'mosaic_unify_strings', 'remove_state': 'mosaic_remove_state', 'simplify': 'mosaic_simplify', 'combine_start_end_nodes': 'mosaic_combine_start_end_nodes'}
GLOBAL_NAMES = {'ArgumentParser': 'mosaic_ArgumentParser', 'Sandbox': 'mosaic_Sandbox', 'subprocess': 'mosaic_subprocess', 'unicorn': 'mosaic_unicorn', 'main': 'mosaic_main', 'ipsw_get_out_path': 'mosaic_ipsw_get_out_path', 'Emulator': 'mosaic_Emulator', 'disassemble': 'mosaic_disassemble', 'Path': 'mosaic_Path', 'dl_kernel': 'mosaic_dl_kernel', 'get_bytes': 'mosaic_get_bytes', 'macho_read_data': 'mosaic_macho_read_data', 'read_filters': 'mosaic_read_filters', 'Filters': 'mosaic_Filters', 'json': 'mosaic_json', 'read_modifiers': 'mosaic_read_modifiers', 'Modifiers': 'mosaic_Modifiers', 'build_operation_node_graph': 'mosaic_build_operation_node_graph', 'processed_nodes': 'mosaic_processed_nodes', '_get_operation_node_graph_paths': 'mosaic__get_operation_node_graph_paths', 'clean_nodes_in_operation_node_graph': 'mosaic_clean_nodes_in_operation_node_graph', 'replace_occurred': 'mosaic_replace_occurred', 'nodes_traversed_for_removal': 'mosaic_nodes_traversed_for_removal', 'remove_edge_in_operation_node_graph': 'mosaic_remove_edge_in_operation_node_graph', 'ong_mark_not': 'mosaic_ong_mark_not', 'get_filter_arg_string_by_offset_no_skip': 'mosaic_get_filter_arg_string_by_offset_no_skip', 'current_path': 'mosaic_current_path', 'find_operation_node_by_offset': 'mosaic_find_operation_node_by_offset', 'reduce_operation_node_graph': 'mosaic_reduce_operation_node_graph', 'num_regex': 'mosaic_num_regex', 'OperationNode': 'mosaic_OperationNode', 'Modifier': 'mosaic_Modifier', '_remove_duplicate_node_edges': 'mosaic__remove_duplicate_node_edges', 'ong_add_to_parent_path': 'mosaic_ong_add_to_parent_path', 'logging': 'mosaic_logging', 'clean_edges_in_operation_node_graph': 'mosaic_clean_edges_in_operation_node_graph', 'ong_end_path': 'mosaic_ong_end_path', 'ReducedGraph': 'mosaic_ReducedGraph', 'build_operation_nodes': 'mosaic_build_operation_nodes', 'paths': 'mosaic_paths', 'struct': 'mosaic_struct', 'logger': 'mosaic_logger', 'remove_duplicate_node_edges': 'mosaic_remove_duplicate_node_edges', 'has_been_processed': 'mosaic_has_been_processed', 'NonTerminalNode': 'mosaic_NonTerminalNode', 'print_operation_node_graph': 'mosaic_print_operation_node_graph', 'ReducedVertice': 'mosaic_ReducedVertice', 'sys': 'mosaic_sys', 'build_operation_node': 'mosaic_build_operation_node', 'get_operation_node_graph_paths': 'mosaic_get_operation_node_graph_paths', 'sandbox_filter': 'mosaic_sandbox_filter', 'TerminalNode': 'mosaic_TerminalNode', 'remove_node_in_operation_node_graph': 'mosaic_remove_node_in_operation_node_graph', 'ReducedEdge': 'mosaic_ReducedEdge', 're': 'mosaic_re', 'ong_add_to_path': 'mosaic_ong_add_to_path', 'InlineModifier': 'mosaic_InlineModifier', 'parse_end_of_line': 'mosaic_parse_end_of_line', 'parse_jump_forward': 'mosaic_parse_jump_forward', 'parse_end': 'mosaic_parse_end', 'parse_character_class': 'mosaic_parse_character_class', 'parse': 'mosaic_parse', 'RegexParser': 'mosaic_RegexParser', 'parse_any_character': 'mosaic_parse_any_character', 'parse_jump_backward': 'mosaic_parse_jump_backward', 'parse_character': 'mosaic_parse_character', 'parse_beginning_of_line': 'mosaic_parse_beginning_of_line', 'INDEX_SIZE': 'mosaic_INDEX_SIZE', 'create_operation_nodes': 'mosaic_create_operation_nodes', 'process_profile': 'mosaic_process_profile', 'os': 'mosaic_os', 'get_policies': 'mosaic_get_policies', 'node_to_c': 'mosaic_node_to_c', 'NUM_PROFILES_OFFSET': 'mosaic_NUM_PROFILES_OFFSET', 'REGEX_COUNT_OFFSET': 'mosaic_REGEX_COUNT_OFFSET', 'VARS_COUNT_OFFSET': 'mosaic_VARS_COUNT_OFFSET', 'sandbox_regex': 'mosaic_sandbox_regex', 'operation_node': 'mosaic_operation_node', 'get_global_vars': 'mosaic_get_global_vars', 'parse_profile': 'mosaic_parse_profile', 'parse_regex_list': 'mosaic_parse_regex_list', 'argparse': 'mosaic_argparse', 'PROFILE_OPS_OFFSET': 'mosaic_PROFILE_OPS_OFFSET', 'display_sandbox_profiles': 'mosaic_display_sandbox_profiles', 'ios16_5_struct': 'mosaic_ios16_5_struct', 'VARS_TABLE_OFFSET': 'mosaic_VARS_TABLE_OFFSET', 'read_sandbox_operations': 'mosaic_read_sandbox_operations', 'extract_string_from_offset': 'mosaic_extract_string_from_offset', 'OPERATION_NODE_SIZE': 'mosaic_OPERATION_NODE_SIZE', 'tqdm': 'mosaic_tqdm', 'REGEX_TABLE_OFFSET': 'mosaic_REGEX_TABLE_OFFSET', 'SandboxData': 'mosaic_SandboxData', 'SandboxString': 'mosaic_SandboxString', 'ReverseStringState': 'mosaic_ReverseStringState', 'get_filter_arg_octal_integer': 'mosaic_get_filter_arg_octal_integer', 'get_filter_arg_regex_by_id': 'mosaic_get_filter_arg_regex_by_id', 'regex_list': 'mosaic_regex_list', 'get_filter_arg_signal_number': 'mosaic_get_filter_arg_signal_number', 'get_filter_arg_string_by_offset': 'mosaic_get_filter_arg_string_by_offset', 'get_filter_arg_socket_domain': 'mosaic_get_filter_arg_socket_domain', 'convert_filter_callback': 'mosaic_convert_filter_callback', 'global_vars': 'mosaic_global_vars', 'get_filter_arg_persona_type': 'mosaic_get_filter_arg_persona_type', 'get_filter_arg_fcntl': 'mosaic_get_filter_arg_fcntl', 'get_filter_arg_network_address': 'mosaic_get_filter_arg_network_address', 'get_filter_arg_task_special_port': 'mosaic_get_filter_arg_task_special_port', 'get_none': 'mosaic_get_none', 'get_filter_arg_machtrap_number': 'mosaic_get_filter_arg_machtrap_number', 'reverse_string': 'mosaic_reverse_string', 'get_filter_arg_socket_option_level': 'mosaic_get_filter_arg_socket_option_level', 'get_filter_arg_string_by_offset_with_type': 'mosaic_get_filter_arg_string_by_offset_with_type', 'get_filter_arg_boolean': 'mosaic_get_filter_arg_boolean', 'get_filter_arg_host_port': 'mosaic_get_filter_arg_host_port', 'get_filter_arg_storage_class_extension': 'mosaic_get_filter_arg_storage_class_extension', 'get_filter_arg_integer': 'mosaic_get_filter_arg_integer', 'get_filter_arg_privilege_id': 'mosaic_get_filter_arg_privilege_id', 'get_filter_arg_owner': 'mosaic_get_filter_arg_owner', 'get_filter_arg_socket_type': 'mosaic_get_filter_arg_socket_type', 'get_filter_arg_csr': 'mosaic_get_filter_arg_csr', 'get_filter_arg_necp_client_action': 'mosaic_get_filter_arg_necp_client_action', 'get_filter_arg_vnode_type': 'mosaic_get_filter_arg_vnode_type', 'get_filter_arg_file_attribute': 'mosaic_get_filter_arg_file_attribute', 'get_filter_arg_socket_option_name': 'mosaic_get_filter_arg_socket_option_name', 'get_filter_arg_memorystatus_control': 'mosaic_get_filter_arg_memorystatus_control', 'get_filter_arg_iokit_usb_subclass': 'mosaic_get_filter_arg_iokit_usb_subclass', 'convert_modifier_callback': 'mosaic_convert_modifier_callback', 'get_filter_arg_iokit_usb': 'mosaic_get_filter_arg_iokit_usb', 'get_filter_arg_syscall_number': 'mosaic_get_filter_arg_syscall_number', 'keep_builtin_filters': 'mosaic_keep_builtin_filters', 'get_filter_arg_entry_attribute': 'mosaic_get_filter_arg_entry_attribute', 'get_filter_arg_process_attribute': 'mosaic_get_filter_arg_process_attribute', 'get_filter_arg_kernel_mig_routine': 'mosaic_get_filter_arg_kernel_mig_routine', 'get_filter_arg_ctl': 'mosaic_get_filter_arg_ctl', 'Node': 'mosaic_Node', 'parse_regex': 'mosaic_parse_regex', 'create_regex_list': 'mosaic_create_regex_list', 'Graph': 'mosaic_Graph'}
TYPE_LABELS = {'mosaic_Emulator': 'Emulator', 'mosaic_Sandbox': 'Sandbox', 'mosaic_Filters': 'Filters', 'mosaic_Modifiers': 'Modifiers', 'mosaic_InlineModifier': 'InlineModifier', 'mosaic_Modifier': 'Modifier', 'mosaic_TerminalNode': 'TerminalNode', 'mosaic_NonTerminalNode': 'NonTerminalNode', 'mosaic_OperationNode': 'OperationNode', 'mosaic_ReducedVertice': 'ReducedVertice', 'mosaic_ReducedEdge': 'ReducedEdge', 'mosaic_ReducedGraph': 'ReducedGraph', 'mosaic_RegexParser': 'RegexParser', 'mosaic_SandboxData': 'SandboxData', 'mosaic_ReverseStringState': 'ReverseStringState', 'mosaic_SandboxString': 'SandboxString', 'mosaic_Node': 'Node', 'mosaic_Graph': 'Graph'}

def resource(boundary_name):
    return str(_BoundaryPath(__file__).parent.parent/'policymosaic'/'data'/boundary_name)

def decoder_invocation(*boundary_arguments):
    return [_boundary_sys.executable,'-m','policymosaic.profile_decoder',*boundary_arguments]

def frame_class(boundary_frame):
    for boundary_key,boundary_value in boundary_frame.frame.f_locals.items():
        if boundary_key=='self' or any(boundary_key.startswith(p+'_self_') for p in ('quay','meadow','mosaic')):
            return type_label(type(boundary_value))
        if boundary_key=='cls' or any(boundary_key.startswith(p+'_cls_') for p in ('quay','meadow','mosaic')):
            return type_label(boundary_value)
    return None

def application_frames():
    return [f for f in _boundary_inspect.stack() if f.frame.f_globals.get('__name__')!=__name__]

def type_label(boundary_type):
    boundary_name = getattr(boundary_type, '__name__', None)
    return TYPE_LABELS.get(boundary_name, boundary_name)

def attribute_name(boundary_owner, boundary_label):
    if isinstance(boundary_owner, _boundary_types.ModuleType):
        return getattr(boundary_owner, '__boundary_names__', {}).get(boundary_label, boundary_label)
    boundary_class = boundary_owner if isinstance(boundary_owner, type) else type(boundary_owner)
    boundary_map = getattr(boundary_class, '__boundary_names__', {})
    return boundary_map.get(boundary_label, boundary_label)

def read_attribute(boundary_owner, boundary_label, boundary_default=_MISSING):
    if boundary_label == '__name__' and isinstance(boundary_owner, type):
        return type_label(boundary_owner)
    boundary_target = attribute_name(boundary_owner, boundary_label)
    try:
        return getattr(boundary_owner, boundary_target)
    except AttributeError:
        try:
            return getattr(boundary_owner, boundary_label)
        except AttributeError:
            if boundary_default is _MISSING: raise
            return boundary_default

def write_attribute(boundary_owner, boundary_label, boundary_value):
    setattr(boundary_owner, attribute_name(boundary_owner, boundary_label), boundary_value)

def has_attribute(boundary_owner, boundary_label):
    try: read_attribute(boundary_owner,boundary_label); return True
    except AttributeError: return False

def remove_attribute(boundary_owner, boundary_label):
    delattr(boundary_owner, attribute_name(boundary_owner,boundary_label))

class AttributeBoundary:
    def __init__(boundary_self,boundary_owner): boundary_self.owner=boundary_owner
    def __getitem__(boundary_self,boundary_label): return read_attribute(boundary_self.owner,boundary_label)
    def __setitem__(boundary_self,boundary_label,boundary_value): write_attribute(boundary_self.owner,boundary_label,boundary_value)
    def __delitem__(boundary_self,boundary_label): remove_attribute(boundary_self.owner,boundary_label)

def attributes(boundary_owner): return AttributeBoundary(boundary_owner)

def callable_contract(boundary_parameters, boundary_label):
    def boundary_decorate(boundary_function):
        @_boundary_functools.wraps(boundary_function)
        def boundary_invoke(*boundary_values, **boundary_keywords):
            boundary_remapped = {boundary_parameters.get(boundary_key,boundary_key):boundary_value
                                 for boundary_key,boundary_value in boundary_keywords.items()}
            try:
                return boundary_function(*boundary_values,**boundary_remapped)
            except (TypeError,AttributeError,ValueError) as boundary_error:
                if boundary_error.args and isinstance(boundary_error.args[0],str):
                    boundary_message=boundary_error.args[0]
                    for boundary_new,boundary_old in TYPE_LABELS.items():
                        boundary_message=boundary_message.replace(boundary_new,boundary_old)
                    boundary_message=boundary_message.replace(boundary_function.__name__,boundary_label)
                    for boundary_old,boundary_new in boundary_parameters.items():
                        boundary_message=boundary_message.replace(boundary_new,boundary_old)
                    boundary_error.args=(boundary_message,)+boundary_error.args[1:]
                raise
        boundary_invoke.__wire_name__=boundary_label
        boundary_signature=_boundary_inspect.signature(boundary_function)
        boundary_reverse={value:key for key,value in boundary_parameters.items()}
        boundary_invoke.__signature__=boundary_signature.replace(parameters=[
            p.replace(name=boundary_reverse.get(p.name,p.name)) for p in boundary_signature.parameters.values()])
        return boundary_invoke
    return boundary_decorate

def class_contract(boundary_label, boundary_fields):
    def boundary_decorate(boundary_class):
        boundary_mapping={}
        for boundary_base in reversed(boundary_class.__mro__[1:]):
            boundary_mapping.update(getattr(boundary_base,'__boundary_names__',{}))
        boundary_mapping.update(boundary_fields)
        boundary_class.__boundary_names__=boundary_mapping
        boundary_class.__wire_name__=boundary_label
        if issubclass(boundary_class,_boundary_enum.Enum) and not issubclass(boundary_class,_boundary_enum.Flag) and '_missing_' not in vars(boundary_class):
            def boundary_missing(boundary_cls,boundary_value):
                raise ValueError(f'{boundary_value!r} is not a valid {boundary_label}')
            boundary_class._missing_=classmethod(boundary_missing)
        # Public entry points retain old spellings only at this boundary.
        for boundary_old,boundary_new in boundary_fields.items():
            if boundary_new in vars(boundary_class) and boundary_old not in vars(boundary_class):
                setattr(boundary_class,boundary_old,vars(boundary_class)[boundary_new])
        if not issubclass(boundary_class,tuple):
            boundary_setter=vars(boundary_class).get('__setattr__',object.__setattr__)
            boundary_deleter=vars(boundary_class).get('__delattr__',object.__delattr__)
            boundary_getter=vars(boundary_class).get('__getattr__')
            def boundary_store(boundary_self,boundary_key,boundary_value):
                boundary_setter(boundary_self,boundary_mapping.get(boundary_key,boundary_key),boundary_value)
            def boundary_fetch(boundary_self,boundary_key):
                boundary_key2=boundary_mapping.get(boundary_key,boundary_key)
                if any(boundary_key2 in vars(boundary_base) for boundary_base in type(boundary_self).__mro__):
                    return object.__getattribute__(boundary_self,boundary_key2)
                if boundary_key2!=boundary_key:
                    try:return object.__getattribute__(boundary_self,boundary_key2)
                    except AttributeError:pass
                if boundary_getter:return boundary_getter(boundary_self,boundary_key)
                raise AttributeError(f"'{boundary_label}' object has no attribute '{boundary_key}'")
            def boundary_delete(boundary_self,boundary_key):
                boundary_deleter(boundary_self,boundary_mapping.get(boundary_key,boundary_key))
            boundary_class.__setattr__=boundary_store
            boundary_class.__getattr__=boundary_fetch
            boundary_class.__delattr__=boundary_delete
        if hasattr(boundary_class,'__dataclass_fields__'):
            boundary_repr=boundary_class.__repr__
            def boundary_represent(boundary_self):
                return boundary_repr(boundary_self).replace(boundary_class.__name__+'(',boundary_label+'(',1)
            boundary_class.__repr__=boundary_represent
        return boundary_class
    return boundary_decorate

def named_record(boundary_label,boundary_fields,**boundary_options):
    boundary_name=GLOBAL_NAMES.get(boundary_label,boundary_label)
    boundary_record=_boundary_namedtuple(boundary_name,boundary_fields,**boundary_options)
    boundary_repr=boundary_record.__repr__
    boundary_record.__wire_name__=boundary_label
    boundary_record.__repr__=lambda boundary_self: boundary_repr(boundary_self).replace(boundary_name+'(',boundary_label+'(',1)
    return boundary_record

def module_contract(boundary_namespace, boundary_names):
    boundary_namespace['__boundary_names__']=boundary_names
    for boundary_old,boundary_new in boundary_names.items():
        if boundary_new in boundary_namespace:
            boundary_value=boundary_namespace[boundary_new]
            if isinstance(boundary_value,type) and any(base.__module__=='unittest.case' for base in boundary_value.__mro__):
                continue
            boundary_namespace.setdefault(boundary_old,boundary_namespace[boundary_new])
