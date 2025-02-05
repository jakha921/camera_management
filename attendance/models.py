from django.db import models


# Create your models here.
class Attendance(models.Model):
    name = models.CharField(max_length=100, verbose_name='FIO')
    pinfl = models.CharField(max_length=20, verbose_name='PINFL', blank=True, null=True)
    date = models.DateField(verbose_name='Sana')
    time = models.TimeField(verbose_name='Vaqt')
    device_id = models.CharField(max_length=100, verbose_name='Device ID')
    card = models.CharField(max_length=20, blank=True, null=True, verbose_name='Karta')
    description = models.TextField(blank=True, null=True, verbose_name='Izoh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_color = models.CharField(max_length=10, blank=True, null=True, default='green',
                                    verbose_name='Vaqtida bo\'lganligi',
                                    help_text='green - vaqtida, red - kechikkan, yellow - sababi bilan kelmagan',
                                    choices=[
                                        ('green', 'green'),
                                        ('red', 'red'),
                                        ('yellow', 'yellow')
                                    ])
    is_in = models.BooleanField(default=True, verbose_name='Ishga keldi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kelgan '
        verbose_name_plural = 'Kelganlar '
        ordering = ['-date', '-time', 'is_in']
        db_table = 'attendance'
        indexes = [
            models.Index(fields=['date', 'time', 'pinfl']),
        ]


class Employee(models.Model):
    last_name = models.CharField(max_length=255, verbose_name='Familiya', blank=True, null=True)
    first_name = models.CharField(max_length=255, verbose_name='Ism', blank=True, null=True)
    middle_name = models.CharField(max_length=255, verbose_name='Otasining ismi', blank=True, null=True)
    pinfl = models.CharField(max_length=20, verbose_name='PINFL', blank=True, null=True)
    dob = models.DateField(verbose_name='Tug\'ilgan kun', blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name='Izoh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='employee/', blank=True, null=True, verbose_name='Rasm')
    bid = models.CharField(max_length=20, blank=True, null=True, verbose_name='Stavka')
    types = models.CharField(max_length=20, blank=True, null=True, verbose_name='Xodim turi',
                             choices=[
                                 ('employee', 'Pesonal xodimlar'),
                                 ('exact_sciences', 'Aniq, texnika va tabiiy fanlar kafedrasi'),
                                 ('economy', 'Iqtisodiyot va axborot texnologiyalari kafedrasi'),
                                 ('linguistic', 'Filologiya va tillarni o\'qitish kafedrasi'),
                                 ('social', 'Ijtimoiy-gumanitar fanlar kafedrasi'),

                             ])

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        ordering = ['last_name', 'first_name', 'middle_name']
        db_table = 'employee'
        indexes = [
            models.Index(fields=[
                'last_name',
                'first_name',
                'middle_name',
                'pinfl'
            ]),
        ]