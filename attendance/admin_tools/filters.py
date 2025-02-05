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

# filter by employee types
class EmployeeTypeFilter(admin.SimpleListFilter):
    title = 'Xodim turi'
    parameter_name = 'employee_type'

    def lookups(self, request, model_admin):
        return (
            ('employee', 'Pesonal xodimlar'),
            ('exact_sciences', 'Aniq, texnika va tabiiy fanlar kafedrasi'),
            ('economy', 'Iqtisodiyot va axborot texnologiyalari kafedrasi'),
            ('linguistic', 'Filologiya va tillarni o\'qitish kafedrasi'),
            ('social', 'Ijtimoiy-gumanitar fanlar kafedrasi'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'employee':
            return queryset.filter(types='employee')
        if self.value() == 'exact_sciences':
            return queryset.filter(types='exact_sciences')
        if self.value() == 'economy':
            return queryset.filter(types='economy')
        if self.value() == 'linguistic':
            return queryset.filter(types='linguistic')
        if self.value() == 'social':
            return queryset.filter(types='social')
        return queryset