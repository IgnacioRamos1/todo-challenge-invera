from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register_user_view, name='register'),
    path('login/', views.login_user_view, name='login'),
]
