from cms.sitemaps import CMSSitemap
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage

from djangocms_blog.sitemaps import BlogSitemap
from djcms.views import HomePage

admin.autodiscover()

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path("post_sitemap.xml", sitemap, {"sitemaps": {"postsitemap": BlogSitemap}}),
    
    # path('sitemap.xml', 'django.contrib.sitemaps.views.sitemap', {
    #     'sitemaps': {'cmspages': CMSSitemap, 'blog': BlogSitemap, }
    # }),
    
    path(
        "favicon.ico/",
        RedirectView.as_view(url=staticfiles_storage.url("djcms/favicons/favicon.ico")),
    ),
]


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path("cms/", include("cms.urls")),
    path("", HomePage.as_view()),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
