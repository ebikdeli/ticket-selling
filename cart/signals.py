from django.db.models.signals import post_init
from django.dispatch import receiver


# @receiver(post_init, sender='cart.Cart')
# def delete_empty_active_orders(sender, instance=None, *args, **kwargs):
#     if not instance.total_quantity:
#         instance.order_cart.filter(is_active=True).delete()
