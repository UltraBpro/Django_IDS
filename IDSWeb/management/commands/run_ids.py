from django.core.management.base import BaseCommand
from IDSWeb.log_analyzer import analyze_log, analyze_stream

class Command(BaseCommand):
    help = 'Runs the IDS log analyzer with file or stream source'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-f', 
            '--file',
            type=str,
            help='Path to the log file'
        )
        group.add_argument(
            '-s',
            '--stream',
            type=str,
            help='URL of the log stream'
        )

    def handle(self, *args, **options):
        if options['file']:
            source = options['file']
            self.stdout.write(self.style.SUCCESS(f'Starting IDS analysis on file: {source}'))
            analyze_log(source)
        elif options['stream']:
            source = options['stream']
            self.stdout.write(self.style.SUCCESS(f'Starting IDS analysis on stream: {source}'))
            analyze_stream(source)
