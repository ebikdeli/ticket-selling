from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    # ? To use in API calls
    path('add-ticket-cart', views.add_ticket_cart, name='add-ticket-cart'),
    path('change-ticket-cart', views.change_ticket_cart, name='change-ticket-cart'),
    path('delete-ticket-cart', views.delete_ticket_cart, name='delete-ticket-cart'),
    path('clean-cart', views.clean_cart, name='clean-cart'),
    path('', views.cart_view, name='cart-view'),
]
