from django.db import models
from django.db.models import Sum
from django.http.request import HttpRequest
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .cart_functions import reset_session, set_session_cart, get_cart_with_id,\
                            get_cart_and_cart_item_id
from ticket.models import TicketSold


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
    
    def sync_session_cart_after_authentication(self, request: HttpRequest, *args, **kwargs):
        """Synchronize Cart and cart session after user authenticated."""
        cart = self
        # Fetch all CartItem of the current Cart
        cartItems = cart.cart_item_cart.all()
        # 1) If cart session is not empty, put its items in the Cart
        try:
            if request.session['cart']:
                # 1- If there are CartItems for current Cart (or Cart is not empty)
                if cartItems:
                    # First we need to list all current CartItems 'product.product_id' field to know what 'product_id's are
                    # already in the 'cart' session to prevent duplication.
                    productId = list()
                    for cI in cartItems:
                        productId.append(str(cI.product.product_id))
                    
                    # Check If the item in the 'cart' session is same as any item in the CartItem
                    for cI in cartItems:
                        for item in request.session['cart']:
                            # Add every item['product_id'] to a list to be used in '1.3' step
                            current_cart_product_id = list()
                            current_cart_product_id.append(item['product_id'])
                            # 1.1- If the session item is already in the CartItem, just add quantity to the current CartItem
                            if cI.product.product_id == item['product_id']:
                                cI.quantity += int(item['quantity'])
                                print(f"{item['product_id']} is already in the cart and updated")
                                cI.save()
                                item['quantity'] = cI.quantity
                            # 1.2- If the session item is not in the CartItem, add new CartItem to the Cart
                            elif item['product_id'] not in productId:
                                cart.cart_item_cart.create(
                                    product=Product.objects.get(product_id=item['product_id']),
                                    quantity=int(item['quantity'])
                                )
                                # Append current 'product_id' to 'productId' list to prevent duplication
                                productId.append(item['product_id'])
                                print(f"{item['product_id']} was not in the cart but added")
                        # 1.3- If the current CartItem is not in the 'cart' session, add it to the session
                        if str(cI.product.product_id) not in current_cart_product_id:
                            # Later we can add ColorPrice functionality to this section
                            request.session['cart'].append({'product_id': cI.product.product_id, 'quantity': int(cI.quantity)})
                # 2- If current Cart is empty (or there is no CartItem) just put all items from cart sesison in the Cart
                else:
                    for item in request.session['cart']:
                        cart.cartitem_cart.create(
                            product=Product.objects.get(product_id=item['product_id']),
                            quantity = int(item['quantity'])
                        )
            # 2) If cart session is empty, check if there is any item in Cart to put them into the empty session
            else:
                if cartItems:
                    for cI in cartItems:
                        request.session['cart'].append({'product_id': cI.product.product_id, 'quantity': int(cI.quantity)})
                # If both the Cart and cart session are empty, just return None
                else:
                    return None
            # Update 'total_quantity' 'price' and 'price_end' session that automatically updated in the current Cart
            set_session_cart(request, cart)
            return True
        except KeyError:
            print('No cart_id found in session so no synchnorization happened')
            return False
