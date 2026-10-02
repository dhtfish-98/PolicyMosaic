# Derived from sandblaster_26 reverse_string.py; BSD-3 provenance retained.
"""Bounded interpreter for the inherited sandbox string-bytecode dialect."""
import logging as mosaic_logging
import struct as mosaic_struct
import sys as mosaic_sys
import policymosaic_boundary as _name_boundary
from policymosaic.safety import PolicyFormatError, bounded_analysis, analysis_step, checked_add, OUTPUT_BYTES, MAX_DEPTH, MAX_ITEMS
mosaic_logger = mosaic_logging.getLogger(__name__)

@_name_boundary.class_contract('ReverseStringState', {'binary_string': 'mosaic_binary_string', 'len': 'mosaic_len', 'pos': 'mosaic_pos', 'base': 'mosaic_base', 'base_stack': 'mosaic_base_stack', 'token': 'mosaic_token', 'token_stack': 'mosaic_token_stack', 'output_strings': 'mosaic_output_strings', 'STATE_UNKNOWN': 'mosaic_STATE_UNKNOWN', 'STATE_TOKEN_BYTE_READ': 'mosaic_STATE_TOKEN_BYTE_READ', 'STATE_CONCAT_BYTE_READ': 'mosaic_STATE_CONCAT_BYTE_READ', 'STATE_CONCAT_SAVE_BYTE_READ': 'mosaic_STATE_CONCAT_SAVE_BYTE_READ', 'STATE_END_BYTE_READ': 'mosaic_STATE_END_BYTE_READ', 'STATE_SPLIT_BYTE_READ': 'mosaic_STATE_SPLIT_BYTE_READ', 'STATE_TOKEN_READ': 'mosaic_STATE_TOKEN_READ', 'STATE_RANGE_BYTE_READ': 'mosaic_STATE_RANGE_BYTE_READ', 'STATE_CONSTANT_READ': 'mosaic_STATE_CONSTANT_READ', 'STATE_SINGLE_BYTE_READ': 'mosaic_STATE_SINGLE_BYTE_READ', 'STATE_PLUS_READ': 'mosaic_STATE_PLUS_READ', 'STATE_RESET_STRING': 'mosaic_STATE_RESET_STRING', 'state_stack': 'mosaic_state_stack', 'state': 'mosaic_state', 'state_byte': 'mosaic_state_byte', 'update_state_unknown': 'mosaic_update_state_unknown', 'update_state_token_byte_read': 'mosaic_update_state_token_byte_read', 'update_state_concat_byte_read': 'mosaic_update_state_concat_byte_read', 'update_state_concat_save_byte_read': 'mosaic_update_state_concat_save_byte_read', 'update_state_end_byte_read': 'mosaic_update_state_end_byte_read', 'update_state_split_byte_read': 'mosaic_update_state_split_byte_read', 'update_state_range_byte_read': 'mosaic_update_state_range_byte_read', 'update_state_token_read': 'mosaic_update_state_token_read', 'update_state_reset_string': 'mosaic_update_state_reset_string', 'update_state_constant_read': 'mosaic_update_state_constant_read', 'update_state_single_byte_read': 'mosaic_update_state_single_byte_read', 'update_state_plus_read': 'mosaic_update_state_plus_read', 'update_state': 'mosaic_update_state', 'get_next_byte': 'mosaic_get_next_byte', 'get_length_minus_1': 'mosaic_get_length_minus_1', 'read_token': 'mosaic_read_token', 'update_base': 'mosaic_update_base', 'update_base_stack': 'mosaic_update_base_stack', 'end_current_token': 'mosaic_end_current_token', 'get_last_byte': 'mosaic_get_last_byte', 'get_substring': 'mosaic_get_substring', 'end_with_subtokens': 'mosaic_end_with_subtokens', 'is_end': 'mosaic_is_end', 'reset_base': 'mosaic_reset_base', 'reset_base_full': 'mosaic_reset_base_full', 'tokens': 'mosaic_tokens'})
class mosaic_ReverseStringState:
    mosaic_STATE_UNKNOWN = 0
    mosaic_STATE_TOKEN_BYTE_READ = 1
    mosaic_STATE_CONCAT_BYTE_READ = 2
    mosaic_STATE_CONCAT_SAVE_BYTE_READ = 3
    mosaic_STATE_END_BYTE_READ = 4
    mosaic_STATE_SPLIT_BYTE_READ = 5
    mosaic_STATE_TOKEN_READ = 6
    mosaic_STATE_RANGE_BYTE_READ = 7
    mosaic_STATE_CONSTANT_READ = 8
    mosaic_STATE_SINGLE_BYTE_READ = 9
    mosaic_STATE_PLUS_READ = 10
    mosaic_STATE_RESET_STRING = 11

    def __init__(self, binary_string):
        if not isinstance(binary_string, (bytes, bytearray)) or len(binary_string) > 65535:
            raise PolicyFormatError('invalid or over-limit string bytecode')
        self.binary_string = bytes(binary_string)
        self.len = len(self.binary_string)
        self.pos = 0
        self.base = ''
        self.base_stack = []
        self.token = ''
        self.tokens = []
        self.token_stack = []
        self.output_strings = []
        self.state_stack = []
        self.state = self.STATE_UNKNOWN
        self.state_byte = 0
        self._output_bytes = 0

    def _transition(self, state):
        self.state_stack.append(self.state)
        self.state = state
        if len(self.state_stack) > MAX_ITEMS:
            raise PolicyFormatError('string state limit reached')

    def mosaic_update_state_unknown(self): self._transition(self.STATE_UNKNOWN)
    def mosaic_update_state_token_byte_read(self): self._transition(self.STATE_TOKEN_BYTE_READ)
    def mosaic_update_state_concat_byte_read(self): self._transition(self.STATE_CONCAT_BYTE_READ)
    def mosaic_update_state_concat_save_byte_read(self): self._transition(self.STATE_CONCAT_SAVE_BYTE_READ)
    def mosaic_update_state_end_byte_read(self): self._transition(self.STATE_END_BYTE_READ)
    def mosaic_update_state_split_byte_read(self): self._transition(self.STATE_SPLIT_BYTE_READ)
    def mosaic_update_state_range_byte_read(self): self._transition(self.STATE_RANGE_BYTE_READ)
    def mosaic_update_state_token_read(self): self._transition(self.STATE_TOKEN_READ)
    def mosaic_update_state_reset_string(self): self._transition(self.STATE_RESET_STRING)
    def mosaic_update_state_constant_read(self): self._transition(self.STATE_CONSTANT_READ)
    def mosaic_update_state_single_byte_read(self): self._transition(self.STATE_SINGLE_BYTE_READ)
    def mosaic_update_state_plus_read(self): self._transition(self.STATE_PLUS_READ)

    def mosaic_update_state(self, b):
        self.state_byte = b
        if b == 10: state = self.STATE_END_BYTE_READ
        elif b == 15: state = self.STATE_CONCAT_BYTE_READ
        elif b >= 128: state = self.STATE_SPLIT_BYTE_READ
        elif b in (0, 7): state = self.STATE_UNKNOWN
        elif b in (5, 6): state = self.STATE_RESET_STRING
        elif b == 8:
            state = self.STATE_CONCAT_SAVE_BYTE_READ
            self.get_substring(2)
        elif 16 <= b < 63: state = self.STATE_CONSTANT_READ
        elif b == 11: state = self.STATE_RANGE_BYTE_READ
        elif b == 2: state = self.STATE_PLUS_READ
        else: state = self.STATE_TOKEN_BYTE_READ
        self._transition(state)

    def mosaic_get_next_byte(self):
        if self.is_end():
            raise PolicyFormatError('truncated string bytecode')
        value = self.binary_string[self.pos]
        self.pos += 1
        return value

    def mosaic_get_length_minus_1(self):
        value = self.get_last_byte()
        return self.get_next_byte() + 65 if value == 4 else value - 63 if value >= 63 else value

    def mosaic_get_substring(self, substr_len):
        if type(substr_len) is not int or substr_len < 0 or substr_len > self.len - self.pos:
            raise PolicyFormatError('truncated string token')
        value = self.binary_string[self.pos:self.pos + substr_len]
        self.pos += substr_len
        return value

    def mosaic_read_token(self, substr_len):
        self.token_stack.append(self.token)
        try:
            self.token = self.get_substring(substr_len).decode('utf-8')
        except UnicodeDecodeError as error:
            raise PolicyFormatError('invalid UTF-8 string token') from error

    def mosaic_update_base(self):
        self.base = checked_add(self.base, self.token)
        self.token = ''

    def mosaic_update_base_stack(self):
        if len(self.base_stack) >= MAX_ITEMS:
            raise PolicyFormatError('string base stack limit reached')
        self.base_stack.append(self.base)
        self.update_base()

    def _append(self, value):
        self._output_bytes += len(value.encode('utf-8'))
        if self._output_bytes > OUTPUT_BYTES or len(self.output_strings) >= MAX_ITEMS:
            raise PolicyFormatError('string expansion limit reached')
        self.output_strings.append(value)

    def mosaic_end_current_token(self):
        self._append(checked_add(self.base, self.token))
        self.token = ''

    def mosaic_get_last_byte(self):
        if not 0 < self.pos <= self.len:
            raise PolicyFormatError('invalid string cursor')
        return self.binary_string[self.pos - 1]

    def mosaic_end_with_subtokens(self, subtokens):
        for subtoken in subtokens:
            analysis_step()
            self._append(checked_add(checked_add(self.base, self.token), subtoken))
        self.token = ''

    def mosaic_is_end(self): return self.pos >= self.len
    def mosaic_reset_base(self):
        if self.base_stack: self.base = self.base_stack.pop()
    def mosaic_reset_base_full(self):
        self.base_stack.clear()
        self.base = ''

@_name_boundary.class_contract('SandboxString', {'rss_stack': 'mosaic_rss_stack', 'parse_byte_string': 'mosaic_parse_byte_string'})
class mosaic_SandboxString:
    def __init__(self):
        self.rss_stack = []
        self._depth = 0

    def mosaic_parse_byte_string(self, s, global_vars):
        if not isinstance(global_vars, (list, tuple)) or len(global_vars) > 255 or any(not isinstance(value, str) for value in global_vars):
            raise PolicyFormatError('invalid string variable catalog')
        if self._depth >= MAX_DEPTH:
            raise PolicyFormatError('string nesting limit reached')
        self._depth += 1
        try:
            with bounded_analysis():
                return self._decode(s, global_vars)
        finally:
            self._depth -= 1

    def _decode(self, s, global_vars):
        state = mosaic_ReverseStringState(s)
        while not state.is_end():
            analysis_step()
            previous = state.state_stack[-1] if state.state_stack else state.STATE_UNKNOWN
            kind = state.state
            if kind in (state.STATE_UNKNOWN, state.STATE_TOKEN_READ):
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_TOKEN_BYTE_READ:
                if previous == state.STATE_TOKEN_READ:
                    raise PolicyFormatError('unsupported adjacent string tokens')
                state.read_token(state.get_length_minus_1())
                state.update_state_token_read()
            elif kind == state.STATE_CONSTANT_READ:
                value = state.get_last_byte()
                if 16 <= value < 46:
                    index = value - 16
                    if index >= len(global_vars):
                        raise PolicyFormatError('string variable index outside catalog')
                    state.token = '${' + global_vars[index] + '}'
                state.update_state(state.get_next_byte())
            elif kind in (state.STATE_CONCAT_BYTE_READ, state.STATE_CONCAT_SAVE_BYTE_READ):
                if previous in (state.STATE_TOKEN_READ, state.STATE_CONSTANT_READ, state.STATE_RANGE_BYTE_READ, state.STATE_SINGLE_BYTE_READ, state.STATE_PLUS_READ):
                    (state.update_base_stack if kind == state.STATE_CONCAT_SAVE_BYTE_READ else state.update_base)()
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_END_BYTE_READ:
                state.end_current_token()
                state.reset_base()
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_RANGE_BYTE_READ:
                state.update_base_stack()
                count = state.get_next_byte() + 1
                ranges = [(state.get_next_byte(), state.get_next_byte()) for _ in range(count)]
                state.token = '[' + ''.join('%c-%c' % pair for pair in ranges) + ']' if all(32 <= value <= 127 for pair in ranges for value in pair) else '[UNSUPPORTED]'
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_SPLIT_BYTE_READ:
                nested = state.get_substring(state.get_last_byte() - 127)
                state.end_with_subtokens(self.parse_byte_string(nested, global_vars))
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_SINGLE_BYTE_READ:
                state.read_token(1)
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_RESET_STRING:
                state.end_current_token()
                state.reset_base_full()
                state.update_state(state.get_next_byte())
            elif kind == state.STATE_PLUS_READ:
                if previous == state.STATE_CONCAT_BYTE_READ:
                    state.token = '+'
                    state.update_base()
                state.read_token(1)
                state.update_state(state.get_next_byte())
            else:
                raise PolicyFormatError('unsupported string state')
        if state.state == state.STATE_END_BYTE_READ:
            state.end_current_token()
        elif state.state not in (state.STATE_UNKNOWN, state.STATE_CONCAT_BYTE_READ):
            raise PolicyFormatError('incomplete string bytecode')
        return state.output_strings


def mosaic_main():
    try:
        raw = mosaic_sys.stdin.buffer.read(65536)
        if len(raw) > 65535:
            raise PolicyFormatError('string input exceeds limit')
        print(mosaic_SandboxString().parse_byte_string(raw[4:], ['FRONT_USER_HOME', 'HOME', 'PROCESS_TEMP_DIR']))
        return 0
    except PolicyFormatError as error:
        print('PolicyMosaic: ' + str(error), file=mosaic_sys.stderr)
        return 2

_name_boundary.module_contract(globals(), {'logger': 'mosaic_logger', 'struct': 'mosaic_struct', 'SandboxString': 'mosaic_SandboxString', 'main': 'mosaic_main', 'logging': 'mosaic_logging', 'sys': 'mosaic_sys', 'ReverseStringState': 'mosaic_ReverseStringState'})
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
