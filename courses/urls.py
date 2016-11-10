from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filter$', views.course_filter, name='filter'),
    url(r'^(?P<course_slug>.+)$', views.detail, name='detail'),
]
