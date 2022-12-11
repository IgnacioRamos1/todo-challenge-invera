from rest_framework import generics, filters

from .serializers import TaskSerializer
from .models import Task
from .mixins import UpdateDestroyAPIView

from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger('main')

class TaskSearchListCreateAPIView(
    generics.ListCreateAPIView,
        ):

    permission_classes = [IsAuthenticated]

    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'expiration_date', 'complete']

    def get_queryset(self):
        queryset = Task.objects.all()

        logger.info(f'User {self.request.user.username} got tasks successfully.')
        return queryset

    def perform_create(self, serializer):
        logger.info(f'User {self.request.user.username} created task successfully.')
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
        logger.info(f'User {self.request.user.username} deleted task successfully.')
        super().perform_delete(instance)

    def perform_patch(self, serializer):
        logger.info(f'User {self.request.user.username} updated task successfully.')
        super().perform_patch(serializer)    

task_update_delete_view = TaskUpdateDeleteAPIView.as_view()
