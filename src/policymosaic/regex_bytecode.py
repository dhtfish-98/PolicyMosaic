# Derived from reverse-sandbox/regex_parser.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import logging as mosaic_logging
import logging.config as _boundary_logging_configuration
mosaic_logging.config.fileConfig(_name_boundary.resource('logger.config'))
mosaic_logger = mosaic_logging.getLogger(__name__)

@_name_boundary.callable_contract({'re': 'mosaic_re_ae57e2c', 'i': 'mosaic_i_35d2cee', 'regex_list': 'mosaic_regex_list_69ae563'}, 'parse_character')
def mosaic_parse_character(mosaic_re_ae57e2c, mosaic_i_35d2cee, mosaic_regex_list_69ae563):
    mosaic_value_fd6422b = chr(mosaic_re_ae57e2c[mosaic_i_35d2cee + 1])
    if mosaic_value_fd6422b == '.':
        mosaic_value_fd6422b = '[.]'
    mosaic_regex_list_69ae563.append({'pos': mosaic_i_35d2cee - 6, 'type': 'character', 'value': mosaic_value_fd6422b})
    return mosaic_i_35d2cee + 1

@_name_boundary.callable_contract({'i': 'mosaic_i_bf0463c', 'regex_list': 'mosaic_regex_list_8b82df0'}, 'parse_beginning_of_line')
def mosaic_parse_beginning_of_line(mosaic_i_bf0463c, mosaic_regex_list_8b82df0):
    mosaic_regex_list_8b82df0.append({'pos': mosaic_i_bf0463c - 6, 'type': 'character', 'value': '^'})

@_name_boundary.callable_contract({'i': 'mosaic_i_11b0437', 'regex_list': 'mosaic_regex_list_4d19b72'}, 'parse_end_of_line')
def mosaic_parse_end_of_line(mosaic_i_11b0437, mosaic_regex_list_4d19b72):
    mosaic_regex_list_4d19b72.append({'pos': mosaic_i_11b0437 - 6, 'type': 'character', 'value': '$'})

@_name_boundary.callable_contract({'i': 'mosaic_i_7ebc9d4', 'regex_list': 'mosaic_regex_list_8262af4'}, 'parse_any_character')
def mosaic_parse_any_character(mosaic_i_7ebc9d4, mosaic_regex_list_8262af4):
    mosaic_regex_list_8262af4.append({'pos': mosaic_i_7ebc9d4 - 6, 'type': 'character', 'value': '.'})

@_name_boundary.callable_contract({'re': 'mosaic_re_e3cc3b7', 'i': 'mosaic_i_de75fc2', 'regex_list': 'mosaic_regex_list_aec2b22'}, 'parse_jump_forward')
def mosaic_parse_jump_forward(mosaic_re_e3cc3b7, mosaic_i_de75fc2, mosaic_regex_list_aec2b22):
    mosaic_jump_to_0931527 = mosaic_re_e3cc3b7[mosaic_i_de75fc2 + 1] + (mosaic_re_e3cc3b7[mosaic_i_de75fc2 + 2] << 8)
    mosaic_regex_list_aec2b22.append({'pos': mosaic_i_de75fc2 - 6, 'type': 'jump_forward', 'value': mosaic_jump_to_0931527})
    return mosaic_i_de75fc2 + 2

@_name_boundary.callable_contract({'re': 'mosaic_re_9bd90e7', 'i': 'mosaic_i_01c5641', 'regex_list': 'mosaic_regex_list_a5ae458'}, 'parse_jump_backward')
def mosaic_parse_jump_backward(mosaic_re_9bd90e7, mosaic_i_01c5641, mosaic_regex_list_a5ae458):
    mosaic_jump_to_2e1bd0c = mosaic_re_9bd90e7[mosaic_i_01c5641 + 1] + (mosaic_re_9bd90e7[mosaic_i_01c5641 + 2] << 8)
    mosaic_regex_list_a5ae458.append({'pos': mosaic_i_01c5641 - 6, 'type': 'jump_backward', 'value': mosaic_jump_to_2e1bd0c})
    mosaic_logger.debug('(0xa) i: %d (0x%x), re[i, i+1, i+2]: 0x%x, 0x%x, 0x%x', mosaic_i_01c5641, mosaic_i_01c5641, mosaic_re_9bd90e7[mosaic_i_01c5641], mosaic_re_9bd90e7[mosaic_i_01c5641 + 1], mosaic_re_9bd90e7[mosaic_i_01c5641 + 2])
    mosaic_logger.debug('value: 0x%x', mosaic_jump_to_2e1bd0c)
    return mosaic_i_01c5641 + 2

@_name_boundary.callable_contract({'re': 'mosaic_re_af7ad16', 'i': 'mosaic_i_f7c278a', 'regex_list': 'mosaic_regex_list_77fd2f0'}, 'parse_character_class')
def mosaic_parse_character_class(mosaic_re_af7ad16, mosaic_i_f7c278a, mosaic_regex_list_77fd2f0):
    mosaic_num_f1fb09c = mosaic_re_af7ad16[mosaic_i_f7c278a] >> 4
    mosaic_i_f7c278a = mosaic_i_f7c278a + 1
    mosaic_logger.debug('i: %d, num: %d', mosaic_i_f7c278a, mosaic_num_f1fb09c)
    mosaic_values_65d4fd2 = []
    mosaic_value_f17498b = '['
    for mosaic_j_dd9b763 in range(0, mosaic_num_f1fb09c):
        mosaic_values_65d4fd2.append(mosaic_re_af7ad16[mosaic_i_f7c278a + 2 * mosaic_j_dd9b763])
        mosaic_values_65d4fd2.append(mosaic_re_af7ad16[mosaic_i_f7c278a + 2 * mosaic_j_dd9b763 + 1])
    mosaic_first_4dbd4c5 = mosaic_values_65d4fd2[0]
    mosaic_last_0a44f4c = mosaic_values_65d4fd2[2 * mosaic_num_f1fb09c - 1]
    if mosaic_first_4dbd4c5 > mosaic_last_0a44f4c:
        mosaic_node_type_e900a46 = 'class_exclude'
        mosaic_value_f17498b += '^'
        for mosaic_j_dd9b763 in range(len(mosaic_values_65d4fd2) - 1, 0, -1):
            mosaic_values_65d4fd2[mosaic_j_dd9b763] = mosaic_values_65d4fd2[mosaic_j_dd9b763 - 1]
        mosaic_values_65d4fd2[0] = mosaic_last_0a44f4c
        for mosaic_j_dd9b763 in range(0, len(mosaic_values_65d4fd2)):
            if mosaic_j_dd9b763 % 2 == 0:
                mosaic_values_65d4fd2[mosaic_j_dd9b763] = mosaic_values_65d4fd2[mosaic_j_dd9b763] + 1
            else:
                mosaic_values_65d4fd2[mosaic_j_dd9b763] = mosaic_values_65d4fd2[mosaic_j_dd9b763] - 1
    else:
        mosaic_node_type_e900a46 = 'class'
    for mosaic_j_dd9b763 in range(0, len(mosaic_values_65d4fd2), 2):
        if mosaic_values_65d4fd2[mosaic_j_dd9b763] < mosaic_values_65d4fd2[mosaic_j_dd9b763 + 1]:
            mosaic_value_f17498b += '%s-%s' % (chr(mosaic_values_65d4fd2[mosaic_j_dd9b763]), chr(mosaic_values_65d4fd2[mosaic_j_dd9b763 + 1]))
        else:
            mosaic_value_f17498b += '%s' % chr(mosaic_values_65d4fd2[mosaic_j_dd9b763])
    mosaic_value_f17498b += ']'
    mosaic_regex_list_77fd2f0.append({'pos': mosaic_i_f7c278a - 6, 'type': mosaic_node_type_e900a46, 'value': mosaic_value_f17498b})
    mosaic_message_4970def = ('values: [', ', '.join([hex(mosaic_j_0af7ee9) for mosaic_j_0af7ee9 in mosaic_values_65d4fd2]), ']')
    mosaic_logger.debug(mosaic_message_4970def)
    return mosaic_i_f7c278a + 2 * mosaic_num_f1fb09c - 1

@_name_boundary.callable_contract({'re': 'mosaic_re_e2b742d', 'i': 'mosaic_i_b6e0f27', 'regex_list': 'mosaic_regex_list_41d2a63'}, 'parse_end')
def mosaic_parse_end(mosaic_re_e2b742d, mosaic_i_b6e0f27, mosaic_regex_list_41d2a63):
    mosaic_regex_list_41d2a63.append({'pos': mosaic_i_b6e0f27 - 6, 'type': 'end', 'value': 0})
    return mosaic_i_b6e0f27 + 1

@_name_boundary.callable_contract({'re': 'mosaic_re_a0a15f0', 'i': 'mosaic_i_a169578', 'regex_list': 'mosaic_regex_list_4b211ba'}, 'parse')
def mosaic_parse(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba):
    if mosaic_re_a0a15f0[mosaic_i_a169578] == 2:
        mosaic_i_a169578 = mosaic_parse_character(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] == 25:
        mosaic_parse_beginning_of_line(mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] == 41:
        mosaic_parse_end_of_line(mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] == 9:
        mosaic_parse_any_character(mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] == 47:
        mosaic_i_a169578 = mosaic_parse_jump_forward(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] & 15 == 10:
        mosaic_i_a169578 = mosaic_parse_jump_backward(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] & 15 == 11:
        mosaic_i_a169578 = mosaic_parse_character_class(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba)
    elif mosaic_re_a0a15f0[mosaic_i_a169578] & 15 == 5:
        mosaic_i_a169578 = mosaic_parse_end(mosaic_re_a0a15f0, mosaic_i_a169578, mosaic_regex_list_4b211ba)
    else:
        mosaic_logger.warning('##########unknown', hex(mosaic_re_a0a15f0[mosaic_i_a169578]))
    return mosaic_i_a169578 + 1

@_name_boundary.class_contract('RegexParser', {'parse': 'mosaic_parse'})
class mosaic_RegexParser(object):

    @staticmethod
    @_name_boundary.callable_contract({'re': 'mosaic_re_a390833', 'i': 'mosaic_i_460e942', 'regex_list': 'mosaic_regex_list_7a35609'}, 'parse')
    def mosaic_parse(mosaic_re_a390833, mosaic_i_460e942, mosaic_regex_list_7a35609):
        while mosaic_i_460e942 < len(mosaic_re_a390833):
            mosaic_i_460e942 = mosaic_parse(mosaic_re_a390833, mosaic_i_460e942, mosaic_regex_list_7a35609)
_name_boundary.module_contract(globals(), {'parse_end_of_line': 'mosaic_parse_end_of_line', 'parse_jump_forward': 'mosaic_parse_jump_forward', 'logger': 'mosaic_logger', 'parse_end': 'mosaic_parse_end', 'parse_character_class': 'mosaic_parse_character_class', 'parse': 'mosaic_parse', 'RegexParser': 'mosaic_RegexParser', 'logging': 'mosaic_logging', 'parse_any_character': 'mosaic_parse_any_character', 'parse_jump_backward': 'mosaic_parse_jump_backward', 'parse_character': 'mosaic_parse_character', 'parse_beginning_of_line': 'mosaic_parse_beginning_of_line'})
