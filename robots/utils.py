from datetime import timedelta
from io import BytesIO

import pandas as pd
from django.db.models import Count
from django.utils import timezone

from robots.models import Robot


def create_report():
    """Функция создания отчета по роботам"""

    # Определяем диапазон дат для последней недели
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    # Запрашиваем данные из модели Robot
    robot_info = (Robot.objects.values("model", "version")
                  .filter(created__range=[start_date, end_date])
                  .annotate(count=Count("id")).order_by("model", "version"))

    # Создаем DataFrame из списка
    df = pd.DataFrame(list(robot_info))

    # Переименовываем столбцы
    df.columns = ['Модель', 'Версия', 'Количество за неделю']

    # Сохраняем DataFrame в Excel-файл в памяти
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Robot_Report", index=False)

    # Возвращаем указатель в начало файла
    excel_file.seek(0)
    return excel_file
