"""jong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from jong.views import RssListView, RssCreateView, RssUpdateView, RssDeleteView, rss_switch_status
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RssListView.as_view(), name='base'),
    path('', RssListView.as_view(), name='rss'),
    path('add/', RssCreateView.as_view(), name='add'),
    url(r'^edit/(?P<pk>\d+)$', RssUpdateView.as_view(), name='edit'),
    url(r'^switch/(?P<pk>\d+)$', rss_switch_status, name='switch'),
    url(r'^delete/(?P<pk>\d+)$', RssDeleteView.as_view(), name='delete'),
    url(r'^api/jong/', include('jong.api.urls')),
]
