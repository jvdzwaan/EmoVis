from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'embodied_emotions.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^corpus/', include('corpus.urls')),
    url(r'^entity_vis/', include('entity_vis.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
