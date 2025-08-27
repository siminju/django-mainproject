from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contents, Tags
from .serializers import PostSerializer, TagsSerializer


class ContentsAPIView(APIView):
    def get(self, request):
        posts = Contents.get_all_posts()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            contents=serializer.save()
            result = PostSerializer(contents).data
        return Response(result)

class TagsAPIView(APIView):
    def get(self, request):
        tags = Tags.get_all_tags()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            tags=serializer.save()
            result = TagsSerializer(tags).data
        return Response(result)

class SeachAPIView(APIView):
    def get(self, request, tag):
        posts = Contents.get_by_tag(tag_name=tag)
        #태그로 콘텐츠를 조회
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class MonthAPIView(APIView):
    def get(self, request, year, month):
        posts = Contents.get_by_month(year=int(year), month=int(month))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)