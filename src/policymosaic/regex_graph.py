# Derived from sandblaster_26; BSD-3-Clause attribution retained in LICENSE/ORIGIN.md.
"""Finite NFA reduction with explicit epsilon closure and regular-expression algebra."""
import logging
import re as _re
import struct
import sys
from dataclasses import dataclass
import policymosaic_boundary as _name_boundary
from policymosaic.regex_bytecode import mosaic_RegexParser
from policymosaic.safety import (PolicyFormatError, MAX_NODES, MAX_DEPTH, MAX_ITEMS,
    OUTPUT_BYTES, TOTAL_REPORT_BYTES, ProfileReader, ReportBuffer, read_local, read_exact,
    bounded_analysis, analysis_step, analysis_guard)

mosaic_logger = logging.getLogger(__name__)
_NODE_NAMES = {'TYPE_JUMP_FORWARD': 'mosaic_TYPE_JUMP_FORWARD', 'TYPE_JUMP_BACKWARD': 'mosaic_TYPE_JUMP_BACKWARD', 'TYPE_CHARACTER': 'mosaic_TYPE_CHARACTER', 'TYPE_END': 'mosaic_TYPE_END', 'FLAG_WHITE': 'mosaic_FLAG_WHITE', 'FLAG_GREY': 'mosaic_FLAG_GREY', 'FLAG_BLACK': 'mosaic_FLAG_BLACK', 'name': 'mosaic_name', 'type': 'mosaic_type', 'value': 'mosaic_value', 'flag': 'mosaic_flag', 'set_name': 'mosaic_set_name', 'set_type_jump_forward': 'mosaic_set_type_jump_forward', 'set_type_jump_backward': 'mosaic_set_type_jump_backward', 'set_type_character': 'mosaic_set_type_character', 'set_type_end': 'mosaic_set_type_end', 'is_type_end': 'mosaic_is_type_end', 'is_type_jump': 'mosaic_is_type_jump', 'is_type_jump_backward': 'mosaic_is_type_jump_backward', 'is_type_jump_forward': 'mosaic_is_type_jump_forward', 'is_type_character': 'mosaic_is_type_character', 'set_value': 'mosaic_set_value', 'set_flag_white': 'mosaic_set_flag_white', 'set_flag_grey': 'mosaic_set_flag_grey', 'set_flag_black': 'mosaic_set_flag_black'}
_GRAPH_NAMES = {'graph_dict': 'mosaic_graph_dict', 'canon_graph_dict': 'mosaic_canon_graph_dict', 'node_list': 'mosaic_node_list', 'start_node': 'mosaic_start_node', 'end_states': 'mosaic_end_states', 'start_state': 'mosaic_start_state', 'regex': 'mosaic_regex', 'unified_regex': 'mosaic_unified_regex', 'add_node': 'mosaic_add_node', 'has_node': 'mosaic_has_node', 'update_node': 'mosaic_update_node', 'add_new_next_to_node': 'mosaic_add_new_next_to_node', 'get_node_for_idx': 'mosaic_get_node_for_idx', 'get_re_index_for_pos': 'mosaic_get_re_index_for_pos', 'fill_from_regex_list': 'mosaic_fill_from_regex_list', 'get_character_nodes': 'mosaic_get_character_nodes', 'find_node_type_jump': 'mosaic_find_node_type_jump', 'reduce': 'mosaic_reduce', 'get_edges': 'mosaic_get_edges', 'convert_to_canonical': 'mosaic_convert_to_canonical', 'need_use_plus': 'mosaic_need_use_plus', 'unify_two_strings': 'mosaic_unify_two_strings', 'unify_strings': 'mosaic_unify_strings', 'remove_state': 'mosaic_remove_state', 'simplify': 'mosaic_simplify', 'combine_start_end_nodes': 'mosaic_combine_start_end_nodes'}


@_name_boundary.class_contract('Node', _NODE_NAMES)
class mosaic_Node:
    mosaic_TYPE_JUMP_FORWARD = 1
    mosaic_TYPE_JUMP_BACKWARD = 2
    mosaic_TYPE_CHARACTER = 3
    mosaic_TYPE_END = 4
    mosaic_FLAG_WHITE = 1
    mosaic_FLAG_GREY = 2
    mosaic_FLAG_BLACK = 3

    def __init__(self, name=None, type=None, value=''):
        if not isinstance(value, str) or len(value.encode('utf-8')) > OUTPUT_BYTES:
            raise PolicyFormatError('invalid or over-limit regex node value')
        self.name, self.type, self.value, self.flag = name, type, value, self.FLAG_WHITE

    def mosaic_set_name(self, name): self.name = name
    def mosaic_set_value(self, value):
        if not isinstance(value, str) or len(value.encode('utf-8')) > OUTPUT_BYTES:
            raise PolicyFormatError('invalid or over-limit regex node value')
        self.value = value
    def mosaic_set_type_jump_forward(self): self.type = self.TYPE_JUMP_FORWARD
    def mosaic_set_type_jump_backward(self): self.type = self.TYPE_JUMP_BACKWARD
    def mosaic_set_type_character(self): self.type = self.TYPE_CHARACTER
    def mosaic_set_type_end(self): self.type = self.TYPE_END
    def mosaic_is_type_end(self): return self.type == self.TYPE_END
    def mosaic_is_type_jump(self): return self.type in (self.TYPE_JUMP_FORWARD, self.TYPE_JUMP_BACKWARD)
    def mosaic_is_type_jump_backward(self): return self.type == self.TYPE_JUMP_BACKWARD
    def mosaic_is_type_jump_forward(self): return self.type == self.TYPE_JUMP_FORWARD
    def mosaic_is_type_character(self): return self.type == self.TYPE_CHARACTER
    def mosaic_set_flag_white(self): self.flag = self.FLAG_WHITE
    def mosaic_set_flag_grey(self): self.flag = self.FLAG_GREY
    def mosaic_set_flag_black(self): self.flag = self.FLAG_BLACK

    def __str__(self):
        label = {self.TYPE_JUMP_FORWARD: 'jump forward', self.TYPE_JUMP_BACKWARD: 'jump backward', self.TYPE_END: 'end'}.get(self.type, self.value)
        return '(%s: %s)' % (self.name, label)


@dataclass(frozen=True)
class _Expression:
    uid: int
    kind: str
    children: tuple
    text: str
    size: int
    depth: int


class _Algebra:
    """Per-analysis immutable expression DAG; None denotes the empty language."""
    def __init__(self):
        self.nodes = {}
        self.epsilon = self._make('atom', (), '')

    def _make(self, kind, children, text=''):
        analysis_step()
        key = kind, tuple(child.uid for child in children), text
        if key in self.nodes:
            return self.nodes[key]
        if len(self.nodes) >= MAX_ITEMS:
            raise PolicyFormatError('regex expression count exceeds limit')
        depth = 1 + max((child.depth for child in children), default=0)
        size = len(text.encode('utf-8')) + sum(child.size + 2 for child in children) + len(children) + 4
        if depth > MAX_DEPTH or size > OUTPUT_BYTES:
            raise PolicyFormatError('regex expression depth or expansion exceeds limit')
        node = _Expression(len(self.nodes), kind, children, text, size, depth)
        self.nodes[key] = node
        return node

    def atom(self, text):
        if not isinstance(text, str) or len(text.encode('utf-8')) > OUTPUT_BYTES:
            raise PolicyFormatError('invalid regex transition label')
        return self._make('atom', (), text)

    def union(self, *nodes):
        children, seen = [], set()
        for node in nodes:
            analysis_step()
            if node is None:
                continue
            for child in (node.children if node.kind == 'union' else (node,)):
                analysis_step()
                if child.uid not in seen:
                    children.append(child); seen.add(child.uid)
        if len(children) > MAX_ITEMS:
            raise PolicyFormatError('regex alternatives exceed limit')
        return None if not children else children[0] if len(children) == 1 else self._make('union', tuple(children))

    def sequence(self, *nodes):
        children = []
        for node in nodes:
            analysis_step()
            if node is None:
                return None
            if node is self.epsilon:
                continue
            children.extend(node.children if node.kind == 'sequence' else (node,))
        if len(children) > MAX_ITEMS:
            raise PolicyFormatError('regex sequence exceeds limit')
        return self.epsilon if not children else children[0] if len(children) == 1 else self._make('sequence', tuple(children))

    def star(self, node):
        if node is None or node is self.epsilon:
            return self.epsilon
        return node if node.kind == 'star' else self._make('star', (node,))

    def render(self, node):
        if node is None:
            return None
        result, size = [], 0
        pending = [(node, 0)]
        while pending:
            analysis_step()
            value, parent = pending.pop()
            if isinstance(value, str):
                size += len(value.encode('utf-8'))
                if size > OUTPUT_BYTES:
                    raise PolicyFormatError('regex presentation exceeds limit')
                result.append(value)
                continue
            if value.kind == 'atom':
                precedence = _fragment_precedence(value.text)
                parts = [value.text]
            elif value.kind == 'union':
                precedence = 1
                parts = []
                for index, child in enumerate(value.children):
                    if index: parts.append('|')
                    parts.append((child, precedence))
            elif value.kind == 'sequence':
                precedence = 2
                parts = [(child, precedence) for child in value.children]
            else:
                precedence = 3
                # Group even a zero-width anchor: a bare ^* or $* is invalid.
                parts = ['(', (value.children[0], 0), ')*']
            if precedence < parent:
                parts = ['('] + parts + [')']
            pending.extend((part, 0) if isinstance(part, str) else part for part in reversed(parts))
        return ''.join(result)


def _fragment_precedence(text):
    """Recognize top-level alternatives without splitting escaped/class data."""
    depth, in_class, escaped, first_close = 0, False, False, None
    alternative = False
    for index, character in enumerate(text):
        analysis_step()
        if escaped:
            escaped = False
            continue
        if character == '\\':
            escaped = True
            continue
        if in_class:
            if character == ']':
                in_class = False
                if text.startswith('[') and first_close is None: first_close = index
            continue
        if character == '[': in_class = True
        elif character == '(':
            depth += 1
            if depth > MAX_DEPTH: raise PolicyFormatError('regex fragment depth exceeds limit')
        elif character == ')':
            depth -= 1
            if depth < 0: raise PolicyFormatError('unbalanced regex transition label')
            if depth == 0 and text.startswith('(') and first_close is None: first_close = index
        elif character == '|' and depth == 0: alternative = True
    if depth or in_class or escaped: raise PolicyFormatError('incomplete regex transition label')
    if alternative: return 1
    if len(text) <= 1 or first_close == len(text) - 1 or (text.startswith('\\') and len(text) in (2, 4)): return 4
    return 2


def _eliminate(edges, state, algebra):
    """R(i,j) := R(i,j) | R(i,k) R(k,k)* R(k,j), from a frozen edge snapshot."""
    incoming = [(source, value) for (source, target), value in edges.items() if target == state and source != state]
    outgoing = [(target, value) for (source, target), value in edges.items() if source == state and target != state]
    loop = algebra.star(edges.get((state, state)))
    result = {pair: value for pair, value in edges.items() if state not in pair}
    for source, before in incoming:
        analysis_step()
        for target, after in outgoing:
            analysis_step()
            pair = source, target
            result[pair] = algebra.union(result.get(pair), algebra.sequence(before, loop, after))
            if len(result) > MAX_ITEMS:
                raise PolicyFormatError('regex canonical edge count exceeds limit')
    return result


@_name_boundary.class_contract('Graph', _GRAPH_NAMES)
class mosaic_Graph:
    def __init__(self):
        self.graph_dict, self.canon_graph_dict, self.node_list = {}, {}, []
        self.start_node, self.start_state, self.end_states = None, -1, []
        self.regex, self.unified_regex = [], ''

    @analysis_guard
    def mosaic_add_node(self, node, next_list=None):
        if not isinstance(node, mosaic_Node) or len(self.graph_dict) >= MAX_NODES and node not in self.graph_dict:
            raise PolicyFormatError('invalid or over-limit regex node')
        self.graph_dict[node] = list(next_list or ())

    def mosaic_has_node(self, node): return node in self.graph_dict
    def mosaic_update_node(self, node, next_list): self.mosaic_add_node(node, next_list)
    def mosaic_add_new_next_to_node(self, node, next):
        if len(self.graph_dict[node]) >= MAX_NODES:
            raise PolicyFormatError('regex adjacency exceeds limit')
        self.graph_dict[node].append(next)

    def mosaic_get_node_for_idx(self, idx):
        return self.node_list[idx] if type(idx) is int and 0 <= idx < len(self.node_list) else None

    def mosaic_get_re_index_for_pos(self, regex_list, pos):
        for candidate in (pos, pos + 1):
            for index, record in enumerate(regex_list):
                analysis_step()
                if record['pos'] == candidate: return index
        return -1

    @analysis_guard
    def mosaic_fill_from_regex_list(self, regex_list):
        if not isinstance(regex_list, (list, tuple)) or not 0 < len(regex_list) <= MAX_NODES:
            raise PolicyFormatError('invalid or over-limit regex records')
        positions = {}
        types = {'jump_forward': 1, 'jump_backward': 2, 'character': 3, 'class': 3, 'class_exclude': 3, 'end': 4}
        nodes = []
        for index, record in enumerate(regex_list):
            analysis_step()
            if not isinstance(record, dict) or set(record) != {'pos', 'type', 'value'} or type(record['pos']) is not int or record['pos'] in positions or not isinstance(record['type'], str) or record['type'] not in types:
                raise PolicyFormatError('invalid or duplicate regex record')
            positions[record['pos']] = index
            nodes.append(mosaic_Node(str(index), types[record['type']], record['value'] if types[record['type']] == 3 else ''))
        graph = {}
        for index, (record, node) in enumerate(zip(regex_list, nodes)):
            analysis_step()
            targets = []
            if node.is_type_jump():
                target = record['value']
                if type(target) is not int:
                    raise PolicyFormatError('invalid regex jump target')
                found = positions.get(target, positions.get(target + 1))
                if found is None:
                    raise PolicyFormatError('regex jump target outside instruction records')
                if node.is_type_jump_forward() and index + 1 < len(nodes): targets.append(nodes[index + 1])
                targets.append(nodes[found])
            elif node.is_type_character():
                if not isinstance(node.value, str): raise PolicyFormatError('invalid regex character label')
                if index + 1 < len(nodes): targets.append(nodes[index + 1])
            graph[node] = list(dict.fromkeys(targets))
        if not any(node.is_type_end() for node in nodes):
            raise PolicyFormatError('regex program has no accepting record')
        self.node_list, self.graph_dict, self.start_node = nodes, graph, nodes[0]
        self.canon_graph_dict, self.end_states, self.regex = {}, [], []
        self.start_state, self.unified_regex = -1, ''

    def _closure(self, starts, graph):
        result, seen, pending = [], set(), list(reversed(starts))
        while pending:
            analysis_step()
            node = pending.pop()
            if not isinstance(node, mosaic_Node): raise PolicyFormatError('invalid regex adjacency node')
            if node in seen: continue
            if node not in graph: raise PolicyFormatError('regex edge references an unknown node')
            seen.add(node)
            if len(seen) > MAX_NODES: raise PolicyFormatError('regex graph size exceeds limit')
            if node.is_type_character() or node.is_type_end(): result.append(node)
            elif node.is_type_jump(): pending.extend(reversed(graph[node]))
            else: raise PolicyFormatError('unsupported regex node type')
        return result

    @analysis_guard
    def mosaic_get_character_nodes(self, node): return self._closure(self.graph_dict[node], self.graph_dict)

    @analysis_guard
    def mosaic_find_node_type_jump(self, current_node, node, backup_dict):
        pending, seen = [current_node], set()
        while pending:
            analysis_step()
            current = pending.pop()
            if current in seen or not current.is_type_jump(): continue
            if current is node: return True
            seen.add(current)
            if len(seen) > MAX_NODES: raise PolicyFormatError('regex graph size exceeds limit')
            pending.extend(backup_dict.get(current, ()))
        return False

    @analysis_guard
    def mosaic_reduce(self):
        if not self.graph_dict: raise PolicyFormatError('empty regex graph')
        if self.start_node is None:
            self.start_node = next((node for node in self.graph_dict if node.name == '0'), next(iter(self.graph_dict)))
        original = {node: tuple(targets) for node, targets in self.graph_dict.items()}
        if len(original) > MAX_NODES: raise PolicyFormatError('regex graph size exceeds limit')
        reduced, indices = {}, set()
        for node in original:
            analysis_step()
            if not isinstance(node, mosaic_Node): raise PolicyFormatError('invalid regex graph node')
            if not isinstance(node.name, str) or not node.name.isascii() or not node.name.isdecimal() or len(node.name) > 4 or int(node.name) >= MAX_NODES or int(node.name) in indices:
                raise PolicyFormatError('invalid or duplicate regex node index')
            indices.add(int(node.name))
            if not node.is_type_jump(): reduced[node] = self._closure(original[node], original)
        # Keep the original entry closure independently: an initial epsilon split
        # can accept empty input or enter several character states.
        self._entry_nodes = self._closure([self.start_node], original)
        self.graph_dict = reduced

    def mosaic_get_edges(self, node):
        targets = self.graph_dict[node]
        return any(target.is_type_end() for target in targets), [(target.value, int(target.name)) for target in targets if target.is_type_character()]

    @analysis_guard
    def mosaic_convert_to_canonical(self):
        if not hasattr(self, '_entry_nodes'): self.mosaic_reduce()
        canonical, accepting = {-1: []}, []
        for node, targets in self.graph_dict.items():
            analysis_step()
            if node.is_type_end(): continue
            index = int(node.name)
            canonical[index] = [(target.value, int(target.name)) for target in targets if target.is_type_character()]
            if any(target.is_type_end() for target in targets): accepting.append(index)
        for node in self._entry_nodes:
            analysis_step()
            if node.is_type_end(): accepting.append(-1)
            else: canonical[-1].append((node.value, int(node.name)))
        self.start_state, self.end_states, self.canon_graph_dict = -1, list(dict.fromkeys(accepting)), canonical

    def _expressions(self):
        if len(self.canon_graph_dict) > MAX_NODES + 1:
            raise PolicyFormatError('regex canonical state count exceeds limit')
        algebra, edges = _Algebra(), {}
        for source, targets in self.canon_graph_dict.items():
            analysis_step()
            if type(source) is not int or not -1 <= source < MAX_NODES or not isinstance(targets, (list, tuple)):
                raise PolicyFormatError('invalid regex canonical graph')
            for pair in targets:
                analysis_step()
                if not isinstance(pair, (list, tuple)) or len(pair) != 2: raise PolicyFormatError('invalid regex canonical edge')
                label, target = pair
                if type(target) is not int or target not in self.canon_graph_dict:
                    raise PolicyFormatError('invalid regex canonical target')
                pair = source, target
                edges[pair] = algebra.union(edges.get(pair), algebra.atom(label))
                if len(edges) > MAX_ITEMS: raise PolicyFormatError('regex canonical edge count exceeds limit')
        return algebra, edges

    def _store_expressions(self, edges, algebra, states):
        graph = {state: [] for state in states}
        for (source, target), value in edges.items():
            analysis_step()
            if value is not None: graph[source].append((algebra.render(value), target))
        self.canon_graph_dict = graph

    @analysis_guard
    def mosaic_remove_state(self, state_to_remove):
        if state_to_remove not in self.canon_graph_dict or state_to_remove == self.start_state or state_to_remove in self.end_states:
            raise PolicyFormatError('cannot remove regex boundary state')
        algebra, edges = self._expressions()
        result = _eliminate(edges, state_to_remove, algebra)
        self._store_expressions(result, algebra, [state for state in self.canon_graph_dict if state != state_to_remove])

    @analysis_guard
    def mosaic_simplify(self):
        algebra, edges = self._expressions()
        states = list(self.canon_graph_dict)
        for state in states:
            analysis_step()
            if state != self.start_state and state not in self.end_states: edges = _eliminate(edges, state, algebra)
        self._store_expressions(edges, algebra, [state for state in states if state == self.start_state or state in self.end_states])

    @analysis_guard
    def mosaic_combine_start_end_nodes(self):
        algebra, edges = self._expressions()
        if self.start_state not in self.canon_graph_dict or any(state not in self.canon_graph_dict for state in self.end_states):
            raise PolicyFormatError('invalid regex accepting states')
        finish = min([-1] + list(self.canon_graph_dict)) - 1
        for state in self.end_states:
            analysis_step()
            edges[state, finish] = algebra.union(edges.get((state, finish)), algebra.epsilon)
        for state in self.canon_graph_dict:
            analysis_step()
            if state != self.start_state: edges = _eliminate(edges, state, algebra)
        expression = algebra.sequence(algebra.star(edges.get((self.start_state, self.start_state))), edges.get((self.start_state, finish)))
        rendered = algebra.render(expression)
        self.regex = [] if rendered is None else [rendered]
        self.unified_regex = '' if rendered is None else rendered

    @analysis_guard
    def mosaic_unify_two_strings(self, s1, s2):
        algebra = _Algebra()
        return algebra.render(algebra.union(algebra.atom(s1), algebra.atom(s2)))

    @analysis_guard
    def mosaic_unify_strings(self, string_list):
        if not isinstance(string_list, (list, tuple)) or len(string_list) > MAX_ITEMS:
            raise PolicyFormatError('invalid or over-limit regex alternatives')
        algebra = _Algebra()
        return algebra.render(algebra.union(*(algebra.atom(text) for text in string_list)))

    def mosaic_need_use_plus(self, initial_string, string_to_add):
        # Compatibility query only; state elimination does not use textual
        # suffix heuristics to infer language equivalence.
        if not string_to_add.endswith('*'): return False
        base = string_to_add[1:-2] if string_to_add.startswith('(') and string_to_add.endswith(')*') else string_to_add[:-1]
        return initial_string.endswith(base) or initial_string.endswith(string_to_add)

    @analysis_guard
    def __str__(self):
        output = ReportBuffer()
        output.write('\n-- Node graph --\n')
        for node in sorted(self.graph_dict, key=lambda item: str(item.name)):
            analysis_step()
            output.write(str(node) + ':')
            for target in self.graph_dict[node]:
                analysis_step()
                output.write(' ' + str(target))
            output.write('\n')
        output.write('\n-- Canonical graph --\n')
        for state, targets in self.canon_graph_dict.items():
            analysis_step()
            prefix = '> ' if state == self.start_state else '# ' if state in self.end_states else '  '
            output.write('%s%d: [' % (prefix, state))
            for index, target in enumerate(targets):
                analysis_step()
                output.write((', ' if index else '') + repr(target))
            output.write(']\n')
        return output.getvalue()


@analysis_guard
def mosaic_create_regex_list(re):
    if not isinstance(re, (bytes, bytearray, list, tuple)) or not 6 <= len(re) <= 65535:
        raise PolicyFormatError('truncated or over-limit regex header')
    result = []
    mosaic_RegexParser.parse(re, 6, result)
    if not result: raise PolicyFormatError('empty regex program')
    positions = {record['pos'] for record in result}
    for record in result:
        analysis_step()
        if record['type'] == 'end' and record['pos'] + 7 >= len(re):
            raise PolicyFormatError('truncated regex end marker')
        if record['type'] in ('jump_forward', 'jump_backward') and record['value'] not in positions and record['value'] + 1 not in positions:
            raise PolicyFormatError('regex jump target outside instruction records')
        # Opcode 2 consumes a literal byte. Preserve the familiar dot display,
        # and escape regex operators instead of treating them as instructions.
        if record['type'] == 'character' and re[record['pos'] + 6] == 2:
            byte = re[record['pos'] + 7]
            record['value'] = '[.]' if byte == 46 else '\\x%02x' % byte if byte < 32 or byte >= 127 else _re.escape(chr(byte))
        elif record['type'] in ('class', 'class_exclude'):
            offset = record['pos'] + 5
            count = re[offset] >> 4
            values = list(re[offset + 1:offset + 1 + count * 2])
            excluded = record['type'] == 'class_exclude'
            if excluded:
                values = [values[-1]] + values[:-1]
                values = [value + (1 if index % 2 == 0 else -1) for index, value in enumerate(values)]
            parts = []
            for lower, upper in zip(values[::2], values[1::2]):
                if not 0 <= lower <= upper <= 255:
                    raise PolicyFormatError('invalid regex character-class interval')
                parts.append(_class_character(lower) + ('-' + _class_character(upper) if lower != upper else ''))
            record['value'] = '[' + ('^' if excluded else '') + ''.join(parts) + ']'
    return result


def _class_character(byte):
    if byte < 32 or byte >= 127: return '\\x%02x' % byte
    value = chr(byte)
    return '\\' + value if value in '\\-]^[' else value


@analysis_guard
def mosaic_parse_regex(re):
    graph = mosaic_Graph()
    graph.fill_from_regex_list(mosaic_create_regex_list(re))
    graph.reduce(); graph.convert_to_canonical(); graph.simplify(); graph.combine_start_end_nodes()
    return graph.regex


def mosaic_main():
    if len(sys.argv) != 2:
        print('Usage: python -m policymosaic.regex_graph <regex-binary-file>', file=sys.stderr)
        return 2
    try:
        with bounded_analysis():
            source = ProfileReader(read_local(sys.argv[1]))
            count = struct.unpack('<H', read_exact(source, 2))[0]
            if count > MAX_NODES: raise PolicyFormatError('regex collection count exceeds limit')
            total = 0
            for _ in range(count):
                analysis_step()
                length = struct.unpack('<H', read_exact(source, 2))[0]
                text = repr(mosaic_parse_regex(tuple(read_exact(source, length)))) + '\n'
                total += len(text.encode('utf-8'))
                if total > TOTAL_REPORT_BYTES: raise PolicyFormatError('regex collection output exceeds limit')
                sys.stdout.write(text)
            if source.tell() != len(source.getbuffer()): raise PolicyFormatError('trailing regex collection bytes')
        return 0
    except (PolicyFormatError, OSError, RecursionError, KeyError, TypeError) as error:
        print('PolicyMosaic: regex analysis could not complete', file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(mosaic_main())
_name_boundary.module_contract(globals(), {'logger': 'mosaic_logger', 'RegexParser': 'mosaic_RegexParser', 'main': 'mosaic_main', 'Node': 'mosaic_Node', 'parse_regex': 'mosaic_parse_regex', 'create_regex_list': 'mosaic_create_regex_list', 'Graph': 'mosaic_Graph'})
