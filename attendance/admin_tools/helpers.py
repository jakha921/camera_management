from datetime import time

from django.utils.html import format_html


def time_to_seconds(t: time) -> int:
    """
    Converts a time object to seconds since midnight.
    """
    return t.hour * 3600 + t.minute * 60 + t.second


def calculate_working_hours(min_time, max_time):
    """
    Calculates working hours in "HH:MM" format, considering break times.
    """
    if not min_time or not max_time:
        return "-"

    # Convert to seconds
    in_seconds = time_to_seconds(min_time)
    out_seconds = time_to_seconds(max_time)

    # Calculate the difference
    diff_seconds = out_seconds - in_seconds

    if diff_seconds <= 0:
        return format_html("<span>-</span>")

    # Deduct 1 hour for breaks if worked more than 6 hours
    if diff_seconds >= 6 * 3600:
        diff_seconds -= 3600

    hours = diff_seconds // 3600
    minutes = (diff_seconds % 3600) // 60
    return f"{hours}:{minutes:02d}", hours


def get_time_for_condition(pinfl, date, is_in, func):
    """
    Query the database for MIN or MAX time based on the condition.
    """
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT {func}(b.time)
            FROM public.attendance AS b
            WHERE is_in = %s AND b.pinfl = %s AND b.date = %s
        """, [is_in, pinfl, date])
        row = cursor.fetchone()

    return row[0] if row else None


def format_time_with_color(time_value, condition_time, condition, link_url):
    """
    Format a time value with color and hyperlink based on a condition.
    """
    from django.utils.html import format_html

    if not time_value:
        return format_html('<span>-</span>')

    color = "green" if condition(time_value, condition_time) else "red"
    return format_html(
        '<a href="{}" style="color: {};">{}</a>',
        link_url,
        color,
        time_value.strftime('%H:%M')
    )
