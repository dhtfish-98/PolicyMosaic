# Derived from reverse-sandbox/reverse_string.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import sys as mosaic_sys
import struct as mosaic_struct
import logging as mosaic_logging
import logging.config as _boundary_logging_configuration
mosaic_logging.config.fileConfig(_name_boundary.resource('logger.config'))
mosaic_logger = mosaic_logging.getLogger(__name__)

@_name_boundary.class_contract('ReverseStringState', {'binary_string': 'mosaic_binary_string', 'len': 'mosaic_len', 'pos': 'mosaic_pos', 'base': 'mosaic_base', 'base_stack': 'mosaic_base_stack', 'token': 'mosaic_token', 'token_stack': 'mosaic_token_stack', 'output_strings': 'mosaic_output_strings', 'STATE_UNKNOWN': 'mosaic_STATE_UNKNOWN', 'STATE_TOKEN_BYTE_READ': 'mosaic_STATE_TOKEN_BYTE_READ', 'STATE_CONCAT_BYTE_READ': 'mosaic_STATE_CONCAT_BYTE_READ', 'STATE_CONCAT_SAVE_BYTE_READ': 'mosaic_STATE_CONCAT_SAVE_BYTE_READ', 'STATE_END_BYTE_READ': 'mosaic_STATE_END_BYTE_READ', 'STATE_SPLIT_BYTE_READ': 'mosaic_STATE_SPLIT_BYTE_READ', 'STATE_TOKEN_READ': 'mosaic_STATE_TOKEN_READ', 'STATE_RANGE_BYTE_READ': 'mosaic_STATE_RANGE_BYTE_READ', 'STATE_CONSTANT_READ': 'mosaic_STATE_CONSTANT_READ', 'STATE_SINGLE_BYTE_READ': 'mosaic_STATE_SINGLE_BYTE_READ', 'STATE_PLUS_READ': 'mosaic_STATE_PLUS_READ', 'STATE_RESET_STRING': 'mosaic_STATE_RESET_STRING', 'state_stack': 'mosaic_state_stack', 'state': 'mosaic_state', 'state_byte': 'mosaic_state_byte', 'update_state_unknown': 'mosaic_update_state_unknown', 'update_state_token_byte_read': 'mosaic_update_state_token_byte_read', 'update_state_concat_byte_read': 'mosaic_update_state_concat_byte_read', 'update_state_concat_save_byte_read': 'mosaic_update_state_concat_save_byte_read', 'update_state_end_byte_read': 'mosaic_update_state_end_byte_read', 'update_state_split_byte_read': 'mosaic_update_state_split_byte_read', 'update_state_range_byte_read': 'mosaic_update_state_range_byte_read', 'update_state_token_read': 'mosaic_update_state_token_read', 'update_state_reset_string': 'mosaic_update_state_reset_string', 'update_state_constant_read': 'mosaic_update_state_constant_read', 'update_state_single_byte_read': 'mosaic_update_state_single_byte_read', 'update_state_plus_read': 'mosaic_update_state_plus_read', 'update_state': 'mosaic_update_state', 'get_next_byte': 'mosaic_get_next_byte', 'get_length_minus_1': 'mosaic_get_length_minus_1', 'read_token': 'mosaic_read_token', 'update_base': 'mosaic_update_base', 'update_base_stack': 'mosaic_update_base_stack', 'end_current_token': 'mosaic_end_current_token', 'get_last_byte': 'mosaic_get_last_byte', 'get_substring': 'mosaic_get_substring', 'end_with_subtokens': 'mosaic_end_with_subtokens', 'is_end': 'mosaic_is_end', 'reset_base': 'mosaic_reset_base', 'reset_base_full': 'mosaic_reset_base_full', 'tokens': 'mosaic_tokens'})
class mosaic_ReverseStringState:
    mosaic_binary_string = ''
    mosaic_len = 0
    mosaic_pos = 0
    mosaic_base = ''
    mosaic_base_stack = []
    mosaic_token = ''
    mosaic_token_stack = []
    mosaic_output_strings = []
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
    mosaic_state_stack = []
    mosaic_state = mosaic_STATE_UNKNOWN
    mosaic_state_byte = 0

    @_name_boundary.callable_contract({'self': 'mosaic_self_73c71f9', 'binary_string': 'mosaic_binary_string_7915ee9'}, '__init__')
    def __init__(mosaic_self_73c71f9, mosaic_binary_string_7915ee9):
        _name_boundary.attributes(mosaic_self_73c71f9)['binary_string'] = mosaic_binary_string_7915ee9
        _name_boundary.attributes(mosaic_self_73c71f9)['len'] = 0
        _name_boundary.attributes(mosaic_self_73c71f9)['pos'] = 0
        _name_boundary.attributes(mosaic_self_73c71f9)['base'] = ''
        _name_boundary.attributes(mosaic_self_73c71f9)['token'] = ''
        _name_boundary.attributes(mosaic_self_73c71f9)['tokens'] = []
        _name_boundary.attributes(mosaic_self_73c71f9)['token_stack'] = []
        _name_boundary.attributes(mosaic_self_73c71f9)['base_stack'] = []
        _name_boundary.attributes(mosaic_self_73c71f9)['output_strings'] = []
        _name_boundary.attributes(mosaic_self_73c71f9)['state_stack'] = []
        _name_boundary.attributes(mosaic_self_73c71f9)['state'] = _name_boundary.attributes(mosaic_self_73c71f9)['STATE_UNKNOWN']
        _name_boundary.attributes(mosaic_self_73c71f9)['state_byte'] = 0

    @_name_boundary.callable_contract({'self': 'mosaic_self_c747041'}, 'update_state_unknown')
    def mosaic_update_state_unknown(mosaic_self_c747041):
        _name_boundary.attributes(mosaic_self_c747041)['state_stack'].append(_name_boundary.attributes(mosaic_self_c747041)['state'])
        _name_boundary.attributes(mosaic_self_c747041)['state'] = _name_boundary.attributes(mosaic_self_c747041)['STATE_UNKNOWN']

    @_name_boundary.callable_contract({'self': 'mosaic_self_31434a1'}, 'update_state_token_byte_read')
    def mosaic_update_state_token_byte_read(mosaic_self_31434a1):
        _name_boundary.attributes(mosaic_self_31434a1)['state_stack'].append(_name_boundary.attributes(mosaic_self_31434a1)['state'])
        _name_boundary.attributes(mosaic_self_31434a1)['state'] = _name_boundary.attributes(mosaic_self_31434a1)['STATE_TOKEN_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_776c238'}, 'update_state_concat_byte_read')
    def mosaic_update_state_concat_byte_read(mosaic_self_776c238):
        _name_boundary.attributes(mosaic_self_776c238)['state_stack'].append(_name_boundary.attributes(mosaic_self_776c238)['state'])
        _name_boundary.attributes(mosaic_self_776c238)['state'] = _name_boundary.attributes(mosaic_self_776c238)['STATE_CONCAT_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_96030af'}, 'update_state_concat_save_byte_read')
    def mosaic_update_state_concat_save_byte_read(mosaic_self_96030af):
        _name_boundary.attributes(mosaic_self_96030af)['state_stack'].append(_name_boundary.attributes(mosaic_self_96030af)['state'])
        _name_boundary.attributes(mosaic_self_96030af)['state'] = _name_boundary.attributes(mosaic_self_96030af)['STATE_CONCAT_SAVE_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_c9b691d'}, 'update_state_end_byte_read')
    def mosaic_update_state_end_byte_read(mosaic_self_c9b691d):
        _name_boundary.attributes(mosaic_self_c9b691d)['state_stack'].append(_name_boundary.attributes(mosaic_self_c9b691d)['state'])
        _name_boundary.attributes(mosaic_self_c9b691d)['state'] = _name_boundary.attributes(mosaic_self_c9b691d)['STATE_END_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_8ff1c9b'}, 'update_state_split_byte_read')
    def mosaic_update_state_split_byte_read(mosaic_self_8ff1c9b):
        _name_boundary.attributes(mosaic_self_8ff1c9b)['state_stack'].append(_name_boundary.attributes(mosaic_self_8ff1c9b)['state'])
        _name_boundary.attributes(mosaic_self_8ff1c9b)['state'] = _name_boundary.attributes(mosaic_self_8ff1c9b)['STATE_SPLIT_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_28b27ff'}, 'update_state_range_byte_read')
    def mosaic_update_state_range_byte_read(mosaic_self_28b27ff):
        _name_boundary.attributes(mosaic_self_28b27ff)['state_stack'].append(_name_boundary.attributes(mosaic_self_28b27ff)['state'])
        _name_boundary.attributes(mosaic_self_28b27ff)['state'] = _name_boundary.attributes(mosaic_self_28b27ff)['STATE_RANGE_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_7080abe'}, 'update_state_token_read')
    def mosaic_update_state_token_read(mosaic_self_7080abe):
        _name_boundary.attributes(mosaic_self_7080abe)['state_stack'].append(_name_boundary.attributes(mosaic_self_7080abe)['state'])
        _name_boundary.attributes(mosaic_self_7080abe)['state'] = _name_boundary.attributes(mosaic_self_7080abe)['STATE_TOKEN_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_6722177'}, 'update_state_reset_string')
    def mosaic_update_state_reset_string(mosaic_self_6722177):
        _name_boundary.attributes(mosaic_self_6722177)['state_stack'].append(_name_boundary.attributes(mosaic_self_6722177)['state'])
        _name_boundary.attributes(mosaic_self_6722177)['state'] = _name_boundary.attributes(mosaic_self_6722177)['STATE_RESET_STRING']

    @_name_boundary.callable_contract({'self': 'mosaic_self_35f6dca'}, 'update_state_constant_read')
    def mosaic_update_state_constant_read(mosaic_self_35f6dca):
        _name_boundary.attributes(mosaic_self_35f6dca)['state_stack'].append(_name_boundary.attributes(mosaic_self_35f6dca)['state'])
        _name_boundary.attributes(mosaic_self_35f6dca)['state'] = _name_boundary.attributes(mosaic_self_35f6dca)['STATE_CONSTANT_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_7795455'}, 'update_state_single_byte_read')
    def mosaic_update_state_single_byte_read(mosaic_self_7795455):
        _name_boundary.attributes(mosaic_self_7795455)['state_stack'].append(_name_boundary.attributes(mosaic_self_7795455)['state'])
        _name_boundary.attributes(mosaic_self_7795455)['state'] = _name_boundary.attributes(mosaic_self_7795455)['STATE_SINGLE_BYTE_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_0442d8d'}, 'update_state_plus_read')
    def mosaic_update_state_plus_read(mosaic_self_0442d8d):
        _name_boundary.attributes(mosaic_self_0442d8d)['state_stack'].append(_name_boundary.attributes(mosaic_self_0442d8d)['state'])
        _name_boundary.attributes(mosaic_self_0442d8d)['state'] = _name_boundary.attributes(mosaic_self_0442d8d)['STATE_PLUS_READ']

    @_name_boundary.callable_contract({'self': 'mosaic_self_6b07fdc', 'b': 'mosaic_b_8f54620'}, 'update_state')
    def mosaic_update_state(mosaic_self_6b07fdc, mosaic_b_8f54620):
        _name_boundary.attributes(mosaic_self_6b07fdc)['state_byte'] = mosaic_b_8f54620
        if mosaic_b_8f54620 == 10:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_end_byte_read']()
        elif mosaic_b_8f54620 == 15:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_concat_byte_read']()
        elif mosaic_b_8f54620 >= 128:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_split_byte_read']()
        elif mosaic_b_8f54620 == 0 or mosaic_b_8f54620 == 7:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_unknown']()
        elif mosaic_b_8f54620 == 5:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_reset_string']()
        elif mosaic_b_8f54620 == 8:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_concat_save_byte_read']()
            _name_boundary.attributes(mosaic_self_6b07fdc)['get_next_byte']()
            _name_boundary.attributes(mosaic_self_6b07fdc)['get_next_byte']()
        elif mosaic_b_8f54620 >= 16 and mosaic_b_8f54620 < 63:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_constant_read']()
        elif mosaic_b_8f54620 == 11:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_range_byte_read']()
        elif mosaic_b_8f54620 == 2:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_plus_read']()
        elif mosaic_b_8f54620 == 6:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_reset_string']()
        else:
            _name_boundary.attributes(mosaic_self_6b07fdc)['update_state_token_byte_read']()
            return

    @_name_boundary.callable_contract({'self': 'mosaic_self_434e01f'}, 'get_next_byte')
    def mosaic_get_next_byte(mosaic_self_434e01f):
        if _name_boundary.attributes(mosaic_self_434e01f)['is_end']():
            return 0
        mosaic_b_2d9d75b = mosaic_struct.unpack('<B', _name_boundary.attributes(mosaic_self_434e01f)['binary_string'][_name_boundary.attributes(mosaic_self_434e01f)['pos']:_name_boundary.attributes(mosaic_self_434e01f)['pos'] + 1])[0]
        mosaic_logger.debug('read byte 0x{:02x}'.format(mosaic_b_2d9d75b))
        _name_boundary.attributes(mosaic_self_434e01f)['pos'] += 1
        return mosaic_b_2d9d75b

    @_name_boundary.callable_contract({'self': 'mosaic_self_5d7362b'}, 'get_length_minus_1')
    def mosaic_get_length_minus_1(mosaic_self_5d7362b):
        mosaic_b_29f496e = mosaic_struct.unpack('<B', _name_boundary.attributes(mosaic_self_5d7362b)['binary_string'][_name_boundary.attributes(mosaic_self_5d7362b)['pos'] - 1:_name_boundary.attributes(mosaic_self_5d7362b)['pos']])[0]
        mosaic_logger.debug('b is 0x{:02x} ({:d})'.format(mosaic_b_29f496e, mosaic_b_29f496e))
        if mosaic_b_29f496e == 4:
            mosaic_b_29f496e = mosaic_struct.unpack('<B', _name_boundary.attributes(mosaic_self_5d7362b)['binary_string'][_name_boundary.attributes(mosaic_self_5d7362b)['pos']:_name_boundary.attributes(mosaic_self_5d7362b)['pos'] + 1])[0]
            mosaic_logger.debug('got larger length 0x{:02x} ({:d})'.format(mosaic_b_29f496e, mosaic_b_29f496e))
            _name_boundary.attributes(mosaic_self_5d7362b)['pos'] += 1
            return mosaic_b_29f496e + 65
        else:
            mosaic_logger.debug('got length 0x{:02x} ({:d})'.format(mosaic_b_29f496e, mosaic_b_29f496e))
            if mosaic_b_29f496e >= 63:
                return mosaic_b_29f496e - 63
            return mosaic_b_29f496e

    @_name_boundary.callable_contract({'self': 'mosaic_self_d59322b', 'substr_len': 'mosaic_substr_len_f39351f'}, 'read_token')
    def mosaic_read_token(mosaic_self_d59322b, mosaic_substr_len_f39351f):
        _name_boundary.attributes(mosaic_self_d59322b)['token_stack'].append(_name_boundary.attributes(mosaic_self_d59322b)['token'])
        try:
            _name_boundary.attributes(mosaic_self_d59322b)['token'] = _name_boundary.attributes(mosaic_self_d59322b)['binary_string'][_name_boundary.attributes(mosaic_self_d59322b)['pos']:_name_boundary.attributes(mosaic_self_d59322b)['pos'] + mosaic_substr_len_f39351f].decode('utf-8')
        except:
            _name_boundary.attributes(mosaic_self_d59322b)['token'] = 'UNSUPPORTED_STRING_TYPE_3'
            pass
        _name_boundary.attributes(mosaic_self_d59322b)['pos'] += mosaic_substr_len_f39351f

    @_name_boundary.callable_contract({'self': 'mosaic_self_7aff883'}, 'update_base')
    def mosaic_update_base(mosaic_self_7aff883):
        _name_boundary.attributes(mosaic_self_7aff883)['base'] += _name_boundary.attributes(mosaic_self_7aff883)['token']
        _name_boundary.attributes(mosaic_self_7aff883)['token'] = ''
        mosaic_logger.debug('update base to "{:s}"'.format(_name_boundary.attributes(mosaic_self_7aff883)['base']))

    @_name_boundary.callable_contract({'self': 'mosaic_self_0204171'}, 'update_base_stack')
    def mosaic_update_base_stack(mosaic_self_0204171):
        _name_boundary.attributes(mosaic_self_0204171)['base_stack'].append(_name_boundary.attributes(mosaic_self_0204171)['base'])
        _name_boundary.attributes(mosaic_self_0204171)['update_base']()

    @_name_boundary.callable_contract({'self': 'mosaic_self_70b8e54'}, 'end_current_token')
    def mosaic_end_current_token(mosaic_self_70b8e54):
        _name_boundary.attributes(mosaic_self_70b8e54)['output_strings'].append(_name_boundary.attributes(mosaic_self_70b8e54)['base'] + _name_boundary.attributes(mosaic_self_70b8e54)['token'])
        _name_boundary.attributes(mosaic_self_70b8e54)['token'] = ''

    @_name_boundary.callable_contract({'self': 'mosaic_self_0b1e58d'}, 'get_last_byte')
    def mosaic_get_last_byte(mosaic_self_0b1e58d):
        return mosaic_struct.unpack('<B', _name_boundary.attributes(mosaic_self_0b1e58d)['binary_string'][_name_boundary.attributes(mosaic_self_0b1e58d)['pos'] - 1:_name_boundary.attributes(mosaic_self_0b1e58d)['pos']])[0]

    @_name_boundary.callable_contract({'self': 'mosaic_self_e0558c8', 'substr_len': 'mosaic_substr_len_d19eab9'}, 'get_substring')
    def mosaic_get_substring(mosaic_self_e0558c8, mosaic_substr_len_d19eab9):
        mosaic_substr_3ef9c2c = _name_boundary.attributes(mosaic_self_e0558c8)['binary_string'][_name_boundary.attributes(mosaic_self_e0558c8)['pos']:_name_boundary.attributes(mosaic_self_e0558c8)['pos'] + mosaic_substr_len_d19eab9]
        mosaic_logger.debug(mosaic_substr_3ef9c2c)
        _name_boundary.attributes(mosaic_self_e0558c8)['pos'] += mosaic_substr_len_d19eab9
        return mosaic_substr_3ef9c2c

    @_name_boundary.callable_contract({'self': 'mosaic_self_3407965', 'subtokens': 'mosaic_subtokens_f05e209'}, 'end_with_subtokens')
    def mosaic_end_with_subtokens(mosaic_self_3407965, mosaic_subtokens_f05e209):
        for mosaic_s_1daa54b in mosaic_subtokens_f05e209:
            _name_boundary.attributes(mosaic_self_3407965)['output_strings'].append(_name_boundary.attributes(mosaic_self_3407965)['base'] + _name_boundary.attributes(mosaic_self_3407965)['token'] + mosaic_s_1daa54b)
            mosaic_logger.debug('output string with subtokens "{:s}"'.format(_name_boundary.attributes(mosaic_self_3407965)['base'] + _name_boundary.attributes(mosaic_self_3407965)['token'] + mosaic_s_1daa54b))
        _name_boundary.attributes(mosaic_self_3407965)['token'] = ''

    @_name_boundary.callable_contract({'self': 'mosaic_self_d65caf7'}, 'is_end')
    def mosaic_is_end(mosaic_self_d65caf7):
        if _name_boundary.attributes(mosaic_self_d65caf7)['pos'] >= len(_name_boundary.attributes(mosaic_self_d65caf7)['binary_string']):
            return True
        return False

    @_name_boundary.callable_contract({'self': 'mosaic_self_bcb2c11'}, 'reset_base')
    def mosaic_reset_base(mosaic_self_bcb2c11):
        if len(_name_boundary.attributes(mosaic_self_bcb2c11)['base_stack']) >= 1:
            _name_boundary.attributes(mosaic_self_bcb2c11)['base'] = _name_boundary.attributes(mosaic_self_bcb2c11)['base_stack'].pop()

    @_name_boundary.callable_contract({'self': 'mosaic_self_06e39e8'}, 'reset_base_full')
    def mosaic_reset_base_full(mosaic_self_06e39e8):
        _name_boundary.attributes(mosaic_self_06e39e8)['base_stack'] = []
        _name_boundary.attributes(mosaic_self_06e39e8)['base'] = ''

@_name_boundary.class_contract('SandboxString', {'rss_stack': 'mosaic_rss_stack', 'parse_byte_string': 'mosaic_parse_byte_string'})
class mosaic_SandboxString:
    mosaic_rss_stack = []

    @_name_boundary.callable_contract({'self': 'mosaic_self_ed51b3f', 's': 'mosaic_s_7d1d36e', 'global_vars': 'mosaic_global_vars_6692752'}, 'parse_byte_string')
    def mosaic_parse_byte_string(mosaic_self_ed51b3f, mosaic_s_7d1d36e, mosaic_global_vars_6692752):
        mosaic_rss_589fa71 = mosaic_ReverseStringState(mosaic_s_7d1d36e)
        mosaic_base_b9af0d3 = ''
        mosaic_reset_base_ed519c8 = False
        mosaic_tokens_10b0740 = []
        mosaic_token_bf407b6 = ''
        while True:
            if _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_UNKNOWN']:
                mosaic_logger.debug('state is STATE_UNKNOWN')
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_TOKEN_READ']:
                mosaic_logger.debug('state is STATE_TOKEN_READ')
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_TOKEN_BYTE_READ']:
                mosaic_logger.debug('state is STATE_TOKEN_BYTE_READ')
                mosaic_prev_state_bbebad7 = _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1]
                if mosaic_prev_state_bbebad7 != _name_boundary.attributes(mosaic_rss_589fa71)['STATE_TOKEN_READ']:
                    mosaic_token_len_70c9a6a = _name_boundary.attributes(mosaic_rss_589fa71)['get_length_minus_1']()
                    _name_boundary.attributes(mosaic_rss_589fa71)['read_token'](mosaic_token_len_70c9a6a)
                    _name_boundary.attributes(mosaic_rss_589fa71)['update_state_token_read']()
                else:
                    mosaic_logger.warn('read token byte from token state')
                    break
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONSTANT_READ']:
                mosaic_logger.debug('state is STATE_CONSTANT_READ')
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_last_byte']()
                if mosaic_b_cdeff8f >= 16 and mosaic_b_cdeff8f < 46:
                    _name_boundary.attributes(mosaic_rss_589fa71)['token'] = '${' + mosaic_global_vars_6692752[mosaic_b_cdeff8f - 16] + '}'
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONCAT_BYTE_READ']:
                mosaic_logger.debug('state is STATE_CONCAT_BYTE_READ')
                if _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_TOKEN_READ'] or _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONSTANT_READ'] or _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_RANGE_BYTE_READ'] or (_name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_SINGLE_BYTE_READ']) or (_name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_PLUS_READ']):
                    _name_boundary.attributes(mosaic_rss_589fa71)['update_base']()
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONCAT_SAVE_BYTE_READ']:
                mosaic_logger.debug('state is STATE_CONCAT_SAVE_BYTE_READ')
                if _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_TOKEN_READ'] or _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONSTANT_READ'] or _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_RANGE_BYTE_READ'] or (_name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_SINGLE_BYTE_READ']) or (_name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_PLUS_READ']):
                    _name_boundary.attributes(mosaic_rss_589fa71)['update_base_stack']()
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_END_BYTE_READ']:
                mosaic_logger.debug('state is STATE_END_BYTE_READ')
                _name_boundary.attributes(mosaic_rss_589fa71)['end_current_token']()
                _name_boundary.attributes(mosaic_rss_589fa71)['reset_base']()
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_RANGE_BYTE_READ']:
                mosaic_logger.debug('state is STATE_RANGE_BYTE_READ')
                _name_boundary.attributes(mosaic_rss_589fa71)['update_base_stack']()
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                mosaic_b_array_d58eac3 = []
                mosaic_all_ascii_169a6ef = True
                mosaic_token_bf407b6 = ''
                for mosaic_i_a6eeea1 in range(0, mosaic_b_cdeff8f + 1):
                    mosaic_b1_3607fa9 = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                    mosaic_b2_c64c562 = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                    if mosaic_b1_3607fa9 < 32 or mosaic_b1_3607fa9 > 127 or mosaic_b2_c64c562 < 32 or (mosaic_b2_c64c562 > 127):
                        mosaic_all_ascii_169a6ef = False
                    mosaic_b_array_d58eac3.append((mosaic_b1_3607fa9, mosaic_b2_c64c562))
                if mosaic_all_ascii_169a6ef == False:
                    mosaic_token_bf407b6 = '[UNSUPPORTED]'
                else:
                    mosaic_token_bf407b6 = '['
                    for mosaic_b1_3607fa9, mosaic_b2_c64c562 in mosaic_b_array_d58eac3:
                        mosaic_token_bf407b6 += '{:c}-{:c}'.format(mosaic_b1_3607fa9, mosaic_b2_c64c562)
                    mosaic_token_bf407b6 += ']'
                _name_boundary.attributes(mosaic_rss_589fa71)['token'] = mosaic_token_bf407b6
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_SPLIT_BYTE_READ']:
                mosaic_logger.debug('state is STATE_SPLIT_BYTE_READ')
                mosaic_substr_len_db2a5d6 = _name_boundary.attributes(mosaic_rss_589fa71)['get_last_byte']() - 127
                mosaic_substr_16c2e06 = _name_boundary.attributes(mosaic_rss_589fa71)['get_substring'](mosaic_substr_len_db2a5d6)
                mosaic_subtokens_e6981af = _name_boundary.attributes(mosaic_self_ed51b3f)['parse_byte_string'](mosaic_substr_16c2e06, mosaic_global_vars_6692752)
                _name_boundary.attributes(mosaic_rss_589fa71)['end_with_subtokens'](mosaic_subtokens_e6981af)
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_SINGLE_BYTE_READ']:
                mosaic_logger.debug('state is STATE_SINGLE_BYTE_READ')
                _name_boundary.attributes(mosaic_rss_589fa71)['read_token'](1)
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_RESET_STRING']:
                mosaic_logger.debug('state is STATE_RESET_STRING')
                _name_boundary.attributes(mosaic_rss_589fa71)['end_current_token']()
                _name_boundary.attributes(mosaic_rss_589fa71)['reset_base_full']()
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_PLUS_READ']:
                mosaic_logger.debug('state is STATE_PLUS_READ')
                if _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONCAT_BYTE_READ']:
                    _name_boundary.attributes(mosaic_rss_589fa71)['token'] = '+'
                    _name_boundary.attributes(mosaic_rss_589fa71)['update_base']()
                else:
                    mosaic_logger.warn('previous state is not concat')
                _name_boundary.attributes(mosaic_rss_589fa71)['read_token'](1)
                mosaic_b_cdeff8f = _name_boundary.attributes(mosaic_rss_589fa71)['get_next_byte']()
                _name_boundary.attributes(mosaic_rss_589fa71)['update_state'](mosaic_b_cdeff8f)
            else:
                mosaic_logger.warn('unknown state ({:d})'.format(_name_boundary.attributes(mosaic_rss_589fa71)['state']))
                break
            if _name_boundary.attributes(mosaic_rss_589fa71)['is_end']():
                break
        if _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_END_BYTE_READ']:
            mosaic_logger.debug('state is STATE_END_BYTE_READ')
            _name_boundary.attributes(mosaic_rss_589fa71)['end_current_token']()
        elif _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_UNKNOWN'] or _name_boundary.attributes(mosaic_rss_589fa71)['state'] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_CONCAT_BYTE_READ']:
            pass
        elif _name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1] == _name_boundary.attributes(mosaic_rss_589fa71)['STATE_END_BYTE_READ']:
            pass
        else:
            mosaic_logger.warn('last state is not STATE_END_BYTE_READ ({:d})'.format(_name_boundary.attributes(mosaic_rss_589fa71)['state']))
            mosaic_logger.warn('previous state ({:d})'.format(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack'][len(_name_boundary.attributes(mosaic_rss_589fa71)['state_stack']) - 1]))
        mosaic_logger.info('output_strings (num: {:d}): {:s}'.format(len(_name_boundary.attributes(mosaic_rss_589fa71)['output_strings']), ','.join(('"{:s}"'.format(mosaic_s_bfe3ef7) for mosaic_s_bfe3ef7 in _name_boundary.attributes(mosaic_rss_589fa71)['output_strings']))))
        return _name_boundary.attributes(mosaic_rss_589fa71)['output_strings']

    @_name_boundary.callable_contract({'self': 'mosaic_self_7692a3b'}, '__init__')
    def __init__(mosaic_self_7692a3b):
        _name_boundary.attributes(mosaic_self_7692a3b)['rss_stack'] = []

@_name_boundary.callable_contract({}, 'main')
def mosaic_main():
    mosaic_s_dd4ac67 = mosaic_sys.stdin.read()
    mosaic_ss_9d54adb = mosaic_SandboxString()
    mosaic_my_global_vars_b8c6df4 = ['FRONT_USER_HOME', 'HOME', 'PROCESS_TEMP_DIR']
    mosaic_l_1e829fd = _name_boundary.attributes(mosaic_ss_9d54adb)['parse_byte_string'](mosaic_s_dd4ac67[4:], mosaic_my_global_vars_b8c6df4)
    print(list(set(mosaic_l_1e829fd)))
if __name__ == '__main__':
    mosaic_sys.exit(mosaic_main())
_name_boundary.module_contract(globals(), {'logger': 'mosaic_logger', 'struct': 'mosaic_struct', 'SandboxString': 'mosaic_SandboxString', 'main': 'mosaic_main', 'logging': 'mosaic_logging', 'sys': 'mosaic_sys', 'ReverseStringState': 'mosaic_ReverseStringState'})
