import json
from json import JSONDecodeError

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customer
from robots.models import Robot
from .models import Order
from .validators import validate_order


@csrf_exempt
def create_order(request):
    """Функция создания заказ"""

    if request.method != "POST":
        return JsonResponse({"ошибка": "Метод не поддерживается"}, status=405)

    # Разбор и валидация JSON
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({"ошибка": "JSON не был передан или имеет неверный формат"}, status=400)

    try:
        data = validate_order(data)
    except ValidationError as e:
        return JsonResponse({"ошибка": f"{e}"})

    email = data["email"]
    robot_serial = f"{data["model"]}-{data["version"]}"

    # Получение или создание клиента
    customer, _ = Customer.objects.get_or_create(email=email)

    # Проверка доступности робота
    available_robot = Robot.objects.filter(serial=robot_serial).exists()
    if available_robot:
        return JsonResponse({"заказ": "Робот есть в наличии"}, status=200)

    # Добавление заказа в список ожидания
    order, created = Order.objects.get_or_create(customer=customer, robot_serial=robot_serial)
    if created:
        return JsonResponse({"заказ": "Ваш заказ добавлен в список ожидания, "
                                      "когда робот будет в наличии вам придет письмо на email"}, status=201)
    else:
        return JsonResponse({"заказ": "Уже в списке ождиания, "
                                      "когда робот будет в наличии вам придет письмо на email"}, status=200)
