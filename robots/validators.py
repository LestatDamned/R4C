from datetime import datetime

from django.core.exceptions import ValidationError


def validate_required_fields(data, required_fields):
    """Проверяет наличие обязательных полей в данных."""
    for field in required_fields:
        if field not in data:
            raise ValidationError({"ошибка": f"Поле '{field}' обязательно для заполнения"})


def validate_string_field(value, field_name, max_length):
    """Проверяет, что поле является строкой и не превышает заданную длину."""
    if not isinstance(value, str) or len(value) > max_length:
        raise ValidationError({"ошибка": f"Поле '{field_name}' должно быть строкой длиной до {max_length} символов"})


def validate_datetime_field(value, field_name):
    """Проверяет, что дата и время соответствуют формату 'YYYY-MM-DD HH:MM:SS'."""
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        raise ValidationError({"ошибка": f"Поле '{field_name}' должно быть в формате 'YYYY-MM-DD HH:MM:SS'"})


def validate_robot(data):
    """Валидатор для данных робота."""
    required_fields = ["model", "version", "created"]
    validate_required_fields(data, required_fields)

    validate_string_field(data["model"], "model", 2)
    validate_string_field(data["version"], "version", 2)
    data["created"] = validate_datetime_field(data["created"], "created")

    return data
