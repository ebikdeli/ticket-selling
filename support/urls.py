from django.urls import path
from . import views


app_name = 'support'

urlpatterns = [
    path('about-contact-us/', views.about_contact_us, name='about-contact-us'),
    path('rule/', views.rule, name='rule'),
    path('faq/', views.faq, name='faq'),
    path('user-message-form', views.user_message_form, name='user-message-form'),
]
