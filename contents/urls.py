from django.urls import path
from .views import ContentsAPIView, TagsAPIView, SeachAPIView, MonthAPIView

urlpatterns = [
    path('contents/', ContentsAPIView.as_view()),
    path('tags/', TagsAPIView.as_view()),
    path('contents/<tag>/', SeachAPIView.as_view()),
    path('contents/<year>/<month>/', MonthAPIView.as_view()),

]