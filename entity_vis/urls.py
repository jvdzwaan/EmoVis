from django.conf.urls import patterns, url

from entity_vis import views

urlpatterns = patterns(
    '',
    url(r'^$', views.entities_in_play, name='entities_in_play'),
    url(r'^entity_words$', views.entity_words, name='entity_words'),
    url(r'^speakingturns/(?P<concept>\w+)/$', views.find_in_speakingturns,
        name='find_in_speakingturns'),
)
