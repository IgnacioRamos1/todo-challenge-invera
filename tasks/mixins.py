from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response


class UpdateDestroyAPIView(
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView                            
                                   ):

    def patch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            return Response(
                {'message': 'You are not the owner of this task.'},
                status=400
                )
        self.partial_update(request, *args, **kwargs)
        return Response(
            {'message': 'Task updated successfully.'},
            status=200
            )

    def delete(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            return Response(
                {'message': 'You are not the owner of this task.'},
                status=400
                )
        self.destroy(request, *args, **kwargs)
        return Response(
            {'message': 'Task deleted successfully.'},
            status=204
            )
