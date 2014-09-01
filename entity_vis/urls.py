from django.conf.urls import patterns, url

from entity_vis import views

urlpatterns = patterns('',
    url(r'^$', views.entities_in_play, name='entities_in_play')
)
