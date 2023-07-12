from typing import Any, Iterable, Optional
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from _resources import func


class Order(models.Model):
    """Represents every Order customer registers"""
    order_id = models.CharField(verbose_name=_('order_id'), max_length=10, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             related_name='order_user',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart',
                            verbose_name=_('cart'),
                            on_delete=models.CASCADE,
                            related_name='order_cart')
    discounts = models.DecimalField(verbose_name=_('discounts'), max_digits=10, decimal_places=0, default=0)
    is_paid = models.BooleanField(verbose_name=_('is_paid'), default=False)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'
        ordering = ['-updated']
    
    def __str__(self):
        return f'{self.order_id}'
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Create order_id field
        if not self.order_id:
            self.order_id = func.get_random_string(6)
        # Create slug field
        if not self.slug:
            self.slug = slugify(self.order_id)
    
    @property
    def price(self):
        """Get order price from the cart"""
        return self.cart.price
    
    @property
    def total_price(self):
        """Get total-price from the current cart"""
        return int(self.cart.total_price - self.discounts)
    
    @property
    def total_quantity(self):
        """Get quantity of the current order"""
        return self.cart.total_quantity
    
    @property
    def tickets(self):
        """Get all tickets for the current Cart"""
        return self.cart.tickets.all()
    
    @property
    def ticketsolds(self):
        """Get all ticketsolds for the current Cart"""
        return self.cart.ticketsold_cart.all()
