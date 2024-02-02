from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register_page, name='register'),

    path('', task_list, name='tasks'),
    path('task/<int:pk>/', task_detail, name='task'),
    path('task-create/', task_create, name='task-create'),
    path('task-update/<int:pk>/', task_update, name='task-update'),
    path('task-delete/<int:pk>/', task_delete, name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]


