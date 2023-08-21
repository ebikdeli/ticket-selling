from django.db.models.signals import post_init
from django.dispatch import receiver


@receiver(post_init, sender='cart.Cart')
def delete_empty_active_orders(sender, instance=None, *args, **kwargs):
    """delete active empty orders"""
    if not instance.total_quantity:
        instance.order_cart.filter(is_active=True).delete()



@receiver(post_init, sender='cart.Cart')
def is_paid_unpaid_orders_ticketsolds(sender, instance, *args, **kwargs):
    """If cart is_paid field is True, set its active orders and ticketsolds is_paid field to True then deactivate the orders"""
    if instance.is_paid:
        orders = instance.order_cart.all()
        for order in orders:
            if not order.is_paid:
                order.is_paid = True
                order.is_active = False
                order.save()
        ticketsolds = instance.ticketsold_cart.all()
        for ts in ticketsolds:
            if not ts.is_paid:
                ts.is_paid = True
                ts.is_active = False
                ts.save()
                instance.ticketsold_cart.remove(ts)
                instance.ticket.remove(ts.ticket)
        instance.is_paid = False
        instance.save()
