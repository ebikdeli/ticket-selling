from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Cart
from ticket.models import TicketSold


class TicketSoldInlines(admin.TabularInline):
    """Show cart ticketsolds as inline models"""
    model = TicketSold
    # This is how we change number of inlines in the parent model
    # https://stackoverflow.com/questions/47864742/remove-add-another-from-django-admin
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin panel has changed"""
    list_display = ['user', 'total_price', 'total_quantity', 'is_paid', 'is_active', 'updated']
    fields = ['user','session_key', ('price', 'total_price', 'total_quantity'), ('is_paid', 'is_active'), 'slug', ('created', 'updated'), 'ticket']
    # readonly_fields = ['session_key', 'created', 'updated', 'tickets', 'price', 'total_price', 'total_quantity']
    readonly_fields = ['session_key', 'created', 'updated', 'price', 'total_price', 'total_quantity']
    inlines = [TicketSoldInlines]
    
    # @admin.display(boolean=False, description='tickets')
    # def tickets(self, obj):
    #     """This field used to show all cart_items belong to this cart"""
    #     tickets = list()
    #     for ticket in obj.ticketsold_cart.all():
    #         tickets.append(ticket.product.name)
    #     if not tickets:
    #         return 'No tickets in the cart'
    #     print(tickets)
    #     return tickets
