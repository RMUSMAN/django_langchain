# your_app/management/commands/import_tickets.py
import csv
from django.core.management.base import BaseCommand
from ...models.ticket import SupportTicket
from datetime import datetime

class Command(BaseCommand):
    help = 'Import support tickets from a CSV file into SQLite'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticket = SupportTicket(
                    ticket_id=int(row['ticket_id']),
                    customer_name=row['customer_name'],
                    issue_description=row['issue_description'],
                    resolution=row['resolution'],
                    date_submitted=datetime.strptime(row['date_submitted'], '%Y-%m-%d').date()
                )
                ticket.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully imported tickets from {csv_file}'))