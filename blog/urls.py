from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.itabn, name='itabn'),
    url(r'^itabn/$', views.itabn, name='itabn'),
    url(r'^itabn/answer$', views.query_answer, name='query_answer'),
    url(r'^posts/$', views.post_list, name='post_list'),
    url(r'^facts/$', views.fact_list, name='fact_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^fact/new/$', views.fact_new, name='fact_new'),
    url(r'^fact/(?P<pk>[0-9]+)/$', views.fact_detail, name='fact_detail'),
]