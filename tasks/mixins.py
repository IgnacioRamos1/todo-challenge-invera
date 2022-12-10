from rest_framework import mixins


class UpdateDestroyAPIView(
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                                   ):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
