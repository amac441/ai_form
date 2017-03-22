from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = patterns('',
                # Examples:
                url(r'^$', 'survey.views.Index', name='home'),
                url(r'^survey/(?P<id>\d+)/$', 'survey.views.SurveyDetail', name='survey_detail'),
                url(r'^response/(?P<id>\d+)/$', 'survey.views.ResponseDetail', name='response_detail'),

                url(r'^confirm/(?P<uuid>\w+)/$', 'survey.views.Confirm', name='confirmation'),
                url(r'^privacy/$', 'survey.views.privacy', name='privacy_statement'),
                url(r'^dashboard/(?P<id>\w+)/$', 'survey.views.dashboard', name='dashboard_detail'),
                url(r'^dashboard/$', 'survey.views.dashboard', name='dashboard'),

                url(r'^maps/$', 'survey.views.Maps', name='maps'),

                # Uncomment the admin/doc line below to enable admin documentation:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                # Uncomment the next line to enable the admin:
                url(r'^admin/', include(admin.site.urls)),

                url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
                url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
                url(r'^post_files/$', 'survey.views.post_files', name='post'),

                # url(r'^chat/', include('djangoChat.urls')),
                )

# media url hackery. le sigh.
urlpatterns += patterns('',
                        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                        )

# urlpatterns += patterns('',
#     url(r'^articles/comments/', include('django_comments.urls')),
# )