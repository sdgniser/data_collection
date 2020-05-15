from django.urls import path
from . import views

urlpatterns = [
    path('', views.Upload, name='upload'),
    path('validate_app_no/', views.ValidateAppNo, name='validate_app_no'),
]
