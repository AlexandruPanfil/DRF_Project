from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/all/', PCAPIView.as_view()),
    path('api/v1/all/<int:pk>/', PCAPIView.as_view()),

]
