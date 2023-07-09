from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Ticket, TicketSold


@admin.register(Ticket)
class TicketAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


@admin.register(TicketSold)
class TicketSoldAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'ticket_code', 'quantity', 'price']
    list_display_links = ['user', 'ticket', 'ticket_code']
    list_editable = ['quantity']
    fields = ['user', 'ticket', 'ticket_code', 'quantity', 'price', 'total_price', 'slug', 'created', 'updated']
    readonly_fields = ['price', 'total_price', 'slug', 'created', 'updated']
    # fieldsets = [
    #     (None, {'fields': ['user', 'ticket', 'ticket_code', 'quantity']})
    #     ('price', {'fields': ['price', 'total_price']}),
    #     ('date and time', {'fields': ['created', 'updated']})
    # ]
