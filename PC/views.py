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
        list_of_objects = PC.objects.all().values()
        return Response({'title': 'All Objects', 'objects': list_of_objects,})

    def post(self, request):
        try:
            post_new = PC.objects.create(
                title = request.data['title'],
                content = request.data['content'],
                cat_id = request.data['cat_id'],
                )
            status_code = 201
            return Response({'post': model_to_dict(post_new), 'success': status_code, })
        except Exception as e:
            return ({'Exception': e})



# class PCAPIView(generics.ListAPIView):
#     queryset = PC.objects.all()
#     serializer_class = PCSerializer
