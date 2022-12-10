from django.urls import path
from . import views


urlpatterns = [
    path('', views.task_search_list_create_view, name='task-list, task-create'),
    path('<int:id>/', views.task_update_delete_view, name='task-delete'),
]
