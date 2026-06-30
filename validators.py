from exceptions import InvalidDataError

def require_text(value, field_name):
    if value is None or not str(value).strip():
        raise InvalidDataError(f"{field_name} is required.")
    return str(value).strip()


def require_positive_number(value, field_name):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise InvalidDataError(f"{field_name} must be a number.")

    if value <= 0:
        raise InvalidDataError(f"{field_name} must be positive.")

    return value


def require_non_negative_number(value, field_name):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise InvalidDataError(f"{field_name} must be a number.")

    if value < 0:
        raise InvalidDataError(f"{field_name} cannot be negative.")

    return value


def require_positive_int(value, field_name):
    if isinstance(value, bool):
        raise InvalidDataError(f"{field_name} must be an integer.")

    try:
        if isinstance(value, float) and not value.is_integer():
            raise ValueError
        value = int(value)
    except (TypeError, ValueError):
        raise InvalidDataError(f"{field_name} must be an integer.")

    if value <= 0:
        raise InvalidDataError(f"{field_name} must be positive.")

    return value


def require_non_negative_int(value, field_name):
    if isinstance(value, bool):
        raise InvalidDataError(f"{field_name} must be an integer.")

    try:
        if isinstance(value, float) and not value.is_integer():
            raise ValueError
        value = int(value)
    except (TypeError, ValueError):
        raise InvalidDataError(f"{field_name} must be an integer.")

    if value < 0:
        raise InvalidDataError(f"{field_name} cannot be negative.")

    return value
