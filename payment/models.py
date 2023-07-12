from django.db import models
from django.db.models import QuerySet
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from _resources.func import get_random_string
import uuid

class Payment(models.Model):
    """Everytime a payment is to be made, a model is created"""
    PGI_CHOICES = [
        ('zarrin', 'zarrin'),
        ('idpay', 'idpay'),
    ]
    payment_id = models.UUIDField(verbose_name=_('payment_id'), max_length=40, default=uuid.uuid4, editable=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            verbose_name=_('user'),
                            related_name='payment_user',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True)
    order = models.ForeignKey('order.Order',
                            verbose_name=_('order'),
                            related_name='payment_order',
                            on_delete=models.SET_NULL,
                            blank=True,
                            null=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0)
    describtion = models.TextField(verbose_name=_('describtion'), blank=True)
    pgi = models.CharField(verbose_name=_('gateway interface (pgi)'), choices=PGI_CHOICES, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'
    
    def __str__(self) -> str:
        return f'{self.payment_id}'
    
    @property
    def cart(self) -> object|None:
        """Get the cart for this payment"""
        if self.order:
            return self.order.cart
        return None
    
    @property
    def tickets(self) -> QuerySet|None:
        """Get tickets of the payment order"""
        if self.order:
            return self.order.tickets
        return None
    
    @property
    def ticketsolds(self) -> QuerySet|None:
        """Get ticketsolds of the payment order"""
        if self.order:
            return self.order.ticketsolds
        return None
