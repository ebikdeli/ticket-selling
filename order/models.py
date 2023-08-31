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
    ticket = models.ManyToManyField('ticket.Ticket',
                                    verbose_name=_('ticket'),
                                    related_name='order_ticket',
                                    blank=True,
                                    null=True)
    authority = models.CharField(verbose_name=_('authority'), blank=True, max_length=50)
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
        """Calculate price of the current order"""
        price = 0
        if self.ticketsold_order.exists():
            for ticketsold in self.ticketsold_order.all():
                price += ticketsold.price
        return price
    
    @property
    def total_price(self):
        """Calculate total_price of the current order"""
        total_price = 0
        if self.ticketsold_order.exists():
            for ticketsold in self.ticketsold_order.all():
                total_price += ticketsold.total_price
        return total_price
    
    @property
    def total_quantity(self):
        """Calculate total_quantity in the current order"""
        total_quantity = 0
        if self.ticketsold_order.exists():
            for ticketsold in self.ticketsold_order.all():
                total_quantity += ticketsold.quantity
        return total_quantity
