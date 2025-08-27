from rest_framework import serializers
from .models import Contents, Tags

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

