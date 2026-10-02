# Derived from reverse-sandbox/modifiers.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import json as mosaic_json

def mosaic_read_modifiers():
    from policymosaic.safety import PolicyFormatError, read_local
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise PolicyFormatError('duplicate packaged catalog key')
            result[key] = value
        return result
    data = mosaic_json.loads(read_local(_name_boundary.resource('modifiers_functions.json'), 1024 * 1024).decode('utf-8'), object_pairs_hook=unique)
    if not isinstance(data, dict) or len(data) > 65536:
        raise PolicyFormatError('invalid packaged catalog')
    output = {}
    for key, value in data.items():
        identifier = int(key, 16)
        if not 0 <= identifier <= 65535 or identifier in output or not isinstance(value, dict) or not isinstance(value.get('name'), str) or value.get('arg_process_fn') is not None and not isinstance(value.get('arg_process_fn'), str):
            raise PolicyFormatError('invalid packaged catalog entry')
        output[identifier] = value
    return output

@_name_boundary.class_contract('Modifiers', {'modifiers': 'mosaic_modifiers', 'exists': 'mosaic_exists', 'get': 'mosaic_get'})
class mosaic_Modifiers(object):
    mosaic_modifiers = mosaic_read_modifiers()

    @staticmethod
    @_name_boundary.callable_contract({'id': 'mosaic_id_933d957'}, 'exists')
    def mosaic_exists(mosaic_id_933d957):
        return mosaic_id_933d957 in _name_boundary.attributes(mosaic_Modifiers)['modifiers']

    @staticmethod
    @_name_boundary.callable_contract({'id': 'mosaic_id_33b1bb9'}, 'get')
    def mosaic_get(mosaic_id_33b1bb9):
        return _name_boundary.attributes(_name_boundary.attributes(mosaic_Modifiers)['modifiers'])['get'](mosaic_id_33b1bb9, None)
_name_boundary.module_contract(globals(), {'read_modifiers': 'mosaic_read_modifiers', 'Modifiers': 'mosaic_Modifiers', 'json': 'mosaic_json'})
