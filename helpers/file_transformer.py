from datetime import datetime

def convert_list_to_touple(list):
    return (*list, )

def transform_to_previous_form(object):
    if 'positions' in object:
        list_positions= []
        for pos in object['positions']:
            list_positions.append(tuple(pos))
        object['positions'] = list_positions
    if 'timestamps' in object:
        list_timestamps = []
        for string_stamp in object['timestamps']:
            list_timestamps.append(datetime.fromisoformat(string_stamp))
        object['timestamps'] = list_timestamps
    return object

