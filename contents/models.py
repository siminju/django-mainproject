from django.db import models

class Tags(models.Model):
    tag_name = models.CharField(max_length=5, unique=True)


class Contents(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    tag_name = models.ForeignKey(Tags, to_field='tag_name',on_delete=models.PROTECT)

