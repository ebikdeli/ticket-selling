from django.urls import path

from . import views


app_name = 'order'

urlpatterns = [
    path('order-form/', views.order_form, name='order-form'),
    path('checkout/', views.checkout, name='checkout'),
    path('detail/<str:order_id>/', views.order_detail, name='order-detail'),
    path('my-tickets/', views.my_tickets, name='my-tickets'),
]
