from .models import PC
from rest_framework import serializers



class PCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = ('title', 'content', 'cat_id')