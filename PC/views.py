from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PC
from .serializers import PCSerializer


# Create your views here.


def index(request):
    return HttpResponse('Hello')


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

            post_new = PC.objects.create(
                title=request.data['title'],
                content=request.data['content'],
                cat_id=request.data['cat_id'],
                )
            status_code = 201
            return Response({'post': PCSerializer(post_new).data, 'success': status_code, })
        except Exception as e:
            return ({'Exception': e})



# class PCAPIView(generics.ListAPIView):
#     queryset = PC.objects.all()
#     serializer_class = PCSerializer
