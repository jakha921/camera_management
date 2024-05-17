from django.db import models


# Create your models here.
class Attendance(models.Model):
    name = models.CharField(max_length=100, verbose_name='FIO')
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
            models.Index(fields=['date', 'time', 'device_id']),
        ]
