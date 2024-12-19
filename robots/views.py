import json
from json import JSONDecodeError

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Robot
from .utils import create_report
from .validators import validate_robot


@csrf_exempt
def create_robot(request):
    """Endpoint для приёма JSON и создания записи о роботе в базе данных"""

    if request.method != "POST":
        return JsonResponse({"ошибка": "Метод не поддерживается"}, status=405)

    try:
        # Получаем входные данные
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({"ошибка": "JSON не был передан или имеет неверный формат"}, status=400)

    try:
        # Валидируем входные данные
        validated_data = validate_robot(data)
    except ValidationError as e:
        return JsonResponse({"ошибка": f"{e}"})

    # Создаем робота в базе данных
    new_robot = Robot.objects.create(
        serial=f"{validated_data['model']}-{validated_data['version']}",
        model=validated_data["model"],
        version=validated_data["version"],
        created=timezone.make_aware(validated_data["created"]),
    )

    # Возвращаем ответ с данными созданного робота
    return JsonResponse({
        "id": new_robot.id,
        "serial": new_robot.serial,
        "model": new_robot.model,
        "version": new_robot.version,
        "created": new_robot.created.strftime('%Y-%m-%d %H:%M:%S')
    }, status=201)


def create_robot_report(request):
    """Endpoint для получения отчета по производству роботов за последнюю неделю"""

    if request.method != "GET":
        return JsonResponse({"ошибка": "Метод не поддерживается"}, status=405)

    # Вызываем create_report для создания Excel-файла
    excel_file = create_report()

    # Возвращаем файл в ответе
    response = HttpResponse(excel_file,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=robot_report.xlsx'
    return response
