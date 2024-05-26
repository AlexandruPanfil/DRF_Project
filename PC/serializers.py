import io

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import PC
from rest_framework import serializers


# My serializer
# class Meta is a class that use a model in Serializer, you can select wich fields do you need or use __all__ to access all fields
class MetaPCSerializer(serializers.ModelSerializer):
    # This function will hide this field and will append there the current user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PC
        # fields = ('title', 'content', 'cat')
        fields = ('__all__')

class PCSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_created = serializers.DateTimeField(read_only=True)
    time_updated = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

    # This method will automatically save the data to db
    # It works with save() method of serializer in views.py
    def create(self, validated_data):
        return PC.objects.create(**validated_data)

    # This method will update the data to db, if instance have no update (in all fields I mean) it will save the old ones
    # It works with put() method of APIView in views.py
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.time_updated = validated_data.get('time_updated', instance.time_updated)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.cat_id = validated_data.get('cat_id', instance.cat_id)
        instance.save()
        return instance


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