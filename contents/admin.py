from django.contrib import admin
from contents.models import Contents, Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("id", "tag_name")
    search_fields = ("tag_name", "id")


@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title", "content", "tag_name__tag_name")
