"""eduqc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from index.views import index, contact

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^contact$', contact, name='contact'),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^markdown/', include( 'django_markdown.urls')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^users/password/', include('password_reset.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
