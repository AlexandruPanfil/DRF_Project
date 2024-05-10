from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics

from .models import PC
from .serializers import PCSerializer


# Create your views here.


def index(request):
    return HttpResponse('Hello')


class PCAPIView(generics.ListAPIView):
    queryset = PC.objects.all()
    serializer_class = PCSerializer
