from rest_framework import generics

from .serializers import TaskSerializer
from .models import Task


class TaskAPIView(
    # StaffEditorPermissionMixin,
    generics.ListCreateAPIView,
        ):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

task_list_view = TaskAPIView.as_view()
