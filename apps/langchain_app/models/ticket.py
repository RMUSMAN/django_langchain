# your_app/models.py
from django.db import models

class SupportTicket(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    issue_description = models.TextField()
    resolution = models.TextField()
    date_submitted = models.DateField()

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.customer_name}"