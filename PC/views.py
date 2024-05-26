from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from .models import PC, Category
from .paginations import SmallSetPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import PCSerializer, MetaPCSerializer


# Create your views here.


def index(request):
    return HttpResponse('Hello, \nThis is a Django Rest Framework Project')

# In case that we will have DRY code we will use ViewSet, it's already a done class with all functionality
# Like this one, ModelViewSet, it has all the functionality for the model
class ViewSetPCAPIView(viewsets.ModelViewSet):
    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer

    # @action is from Router, it gets methods of request what will be used (in our case it's 'get' )
    # http://127.0.0.1:8000/api/v1/router/categories/
    @action(methods=['get', ], detail=False)
    def categories(self, request):
        cats = Category.objects.all()
        return Response({'Names': [c.name for c in cats]})
        # If you want all objetcs do not forget to use .values() after you select all onjects in that model
        # cats = Category.objects.all().values()
        # return Response({'Category': cats}, )

    # detail is for more details, like in this case
    # http://127.0.0.1:8000/api/v1/router/{pk}/detailed/
    @action(methods=['get'], detail=True)
    def detailed(self, reqeust, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'Category': cats.name})


# This is a more advanced ViewSet, here you can use default mixins of Rest_Framework
# and choose wich one you want to use
class ViewSetUpdatePCAPIView(mixins.CreateModelMixin,    # For Create an object in db
                             mixins.RetrieveModelMixin,  # For Read-only an object from db
                             mixins.UpdateModelMixin,    # For Update the object in db
                             mixins.DestroyModelMixin,   # For Delete the object in db
                             mixins.ListModelMixin,      # For View all the objects in db
                             GenericViewSet):            # Generic ViewSet :)

    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer


# ListAPIView is working only with get request
# ListCreateAPIView have the same performance as ListAPIView and
# can create one more instance (working with get and post requests)
class ListPCAPIView(generics.ListAPIView):
    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = SmallSetPagination

# UpdateAPIView is working with put and patch requests
class UpdatePCAPIView(generics.RetrieveUpdateAPIView):
    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    authentication_classes = (TokenAuthentication, )


# DestroyAPIView is working with delete request
class DeletePCAPIView(generics.RetrieveDestroyAPIView):
    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer
    permission_classes = (IsAdminOrReadOnly,)


# RetrieveUpdateDestroyAPIView is a multi-functional API with get, put and delete requests
# (better to check it in browser, there is a better look with all requests)
class DetailedPCAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PC.objects.all()
    serializer_class = MetaPCSerializer


# APIView is a general API, this is the base of all others, you can manage as you want,
# But you should declare all the methods and logic in this instance
class PCAPIView(APIView):
    def get(self, request):
        # list_of_objects = PC.objects.all().values()
        # return Response({'title': 'All Objects', 'objects': list_of_objects,})
        list_of_objects = PC.objects.all()
        return Response({'posts': PCSerializer(list_of_objects, many=True).data})


    def post(self, request):
        try:
            serializer = PCSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            status_code = 201
            return Response({'post': serializer.data, 'success': status_code, })
        except Exception as e:
            return ({'Exception': e})

    def put(self, request, *args, **kwargs):
        # Here we are getting the id of object
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'error': 'The Put Method Not Allowed'})

        try:
            # Here we are taking all data from the selected object
            instance = PC.objects.get(pk=pk)

        except:
            # It will raise exception if the key doesn't exist, Ex: if you want to create new object it will raise exception
            return Response({'error': "The selected object doesn't exist"})

        # Here it is forwarding to update method of serializer and saving the new data
        serializer = PCSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({'error': 'The Delete Method Not Allowed '})

        try:
            instance = PC.objects.get(pk=pk)
        except:
            return Response({'error': "The selected object doesn't exist"})

        instance.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'deleted_post': str(pk)})

# class PCAPIView(generics.ListAPIView):
#     queryset = PC.objects.all()
#     serializer_class = PCSerializer
