from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.utils import send_notification_to_customers
from robots.models import Robot


@receiver(post_save, sender=Robot)
def new_robots_available(instance, created, **kwargs):
    """Обрабатывает сигнал появления нового робота и отправляет уведомления заказчикам."""

    # Проверяем, что робот только что создан
    if created:
        # Получаем заказы, ожидающие данного робота
        orders = Order.objects.filter(robot_serial=instance.serial).select_related("customer")
        email_addresses = [order.customer.email for order in orders]

        # Отправляем уведомление клиентам, если такие есть
        if email_addresses:
            send_notification_to_customers(instance.model, instance.version, email_addresses)
