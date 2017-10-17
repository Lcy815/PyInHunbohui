# coding = utf-8

from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesViews.as_view(), name='archives'),
    # url(r'^category/(?P<name>.+)/$', views.category, name='category'),
    url(r'^category/(?P<name>.+)/$', views.CategoryViews.as_view(), name='category'),
    url(r'^index$', views.IndexViews.as_view(), name='index'),
    url(r'^tag/(?P<name>.+)/$', views.TagViews.as_view(), name='tag'),
    # url(r'^search/$', views.search, name='search'),
]


