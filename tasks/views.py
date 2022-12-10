from rest_framework import generics

from .serializers import TaskSerializer
from .models import Task
from .mixins import UpdateDestroyAPIView


class TaskListCreateAPIView(
    # StaffEditorPermissionMixin,
    generics.ListCreateAPIView,
        ):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

task_list_create_view = TaskListCreateAPIView.as_view()


class TaskUpdateDeleteAPIView(
    # StaffEditorPermissionMixin,
    UpdateDestroyAPIView,
    generics.GenericAPIView,
        ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def perform_delete(self, instance):
        super().perform_delete(instance)

    def perform_patch(self, serializer):
        super().perform_patch(serializer)    

task_update_delete_view = TaskUpdateDeleteAPIView.as_view()
