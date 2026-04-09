from django.urls import path
from . import views

app_name = 'algorithms'

urlpatterns = [
    path('', views.index, name='index'),
    path('bubble_sort/', views.bubble_sort, name='bubble_sort'),
    path('quick_sort/', views.quick_sort, name='quick_sort'),
    path('insertion_sort/', views.insertion_sort, name='insertion_sort'),
    path('merge_sort/', views.merge_sort, name='merge_sort'),
    path('bfs/', views.bfs, name='bfs'),
    path('dfs/', views.dfs, name='dfs'),
    path('heap_sort/', views.heap_sort, name='heap_sort'),
]