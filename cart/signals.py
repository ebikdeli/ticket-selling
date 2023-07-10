from django.db.models.signals import post_init
from django.dispatch import receiver


@receiver(post_init, sender='cart.Cart')
def future_use(sender, instance=None, *args, **kwargs):
    pass