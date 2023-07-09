from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='ticket.TicketSold')
def add_to_ticket_number_sold(sender, instance, created, **kwargs):
    """If a user bought a ticket, add the quantity of the sold ticket to the Ticket.number_sold"""
    if created:
        instance.ticket.number_sold += instance.quantity
        instance.ticket.save()
