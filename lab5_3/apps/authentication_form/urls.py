from django.urls import path

from . import views

app_name = 'main_form'
urlpatterns = [
    path('', views.index, name='index'),
]
