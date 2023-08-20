from django.urls import path

from . import views


app_name = 'payment'

urlpatterns = [
    path('success/', views.payment_success, name='payment-success'),
    path('failed/', views.payment_failed, name='payment-failed'),
    path('pgi/<str:order_id>/', views.payment_request, name='payment-request'),
    path('zarrin/<str:order_id>/', views.zarrin_pal_request, name='zarrin-pal'),
    path('next-pay/<str:order_id>/', views.next_pay_request, name='next-pay'),
]
