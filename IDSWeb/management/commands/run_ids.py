from django.core.management.base import BaseCommand
from IDSWeb.log_analyzer import analyze_log

class Command(BaseCommand):
    help = 'Runs the IDS log analyzer'

    def add_arguments(self, parser):
        parser.add_argument('log_file', type=str, help='Path to the log file')

    def handle(self, *args, **options):
        log_file = options['log_file']
        self.stdout.write(self.style.SUCCESS(f'Starting IDS analysis on {log_file}'))
        analyze_log(log_file)
