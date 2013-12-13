from django.contrib import admin
from longform.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_status",
                    "date_modified", "date_published",)
    list_filter = ("published_status", "date_published",
                   "date_modified", "author",)
    ordering = ("-date_published", "published_status",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content",)

admin.site.register(Article, ArticleAdmin)
