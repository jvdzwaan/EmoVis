from django.conf.urls import patterns, url

from corpus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^title/(?P<title_id>\w+)/$', views.show_title, name='get_title'),
    url(r'^author/(?P<author_id>\w+)/$', views.show_author, name='show_author'),
    url(r'^all_plays/$', views.show_all_plays, name='show_all_plays'),
    url(r'^year/(?P<year>\w+)/$', views.show_year, name='show_year'),
    url(r'^genres/$', views.show_genres, name='show_genres'),
)
