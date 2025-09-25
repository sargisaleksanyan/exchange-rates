import json
from typing import List


def get_value_from_json(data, key):
    if data is not None and key in data:
        return data[key]

    return None


# this function retrives deeply nested object and array is array of keys
def get_value_from_json_by_array(data, keys: List[str]):
    if data is not None:
        for i in range(0, len(keys)):
            key = keys[i]
            if key in data:
                data = data[key]
                if (i == len(keys) - 1):
                    return data

    return None


def get_value_from_json_recursively(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = get_value_from_json_recursively(v, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = get_value_from_json_recursively(item, key)
            if result is not None:
                return result
    return None


def get_value_from_json_by_queue(data, key):
    queue = [data]

    while (len(queue) > 0):
        element = queue.pop(0)

        if isinstance(element, dict):
            if key in element:
                return element[key]
            for k in element.keys():
                v = element[k]
                if (v is not None):
                    queue.append(v)
        elif isinstance(element, list):
            for item in element:
                queue.append(item)

    return None


def parse_string_to_json(json_string: str):
    try:
        json_object = json.loads(json_string)
        return json_object
    except Exception as error:
        print('Error occurred while parsing json', error)  # TODO add logger
    return None


def convert_dict_to_json(json_string: dict):
    try:
        json_dump = json.dumps(json_string)
        return json_dump
    except Exception as error:
        print('Error occurred while dumping json', error)  # TODO add logger
    return None
