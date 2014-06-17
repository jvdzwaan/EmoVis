from django.conf.urls import patterns, url

from corpus import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^title/(?P<title_id>\w+)/$', views.show_title, name='get_title')
)
