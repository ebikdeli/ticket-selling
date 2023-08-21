from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Ticket, TicketSold


@admin.register(Ticket)
class TicketAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['name', 'ticket_number', 'price', 'is_active', 'is_ended', 'lottery_date']
    fields = ['name', 'ticket_number', 'price', 'prize_value', 'number_sold', 'is_active', 'is_ended', 'image', 'lottery_date', 'content', 'slug']


@admin.register(TicketSold)
class TicketSoldAdmin(admin.ModelAdmin):
    list_display = ['ticket_code', 'user', 'ticket', 'quantity', 'price', 'status']
    list_display_links = ['ticket', 'ticket_code']
    list_editable = ['quantity']
    fields = ['user', 'ticket', 'ticket_code', 'quantity', 'price', 'total_price', 'is_paid', 'is_active', 'slug', 'created', 'updated']
    readonly_fields = ['price', 'total_price', 'slug', 'created', 'updated']
    # fieldsets = [
    #     (None, {'fields': ['user', 'ticket', 'ticket_code', 'quantity']})
    #     ('price', {'fields': ['price', 'total_price']}),
    #     ('date and time', {'fields': ['created', 'updated']})
    # ]
