# Derived from reverse-sandbox/filters.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import json as mosaic_json

def mosaic_read_filters():
    from policymosaic.safety import PolicyFormatError, read_local
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise PolicyFormatError('duplicate packaged catalog key')
            result[key] = value
        return result
    data = mosaic_json.loads(read_local(_name_boundary.resource('filters.json'), 1024 * 1024).decode('utf-8'), object_pairs_hook=unique)
    if not isinstance(data, dict) or len(data) > 65536:
        raise PolicyFormatError('invalid packaged catalog')
    output = {}
    for key, value in data.items():
        identifier = int(key, 16)
        if not 0 <= identifier <= 65535 or identifier in output or not isinstance(value, dict) or not isinstance(value.get('name'), str) or value.get('arg_process_fn') is not None and not isinstance(value.get('arg_process_fn'), str):
            raise PolicyFormatError('invalid packaged catalog entry')
        output[identifier] = value
    return output

@_name_boundary.class_contract('Filters', {'filters': 'mosaic_filters', 'exists': 'mosaic_exists', 'get': 'mosaic_get'})
class mosaic_Filters(object):
    mosaic_filters = mosaic_read_filters()

    @staticmethod
    @_name_boundary.callable_contract({'id': 'mosaic_id_1da4eec'}, 'exists')
    def mosaic_exists(mosaic_id_1da4eec):
        return mosaic_id_1da4eec in _name_boundary.attributes(mosaic_Filters)['filters']

    @staticmethod
    @_name_boundary.callable_contract({'id': 'mosaic_id_d6e8e1a'}, 'get')
    def mosaic_get(mosaic_id_d6e8e1a):
        return _name_boundary.attributes(_name_boundary.attributes(mosaic_Filters)['filters'])['get'](mosaic_id_d6e8e1a, None)
_name_boundary.module_contract(globals(), {'read_filters': 'mosaic_read_filters', 'Filters': 'mosaic_Filters', 'json': 'mosaic_json'})
