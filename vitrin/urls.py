from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('992180', views.enamad_identifier, name='enamad-identifier'),
    path('', views.index, name='index'),
]
