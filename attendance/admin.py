from datetime import time
from functools import lru_cache

from django.contrib import admin
from django.db import models
from django.db.models import Subquery, OuterRef, Min, Max
from django.forms import Textarea
from django.urls import reverse
from django.utils.html import format_html

from attendance.admin_tools.actions import (
    absent_report_by_pinfl,
    attendance_report_by_pinfl
)
from attendance.admin_tools.filters import ComeLateFilter, WentEarlyFilter, EmployeeTypeFilter
from attendance.admin_tools.helpers import calculate_working_hours, get_time_for_condition, \
    format_time_with_color
from attendance.models import Attendance, Employee

# Register your models here.
admin.site.site_header = 'Ishchilarning kelib ketish sistemase'
admin.site.site_title = 'Ishchilarning kelib ketish sistemase'
admin.site.index_title = 'Ishchilarning kelib ketish sistemase'


@lru_cache(maxsize=10000)
def get_time_for_condition(pinfl, date, is_in, agg_type):
    """Cache database queries for time aggregation."""
    return Attendance.objects.filter(pinfl=pinfl, date=date, is_in=is_in).aggregate(
        result=Min('time') if agg_type == "MIN" else Max('time')
    )['result']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['pinfl_display', 'name', 'date', 'min_in_time', 'max_out_time', 'working_time', 'description']
    search_fields = ['name', 'device_id', 'pinfl']
    list_filter = [ComeLateFilter, WentEarlyFilter]
    ordering = ['-date', '-time']
    list_per_page = 15
    list_max_show_all = 100
    date_hierarchy = 'date'
    actions = [
        # attendance_report,
        absent_report_by_pinfl,
        attendance_report_by_pinfl,
    ]
    readonly_fields = ['device_id']

    list_editable = ['description']

    # Уменьшаем размер поля "description"
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 30})},
    }

    def get_queryset(self, request):
        """
        Overriding get_queryset to eliminate duplicates by grouping by unique identifiers.
        """
        qs = super().get_queryset(request)

        # Subquery to get the earliest record for each pinfl and date
        subquery = qs.filter(
            pinfl=OuterRef('pinfl'),
            date=OuterRef('date')
        ).order_by('id').values('id')[:1]

        # Filter the queryset to include only the earliest record for each group
        return qs.filter(id__in=Subquery(subquery))

    def min_in_time(self, obj):
        min_time = get_time_for_condition(obj.pinfl, obj.date, True, "MIN")
        min_in_url = reverse('admin:attendance_attendance_change', args=[obj.pk])
        return format_time_with_color(min_time, time(9, 5), lambda x, y: x <= y, min_in_url)

    min_in_time.short_description = 'Keldi'

    def max_out_time(self, obj):
        max_time = get_time_for_condition(obj.pinfl, obj.date, False, "MAX")
        print('max_time:', obj.pinfl, obj.name, obj.date, max_time)
        max_out_url = reverse('admin:attendance_attendance_change', args=[obj.pk])
        return format_time_with_color(max_time, time(18, 0), lambda x, y: x >= y, max_out_url)

    max_out_time.short_description = 'Ketdi'

    def working_time(self, obj):
        min_time = get_time_for_condition(obj.pinfl, obj.date, True, "MIN")
        max_time = get_time_for_condition(obj.pinfl, obj.date, False, "MAX")

        if not min_time or not max_time:
            return format_html('<span>-</span>')
        elif max_time < min_time:
            return format_html('<span>-</span>')

        # Adjust times to working hours
        min_time = max(min_time, time(9, 0))
        max_time = min(max_time, time(18, 0))

        diff_str, hours = calculate_working_hours(min_time, max_time)
        color = "green" if hours >= 8 else "red"

        return format_html('<span style="color: {};">{}</span>', color, diff_str)

    working_time.short_description = 'Ish vaqti (soat)'

    def get_list_display(self, request):
        """
        Dynamically update list_display based on the presence of pinfl.
        If pinfl exists, display the employee full name instead of name and set pinfl to device_id.
        """
        if Attendance.objects.filter(pinfl__isnull=False).exists():
            return ['pinfl_display', 'employee', 'date', 'min_in_time', 'max_out_time', 'working_time', 'description']
        return ['device_id', 'name', 'date', 'min_in_time', 'max_out_time', 'working_time', 'description']

    def employee(self, obj):
        if obj.pinfl:
            employee = Employee.objects.filter(pinfl=obj.pinfl).first()
            if employee:
                return f"{employee.last_name} {employee.first_name}"
        return obj.name

    employee.short_description = 'Employee'

    def pinfl_display(self, obj):
        return obj.pinfl or obj.device_id

    pinfl_display.short_description = 'PINFL / Device ID'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'pinfl', 'description', 'images_preview']
    search_fields = ['last_name', 'first_name', 'middle_name', 'pinfl']
    list_per_page = 50
    # readonly_fields = ['pinfl']
    list_filter = [EmployeeTypeFilter]
    ordering = ['image', 'last_name', 'first_name']

    def images_preview(self, obj):
        return format_html('<img src="{}" width="50" height="75" />', obj.image.url) if obj.image else '-'

    images_preview.short_description = 'Rasm'
