from rest_framework import generics

from .serializers import TaskSerializer
from .models import Task


class TaskDetailAPIView(
    # StaffEditorPermissionMixin,
    generics.ListAPIView,
        ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

task_list_view = TaskDetailAPIView.as_view()


class TaskCreateAPIView(
    # StaffEditorPermissionMixin,
    generics.CreateAPIView,
        ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save()

task_create_view = TaskCreateAPIView.as_view()
