from django.urls import path
from rango import views

app_name = 'mango'

urlpatterns = [
    path('', views.index, name='index'),
]
