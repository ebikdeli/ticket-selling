from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from _resources.func import get_random_string


def ticket_image_path(instance, filename):
    return f'tickets/{instance.updated}/{filename}'


class Ticket(models.Model):
    """Model for Ticket"""
    name = models.CharField(verbose_name=_('name'), max_length=50)
    # 'ticket_number' filled by the admin after admin bought the real ticket from Trendyol
    ticket_number = models.CharField(verbose_name=_('ticket_number'), max_length=20, blank=True)
    price = models.DecimalField(verbose_name=_('price'), decimal_places=0, max_digits=10)
    discount =  models.DecimalField(verbose_name=_('discount'), decimal_places=0, max_digits=10, default=0)
    number_sold = models.PositiveIntegerField(verbose_name=_('number_sold'), default=0)
    is_acive = models.BooleanField(verbose_name=_('is_active'), default=True)
    image = models.ImageField(verbose_name=_('image'), upload_to=ticket_image_path, blank=True, null=True)
    lottery_date = models.DateTimeField(verbose_name=_('lottery date'))
    content = models.TextField(verbose_name=_('content'), blank=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Ticket'
        ordering = ['-updated',]
    
    def __str__(self) -> str:
        return f'{self.slug}'
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(f'{self.name}_{self.ticket_number}')
        return super().save(*args, **kwargs)


class TicketSold(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             related_name='ticketsold_user',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    ticket = models.ForeignKey('Ticket',
                               verbose_name=_('ticket'),
                               related_name='ticketsold_ticket',
                               on_delete=models.CASCADE
                               )
    cart = models.ForeignKey('cart.Cart',
                             verbose_name=_('cart'),
                             related_name='ticketsold_cart',
                             on_delete=models.CASCADE)
    ticket_code = models.CharField(verbose_name=_('ticket_code'), max_length=10, blank=True)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)
    is_paid = models.BooleanField(verbose_name=_('is_paid'), default=True)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    
    class Meta:
        verbose_name = 'TicketSold'
        verbose_name_plural = 'TicketSold'
        ordering = ['-updated',]
    
    def __str__(self) -> str:
        return super().__str__()
    
    def save(self, *args, **kwargs) -> None:
        if not self.ticket_code:
            self.ticket_code = get_random_string(10)
        if self.user:
            self.slug = slugify(f'{self.user.username}_{self.ticket.name}')
        else:
            self.slug = slugify(f'{self.ticket.name}')
        return super().save(*args, **kwargs)
    
    @property
    def price(self):
        return int(self.ticket.price * self.quantity)
    
    @property
    def total_price(self):
        return int(self.ticket.price - self.ticket.discount) * self.quantity
