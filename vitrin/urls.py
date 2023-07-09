from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('show-tickets/', views.show_tickets, name='show-tickets'),
    path('', views.index, name='index'),
]
