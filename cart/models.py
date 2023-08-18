from django.db import models
from django.db.models import Sum
from django.http.request import HttpRequest
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .cart_functions import reset_session, set_session_cart, get_cart_with_id,\
                            get_cart_and_cart_item_id
from ticket.models import Ticket, TicketSold


class Cart(models.Model):
    """Any user (even unauthenticated ones) has a cart that works with 'cart' session."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE,
                             related_name='cart_user',
                             blank=True,
                             null=True)
    session_key = models.CharField(verbose_name=_('session key'), blank=True, max_length=30)
    ticket = models.ManyToManyField('ticket.Ticket',
                                     verbose_name=_('ticket'),
                                     related_name='cart_tickets')
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    def __str__(self) -> str:
        if self.user:
            return f'{self.user.username}_Cart({self.id})'
        return f'Cart({self.id})'
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug and self.user:
            self.slug = slugify(f'{self.user.username}_cart')
        elif not self.slug and not self.user:
            self.slug = f'cart({self.id})'
        return super().save(*args, **kwargs)
    
    @property
    def price(self):
        """Calculate price of the current cart"""
        price = 0
        if self.ticketsold_cart.exists():
            for ticketsold in self.ticketsold_cart.all():
                price += ticketsold.price
        return price
    
    @property
    def total_price(self):
        """Calculate total_price of the current cart"""
        total_price = 0
        if self.ticketsold_cart.exists():
            for ticketsold in self.ticketsold_cart.all():
                total_price += ticketsold.total_price
        return total_price
    
    @property
    def total_quantity(self):
        """Calculate total_quantity in the current cart"""
        total_quantity = 0
        if self.ticketsold_cart.exists():
            for ticketsold in self.ticketsold_cart.all():
                total_quantity += ticketsold.quantity
        return total_quantity
    
    def append_ticket(self, request: HttpRequest, quantity: (str or int), ticket:object, *args, **kwargs) -> bool:
        """Append new ticket to the current cart by creating new TicketSold if not exists"""
        cart = self
        ticketsold_qs = TicketSold.objects.filter(cart=cart, ticket=ticket)
        # If ticket is already in the user cart
        if ticketsold_qs.exists():
            print(f'{ticket.name} already exists in the cart just update it')
            ticketsold = ticketsold_qs.get()
            ticketsold.quantity += int(quantity)
            ticketsold.save()
            # Update 'cart' session with new quantity
            for ticketsold_session in request.session['cart']:
                if ticketsold_session['ticketsold_id'] == ticketsold.id:
                    ticketsold_session['quantity'] += int(quantity)
        # If the icketsold is not in the cart before
        else:
            ticketsold = cart.ticketsold_cart.create(ticket=ticket)
            if request.user.is_authenticated:
                ticketsold.user = request.user
                ticketsold.save()
            print('New ticketsold created')
            # Update 'cart' session with new quantity
            new_ticket_data = {'ticketsold_id': str(ticketsold.id),
                               'ticket_id': ticket.id,
                               'quantity': int(quantity)}
            request.session['cart'].append(new_ticket_data)
        # If the ticket is not in the cart append it to the cart else igonre following block
        if not ticket in self.ticket.all():
            print('add ticket to the cart')
            self.ticket.add(ticket)
        else:
            print('ticket already is in the cart')
        # Update session with updated Cart
        set_session_cart(request, cart)
        return True

    def change_ticket_quantity(self,request: HttpRequest, quantity: (str or int), ticketsold: object, *args, **kwargs) -> bool:
        """Change the quantity of an ticketsold"""
        # Subtract number of added item from product stock
        ticketsold.quantity = int(quantity)
        ticketsold.save()
        # Update 'cart' session with new quantity
        for ticketsold_session in request.session['cart']:
            if ticketsold_session['ticketsold_id'] == ticketsold.id:
                ticketsold_session['quantity'] = int(quantity)
        # Update session with updated Cart
        set_session_cart(request, ticketsold.cart)
        return True

    def delete_item(self, request:HttpRequest, ticketsold:object , *args, **kwargs) -> bool:
        """Delete an ticket from the cart. If properly executed returns True else False"""
        # Remove ticket from cart
        ticket = ticketsold.ticket
        self.ticket.remove(ticket)
        ticketsold.delete()
        # Delete current ticket from 'cart' session
        for ticketsold_session in request.session['cart']:
            if ticketsold_session['ticketsold_id'] == ticketsold.id:
                request.session['cart'].remove(ticketsold_session)
        # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
        set_session_cart(request, ticketsold.cart)
        return True
    
    def clean(self, request):
        """Clean current Cart totally"""
        if self.ticketsold_cart.exists():
            for ticketsold in self.ticketsold_cart.all():
                # Remove related ticket from cart.ticket field
                self.ticket.remove(ticketsold.ticket)
                ticketsold.delete()
            self.save()
        reset_session(request)
        return True
    
    def sync_session_cart_after_authentication(self, request: HttpRequest, *args, **kwargs):
        """Synchronize Cart and cart session after user authenticated."""
        cart = self
        # Fetch all CartItem of the current Cart
        ticketsolds_qs = cart.ticketsold_cart.all()
        # 1) If cart session is not empty, put its items in the Cart
        try:
            if request.session['cart']:
                # 1- If there are TicketSolds for current Cart (or Cart is not empty)
                if ticketsolds_qs.exists():
                    # First we need to list all current TicketSold to know what 'ticket_id' are
                    # already in the 'cart' session to prevent duplication.
                    ticket_id_list = list()
                    for ticketsold in ticketsolds_qs:
                        ticket_id_list.append(str(ticketsold.ticket.id))
                    
                    # Check If the ticket in the 'cart' session is same as any ticket in the TicketSold
                    for ticketsold in ticketsolds_qs:
                        for ticketsold_session in request.session['cart']:
                            # Add every ticketsold_session['ticket_id'] to a list to be used in '1.3' step
                            current_cart_ticket_id = list()
                            current_cart_ticket_id.append(ticketsold_session['ticket_id'])
                            # 1.1- If the session ticketsold_session is already in the TicketSold, just add quantity to the current TicketSold
                            if ticketsold.ticket.id == ticketsold_session['ticket_id']:
                                ticketsold.quantity += int(ticketsold_session['quantity'])
                                print(f"{ticketsold_session['ticket_id']} is already in the cart and updated")
                                ticketsold.save()
                                ticketsold_session['quantity'] = ticketsold.quantity
                            # 1.2- If the session ticketsold is not in the TicketSold, add new TicketSold to the Cart
                            elif ticketsold_session['ticket_id'] not in ticket_id_list:
                                cart.ticketsold_cart.create(
                                    user=request.user,
                                    ticket=Ticket.objects.get(id=ticketsold_session['ticket_id']),
                                    quantity=int(ticketsold_session['quantity'])
                                )
                                # Append current 'ticket_id' to 'ticket_id_list' list to prevent duplication
                                ticket_id_list.append(ticketsold_session['ticket_id'])
                                print(f"{ticketsold_session['ticket_id']} was not in the cart but added")
                        # 1.3- If the current TicketSold is not in the 'cart' session, add it to the session
                        if str(ticketsold.ticket.id) not in current_cart_ticket_id:
                            request.session['cart'].append({
                                'ticket_id': ticketsold.ticket.id,
                                'ticketsold_id': ticketsold.id,
                                'quantity': int(ticketsold.quantity)})
                # 2- If current Cart is empty (or there is no CartItem) just put all tickets from cart sesison in the Cart
                else:
                    for ticketsold_session in request.session['cart']:
                        cart.ticketsold_cart.create(
                            user=request.user,
                            ticket=Ticket.objects.get(id=ticketsold_session['ticket_id']),
                            quantity = int(['quantity'])
                        )
            # 2) If cart session is empty, check if there is any ticket in current Cart to put them into the empty session
            else:
                if ticketsolds_qs.exists():
                    for ticketsold in ticketsolds_qs:
                        request.session['cart'].append({
                            'ticket_id': ticketsold.ticket.id,
                            'ticketsold_id': ticketsold.id,
                            'quantity': int(ticketsold.quantity)
                            })
                # If both the Cart and cart session are empty, just return None
                else:
                    return None
            # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
            set_session_cart(request, cart)
            return True
        except KeyError:
            print('No cart_id found in session so no synchnorization happened')
            return False
