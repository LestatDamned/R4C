from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from robots.validators import validate_required_fields, validate_string_field


def validate_email_field(email):
    """Проверяет корректность email."""
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError({"ошибка": "email имеет некорректный формат"})


def validate_order(data):
    """Валидатор для данных заказа."""
    required_fields = ["email", "model", "version"]
    validate_required_fields(data, required_fields)

    validate_string_field(data["model"], "model", 2)
    validate_string_field(data["version"], "version", 2)
    validate_email_field(data["email"])

    return data
