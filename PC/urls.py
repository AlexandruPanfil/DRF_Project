from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .routers import router
from .views import *


urlpatterns = [
    path('', index),
    path('api-auth/', include('rest_framework.urls')),

    # Basic API View
    path('api/v1/all/', PCAPIView.as_view()),  # http://127.0.0.1:8000/api/v1/all/
    path('api/v1/all/<int:pk>/', PCAPIView.as_view()),  # http://127.0.0.1:8000/api/v1/all/{pk}/

    # Updated API Views (List, Update, Retrieve...)
    path('api/v1/list', ListPCAPIView.as_view()),
    path('api/v1/update/<int:pk>/', UpdatePCAPIView.as_view()),
    path('api/v1/delete/<int:pk>/', DeletePCAPIView.as_view()),
    path('api/v1/detail/<int:pk>/', DetailedPCAPIView.as_view()),

    # Basic ViewSet
    # in .as_view() we are adding additional arguments, like what will do the ViewSet if we have different requests
    path('api/v1/viewset', ViewSetPCAPIView.as_view({'get': 'list', 'post': 'create'})),
    path('api/v1/viewset/<int:pk>/', ViewSetPCAPIView.as_view({'put': 'update'})),

    # Router urls
    path('api/v1/', include(router.urls)),  # http://127.0.0.1:8000/api/v1/{router}

    # Djoser Auth
    path('api/v1/auth/djoser/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # Simple JWT
    # This API are making JWT Tokens, one is creating, second is refreshing and last one verify
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
