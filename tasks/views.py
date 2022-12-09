from rest_framework import generics

from .serializers import TaskSerializer
from .models import Task


class TaskDetailAPIView(
    # StaffEditorPermissionMixin,
    generics.ListAPIView,
    generics.CreateAPIView,
        ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

task_list_view = TaskDetailAPIView.as_view()
