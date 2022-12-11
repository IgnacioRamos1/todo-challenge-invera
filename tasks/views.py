from rest_framework import generics, filters

from .serializers import TaskSerializer
from .models import Task
from .mixins import UpdateDestroyAPIView

from rest_framework.permissions import IsAuthenticated

class TaskSearchListCreateAPIView(
    generics.ListCreateAPIView,
        ):

    permission_classes = [IsAuthenticated]

    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'expiration_date', 'complete']

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()

task_search_list_create_view = TaskSearchListCreateAPIView.as_view()


class TaskUpdateDeleteAPIView(
    # StaffEditorPermissionMixin,
    UpdateDestroyAPIView,
    generics.GenericAPIView,
        ):

    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def perform_delete(self, instance):
        super().perform_delete(instance)

    def perform_patch(self, serializer):
        super().perform_patch(serializer)    

task_update_delete_view = TaskUpdateDeleteAPIView.as_view()
