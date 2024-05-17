from django.contrib import admin
from django.db import connection
from django.urls import reverse
from django.utils.html import format_html

from attendance.models import Attendance

from django.utils.safestring import mark_safe

# Register your models here.
admin.site.site_header = 'Ishchilarning kelib ketish sistemase'
admin.site.site_title = 'Ishchilarning kelib ketish sistemase'
admin.site.index_title = 'Ishchilarning kelib ketish sistemase'


@admin.register(Attendance)
class QuestionAdmin(admin.ModelAdmin):
    # list_display = ['device_id', 'name', 'date', 'time', 'color_status']
    list_display = ['device_id', 'name', 'date', 'min_in_time', 'max_out_time', 'color_status', 'status_color']

    search_fields = ['name', 'device_id']
    list_filter = ['status_color', 'is_in']
    ordering = ['-date', '-time']
    list_per_page = 15
    list_max_show_all = 100
    date_hierarchy = 'date'
    actions = ['download_csv']
    readonly_fields = ['device_id']
    list_editable = ['status_color']

    # if user is not superuser remove clickable field
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return []

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

        writer = csv.writer(response)
        # writer.writerow(['Name', 'Date', 'Time', 'Device ID'])
        writer.writerow(['№', 'FIO', 'Sana', 'Vaqt'])

        for index, item in enumerate(queryset):
            # change date format to 'DD-MM-YYYY'
            writer.writerow([index + 1, item.name, item.date.strftime('%d-%m-%Y'), item.time])

        return response

    download_csv.short_description = 'CSV fayl qilib yuklash'

    def color_status(self, obj):
        if obj.status_color == 'red':
            # show red circle if time > 09:01:00
            return mark_safe('<span style="color: red;">&#11044;</span>')
        elif obj.status_color == 'yellow':
            return mark_safe('<span style="color: yellow;">&#11044;</span>')
        else:
            return mark_safe('<span style="color: green;">&#11044;</span>')

    color_status.short_description = 'Status'
    readonly_fields = ['color_status']

    def min_in_time(self, obj):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT min(b.time)
                FROM public.attendance AS b
                WHERE is_in = True AND b.device_id = %s AND b.date = %s
            """, [obj.device_id, obj.date])
            row = cursor.fetchone()

        # set as link to change page
        min_in_url = reverse('admin:attendance_attendance_change',
                             args=[obj.pk]) if row else ''

        if row[0]:
            return format_html('<a href="{}">{}</a>', min_in_url, row[0])
        else:
            return format_html('<span>-</span>')

    min_in_time.short_description = 'Keldi'

    def max_out_time(self, obj):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT max(b.time)
                FROM public.attendance AS b
                WHERE is_in = False AND b.device_id = %s AND b.date = %s
            """, [obj.device_id, obj.date])
            row = cursor.fetchone()

        # set as link to change page
        max_out_url = reverse('admin:attendance_attendance_change',
                              args=[obj.pk]) if row else ''
        if row[0]:
            return format_html('<a href="{}">{}</a>', max_out_url, row[0])
        else:
            return format_html('<span>-</span>')

    max_out_time.short_description = 'Ketdi'

    def changelist_view(self, request, extra_context=None):
        if not request.GET.get('is_in__exact'):
            q = request.GET.copy()
            q['is_in__exact'] = 'True'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)
