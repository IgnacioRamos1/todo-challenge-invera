from django.urls import path

from . import views

urlpatterns = [
    path('critical/', views.critical_log_view, name='critical_log_view'),
    path('error/', views.error_log_view, name='error_log_view'),
    path('warning/', views.warning_log_view, name='warning_log_view'),
    path('info/', views.info_log_view, name='info_log_view'),
    path('debug/', views.debug_log_view, name='debug_log_view'),
]
