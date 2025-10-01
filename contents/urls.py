from django.urls import path
from .views import (
    ContentsAPIView,
    SeachAPIView,
    CMonthAPIView,
    StampAPIView,
    SMonthAPIView,
    TargetAPIView,
    TargetachieveAPIView,
    TagAPIView, ContentAPIView, TGAPIView,
)

urlpatterns = [
    path("contents/", ContentsAPIView.as_view()),
    path("tags/<str:tag_name>/", TagAPIView.as_view()),
    path("contents/<int:id>/", ContentAPIView.as_view()),
    path("contents/<str:tag_name>/", SeachAPIView.as_view()),
    path("contents/<int:year>/<int:month>/", CMonthAPIView.as_view()),
    path("stamps/", StampAPIView.as_view()),
    path("stamps/<int:year>/<int:month>/", SMonthAPIView.as_view()),
    path("targets/", TargetAPIView.as_view()),
    path("targets/achieve/<int:year>/<int:month>/", TargetachieveAPIView.as_view()),
    path("targets/<id>/", TGAPIView.as_view()),
    path('api/contents/<int:id>/', ContentsAPIView.as_view(), name='content-detail'),
]
