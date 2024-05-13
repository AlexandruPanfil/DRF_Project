from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PC
from .serializers import PCSerializer, EasyPCSerializer


# Create your views here.


def index(request):
    return HttpResponse('Hello, \nThis is a Django Rest Framework Project')

class ListPCAPIView(generics.ListAPIView):
    queryset = PC.objects.all()
    serializer_class = ListPCSerializer


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
