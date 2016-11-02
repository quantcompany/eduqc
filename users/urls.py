from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signout$', views.signout, name='signout'),
    url(r'^verify/(?P<code>.+)$', views.verify, name='verify'),
    url(r'^(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^me$', views.me, name='me'),
    # url(r'^profile$', views.profile, name='profile'),
]
