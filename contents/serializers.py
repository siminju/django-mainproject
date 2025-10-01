from rest_framework import serializers
from .models import Contents, Tags, Targets, Stamps, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Targets
        fields = "__all__"


class StampsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamps
        fields = "__all__"


class TargetlistSerializer(serializers.Serializer):
    target_name = serializers.CharField(max_length=50)
    value = serializers.IntegerField()
    is_achieved = serializers.BooleanField()


class TargetachieveSerializer(serializers.Serializer):
    stamp = serializers.IntegerField()
    targets = TargetlistSerializer(many=True)


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"  # 필요한 필드만 넣으세요
