# attendance/management/commands/rundatatask.py

from django.core.management.base import BaseCommand
from attendance.tasks import run_parsing


class Command(BaseCommand):
    help = 'Run data parsing task'

    def handle(self, *args, **options):
        print('Running data parsing task')
        run_parsing()
        print('Data parsing task completed')
        self.stdout.write(self.style.SUCCESS('Data parsing task completed successfully'))
