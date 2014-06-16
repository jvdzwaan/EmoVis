from django.conf.urls import patterns, url

from corpus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
