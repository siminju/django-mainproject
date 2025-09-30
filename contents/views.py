from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contents, Tags, Stamps, Targets, Tag
from .serializers import (
    PostSerializer,
    TagsSerializer,
    StampsSerializer,
    TargetSerializer,
    TargetachieveSerializer,
    ContentsSerializer,
    TagSerializer
)
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status




class ContentsAPIView(APIView):
    def get(self, request):
        posts = Contents.get_all_posts()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():  # 유훃하면
            contents = serializer.save()  # 저장
            result = PostSerializer(contents).data  # 번역

        latest_stamp = (
            Stamps.objects.latest().created_at.date()
        )  # 가장 최신 데이터를 불러오는 코드 (가장 최근 스템프조회)
        today = timezone.now().date()

        if today != latest_stamp:
            Stamps.create_stamp()
            stamps = len(Stamps.get_by_month(today.year, today.month))  # 갯수를 채크
            targets = Targets.get_all_targets()
            for target in targets:
                if target.value == stamps:
                    return Response(
                        {
                            "result": result,
                            "message": f"{target.name} 목표를 달성했습니다.",
                        }
                    )
        else:
            print("스템프 있음")

        return Response(result)  # 번역한것을 응답해준다.

class ContentAPIView(APIView):
    def get(self, request, id):
        post = Contents.objects.get(id=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, id):
        contents = contents.objects.get(id=id)
        contents_title = contents_title
        contents.delete()
        return Response({"message": f"{contents_title}를 삭제했습니다."})


    def put(self, request, id):
        contents = get_object_or_404(Contents, id=id)
        serializer = ContentsSerializer(contents, data=request.data, partial=True)  # partial=True: 일부 필드만 업데이트 가능

        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{serializer.data.get('content', '콘텐츠')}를 수정했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class TagsAPIView(APIView): 매니저님이랑 같이 했던 부분
#     def get(self, request):
#         tags = Tags.get_all_tags()
#         serializer = TagsSerializer(tags, many=True)
#         return Response(serializer.data)

class SeachAPIView(APIView):
    def get(self, request, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def post(self, request):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            tags = serializer.save()
            result = TagsSerializer(tags).data
        return Response(result)


class TagAPIView(APIView):
    def get(self, request, tag_name):
        tag = Tags.objects.get(id=id)
        serializer = TagsSerializer(tag)
        return Response(serializer.data)

    def delete(self, request, id):
        tag = Tags.objects.get(id=id)
        tag_name = tag.tag_name
        tag.delete()
        return Response({"message": f"{tag_name}을 삭제했습니다."})


class SeachAPIView(APIView):
    def get(self, request, tag_name):
        contents = Contents.objects.filter(tag_name=tag_name)
        # 태그로 콘텐츠를 조회
        serializer = ContentsSerializer(contents, many=True)
        return Response(serializer.data)


class CMonthAPIView(APIView):
    def get(self, request, year, month):
        data = cache.get(
            f"{year}{month}content"
        )  # redis조회 cache 데이터베이스, f-str 쓰는 이유는 숫자가 변하기 때문
        if data is not None:
            print("redis 사용")
            return Response(data)
        else:
            stamps = Stamps.get_by_month(year=int(year), month=int(month))
            serializer = StampsSerializer(stamps, many=True)
            cache.set(
                f"{year}{month}content", serializer.data, timeout=1800
            )  # key, value
            print("db 사용")
            return Response(serializer.data)


class StampAPIView(APIView):
    def get(self, request):
        data = Stamps.get_all()
        serializer = StampsSerializer(data, many=True)
        return Response(serializer.data)


class SMonthAPIView(APIView):
    def get(self, request, year, month):
        data = cache.get(f"{year}{month}stamp")  # redis조회 cache 데이터베이스
        if data is not None:
            print("redis 사용")
            return Response(data)
        else:
            stamps = Stamps.get_by_month(year=int(year), month=int(month))  # 조회
            serializer = StampsSerializer(stamps, many=True)
            cache.set(
                f"{year}{month}stamp", serializer.data, timeout=1800
            )  # key, value 저장
            print("db 사용")
            return Response(serializer.data)


class TargetAPIView(APIView):

    def post(self, request):
        try:
            r_value = request.data.get("value")
            value = int(r_value)

            if Targets.objects.filter(value=value).exists():
                return Response({"error": "존재하는 목표입니다."})

            serializer = TargetSerializer(data=request.data)
            if serializer.is_valid():
                target = serializer.save()
                result = TargetSerializer(target).data
                return Response(result)

            else:
                return Response(serializer.errors)

        except ValueError:
            return Response({"error": "목표값을 확인해주세요."})

class TGAPIView(APIView):

    def get(self, request, id):
        targets = Targets.objects.get(id=id) #목표를 아이디로 조회하고 목표들이란 변수에 담는다.
        serializer = TargetSerializer(targets) # 목표들이 담긴 변수를 번역기에 넣고 돌린다.
        return Response(serializer.data) #번역한 내용을 응답해준다.

    def put(self, request, id):
        targets = get_object_or_404(Targets, id=id) #목표를 id로 가져온다 그게 아니면 404에러를 보내준다 그것을 목표라는 변수에 담는다.
        serializer = TargetSerializer(targets, data=request.data, partial=True)  # partial=True: 일부 필드만 업데이트 가능

        if serializer.is_valid(): #유효성 검사를 하고 유효하면
            serializer.save() #저장을 한다.
            return Response({"message": f"{serializer.data.get('target', '목표')}를 수정했습니다."}, status=status.HTTP_200_OK) #수정했다는 메시지를 보낸다, 200ok를 보내준다.
        else: #그게 아니면
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #400 에러 코드를 보낸다.

    def delete(self, request, id): #번역기를 넣는 이유는 무엇을 지웠는지 알기 위해서였다.
        target = Targets.objects.get(id=id) #목표를 조회한다 아이디로 그걸 목표라는 변수에 담는다.
        target_name = target.name #목표 이름이란 변수에 목표의 이름을 담는다.
        target.delete() #목표를 삭제한다.
        return Response({"message": f"{target_name}을 삭제했습니다."}) #목표를 삭제했다는 메시지를 응답해준다.


class TargetachieveAPIView(APIView):
    def get(self, request, year, month):
        stamps = len(
            Stamps.get_by_month(year=int(year), month=int(month))
        )  # len으로 갯수채크
        targets = Targets.get_all_targets()  # 모든 targets를 targets라는 변수에 담는다.
        result = []
        for target in targets:
            achieve = {
                "target_name": target.name,
                "value": target.value,
                "is_achieved": True if target.value <= stamps else False,
            }  # True아니면 False를 achieve를 변수에 넣는다.
            result.append(achieve)
        serializer = TargetachieveSerializer({"stamp": stamps, "targets": result})
        return Response(serializer.data)


class TagsAPIView(APIView):
    def get(self, request, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)