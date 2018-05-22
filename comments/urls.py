from django.conf.urls import url

from . import views

app_name = 'comments'


urlpatterns = [
    # url(r'^comment/post/(?P<pk>\d+)/$', views.post_comment, name='post_comment'),
    url(r'^comment/post/$', views.post_comment, name='post_comment'),
    url(r'^captcha/$', views.captcha, name='captcha'),
]
