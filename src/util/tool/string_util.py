import math

decimal_points = 7


def convert_to_float(value: str) -> float | str | None:
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
