from datetime import time

from django.contrib import admin


class ComeLateFilter(admin.SimpleListFilter):
    title = 'Kelgan vaqt buyicha saralash'
    parameter_name = 'come_late'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Kechikkan'),
            ('false', 'Vaqtida kelgan'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(time__gt=time(9, 5))
        if self.value() == 'false':
            return queryset.filter(time__lte=time(9, 5))
        return queryset


class WentEarlyFilter(admin.SimpleListFilter):
    title = 'Ketgan vaqt buyicha saralash'
    parameter_name = 'went_early'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Oldin ketgan'),
            ('false', 'Vaqtida ketgan'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(time__lt=time(18, 0))
        if self.value() == 'false':
            return queryset.filter(time__gte=time(18, 0))
        return queryset