from django.urls import path, include
from rest_framework import routers

from .views import *


# Do not do my mistake, write () in the end of ...Router()
# If we define this router we will use ViewSet at maximum, in a single page
# you will have all http requests (get, post, put, delete)
router = routers.SimpleRouter()
# Here we need to define the r'{route}' and our ViewSet,
# if you do not use queryset in ViewSet, then you will have to define basename (the name of model)
router.register(prefix=r"router/viewset", viewset=ViewSetPCAPIView)

urlpatterns = [
    path('', index),
    path('api-auth/', include('rest_framework.urls')),

    # Basic API View
    path('api/v1/all/', PCAPIView.as_view()),
    path('api/v1/all/<int:pk>/', PCAPIView.as_view()),

    # Updated API Views (List, Update, Retrieve...)
    path('api/v1/list', ListPCAPIView.as_view()),
    path('api/v1/update/<int:pk>', UpdatePCAPIView.as_view()),
    path('api/v1/detail/<int:pk>', DetailedPCAPIView.as_view()),

    # Basic ViewSet
    # in .as_view() we are adding additional arguments, like what will do the ViewSet if we have different requests
    path('api/v1/viewset', ViewSetPCAPIView.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/viewset/<int:pk>', ViewSetPCAPIView.as_view({'put': 'update'})),

    # Router urls
    path('api/v1/', include(router.urls)), # http://127.0.0.1/api/v1/{router}

]
