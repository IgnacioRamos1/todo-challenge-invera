from rest_framework import generics
from rest_framework.response import Response

from .serializers import LogSerializer


class CriticalLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    queryset = []

    def get(self, request):
        with open('logs/critical.log', 'r') as f:
            return Response([line.rstrip('\n') for line in f])


critical_log_view = CriticalLogAPIView.as_view()


class ErrorLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    queryset = []

    def get(self, request):
        with open('logs/error.log', 'r') as f:
            return Response([line.rstrip('\n') for line in f])


error_log_view = ErrorLogAPIView.as_view()


class WarningLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    queryset = []

    def get(self, request):
        with open('logs/warning.log', 'r') as f:
            return Response([line.rstrip('\n') for line in f])


warning_log_view = WarningLogAPIView.as_view()


class InfoLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    queryset = []

    def get(self, request):
        with open('logs/info.log', 'r') as f:
            return Response([line.rstrip('\n') for line in f])


info_log_view = InfoLogAPIView.as_view()


class DebugLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    queryset = []

    def get(self, request):
        with open('logs/debug.log', 'r') as f:
            return Response([line.rstrip('\n') for line in f])


debug_log_view = DebugLogAPIView.as_view()
