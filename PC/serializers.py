import io

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import PC
from rest_framework import serializers


# My serializer
# class PCSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PC
#         fields = ('title', 'content', 'cat_id')


class PCSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_created = serializers.DateTimeField(read_only=True)
    time_updated = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()




# Model for test, just with 2 fields
# class PCModel():
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

# The serializer of model and of test
# class PCSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()

# A encode and decode functions that are showing how works a serializer
# def encode():
#     model = PCModel('Alex', 'Testing Serializer Model API')
#     model_sr = PCSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title": "Alex", "content": "Testing Serializer Model API"}')
#     data = JSONParser().parse(stream)
#     serializer = PCSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)