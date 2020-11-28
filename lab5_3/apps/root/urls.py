from django.urls import path

from . import views

app_name = 'root'
urlpatterns = [
    path('', views.show_tables, name='show_tables'),
    path('table/', views.show_table, name='show_table'),
    path('table_backup/', views.show_table_old, name='show_table_old'),
    path('db_dumps/', views.show_dumps, name='show_dumps'),
    path('enter_table/', views.enter_table, name='enter_table'),
    path('back_num/', views.back_num, name='back_num'),
]
