from django.contrib import admin
from attendance.models import Attendance


# Register your models here.
admin.site.site_header = 'Ishchilarning kelib ketish sistemase'
admin.site.site_title = 'Ishchilarning kelib ketish sistemase'
admin.site.index_title = 'Ishchilarning kelib ketish sistemase'

@admin.register(Attendance)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'date', 'time']
    search_fields = ['name', 'device_id']
    # list_filter = ['date', 'time']
    ordering = ['-date', '-time']
    list_per_page = 10
    list_max_show_all = 100
    date_hierarchy = 'date'
    actions = ['download_csv']

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
        writer.writerow(['Name', 'Date', 'Time', 'Device ID'])

        for item in queryset:
            writer.writerow([item.name, item.date, item.time, item.device_id])

        return response

    download_csv.short_description = 'Download CSV file'
