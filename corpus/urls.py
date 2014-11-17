from django.conf.urls import patterns, url

from corpus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^title/(?P<title_id>\w+)/$', views.show_title, name='get_title'),
    url(r'^author/(?P<author_id>\w+)/$', views.show_author, name='show_author'),
    url(r'^all_plays/$', views.show_all_plays, name='show_all_plays'),
    url(r'^trial_annotations/$', views.show_trial_annotations),
    url(r'^year/(?P<year>\w+)/$', views.show_year, name='show_year'),
    url(r'^genres/$', views.show_genres, name='show_genres'),
    url(r'^genre/(?P<genre_id>\w+)$', views.show_genre, name='show_genre'),
    url(r'^subgenre/(?P<genre_id>\w+)$', views.show_subgenre),
    url(r'^originals$', views.show_first_year_of_publication),
    url(r'^entity_stats/$', views.entity_statistics_for_corpus,
        name='entity_statistics_for_corpus'),
    url(r'^entity_stats/(?P<title_id>\w+)/$',
        views.entity_statistics_for_title, name='entity_statistics_for_title'),
    url(r'^subgenre_stats/$', views.subgenre_entity_statistics_for_corpus,
        name='subgenre_entity_statistics_for_corpus'),

    url(r'^titles$', views.TitleViewSet.as_view(), name='title-list'),
    url(r'^titles/(?P<pk>[\w]+)/$', views.TitleInstanceView.as_view(),
        name='title-instance'),
    url(r'^titles/(?P<pk>[\w]+)/wordcloud/$',
        views.title_wordcloud, name='title-wordcloud'),
)
