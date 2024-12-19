from django.conf import settings
from django.core.mail import send_mail


def send_notification_to_customers(model_name, model_version, customers):
    """Отправляет уведомление о наличии робота."""

    # Формируем сообщение с информацией о роботе
    email_body = f"""
    <p>Добрый день!</p>

    <p>Недавно вы интересовались нашим роботом модели {model_name}, версии {model_version}.</p>

    <p>Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.</p>
    """

    # Тема письма
    subject = f"Модель {model_name}-{model_version} теперь в наличии"

    # Отправка письма
    send_mail(
        subject=subject,
        message=email_body,
        html_message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=customers,
        fail_silently=False,
    )