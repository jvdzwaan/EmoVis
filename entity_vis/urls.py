from django.conf.urls import patterns, url

from entity_vis import views

urlpatterns = patterns(
    '',
    url(r'^entity_graph_title/(?P<title_id>\w+)/$', views.entities_in_play,
        name='entities_in_play'),
    url(r'^entity_words$', views.entity_words, name='entity_words'),
    url(r'^speakingturns/(?P<concept>\w+)/$', views.find_in_speakingturns,
        name='find_in_speakingturns'),
    url(r'^entity_word_pairs$', views.entity_word_pairs,
        name='entity_word_pairs'),
    url(r'^browse_entities$', views.browse_entities, name='browse_entities'),
    url(r'^entity_categories$', views.entity_categories,
        name='entity_categories'),
    url(r'^subgenres_stats_time$', views.subgenres_stats_time,
        name='subgenres_stats_time'),
)
