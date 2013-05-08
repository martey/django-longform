from django.views.generic import (ArchiveIndexView, DateDetailView, DetailView,
                                  YearArchiveView)
from django.views.generic.list import ListView
from longform.models import Article
from taggit.models import Tag


def _get_all_years():
    """
    Retrieve years from published articles.

    To save time (and SQL queries), we assume that we have written
    at least one article a year and grab the years from the first
    and last articles.

    """
    articles = Article.objects.published.order_by("-date_published")
    return range(articles[0].date_published.year,
                 articles[len(articles) - 1].date_published.year - 1, -1)


class ArticleArchiveIndexView(ArchiveIndexView):
    allow_empty = True
    date_field = "date_published"

    def get_context_data(self, **kwargs):
        context = super(ArticleArchiveIndexView,
                        self).get_context_data(**kwargs)
        context["years"] = _get_all_years()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.published


class ArticleDateDetailView(DateDetailView):
    context_object_name = "article"
    date_field = "date_published"
    model = Article
    month_format = "%m"


class ArticleTagView(ListView):

    def get_context_data(self, **kwargs):
        context = super(ArticleTagView, self).get_context_data(**kwargs)

        context["tag"] = Tag.objects.get(slug=self.kwargs["slug"])
        return context

    def get_queryset(self):
        return Article.objects.published.filter(tags__slug=self.kwargs["slug"])


class ArticlePreviewView(DetailView):
    context_object_name = "article"
    model = Article


class ArticleYearArchiveView(YearArchiveView):
    date_field = "date_published"
    make_object_list = True

    def get_context_data(self, **kwargs):
        context = super(ArticleYearArchiveView,
                        self).get_context_data(**kwargs)

        context["years"] = _get_all_years()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.pub_by_year(self.get_year())
