from django.conf.urls import patterns, url, include
from longform.views import (ArticleArchiveIndexView, ArticleDateDetailView,
                            ArticlePreviewView, ArticleYearArchiveView)

urlpatterns = patterns(
    "longform.views",
    url(r"^(?P<year>\d{4})/$",
        ArticleYearArchiveView.as_view(),
        name="longform-year-archive"),
    url(r"^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$",
        ArticleDateDetailView.as_view(),
        name="longform-article-detail"),
    url(r"^preview/(?P<pk>\d+)/$",
        ArticlePreviewView.as_view(),
        name="longform-article-preview"),
    url(r"^$",
        ArticleArchiveIndexView.as_view(),
        name="longform-index"),
)
