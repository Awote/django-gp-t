from django.core.management.base import BaseCommand
from reports_worker.queue_listener import ReportDataListener

class Command(BaseCommand):
    help = 'Launches Listener for user_created message : RaabitMQ'
    def handle(self, *args, **options):
        td = ReportDataListener()
        td.start()
        self.stdout.write("Started Consumer Thread")