def convert_to_float(value: str) -> float | str | None:
    try:
        return float(value)
    except Exception as err:
        print('Error while converting string to float ', value)

    return value
