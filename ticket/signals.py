"""When using post_init signal we must be really careful because this signal also called before the instance created"""
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.utils import timezone




@receiver(post_save, sender='ticket.TicketSold')
def add_to_ticket_number_sold(sender, instance, created, **kwargs):
    """If a user bought a ticket, add the quantity of the sold ticket to the Ticket.number_sold"""
    if created:
        instance.ticket.number_sold += instance.quantity
        instance.ticket.save()


@receiver(post_init, sender='ticket.Ticket')
def deactivate_expired_tickets(sender, instance, *args, **kwargs):
    """Check Ticket if lottery_date is past, deativate the ticket"""
    # https://docs.djangoproject.com/en/4.2/topics/i18n/timezones/#naive-and-aware-datetime-objects
    if instance.id:
        if not instance.is_ended:
            now = timezone.now()
            if now > instance.lottery_date:
                instance.is_ended = True
                instance.is_active = False
                instance.save()
