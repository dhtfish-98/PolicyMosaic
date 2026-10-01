# Derived from reverse-sandbox/filters.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import json as mosaic_json

@_name_boundary.callable_contract({}, 'read_filters')
def mosaic_read_filters():
    mosaic_temp_6b15a29 = {}
    mosaic_filters_b11664d = {}
    with open(_name_boundary.resource('filters.json')) as mosaic_data_12e6e5e:
        mosaic_temp_6b15a29 = mosaic_json.load(mosaic_data_12e6e5e)
        for mosaic_key_7589bd7, mosaic_value_024ef92 in mosaic_temp_6b15a29.items():
            mosaic_filters_b11664d[int(str(mosaic_key_7589bd7), 16)] = mosaic_value_024ef92
    return mosaic_filters_b11664d

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
