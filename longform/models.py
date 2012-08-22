from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from markdown import markdown
from taggit.managers import TaggableManager


class ArticleManager(models.Manager):
    def _get_published(self):
        return self.get_query_set().filter(published_status=True,
                                           date_published__lte=timezone.now())

    def _get_drafts(self):
        return self.get_query_set().filter(published_status=False)

    drafts = property(_get_drafts)
    published = property(_get_published)

    # The following methods only get published posts.

    def pub_by_year(self, year):
        return self.get_query_set().filter(date_published__year=year,
                                           date_published__lte=timezone.now(),
                                           published_status=True)

    def pub_by_month(self, year, month):
        return self.get_query_set().filter(date_published__year=year,
                                           date_published__month=month,
                                           date_published__lte=timezone.now(),
                                           published_status=True)

    def pub_by_day(self, year, month, day):
        return self.get_query_set().filter(date_published__year=year,
                                           date_published__month=month,
                                           date_published__day=day,
                                           date_published__lte=timezone.now(),
                                           published_status=True)


class Article(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User)
    excerpt = models.TextField(blank=True, null=True,
                               help_text="Optional excerpt.")
    excerpt_html = models.TextField(blank=True, editable=False)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True, editable=False)

    slug = models.SlugField(max_length=200, unique_for_date="date_published")
    guid = models.CharField(editable=False, max_length=250)

    published_status = models.BooleanField(default=False)

    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=timezone.now)

    objects = ArticleManager()
    tags = TaggableManager()

    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        if self.is_published():
            # Convert to local server time. See 
            # <http://ur1.ca/9z40w> and <http://ur1.ca/9z40r>
            local_date_published = timezone.localtime(self.date_published)
            return ("longform-article-detail", (), {
                "year": local_date_published.strftime("%Y"),
                "month": local_date_published.strftime("%m"),
                "day": local_date_published.strftime("%d"),
                "slug": self.slug,
            })
        else:
            return ("longform-article-preview", (), {"id": self.id})

    def is_published(self):
        """Returns True is article is publicly available."""
        return self.published_status and self.date_published <= timezone.now()

    def save(self):
        # Create GUID if one does not already exist and post is published.
        # See <http://ur1.ca/9xxnw>.
        if self.published_status:
            if not self.guid:
                current_site = Site.objects.get_current()
                self.guid = "tag:%s,%s:%s" % (
                    current_site.domain,
                    self.date_published.strftime("%Y-%m-%d"),
                    self.get_absolute_url())
        # markdown to HTML conversion (w/ footnotes)
        self.content_html = markdown(self.content, ["footnotes"])
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt, ["footnotes"])

        super(Article, self).save()
