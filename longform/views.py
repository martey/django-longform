from django.views.generic import (ArchiveIndexView, DateDetailView, DetailView,
                                  YearArchiveView)
from longform.models import Article


def _get_all_years():
    """
    Retrieve years from published articles.

    To save time (and SQL queries), we assume that we have written
    at least one article a year and grab the years from the first
    and last articles.

    """
    articles = Article.objects.published.order_by("-date_published")
    return range(articles[0].date_published.year,
                 articles[len(articles)-1].date_published.year-1, -1)


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

    def get_year(self, **kwargs):
        """Coerce year into integer for comparison purposes."""
        year = super(ArticleYearArchiveView, self).get_year(**kwargs)
        return int(year)
