from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^execute$', views.execute, name='execute'),
    url(r'^cancel$', views.cancel, name='cancel'),
]
