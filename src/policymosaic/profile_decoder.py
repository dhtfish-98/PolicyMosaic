#!/usr/bin/env python3
# Derived from sandblaster_26; upstream copyright and BSD-3 license retained.
"""Finite local profile decoding with explicit layout and report boundaries."""
import argparse as mosaic_argparse
from collections import deque
import copy
import logging as mosaic_logging
import os as mosaic_os
from pathlib import Path
import re
import struct as mosaic_struct
import sys as mosaic_sys
import tempfile
import subprocess as mosaic_subprocess
import tqdm as mosaic_tqdm
import policymosaic_boundary as _name_boundary
import policymosaic.rule_graph as mosaic_operation_node
import policymosaic.filter_decoder as mosaic_sandbox_filter
import policymosaic.regex_graph as mosaic_sandbox_regex
from policymosaic.filter_catalog import mosaic_Filters
from policymosaic.safety import (PolicyFormatError, ProfileReader, read_exact, read_local,
    safe_component, write_exclusive, ReportBuffer, bounded_analysis, analysis_step,
    run_tool, publication_scope, INPUT_BYTES, OUTPUT_BYTES, MAX_NODES, MAX_PROFILES, MAX_DEPTH)

mosaic_REGEX_TABLE_OFFSET = 2
mosaic_REGEX_COUNT_OFFSET = 4
mosaic_VARS_TABLE_OFFSET = 6
mosaic_VARS_COUNT_OFFSET = 8
mosaic_NUM_PROFILES_OFFSET = 10
mosaic_PROFILE_OPS_OFFSET = 4
mosaic_OPERATION_NODE_SIZE = 8
mosaic_INDEX_SIZE = 2
mosaic_ios16_5_struct = mosaic_struct.Struct('<HHBBBxHHH')
mosaic_logger = mosaic_logging.getLogger(__name__)

@_name_boundary.class_contract('SandboxData', {'release': 'mosaic_release', 'data_file': 'mosaic_data_file', 'header_size': 'mosaic_header_size', 'type': 'mosaic_type', 'op_nodes_count': 'mosaic_op_nodes_count', 'sb_ops_count': 'mosaic_sb_ops_count', 'vars_count': 'mosaic_vars_count', 'states_count': 'mosaic_states_count', 'num_profiles': 'mosaic_num_profiles', 'regex_count': 'mosaic_regex_count', 'entitlements_count': 'mosaic_entitlements_count', 'regex_table_offset': 'mosaic_regex_table_offset', 'vars_offset': 'mosaic_vars_offset', 'states_offset': 'mosaic_states_offset', 'entitlements_offset': 'mosaic_entitlements_offset', 'profiles_offset': 'mosaic_profiles_offset', 'profiles_end_offset': 'mosaic_profiles_end_offset', 'operation_nodes_size': 'mosaic_operation_nodes_size', 'operation_nodes_offset': 'mosaic_operation_nodes_offset', 'base_addr': 'mosaic_base_addr', 'regex_list': 'mosaic_regex_list', 'global_vars': 'mosaic_global_vars', 'policies': 'mosaic_policies', 'sb_ops': 'mosaic_sb_ops', 'operation_nodes': 'mosaic_operation_nodes', 'ops_to_reverse': 'mosaic_ops_to_reverse'})
class mosaic_SandboxData:
    def __init__(self, release, ios16_struct_size, header, op_nodes_count, sb_ops_count,
                 vars_count, states_count, num_profiles, regex_count,
                 entitlements_count, instructions_count):
        values = (release, ios16_struct_size, header, op_nodes_count, sb_ops_count,
                  vars_count, states_count, num_profiles, regex_count,
                  entitlements_count, instructions_count)
        if any(type(value) is not int or value < 0 for value in values):
            raise PolicyFormatError('layout fields must be nonnegative integers')
        self.release = release
        self.data_file = None
        self.header_size = ios16_struct_size
        self.type = header
        self.op_nodes_count = op_nodes_count
        self.sb_ops_count = sb_ops_count
        self.vars_count = vars_count
        self.states_count = states_count
        self.num_profiles = num_profiles
        self.regex_count = regex_count
        self.entitlements_count = entitlements_count
        self.regex_table_offset = ios16_struct_size + (2 if release > 17 else 0)
        self.vars_offset = self.regex_table_offset + regex_count * 2
        self.states_offset = self.vars_offset + vars_count * 2
        self.entitlements_offset = self.states_offset + states_count * 2
        self.profiles_offset = self.entitlements_offset + entitlements_count * 2
        if release > 17 and entitlements_count:
            self.profiles_offset += 72 + (4 if release > 18 else 0)
        profile_prefix = 8 if release > 17 else 4
        self.profiles_end_offset = self.profiles_offset + num_profiles * (sb_ops_count * 2 + profile_prefix)
        nodes_start = self.profiles_end_offset + (sb_ops_count * 2 if not header else 0)
        self.operation_nodes_offset = (nodes_start + 7) & ~7
        self.operation_nodes_size = op_nodes_count * 8
        self.base_addr = self.operation_nodes_offset + self.operation_nodes_size
        self.regex_list = None
        self.global_vars = None
        self.policies = None
        self.sb_ops = None
        self.operation_nodes = None
        self.ops_to_reverse = None

    @_name_boundary.callable_contract({'self': 'mosaic_self_5b6c255'}, '__repr__')
    def __repr__(mosaic_self_5b6c255) -> str:
        return f"\n                struct_size: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['header_size'])}\n                header: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['type'])}\n                op_nodes_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['op_nodes_count'])}\n                sb_ops_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['sb_ops_count'])}\n                vars_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['vars_count'])}\n                states_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['states_count'])}\n                num_profiles: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['num_profiles'])}\n                re_table_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['regex_count'])}\n                entitlements_count: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['entitlements_count'])}\n\n                regex_table_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['regex_table_offset'])}\n                pattern_vars_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['vars_offset'])}\n                states_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['states_offset'])}\n                entitlements_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['entitlements_offset'])}\n                profiles_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['profiles_offset'])}\n                profiles_end_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['profiles_end_offset'])}\n                operation_nodes_offset: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['operation_nodes_offset'])}\n                operation_nodes_size: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['operation_nodes_size'])}\n                base_adrr: {hex(_name_boundary.attributes(mosaic_self_5b6c255)['base_addr'])}\n                "

def mosaic_parse_profile(infile, args):
    infile.seek(0)
    fields = mosaic_struct.unpack('<HHBBBxHHHH', read_exact(infile, 16))
    try:
        release = int(args.release)
    except (ValueError, TypeError, AttributeError) as error:
        raise PolicyFormatError('release must be a supported integer layout selector') from error
    if release not in (17, 18, 19, 20, 21, 22, 23, 24, 25, 26):
        raise PolicyFormatError('unsupported profile layout release')
    header, nodes, operations, variables, states, profiles, regexes, entitlements, instructions = fields
    if header not in (0, 0x8000):
        raise PolicyFormatError('unsupported profile header')
    # The upstream release 18+ dialect swaps these wire fields by bundle kind.
    if release == 17:
        counts = (profiles, regexes, entitlements)
    elif header == 0:
        counts = (entitlements, profiles, regexes)
    else:
        counts = (regexes, entitlements, profiles)
    data = mosaic_SandboxData(release, 14, header, nodes, operations, variables,
                             states, *counts, instructions)
    data.data_file = infile
    return data


def mosaic_extract_string_from_offset(f, offset, base_addr):
    if type(offset) is not int or offset < 0 or type(base_addr) is not int or base_addr < 0:
        raise PolicyFormatError('invalid string offset')
    f.seek(base_addr + offset * 8)
    length = mosaic_struct.unpack('<H', read_exact(f, 2))[0]
    if not length:
        raise PolicyFormatError('zero-length string record')
    try:
        return read_exact(f, length - 1).decode('utf-8')
    except UnicodeDecodeError as error:
        raise PolicyFormatError('invalid UTF-8 string record') from error


def mosaic_get_global_vars(f, vars_offset, num_vars, base_address):
    offsets = mosaic_get_policies(f, vars_offset, num_vars)
    return [mosaic_extract_string_from_offset(f, offset, base_address) for offset in offsets]


def mosaic_get_policies(f, offset, count):
    if type(count) is not int or not 0 <= count <= 65535:
        raise PolicyFormatError('invalid index count')
    f.seek(offset)
    return mosaic_struct.unpack('<%dH' % count, read_exact(f, count * 2))


def _profile_size(data):
    return data.sb_ops_count * 2 + (8 if data.release > 17 else 4)


def mosaic_display_sandbox_profiles(infile, profiles_offset, num_profiles, base_addr):
    if not 0 <= num_profiles <= MAX_PROFILES:
        raise PolicyFormatError('profile count exceeds limit')
    # Legacy direct API does not supply operations/release; derive the validated
    # layout from its data file when possible, rather than assuming 376-byte rows.
    data = getattr(infile, '_policy_data', None)
    if data is None:
        raise PolicyFormatError('profile listing requires validated layout context')
    names = []
    for index in range(num_profiles):
        infile.seek(profiles_offset + _profile_size(data) * index)
        name_offset = mosaic_struct.unpack('<H', read_exact(infile, 2))[0]
        names.append(mosaic_extract_string_from_offset(infile, name_offset, base_addr))
    for name in names:
        print(name.encode('unicode_escape').decode('ascii'))
    return names


def mosaic_read_sandbox_operations(parser, args, sandbox_data):
    try:
        text = read_local(args.operations_file, 1024 * 1024).decode('utf-8')
    except UnicodeDecodeError as error:
        raise PolicyFormatError('operations file is not UTF-8') from error
    operations = text.splitlines()
    operations = [line.strip() for line in operations]
    if len(operations) != sandbox_data.sb_ops_count or not operations or len(set(operations)) != len(operations):
        raise PolicyFormatError('operation labels must be unique and match the profile count')
    if any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.*-]{0,127}', label) for label in operations):
        raise PolicyFormatError('invalid operation label')
    sandbox_data.sb_ops = operations
    selected = args.operation or []
    if any(label not in operations for label in selected):
        raise PolicyFormatError('requested operation is unavailable')
    sandbox_data.ops_to_reverse = selected or None


def mosaic_parse_regex_list(infile, sandbox_data):
    offsets = mosaic_get_policies(infile, sandbox_data.regex_table_offset, sandbox_data.regex_count)
    result = []
    with bounded_analysis():
        for offset in offsets:
            analysis_step()
            infile.seek(sandbox_data.base_addr + offset * 8)
            length = mosaic_struct.unpack('<H', read_exact(infile, 2))[0]
            result.append(mosaic_sandbox_regex.parse_regex(tuple(read_exact(infile, length))))
    sandbox_data.regex_list = result


def _validate_links(nodes):
    # Both match/unmatch and inline policy references must terminate. Shared
    # children are allowed. Graph depth bounds the retained recursive formatter.
    colors = {}
    heights = {}

    def children_of(node):
        if node.non_terminal:
            return [node.non_terminal.match, node.non_terminal.unmatch]
        if node.terminal and node.terminal.inline_operation_node:
            return [node.terminal.inline_operation_node]
        return []

    for start in nodes:
        if colors.get(id(start)) == 2:
            continue
        pending = [(start, False, 0)]
        while pending:
            analysis_step()
            node, finished, depth = pending.pop()
            identity = id(node)
            if finished:
                children = children_of(node)
                height = 1 + max((heights[id(child)] for child in children), default=0)
                if height > MAX_DEPTH:
                    raise PolicyFormatError('operation graph depth exceeds limit')
                heights[identity] = height
                colors[identity] = 2
                continue
            if colors.get(identity) == 1:
                raise PolicyFormatError('cyclic operation graph')
            if colors.get(identity) == 2:
                continue
            if depth > MAX_DEPTH:
                raise PolicyFormatError('operation graph depth exceeds limit')
            colors[identity] = 1
            pending.append((node, True, depth))
            children = children_of(node)
            if any(child is None for child in children):
                raise PolicyFormatError('missing operation graph reference')
            pending.extend((child, False, depth + 1) for child in reversed(children))


def mosaic_create_operation_nodes(infile, sandbox_data, keep_builtin_filters):
    if not 1 <= sandbox_data.op_nodes_count <= MAX_NODES:
        raise PolicyFormatError('operation node count exceeds limit or is empty')
    nodes = mosaic_operation_node.build_operation_nodes(infile, sandbox_data.op_nodes_count)
    sandbox_data.operation_nodes = nodes
    for node in nodes:
        analysis_step()
        node.convert_filter(mosaic_sandbox_filter.convert_filter_callback, infile, sandbox_data, keep_builtin_filters)
    _validate_links(nodes)
    return nodes


def mosaic_node_to_c(node):
    pending = deque([node])
    visited = set()
    output = ReportBuffer()
    while pending:
        analysis_step()
        current = pending.popleft()
        if id(current) in visited:
            continue
        visited.add(id(current))
        if len(visited) > MAX_NODES:
            raise PolicyFormatError('operation graph size exceeds limit')
        output.write('node_%x:; // %r\n' % (current.offset, current.raw))
        if current.terminal:
            output.write(current.c_repr() + '\n\n')
        else:
            branch = current.non_terminal
            if branch is None or branch.match is None or branch.unmatch is None:
                raise PolicyFormatError('missing C graph reference')
            output.write('if (%s) goto node_%x;\nelse goto node_%x;\n\n' %
                         (current.c_repr(), branch.match_offset, branch.unmatch_offset))
            pending.extend((branch.match, branch.unmatch))
    return output.getvalue().strip()


def mosaic_process_profile(infile, outfname, sb_ops, ops_to_reverse, op_table, operation_nodes, c_output, macho):
    if not op_table or len(op_table) != len(sb_ops):
        raise PolicyFormatError('operation table and labels differ')
    if any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.*-]{0,127}', label) for label in sb_ops):
        raise PolicyFormatError('invalid operation label')
    output_name = Path(outfname)
    safe_component(output_name.name)
    c_output = bool(c_output or macho)
    nodes = {node.offset: node for node in operation_nodes}
    if len(nodes) != len(operation_nodes) or any(offset not in nodes for offset in op_table):
        raise PolicyFormatError('operation table contains an invalid node reference')
    default = nodes[op_table[0]]
    if not default.terminal:
        raise PolicyFormatError('default operation must be terminal')
    output = ReportBuffer()
    with bounded_analysis():
        if c_output:
            for name in ('allow(const char *)', 'deny(const char *)', 'unparsed_filter()', 'subpath()', 'subpath_prefix()'):
                output.write('extern long %s;\n' % name)
            for entry in mosaic_Filters.filters.values():
                name = entry['name'] or 'literal'
                for suffix in ('', '_regex', '_literal', '_prefix'):
                    output.write('extern long %s%s();\n' % (name.replace('-', '_'), suffix))
        else:
            output.write('(version 1)\n(%s default)\n' % default.terminal)
        for index, offset in enumerate(op_table[1:], 1):
            analysis_step()
            operation = sb_ops[index]
            if ops_to_reverse and operation not in ops_to_reverse:
                continue
            node = nodes[offset]
            if c_output:
                output.write('long %s()\n{\n' % operation.replace('-', '_').replace('*', '$'))
                output.write(mosaic_node_to_c(node))
                output.write('\n}\n\n')
                continue
            # Upstream reducer carries mutable per-operation traversal state.
            # Clear it and rebuild fresh nodes per profile in the caller.
            fresh_nodes = {item.offset: item for item in copy.deepcopy(operation_nodes)}
            node = fresh_nodes[offset]
            fresh_default = fresh_nodes[op_table[0]]
            mosaic_operation_node.mosaic_processed_nodes.clear()
            graph = mosaic_operation_node.build_operation_node_graph(node, fresh_default)
            if graph:
                reduced = mosaic_operation_node.reduce_operation_node_graph(graph)
                reduced.str_simple_with_metanodes()
                reduced.print_vertices_with_operation_metanodes(operation, default.terminal.is_allow(), output)
            elif node.terminal and (node.terminal.type != default.terminal.type or any(node.terminal.db_modifiers.values())):
                output.write('(%s %s)\n' % (node.terminal, operation))
    suffix = '.c' if c_output else '.sb'
    report = output.getvalue().encode('utf-8')
    if macho:
        # The generated representation is never run. Compile in a private
        # temporary directory and publish only a bounded, validated regular file.
        with tempfile.TemporaryDirectory(prefix='policymosaic-compile-') as folder:
            source = Path(folder) / 'profile.c'
            binary = Path(folder) / 'profile.macho'
            write_exclusive(source, report)
            run_tool(['clang', str(source), '-dynamiclib', '-g', '-O0', '-undefined', 'dynamic_lookup',
                      '-Wno-everything', '-o', str(binary)])
            compiled = read_local(binary, OUTPUT_BYTES)
            if len(compiled) < 32 or compiled[:4] != b'\xcf\xfa\xed\xfe' or mosaic_struct.unpack_from('<I', compiled, 12)[0] != 6:
                raise PolicyFormatError('compiler did not produce a 64-bit Mach-O dynamic library report')
        write_exclusive(str(output_name) + suffix, report)
        write_exclusive(output_name, compiled)
    else:
        write_exclusive(str(output_name) + suffix, report)
    return str(output_name) + suffix


def mosaic_main():
    parser = mosaic_argparse.ArgumentParser(description='Inspect an authorized local binary sandbox profile; reports do not prove runtime policy.')
    parser.add_argument('filename')
    parser.add_argument('-r', '--release', required=True)
    parser.add_argument('-o', '--operations_file', required=True)
    parser.add_argument('-p', '--profile', nargs='+')
    parser.add_argument('-n', '--operation', nargs='+')
    parser.add_argument('-d', '--directory')
    parser.add_argument('-psb', '--print_sandbox_profiles', action='store_true')
    parser.add_argument('-kbf', '--keep_builtin_filters', action='store_true')
    parser.add_argument('-c', '--c_output', action='store_true')
    parser.add_argument('-m', '--macho', action='store_true', help='compile the C report with clang; does not run it')
    args = parser.parse_args()
    try:
        with bounded_analysis(), publication_scope():
            reader = ProfileReader(read_local(args.filename))
            data = mosaic_parse_profile(reader, args)
            reader._policy_data = data
            if data.base_addr > len(reader.getbuffer()) or data.num_profiles > MAX_PROFILES:
                raise PolicyFormatError('profile layout exceeds input or profile count limit')
            if not 1 <= data.op_nodes_count <= MAX_NODES:
                raise PolicyFormatError('operation node count exceeds limit or is empty')
            mosaic_read_sandbox_operations(parser, args, data)
            if args.print_sandbox_profiles:
                if data.type != 0x8000:
                    raise PolicyFormatError('profile listing requires a bundle')
                mosaic_display_sandbox_profiles(reader, data.profiles_offset, data.num_profiles, data.base_addr)
                return 0
            mosaic_parse_regex_list(reader, data)
            data.global_vars = mosaic_get_global_vars(reader, data.vars_offset, data.vars_count, data.base_addr)
            data.policies = mosaic_get_policies(reader, data.entitlements_offset, data.entitlements_count)
            directory = Path(args.directory or mosaic_os.getcwd())
            plans = []
            count = data.num_profiles if data.type else 1
            for index in range(count):
                analysis_step()
                offset = data.profiles_offset + (_profile_size(data) * index if data.type else 0)
                if data.type:
                    reader.seek(offset)
                    name_offset = mosaic_struct.unpack('<H', read_exact(reader, 2))[0]
                    name = mosaic_extract_string_from_offset(reader, name_offset, data.base_addr)
                    if args.profile and name not in args.profile:
                        continue
                    prefix = 8 if data.release > 17 else 4
                else:
                    name = Path(args.filename).stem
                    prefix = 0
                component = safe_component(name)
                if component in {plan[0] for plan in plans}:
                    raise PolicyFormatError('derived profile output names collide')
                table = mosaic_get_policies(reader, offset + prefix, data.sb_ops_count)
                plans.append((component, table))
            for component, table in plans:
                reader.seek(data.operation_nodes_offset)
                nodes = mosaic_create_operation_nodes(reader, data, args.keep_builtin_filters)
                mosaic_process_profile(reader, str(directory / component), data.sb_ops,
                    data.ops_to_reverse, table, nodes, args.c_output, args.macho)
        return 0
    except (PolicyFormatError, OSError, UnicodeError, IndexError, KeyError, AssertionError, RecursionError) as error:
        # Do not print raw input payloads, external diagnostics, or account data.
        detail = str(error) if isinstance(error, PolicyFormatError) else 'profile inspection could not complete'
        print('PolicyMosaic: ' + detail, file=mosaic_sys.stderr)
        return 2


_name_boundary.module_contract(globals(), {'INDEX_SIZE': 'mosaic_INDEX_SIZE', 'create_operation_nodes': 'mosaic_create_operation_nodes', 'process_profile': 'mosaic_process_profile', 'os': 'mosaic_os', 'get_policies': 'mosaic_get_policies', 'node_to_c': 'mosaic_node_to_c', 'NUM_PROFILES_OFFSET': 'mosaic_NUM_PROFILES_OFFSET', 'REGEX_COUNT_OFFSET': 'mosaic_REGEX_COUNT_OFFSET', 'logging': 'mosaic_logging', 'Filters': 'mosaic_Filters', 'VARS_COUNT_OFFSET': 'mosaic_VARS_COUNT_OFFSET', 'sandbox_regex': 'mosaic_sandbox_regex', 'operation_node': 'mosaic_operation_node', 'get_global_vars': 'mosaic_get_global_vars', 'subprocess': 'mosaic_subprocess', 'struct': 'mosaic_struct', 'logger': 'mosaic_logger', 'parse_profile': 'mosaic_parse_profile', 'parse_regex_list': 'mosaic_parse_regex_list', 'argparse': 'mosaic_argparse', 'PROFILE_OPS_OFFSET': 'mosaic_PROFILE_OPS_OFFSET', 'main': 'mosaic_main', 'sys': 'mosaic_sys', 'display_sandbox_profiles': 'mosaic_display_sandbox_profiles', 'ios16_5_struct': 'mosaic_ios16_5_struct', 'VARS_TABLE_OFFSET': 'mosaic_VARS_TABLE_OFFSET', 'sandbox_filter': 'mosaic_sandbox_filter', 'read_sandbox_operations': 'mosaic_read_sandbox_operations', 'extract_string_from_offset': 'mosaic_extract_string_from_offset', 'OPERATION_NODE_SIZE': 'mosaic_OPERATION_NODE_SIZE', 'tqdm': 'mosaic_tqdm', 'REGEX_TABLE_OFFSET': 'mosaic_REGEX_TABLE_OFFSET', 'SandboxData': 'mosaic_SandboxData'})
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
