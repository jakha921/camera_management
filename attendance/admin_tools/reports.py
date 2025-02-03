from attendance.admin_tools.helpers import calculate_working_hours


def working_time(self, obj):
    """
    Возвращает рабочее время в формате "ЧЧ:ММ".
    1) Обрезаем (09:00 .. 18:00).
    2) Считаем разницу прихода и ухода.
    3) Если > 6ч, вычитаем 1 час на обед (пример).
    4) Выводим HH:MM.
    """
    from datetime import time
    from django.db import connection
    from django.utils.html import format_html

    # 1. Получаем min_time (приход)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MIN(b.time)
            FROM public.attendance AS b
            WHERE is_in = True AND b.device_id = %s AND b.date = %s
        """, [obj.device_id, obj.date])
        row_in = cursor.fetchone()
    min_time = row_in[0] if row_in and row_in[0] else None

    # 2. Получаем max_time (уход)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MAX(b.time)
            FROM public.attendance AS b
            WHERE is_in = False AND b.device_id = %s AND b.date = %s
        """, [obj.device_id, obj.date])
        row_out = cursor.fetchone()
    max_time = row_out[0] if row_out and row_out[0] else None

    # Нет данных?
    if not min_time or not max_time:
        return format_html("<span>-</span>")
    elif max_time < min_time:
        return format_html("<span>-</span>")

    # "Обрезаем" время
    if min_time < time(9, 5):
        min_time = time(9, 0)
    if max_time > time(18, 0):
        max_time = time(18, 0)

    diff_str, hours = calculate_working_hours(min_time, max_time)
    color = "green" if (hours >= 8) else "red"

    return format_html(
        '<span style="color: {};">{}</span>',
        color,
        diff_str
    )

working_time.short_description = 'Ish vaqti (soat)'
