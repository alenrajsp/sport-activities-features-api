from datetime import datetime

from sport_activities_features.interruptions.exercise_event import ExerciseEvent


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
    if 'events' in object:
        pass #will be updated if needed in reverse
    return object

