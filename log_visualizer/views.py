from rest_framework import generics
from rest_framework.response import Response
from .serializers import LogSerializer


class CriticalLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer

    def get(self, request, *args, **kwargs):
        with open('logs/critical.log', 'r') as f:
            return Response(f.read())

critical_log_view = CriticalLogAPIView.as_view()

class ErrorLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer

    def get(self, request, *args, **kwargs):
        with open('logs/error.log', 'r') as f:
            return Response(f.read())

error_log_view = ErrorLogAPIView.as_view()

class WarningLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer

    def get(self, request, *args, **kwargs):
        with open('logs/warning.log', 'r') as f:
            return Response(f.read())

warning_log_view = WarningLogAPIView.as_view()

class InfoLogAPIView(generics.ListAPIView):
    
    serializer_class = LogSerializer

    def get(self, request, *args, **kwargs):
        with open('logs/info.log', 'r') as f:
            return Response(f.read())

info_log_view = InfoLogAPIView.as_view()

class DebugLogAPIView(generics.ListAPIView):

    serializer_class = LogSerializer
    
    def get(self, request, *args, **kwargs):
        with open('logs/debug.log', 'r') as f:
            return Response(f.read())

debug_log_view = DebugLogAPIView.as_view()
