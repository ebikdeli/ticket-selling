from django.urls import path

from . import views


app_name = 'payment'

urlpatterns = [
    path('zarrinpal/<str:order_id>/', views.zarrinpal_request, name='zarrinpal-request'),
    path('zarrinpal-result/<str:order_id>/<str:payment_id>/', views.zarrinpal_result_redirect, name='zarrinpal_result_redirect'),
    path('success/<str:order_id>/<str:payement_id>/', views.payment_success, name='payment-success'),
    path('failed/<str:order_id>/<str:message>/', views.payment_failed, name='payment-failed'),
]
