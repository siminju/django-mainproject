from django.db import models
from datetime import datetime

class Tags(models.Model):
    tag_name = models.CharField(max_length=5, unique=True)

    @classmethod
    def get_all_tags(cls):
        return cls.objects.all().order_by('tag_name')

class Contents(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    tag_name = models.ForeignKey(to=Tags, on_delete=models.PROTECT)

    @classmethod
    def get_all_posts(cls):
        return cls.objects.all().order_by('created_at')

    @classmethod
    def get_by_tag(cls, tag_name):
        return cls.objects.filter(tag_name__tag_name=tag_name)

    @classmethod
    def get_by_month(cls, year: int, month: int):
        """
        연(year)과 월(month)을 기준으로 해당 월의 콘텐츠 조회
        예: Contents.get_by_month(2025, 9)
        """
        try:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            return cls.objects.filter(created_at__gte=start_date, created_at__lt=end_date)
        except ValueError:
            return cls.objects.none()

