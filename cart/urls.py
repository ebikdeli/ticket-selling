from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    # ? To use in API calls
    path('add-product-cart', views.add_product_cart, name='add-product-cart'),
    path('change-product-cart', views.change_product_cart, name='change-product-cart'),
    path('delete-item-cart', views.delete_item_cart, name='delete-item-cart'),
    path('', views.cart_view, name='cart_view'),
]
