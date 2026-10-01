# Derived from reverse-sandbox/modifiers.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import json as mosaic_json

@_name_boundary.callable_contract({}, 'read_modifiers')
def mosaic_read_modifiers():
    mosaic_modifiers_1631d3f = {}
    with open(_name_boundary.resource('modifiers_functions.json')) as mosaic_data_a7a9546:
        mosaic_temp_d1ebc07 = mosaic_json.load(mosaic_data_a7a9546)
        for mosaic_key_01a7edf, mosaic_value_558ff26 in mosaic_temp_d1ebc07.items():
            mosaic_modifiers_1631d3f[int(str(mosaic_key_01a7edf), 16)] = mosaic_value_558ff26
    return mosaic_modifiers_1631d3f

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
