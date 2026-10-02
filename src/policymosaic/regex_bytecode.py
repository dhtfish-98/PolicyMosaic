# Derived from sandblaster_26 regex_parser.py; BSD-3 provenance retained.
"""Checked bytecode records retaining the upstream public wire labels."""
import logging as mosaic_logging
import policymosaic_boundary as _name_boundary
from policymosaic.safety import PolicyFormatError, MAX_NODES, analysis_step
mosaic_logger = mosaic_logging.getLogger(__name__)


def _byte(code, offset):
    if type(offset) is not int or not 0 <= offset < len(code):
        raise PolicyFormatError('truncated regex operand')
    value = code[offset]
    if type(value) is not int or not 0 <= value <= 255:
        raise PolicyFormatError('invalid regex byte')
    return value


def _append(records, position, kind, value):
    if len(records) >= MAX_NODES:
        raise PolicyFormatError('regex record limit reached')
    records.append({'pos': position, 'type': kind, 'value': value})


def mosaic_parse_character(re, i, regex_list):
    value = chr(_byte(re, i + 1))
    _append(regex_list, i - 6, 'character', '[.]' if value == '.' else value)
    return i + 1


def mosaic_parse_beginning_of_line(i, regex_list):
    _append(regex_list, i - 6, 'character', '^')


def mosaic_parse_end_of_line(i, regex_list):
    _append(regex_list, i - 6, 'character', '$')


def mosaic_parse_any_character(i, regex_list):
    _append(regex_list, i - 6, 'character', '.')


def mosaic_parse_jump_forward(re, i, regex_list):
    target = _byte(re, i + 1) | (_byte(re, i + 2) << 8)
    _append(regex_list, i - 6, 'jump_forward', target)
    return i + 2


def mosaic_parse_jump_backward(re, i, regex_list):
    target = _byte(re, i + 1) | (_byte(re, i + 2) << 8)
    _append(regex_list, i - 6, 'jump_backward', target)
    return i + 2


def mosaic_parse_character_class(re, i, regex_list):
    count = _byte(re, i) >> 4
    if not count:
        raise PolicyFormatError('empty regex character class')
    values = [_byte(re, i + 1 + index) for index in range(count * 2)]
    excluded = values[0] > values[-1]
    if excluded:
        values = [values[-1]] + values[:-1]
        values = [value + (1 if index % 2 == 0 else -1) for index, value in enumerate(values)]
        if any(not 0 <= value <= 255 for value in values):
            raise PolicyFormatError('invalid excluded regex range')
    parts = [('%c-%c' % (start, end)) if start < end else chr(start)
             for start, end in zip(values[::2], values[1::2])]
    _append(regex_list, i + 1 - 6, 'class_exclude' if excluded else 'class',
            '[' + ('^' if excluded else '') + ''.join(parts) + ']')
    return i + count * 2


def mosaic_parse_end(re, i, regex_list):
    _byte(re, i)
    _append(regex_list, i - 6, 'end', 0)
    # Retained dialect advances by two bytes for an end marker.
    return i + 1


def mosaic_parse(re, i, regex_list):
    analysis_step()
    opcode = _byte(re, i)
    if opcode == 2: i = mosaic_parse_character(re, i, regex_list)
    elif opcode == 25: mosaic_parse_beginning_of_line(i, regex_list)
    elif opcode == 41: mosaic_parse_end_of_line(i, regex_list)
    elif opcode == 9: mosaic_parse_any_character(i, regex_list)
    elif opcode == 47: i = mosaic_parse_jump_forward(re, i, regex_list)
    elif opcode & 15 == 10: i = mosaic_parse_jump_backward(re, i, regex_list)
    elif opcode & 15 == 11: i = mosaic_parse_character_class(re, i, regex_list)
    elif opcode & 15 == 5: i = mosaic_parse_end(re, i, regex_list)
    else: raise PolicyFormatError('unsupported regex opcode')
    return i + 1

@_name_boundary.class_contract('RegexParser', {'parse': 'mosaic_parse'})
class mosaic_RegexParser:
    @staticmethod
    def mosaic_parse(re, i, regex_list):
        if not isinstance(re, (bytes, bytearray, tuple, list)) or len(re) > 65535:
            raise PolicyFormatError('invalid or over-limit regex bytecode')
        while i < len(re):
            i = mosaic_parse(re, i, regex_list)

_name_boundary.module_contract(globals(), {'parse_end_of_line': 'mosaic_parse_end_of_line', 'parse_jump_forward': 'mosaic_parse_jump_forward', 'logger': 'mosaic_logger', 'parse_end': 'mosaic_parse_end', 'parse_character_class': 'mosaic_parse_character_class', 'parse': 'mosaic_parse', 'RegexParser': 'mosaic_RegexParser', 'logging': 'mosaic_logging', 'parse_any_character': 'mosaic_parse_any_character', 'parse_jump_backward': 'mosaic_parse_jump_backward', 'parse_character': 'mosaic_parse_character', 'parse_beginning_of_line': 'mosaic_parse_beginning_of_line'})
