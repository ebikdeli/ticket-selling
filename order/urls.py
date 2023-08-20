from django.urls import path

from . import views


app_name = 'order'

urlpatterns = [
    path('detail/<str:order_id>/', views.order_detail, name='order-detail'),
    path('my-tickets/', views.my_tickets, name='my-tickets'),
    path('', views.order, name='order'),
]
