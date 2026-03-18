import math

decimal_points = 7


def find_substring_index(text: str, substring: str):
    if substring in text:
        return text.index(substring)
    return -1


def is_float_ok(float_value: None | float):
    try:
        return float_value is not None and float_value > 0
    except Exception as err:
        print('Error while checking float ', float_value)
    return False


def convert_to_float(value: str) -> float | str | None:
    if value is None:
        return None
    try:
        return float(value)
    except Exception as err:
        print('Error while converting string to float ', value)

    return None


def convert_to_reverse_float(value: str) -> float | str | None:
    try:
        float_value = float(value)
        if float_value > 0:
            truncated = math.floor(float_value * 10 ** decimal_points) / 10 ** decimal_points
            return 1 / truncated
    except Exception as err:
        print('Error while converting string to float ', value)

    return value


def get_element_text(td_elements, headers: dict, header: str):
    if (header not in headers):
        return None
    index = headers[header]
    if index < 0:
        return None

    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def get_element_text_by_index(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None
